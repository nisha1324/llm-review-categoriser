"""Business themes a product / support team would act on.

Each review gets exactly one primary theme. Descriptions are shared by the
LLM prompt and the keyword baseline so both backends use the same definitions.
"""
THEMES = {
    "battery_power": "Battery life, charging, chargers, power adapters.",
    "audio_call_quality": "Sound, volume, microphone, call clarity, static, dropped calls, reception.",
    "build_durability": "Build quality, materials, breaking, stopped working, defects, reliability over time.",
    "fit_comfort": "How a headset/case/clip fits or feels to wear or hold.",
    "ease_of_use": "Setup, pairing, Bluetooth connection, buttons, software, instructions, compatibility.",
    "features_design": "Phone features and looks: camera, screen, display, keypad, ringtones, design, colour.",
    "value_price": "Price, value for money, cost, cheap, worth it, refunds.",
    "service_delivery": "Seller/manufacturer service, shipping, delivery, packaging, returns, warranty.",
    "general_sentiment": "Overall opinion with no specific product aspect (e.g. 'Great product!').",
}

THEME_NAMES = list(THEMES)
