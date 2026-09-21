import logging
import threading
import queue
import sys
import json
from typing import Callable
from deep_translator import GoogleTranslator

# Map languages to language codes for deep-translator
LANG_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr"
}

logger = logging.getLogger(__name__)

# Try to import Android TTS, fallback to pyttsx3
try:
    from jnius import autoclass # type: ignore
    Locale = autoclass('java.util.Locale')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
    
    class TTSListener:
        def __init__(self):
            self.tts = TextToSpeech(PythonActivity.mActivity, self)
            
        def onInit(self, status):
            if status == TextToSpeech.SUCCESS:
                self.tts.setLanguage(Locale.US)
                
    android_tts = TTSListener()
    USE_ANDROID_TTS = True
    logger.info("Using Android Native TTS.")
except ImportError:
    USE_ANDROID_TTS = False
    logger.info("Android Native TTS not found, falling back to pyttsx3.")
    try:
        import pyttsx3
    except ImportError:
        logger.warning("pyttsx3 not found. TTS will not work.")

try:
    from vosk import Model, KaldiRecognizer
    import pyaudio
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False
    logger.warning("Vosk or pyaudio not found. STT will not work.")

from core.config import VOSK_MODEL_PATH_EN, VOSK_MODEL_PATH_HI

class VoiceAssistant:
    def __init__(self):
        self.is_listening = False
        self._stt_thread = None
        
        self.tts_queue = queue.Queue()
        if not USE_ANDROID_TTS and 'pyttsx3' in sys.modules:
            self._tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
            self._tts_thread.start()
        else:
            self._tts_thread = None

        self.language = "English"
        
        self.stt_models = {}
        if VOSK_AVAILABLE:
            # Load English Model
            if VOSK_MODEL_PATH_EN.exists():
                try:
                    self.stt_models["English"] = Model(str(VOSK_MODEL_PATH_EN))
                except Exception as e:
                    logger.error(f"Failed to load Vosk EN model: {e}")
                    
            # Load Hindi Model
            if VOSK_MODEL_PATH_HI.exists():
                try:
                    self.stt_models["Hindi"] = Model(str(VOSK_MODEL_PATH_HI))
                except Exception as e:
                    logger.error(f"Failed to load Vosk HI model: {e}")

    def _tts_worker(self):
        # Initialize pyttsx3 in the same thread that will run it
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        
        # Store engine in self so speak() can change voice dynamically if needed
        # Actually, pyttsx3 is not thread safe across threads, so we'll pass language in the queue
        
        while True:
            item = self.tts_queue.get()
            if item is None:
                break
            
            text, lang = item
            
            # Translate if needed
            if lang != "English" and lang in LANG_CODES:
                try:
                    translator = GoogleTranslator(source='en', target=LANG_CODES[lang])
                    text = translator.translate(text)
                except Exception as e:
                    logger.error(f"TTS Translation failed: {e}")
                    
            # Try to set voice
            voices = engine.getProperty('voices')
            target_voice = None
            for voice in voices:
                if lang == "Hindi" and ("hi" in voice.id.lower() or "hindi" in voice.name.lower()):
                    target_voice = voice.id
                    break
                elif lang == "English" and ("en" in voice.id.lower() or "english" in voice.name.lower()):
                    target_voice = voice.id
                    break
                    
            if target_voice:
                engine.setProperty('voice', target_voice)
                
            engine.say(text)
            engine.runAndWait()
            self.tts_queue.task_done()

    def speak(self, text: str, lang: str = None):
        """Speaks the text aloud using local TTS."""
        lang = lang or self.language
        logger.info(f"TTS [{lang}]: {text}")
        if USE_ANDROID_TTS:
            android_tts.tts.speak(text, TextToSpeech.QUEUE_FLUSH, None)
        elif self._tts_thread:
            self.tts_queue.put((text, lang))
        else:
            logger.warning(f"No TTS engine available to say: {text}")

    def listen(self, callback: Callable[[str], None], lang: str = None):
        """Starts listening and calls callback with transcribed text."""
        lang = lang or self.language
        stt_model = self.stt_models.get(lang)
        
        if not VOSK_AVAILABLE or not stt_model:
            logger.warning(f"STT Engine not available for language: {lang}")
            callback("STT Engine not available")
            return

        if self.is_listening:
            return

        self.is_listening = True
        logger.info(f"Started listening in {lang}...")
        
        def _listen_loop():
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
            stream.start_stream()
            rec = KaldiRecognizer(stt_model, 16000)

            while self.is_listening:
                data = stream.read(4000, exception_on_overflow=False)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    res = json.loads(rec.Result())
                    text = res.get('text', '')
                    if text:
                        if lang != "English" and lang in LANG_CODES:
                            try:
                                translator = GoogleTranslator(source=LANG_CODES[lang], target='en')
                                translated_text = translator.translate(text)
                                callback(translated_text)
                            except Exception as e:
                                logger.error(f"STT Translation failed: {e}")
                                callback(text)
                        else:
                            callback(text)

            stream.stop_stream()
            stream.close()
            p.terminate()

        self._stt_thread = threading.Thread(target=_listen_loop, daemon=True)
        self._stt_thread.start()
    
    def stop_listening(self):
        self.is_listening = False
        logger.info("Stopped listening.")
