"""Offline keyword baseline: no API key needed, fully reproducible.

Scores each theme by keyword hits and picks the highest; ties go to the theme
listed first in PRIORITY (specific aspects before generic ones). Reviews with
no hit fall back to 'general_sentiment'.
"""
import re

KEYWORDS = {
    "battery_power": ["battery", "batteries", "charge", "charger", "charging", "charged",
                      "recharge", "power", "talk time", "standby"],
    "audio_call_quality": ["sound", "audio", "volume", "loud", "hear", "heard", "hearing",
                           "mic", "microphone", "static", "noise", "echo", "call", "calls",
                           "reception", "signal", "clear", "clarity", "voice", "speaker",
                           "ear piece", "earpiece"],
    "build_durability": ["broke", "broken", "break", "breaks", "cheaply made", "flimsy",
                         "quality", "sturdy", "durable", "plastic", "cracked", "crack",
                         "stopped working", "died", "dead", "defective", "fell apart",
                         "junk", "piece of", "lasted", "months", "weeks"],
    "fit_comfort": ["fit", "fits", "comfortable", "uncomfortable", "comfort", "ear",
                    "ears", "wear", "wearing", "clip", "holster", "snug", "loose", "hurts"],
    "ease_of_use": ["easy", "easier", "difficult", "setup", "set up", "pair", "paired",
                    "pairing", "bluetooth", "connect", "connection", "button", "buttons",
                    "menu", "software", "instructions", "use", "user", "compatible",
                    "works with", "plug", "converter"],
    "features_design": ["camera", "picture", "pictures", "pics", "screen", "display",
                        "keypad", "keyboard", "keys", "ringtone", "ringtones", "design",
                        "color", "colour", "looks", "look", "style", "stylish", "sleek",
                        "features", "games", "video"],
    "value_price": ["price", "priced", "value", "money", "cost", "cheap", "worth",
                    "dollars", "$", "bargain", "expensive", "refund", "deal"],
    "service_delivery": ["service", "customer", "shipping", "shipped", "delivery",
                         "arrived", "seller", "vendor", "amazon", "return", "returned",
                         "warranty", "replacement", "package", "packaging", "support",
                         "company", "verizon", "store"],
}

PRIORITY = ["battery_power", "audio_call_quality", "build_durability", "fit_comfort",
            "features_design", "value_price", "service_delivery", "ease_of_use"]

_PATTERNS = {
    theme: [re.compile(r"(?<![a-z])" + re.escape(k) + r"(?![a-z])") for k in kws]
    for theme, kws in KEYWORDS.items()
}


def classify(text: str) -> str:
    low = text.lower()
    scores = {t: sum(bool(p.search(low)) for p in pats) for t, pats in _PATTERNS.items()}
    best = max(scores.values())
    if best == 0:
        return "general_sentiment"
    return next(t for t in PRIORITY if scores[t] == best)


def classify_many(texts: list[str]) -> list[str]:
    return [classify(t) for t in texts]
