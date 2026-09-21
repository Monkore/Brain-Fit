from kivymd.app import MDApp
from core.config import FONT_SIZE_HEADING, FONT_SIZE_BODY, FONT_SIZE_BUTTON, MIN_TOUCH_TARGET

def apply_senior_theme(app: MDApp):
    """
    Applies high-contrast, large-font senior-first theme.
    """
    app.theme_cls.primary_palette = "Blue"  # Deep blue for high contrast
    app.theme_cls.accent_palette = "Orange" # Bright orange for calls to action
    app.theme_cls.theme_style = "Light"     # Default light mode, high contrast text
    app.theme_cls.material_style = "M3"     # Modern Material 3

    # KivyMD typography doesn't easily let us redefine 'H1' dynamically without deep hooks,
    # but we can provide helper classes or variables for our custom widgets.
    
    # We will define a global dictionary for our custom fonts to be used in KV
    app.custom_fonts = {
        "heading": FONT_SIZE_HEADING,
        "body": FONT_SIZE_BODY,
        "button": FONT_SIZE_BUTTON,
    }
    
    app.touch_target = MIN_TOUCH_TARGET
