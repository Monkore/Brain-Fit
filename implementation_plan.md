# BrainFit AI – Implementation Plan

This document outlines the architecture, database schema, module structure, and development plan for BrainFit AI, a senior-first cognitive wellness operating system for Android.

## User Review Required

> [!IMPORTANT]
> **Voice & ML Models Size:** The application requires offline models for Voice Recognition (Vosk), Text-To-Speech, and Pose Detection (MediaPipe). These models can be quite large (100MB+ total). Should we include these models directly in the APK, or have the app download them on first launch? (Direct inclusion will make the APK very large, which is standard for offline apps but might hit Play Store limits if you plan to publish there eventually).
>
> **Development Phasing:** Given the massive scope (dozens of mini-games, pose detection, voice AI), we propose a phased approach, starting with the core framework, a few key modules (e.g., one memory task, one yoga task), and the voice assistant. Does this phased execution sound good?

## Proposed Architecture

The application will follow a clean, modular architecture (Model-View-ViewModel / Service-Repository pattern) to ensure maintainability and scalability.

### Directory Structure

```text
brainfit_ai/
│
├── main.py                     # Application entry point
├── buildozer.spec              # Build configuration for Android APK
│
├── assets/                     # Static assets
│   ├── fonts/                  # Large, readable fonts (e.g., Roboto, OpenDyslexic)
│   ├── models/                 # Vosk offline voice models, MediaPipe models
│   ├── images/                 # High-contrast icons and illustrations
│   └── audio/                  # Guided meditation audio, sound effects
│
├── core/                       # Core configuration and utilities
│   ├── config.py               # App settings, theme colors, sizes
│   ├── constants.py            # Enums, string constants
│   ├── database.py             # SQLite connection and setup
│   └── localization/           # English/Hindi translation mappings
│
├── models/                     # Data models (Entities)
│   ├── user.py                 # User profile and preferences
│   ├── checkin.py              # Daily wellness check-in data
│   ├── activity.py             # Exercise definitions
│   └── performance.py          # Session results and feedback
│
├── repositories/               # Database access layer
│   ├── user_repo.py            
│   ├── checkin_repo.py
│   ├── performance_repo.py
│   └── analytics_repo.py
│
├── services/                   # Business logic and engines
│   ├── recommendation.py       # Adaptive Recommendation Engine
│   ├── difficulty.py           # Adaptive Difficulty Engine
│   ├── safety.py               # Safety Engine (monitoring fatigue/stress)
│   ├── scoring.py              # Cognitive Scoring Engine
│   └── analytics_manager.py    # Generates data for Progress Analytics
│
├── engines/                    # Complex AI / Hardware integration
│   ├── voice_assistant.py      # Vosk STT and pyttsx3/Native TTS integration
│   ├── pose_detection.py       # MediaPipe skeleton tracking and scoring
│   └── translator.py           # Offline text/audio translation service
│
├── ui/                         # Kivy/KivyMD Frontend
│   ├── main_window.kv          # Root window layout
│   ├── theme.py                # Senior-first typography and color palettes
│   ├── components/             # Reusable UI widgets
│   │   ├── large_button.py
│   │   ├── voice_toggle.py
│   │   └── accessible_label.py
│   ├── screens/                # Application Screens
│   │   ├── onboarding/
│   │   ├── dashboard/          # Home screen (Greeting, Score, Plan)
│   │   ├── checkin/            # Mood and energy sliders
│   │   ├── modules/            # UI for specific training modules
│   │   │   ├── processing_speed/
│   │   │   ├── memory/
│   │   │   ├── yoga/           # Incorporates camera feed for pose detection
│   │   │   └── ... (other modules)
│   │   └── analytics/          # Simple progress visualizations
│   └── viewmodels/             # Logic linking UI to Services
│
└── tests/                      # Unit tests
```

### Database Schema (SQLite)

We will use SQLite with simple, robust tables.

- **`users`**: `id`, `name`, `age`, `gender`, `language`, `activity_level`, `sleep_duration`, `meditation_exp`, `exercise_freq`, `created_at`
- **`daily_checkins`**: `id`, `user_id`, `date`, `mood`, `stress`, `anxiety`, `energy`, `focus`, `motivation`, `mental_fatigue`, `sleep_hours`
- **`activities`**: `id`, `module_type` (e.g., 'Memory', 'Yoga'), `name`, `description`, `base_difficulty`
- **`sessions`**: `id`, `user_id`, `date`, `status` (planned, completed)
- **`session_activities`**: `id`, `session_id`, `activity_id`, `order`, `status`
- **`performance_logs`**: `id`, `session_activity_id`, `score`, `accuracy`, `duration_seconds`, `difficulty_feedback`, `enjoyment_feedback`, `energy_after`, `timestamp`
- **`analytics_summary`**: `id`, `user_id`, `date`, `resilience_score`, `speed_score`, `memory_score`, `attention_score`, `executive_score`

## Core Engines Design

1. **Adaptive Recommendation Engine**:
   - Runs nightly or on daily app open.
   - Inputs: User profile, yesterday's check-in, recent performance_logs.
   - Logic: Generates a `Session` with a list of `Activities`. If stress is > 7, it swaps High-Cognitive tasks for Meditation/Breathing.

2. **Adaptive Difficulty Engine**:
   - Evaluates performance metrics immediately after an activity.
   - Rules: If user selects "Too Easy" and accuracy > 90%, increment base difficulty for next time. If "Too Hard", decrement. Also applies age-based modifiers (e.g., slower initial timer for 76+).

3. **Safety Engine**:
   - Listens to check-ins and post-exercise feedback.
   - If energy is "Low" after a task, it dynamically modifies the rest of the day's `Session` to lighter tasks or suggests rest.

4. **Voice Assistant Engine (Offline)**:
   - Uses **Vosk** for speech-to-text. We will include a lightweight English/Hindi acoustic model.
   - Uses **Android Native TTS** (via `pyjnius` or `plyer`) for text-to-speech, falling back to `pyttsx3` for desktop testing.
   - Exposes a simple `listen_command()` and `speak(text)` API.

5. **Pose Detection Engine**:
   - Uses **MediaPipe** Pose solution.
   - Captures frames from Android camera (via Kivy camera module or OpenCV android ports).
   - Calculates angles (e.g., knee bend, arm raise) and compares against ideal pose heuristics for Yoga and Dual-Task training.

## Senior-First UI Guidelines (KivyMD)

- **Typography**: Minimum 24sp for buttons, 30sp for headers.
- **Contrast**: High contrast ratios (WCAG AAA compliant), avoiding subtle grays. Use bold, clear colors.
- **Touch Targets**: Minimum `dp(64)` padding/margin for interactive elements.
- **Navigation**: Flat hierarchy. The Home screen is the hub.
- **Clutter**: Max 3-4 interactive elements per screen.
- **Feedback**: Immediate auditory and visual confirmation for every tap.

## Verification Plan

### Automated Verification
- Unit tests for Recommendation, Difficulty, and Safety engines to ensure logic correctly adapts to mock inputs.
- SQLite schema validation.

### Manual Verification
- Run the app locally on a desktop environment (using a webcam for MediaPipe) to test flow, UI scaling, and Voice logic.
- Compile to APK using Buildozer and test on an Android device to verify:
  1. Complete offline functionality (turn on Airplane mode).
  2. Vosk voice recognition on Android.
  3. Camera access and MediaPipe performance on mobile.
  4. Native TTS behavior.

## Execution Strategy

Due to the immense size of the project, I propose the following execution order:
1. **Phase 1: Foundation**: Project setup, SQLite database, UI theme, Core engines skeleton, Home Screen.
2. **Phase 2: Core UX**: Onboarding flow, Daily Check-in, Emergency Contact, Settings.
3. **Phase 3: Intelligence & Voice**: Voice Assistant Engine integration, Recommendation Engine logic.
4. **Phase 4: Modules (Batch 1)**: Processing Speed, Memory, Attention, Meditation.
5. **Phase 5: Advanced Modules (Batch 2)**: Yoga (MediaPipe), Dual-Task, Language.
6. **Phase 6: Finalization**: Analytics dashboard, APK Packaging (Buildozer spec).
