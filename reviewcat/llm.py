"""Claude backend: batches reviews and forces a JSON answer via tool use.

Needs ANTHROPIC_API_KEY (read from a gitignored .env). Without a key, use the
offline baseline instead; run_categoriser.py picks automatically.
"""
import json
import os

from .taxonomy import THEMES, THEME_NAMES

MODEL = "claude-haiku-4-5-20251001"
BATCH_SIZE = 25

SYSTEM = (
    "You label short customer reviews of mobile-phone accessories for a product team. "
    "Pick the ONE theme that best describes what the review is about.\n\nThemes:\n"
    + "\n".join(f"- {k}: {v}" for k, v in THEMES.items())
)

TOOL = {
    "name": "record_labels",
    "description": "Record one theme per review id.",
    "input_schema": {
        "type": "object",
        "properties": {
            "labels": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "review_id": {"type": "string"},
                        "theme": {"type": "string", "enum": THEME_NAMES},
                    },
                    "required": ["review_id", "theme"],
                },
            }
        },
        "required": ["labels"],
    },
}


def build_user_message(batch: list[tuple[str, str]]) -> str:
    return "Label each review:\n" + json.dumps(
        [{"review_id": rid, "text": text} for rid, text in batch], ensure_ascii=False
    )


def parse_labels(tool_input: dict, expected_ids: list[str]) -> dict[str, str]:
    """Validate the model's answer; unknown/missing ids become 'general_sentiment'."""
    got = {
        item["review_id"]: item["theme"]
        for item in tool_input.get("labels", [])
        if item.get("theme") in THEMES
    }
    return {rid: got.get(rid, "general_sentiment") for rid in expected_ids}


def has_key() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def classify_many(ids: list[str], texts: list[str], client=None) -> dict[str, str]:
    if client is None:
        import anthropic
        client = anthropic.Anthropic()
    out: dict[str, str] = {}
    pairs = list(zip(ids, texts))
    for i in range(0, len(pairs), BATCH_SIZE):
        batch = pairs[i:i + BATCH_SIZE]
        resp = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=SYSTEM,
            tools=[TOOL],
            tool_choice={"type": "tool", "name": "record_labels"},
            messages=[{"role": "user", "content": build_user_message(batch)}],
        )
        block = next(b for b in resp.content if b.type == "tool_use")
        out.update(parse_labels(block.input, [rid for rid, _ in batch]))
    return out
