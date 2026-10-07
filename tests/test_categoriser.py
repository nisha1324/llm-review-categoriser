"""Offline tests: no network, no API key."""
from types import SimpleNamespace

import pandas as pd

from reviewcat import baseline, llm
from reviewcat.taxonomy import THEME_NAMES
from prepare_data import clean
from analyse_themes import theme_table


def test_baseline_picks_specific_themes():
    assert baseline.classify("Battery life is also great!") == "battery_power"
    assert baseline.classify("Reception is terrible and full of static.") == "audio_call_quality"
    assert baseline.classify("All three broke within two months of use.") == "build_durability"
    assert baseline.classify("Waste of money.") == "value_price"
    assert baseline.classify("You won't regret it!") == "general_sentiment"


def test_baseline_whole_word_match():
    # 'ear' must not match inside 'year' / 'clear'
    assert baseline.classify("Had it a year now") == "general_sentiment"


def test_baseline_only_returns_known_themes():
    for text in ["", "charger broke", "great price and fast shipping", "???"]:
        assert baseline.classify(text) in THEME_NAMES


def test_clean_drops_duplicates_and_assigns_ids():
    raw = pd.DataFrame({"text": [" Good ", "Good", "Bad", ""], "label": [1, 1, 0, 0]})
    out = clean(raw)
    assert out["text"].tolist() == ["Good", "Bad"]
    assert out["review_id"].tolist() == ["r0001", "r0002"]
    assert out["sentiment"].tolist() == ["positive", "negative"]


def test_parse_labels_validates_model_output():
    tool_input = {"labels": [
        {"review_id": "r1", "theme": "battery_power"},
        {"review_id": "r2", "theme": "not_a_theme"},
    ]}
    out = llm.parse_labels(tool_input, ["r1", "r2", "r3"])
    assert out == {"r1": "battery_power", "r2": "general_sentiment", "r3": "general_sentiment"}


def test_llm_classify_many_with_mock_client():
    calls = []

    class FakeMessages:
        def create(self, **kwargs):
            calls.append(kwargs)
            assert kwargs["tool_choice"]["name"] == "record_labels"
            block = SimpleNamespace(type="tool_use", input={"labels": [
                {"review_id": "a", "theme": "value_price"},
                {"review_id": "b", "theme": "fit_comfort"},
            ]})
            return SimpleNamespace(content=[block])

    client = SimpleNamespace(messages=FakeMessages())
    out = llm.classify_many(["a", "b"], ["cheap", "fits well"], client=client)
    assert out == {"a": "value_price", "b": "fit_comfort"}
    assert len(calls) == 1


def test_theme_table_rates():
    df = pd.DataFrame({"theme": ["x", "x", "y"],
                       "sentiment": ["negative", "positive", "negative"]})
    t = theme_table(df)
    assert t.loc["x", "negative_rate_pct"] == 50.0
    assert t.loc["y", "share_of_all_negatives_pct"] == 50.0
