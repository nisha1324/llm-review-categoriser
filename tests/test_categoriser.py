"""Offline tests: no network, no API key."""
from types import SimpleNamespace

import pandas as pd

from reviewcat import baseline, llm
from reviewcat.taxonomy import THEME_NAMES
from prepare_data import clean
from analyse_themes import theme_table
from evaluate import ROOT, confusion, per_theme_scores
from drilldown import assign, sub_table
from reviewcat.subissues import OTHER, describes_failure, sub_issue


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


def test_evaluation_scores_and_confusion():
    merged = pd.DataFrame({
        "gold_theme": ["battery_power", "battery_power", "value_price", "general_sentiment"],
        "theme":      ["battery_power", "general_sentiment", "value_price", "value_price"],
    })
    s = per_theme_scores(merged).set_index("theme")
    assert s.loc["battery_power", ["precision", "recall"]].tolist() == [1.0, 0.5]
    assert s.loc["value_price", ["precision", "recall"]].tolist() == [0.5, 1.0]
    assert s.loc["fit_comfort", "f1"] == 0.0
    cm = confusion(merged)
    assert cm.shape == (9, 9) and cm.values.sum() == 4
    assert cm.loc["battery_power", "general_sentiment"] == 1


def test_gold_labels_are_valid():
    gold = pd.read_csv(ROOT / "data" / "gold" / "gold_labels.csv")
    assert len(gold) == 150 and gold.review_id.is_unique
    assert set(gold.gold_theme) <= set(THEME_NAMES)


def test_sub_issue_rules_split_themes():
    assert sub_issue("battery_power", "The battery runs down quickly.") == "short_battery_life"
    assert sub_issue("battery_power", "I bought two of them and neither will charge.") == "charger_fails_or_slow"
    # battery-life wording wins over the word 'charger'
    assert sub_issue("battery_power", "Tied to charger for calls over 45 minutes.") == "short_battery_life"
    assert sub_issue("audio_call_quality", "Mic Doesn't work.") == "caller_cant_hear_me"
    assert sub_issue("build_durability", "They work about 2 weeks then break.") == "failed_after_short_use"
    assert sub_issue("service_delivery", "Can't store anything but numbers.") == OTHER
    assert sub_issue("fit_comfort", "Too tight.") == OTHER  # theme without rules


def test_describes_failure():
    assert describes_failure("Doesn't Work.")
    assert describes_failure("All three broke within two months of use.")
    assert not describes_failure("It always cuts out and says signal failed.")
    assert not describes_failure("The battery runs down quickly.")


def test_sub_table_shares_add_up_per_theme():
    df = pd.DataFrame({
        "review_id": ["r1", "r2", "r3", "r4", "r5"],
        "text": ["Battery has no life.", "The charger did not work.", "Bad.", "Great!",
                 "Reception is terrible."],
        "sentiment": ["negative", "negative", "negative", "negative", "positive"],
        "theme": ["battery_power", "battery_power", "battery_power", "general_sentiment",
                  "audio_call_quality"],
    })
    sub = assign(df)
    assert len(sub) == 3  # positives and themes without rules are left out
    t = sub_table(sub)
    shares = t.groupby("theme", observed=True)["share_of_theme_negatives_pct"].sum()
    assert ((shares - 100).abs() <= 0.2).all()  # rounding to 1 dp
    assert t["sub_issue"].iloc[-1] == OTHER  # 'other' listed last in its theme
