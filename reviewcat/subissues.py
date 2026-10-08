"""Sub-issues inside the four themes with the most negative feedback.

A theme tells the team *where* the problem is ("battery"); a sub-issue tells
them *what* to fix ("the charger doesn't work" vs "the battery drains fast").
Rules are checked in order and the first match wins, so every negative review
gets exactly one sub-issue and the shares add up to 100%. Reviews that match
no rule become 'other_unclear', which is reported rather than hidden (many of
them are reviews the baseline routed to the wrong theme).

The rules were written after reading the negative reviews in each theme, so
they describe this dataset; they are not a general-purpose classifier.
"""
import re

# Mentions a short time span: "2 days", "a week later", "three months", "a year".
SHORT_SPAN = (r"(\d+|a|one|two|three|four|few|couple of|several)\s+"
              r"(day|days|week|weeks|month|months|year|years)|lasted one day|first time")

RULES = {
    "audio_call_quality": [
        ("reception_dropped_calls", ["reception", "signal", "bars", "drop", "drops",
                                     "dropped", "cuts out"]),
        ("missed_incoming_calls", ["receiving a call", "call is coming in", "missed numerous calls",
                                   "stops ringing", "answer calls"]),
        ("caller_cant_hear_me", ["mic", "microphone", "hear me", "hear you", "yell",
                                 "shouting", "talking real loud"]),
        ("noise_echo_or_leak", ["static", "noise", "noises", "echo", "buzz", "buzzing",
                                "tick", "distorted", "garbled", "muffled", "tinny", "muddy",
                                "leaks out", "audio delay", "anyone near you will hear"]),
        ("too_quiet_cant_hear", ["volume", "loud", "hear", "hearing", "barely"]),
        ("poor_sound_general", ["sound", "audio", "voice", "clarity", "not clear"]),
    ],
    "battery_power": [
        ("short_battery_life", ["battery life", "runs down", "drain", "drains", "drained",
                                "hold charge", "holds the charge", "dead", "dying", "dieing",
                                "talk time", "lasts", "few hours", "left in the morning",
                                "tied to charger", "has no life"]),
        ("charger_fails_or_slow", ["charger", "adapter", "charging current", "will not charge",
                                   "not recharge", "neither will charge", "didn't charge",
                                   "does not charge", "forever to charge"]),
        ("battery_faulty_or_poor", ["battery"]),
    ],
    "build_durability": [
        ("failed_after_short_use", SHORT_SPAN),
        ("broke_or_cracked", ["broke", "break", "breaks", "cracked", "blew up"]),
        ("cheap_materials", ["cheap", "cheaply", "flimsy", "plastic", "weak material",
                             "creaks", "floppy", "saggy"]),
        ("vague_quality_or_junk", ["quality", "junk", "crap", "trash", "defective"]),
    ],
    "service_delivery": [
        ("returns_refunds_warranty", ["return", "returned", "refund", "warranty",
                                      "restocking"]),
        ("carrier_network", ["verizon", "sprint", "t-mobile", "cingular"]),
        ("customer_support", ["customer service", "tech support", "support", "contacting",
                              "contacted", "company"]),
        ("retailer_or_listing", ["amazon", "the store", "this store", "website", "online",
                                 "description"]),
    ],
}

OTHER = "other_unclear"

# "It doesn't work / it broke": a product failure, whatever theme it was routed to.
FAILURE = re.compile(
    r"(?<![a-z])(broke|broken|died|stopped working|stopped charging|"
    r"doesn'?t work|does not work|didn'?t work|did not work|never worked|not working|"
    r"wont work|won'?t work|defective|(?<!signal )failed|blew up|went black|"
    r"nothing happens|doesn'?t turn on|will not charge|neither will charge|"
    r"didn'?t charge|does not charge)(?![a-z])"
)


def _compile(rule) -> re.Pattern:
    body = rule if isinstance(rule, str) else "|".join(re.escape(w) for w in rule)
    return re.compile(r"(?<![a-z])(" + body + r")(?![a-z])")


_COMPILED = {
    theme: [(name, _compile(rule)) for name, rule in rules]
    for theme, rules in RULES.items()
}

THEMES = list(RULES)


def sub_issue(theme: str, text: str) -> str:
    """First matching sub-issue for a review in `theme`, else 'other_unclear'."""
    low = text.lower()
    for name, pat in _COMPILED.get(theme, []):
        if pat.search(low):
            return name
    return OTHER


def describes_failure(text: str) -> bool:
    """Review says the product doesn't work at all, broke or died."""
    return bool(FAILURE.search(text.lower()))
