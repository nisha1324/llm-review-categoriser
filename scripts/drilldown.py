"""What exactly goes wrong inside each negative theme?

Splits the negative reviews of the four most-complained-about themes into
sub-issues (rules in reviewcat/subissues.py), and flags reviews in *any* theme
that describe a product that doesn't work at all.

Writes results/drilldown_<backend>.md, results/subissues_<backend>.csv and
results/charts/subissues_<backend>.png.
"""
import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from reviewcat.subissues import OTHER, THEMES, describes_failure, sub_issue  # noqa: E402

NEG = "#c0504d"
GREY = "#b0b0b0"


def assign(df: pd.DataFrame) -> pd.DataFrame:
    """Negative reviews in the drill-down themes, with their sub-issue."""
    neg = df[(df["sentiment"] == "negative") & df["theme"].isin(THEMES)].copy()
    neg["sub_issue"] = [sub_issue(t, x) for t, x in zip(neg["theme"], neg["text"])]
    return neg[["review_id", "theme", "sub_issue", "text"]]


def sub_table(sub: pd.DataFrame) -> pd.DataFrame:
    t = sub.groupby(["theme", "sub_issue"]).size().rename("reviews").reset_index()
    t["share_of_theme_negatives_pct"] = (
        100 * t["reviews"] / t.groupby("theme")["reviews"].transform("sum")).round(1)
    t["is_other"] = t["sub_issue"] == OTHER
    t["theme"] = pd.Categorical(t["theme"], THEMES)
    return (t.sort_values(["theme", "is_other", "reviews"], ascending=[True, True, False])
             .drop(columns="is_other").reset_index(drop=True))


def failure_table(df: pd.DataFrame) -> pd.DataFrame:
    neg = df[df["sentiment"] == "negative"].copy()
    neg["failure"] = neg["text"].map(describes_failure)
    t = neg.groupby("theme")["failure"].agg(negatives="size", describes_failure="sum")
    t["failure_share_pct"] = (100 * t["describes_failure"] / t["negatives"]).round(1)
    return t.sort_values("describes_failure", ascending=False)


def examples(sub: pd.DataFrame, theme: str, issue: str, n: int = 2) -> list[str]:
    """Short, readable quotes: the n shortest reviews of at least 30 characters."""
    g = sub[(sub["theme"] == theme) & (sub["sub_issue"] == issue)]["text"]
    g = g[g.str.len() >= 30]
    return g.loc[g.str.len().sort_values(kind="stable").index].head(n).tolist()


def chart(t: pd.DataFrame, path: Path, backend: str) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(11, 6.5))
    xmax = t["reviews"].max() * 1.3
    for ax, theme in zip(axes.flat, THEMES):
        d = t[t["theme"] == theme].iloc[::-1]
        colors = [GREY if s == OTHER else NEG for s in d["sub_issue"]]
        ax.barh(d["sub_issue"], d["reviews"], color=colors, height=0.6)
        for y, (n, p) in enumerate(zip(d["reviews"], d["share_of_theme_negatives_pct"])):
            ax.text(n + 0.3, y, f"{n} ({p:.0f}%)", va="center", fontsize=9)
        ax.set_title(f"{theme} ({int(d['reviews'].sum())} negative reviews)",
                     fontsize=10, loc="left")
        ax.set_xlim(0, xmax)
        ax.tick_params(axis="y", labelsize=9)
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle(f"What goes wrong inside each theme ({backend} labels; grey = no rule matched)",
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", default="baseline")
    backend = ap.parse_args().backend
    df = pd.read_csv(ROOT / "data" / "processed" / f"labelled_{backend}.csv")

    sub = assign(df)
    t = sub_table(sub)
    f = failure_table(df)
    (ROOT / "results" / "charts").mkdir(parents=True, exist_ok=True)
    sub.to_csv(ROOT / "results" / f"subissues_{backend}.csv", index=False)
    chart(t, ROOT / "results" / "charts" / f"subissues_{backend}.png", backend)

    md = [f"# Sub-issue drill-down ({backend} labels)", "",
          f"{len(sub)} negative reviews in {len(THEMES)} themes. Rules: `reviewcat/subissues.py`; "
          f"first match wins. Every assignment: `results/subissues_{backend}.csv`.", ""]
    for theme in THEMES:
        d = t[t["theme"] == theme]
        md += [f"## {theme} ({int(d['reviews'].sum())} negatives)", "",
               "| Sub-issue | Reviews | Share | Examples |", "|---|---:|---:|---|"]
        for _, r in d.iterrows():
            ex = " / ".join(f"“{e}”" for e in examples(sub, theme, r["sub_issue"]))
            ex = ex.replace("|", "\\|")
            md.append(f"| {r['sub_issue']} | {r['reviews']} | "
                      f"{r['share_of_theme_negatives_pct']}% | {ex} |")
        md.append("")
    total_fail = int(f["describes_failure"].sum())
    total_neg = int(f["negatives"].sum())
    md += ["## Product failures across all themes", "",
           f"{total_fail} of {total_neg} negative reviews "
           f"({100 * total_fail / total_neg:.1f}%) say the product doesn't work, broke or died. "
           "By the theme the baseline gave them:", "",
           f.reset_index().to_markdown(index=False), ""]
    (ROOT / "results" / f"drilldown_{backend}.md").write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
