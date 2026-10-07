# LLM review categoriser

> 🚧 **In progress.** First step done: data, theme taxonomy, offline baseline, Claude backend (mock-tested) and a first theme analysis.

**Business question:** a product team gets hundreds of short reviews. Which *themes* (battery, call quality, durability, delivery…) drive the negative ones, so the team knows what to fix first?

Reading reviews by hand doesn't scale. This project labels every review with one business theme, using an LLM (Claude) when an API key is available and an offline keyword baseline otherwise. It then measures which themes carry the most negative feedback.

## Data
[UCI Sentiment Labelled Sentences](https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences) (Kotzias et al., 2015), Amazon cell-phone file: 1,000 one-sentence reviews of phones and accessories, each labelled positive or negative. Licence: **CC BY 4.0**. It's fetched by `scripts/download_data.py` (58 KB). After trimming and removing exact duplicates, 990 reviews remain (497 negative, 493 positive).

## Approach
1. **Taxonomy** (`reviewcat/taxonomy.py`): 9 themes a product/support team can act on: `battery_power`, `audio_call_quality`, `build_durability`, `fit_comfort`, `ease_of_use`, `features_design`, `value_price`, `service_delivery`, and `general_sentiment` for reviews with no specific aspect.
2. **Two interchangeable backends:**
   - `reviewcat/baseline.py`: a whole-word keyword scorer. It's free, offline and reproducible, and serves as the benchmark.
   - `reviewcat/llm.py`: Claude (`claude-haiku-4-5`) labels 25 reviews per call. A forced tool call makes it return JSON restricted to the theme list, and invalid or missing answers fall back to `general_sentiment`.
3. **Analysis** (`scripts/analyse_themes.py`): theme × sentiment table, negative rate per theme, and each theme's share of all negatives.

## First results (keyword baseline)
⚠️ These are **baseline labels**, not LLM labels. No API key was available for this run. The baseline's accuracy hasn't been measured yet (that's the next step), so read these as directional.

![Reviews by theme](results/charts/negative_share_baseline.png)

| Theme | Reviews | Negative rate | Share of all negatives |
|---|---:|---:|---:|
| general_sentiment | 411 | 47.2% | 39.0% |
| audio_call_quality | 129 | 54.3% | 14.1% |
| battery_power | 79 | 60.8% | 9.7% |
| build_durability | 67 | 65.7% | 8.9% |
| ease_of_use | 72 | 47.2% | 6.8% |
| service_delivery | 53 | 60.4% | 6.4% |
| fit_comfort | 61 | 44.3% | 5.4% |
| value_price | 62 | 41.9% | 5.2% |
| features_design | 56 | 39.3% | 4.4% |

Full table: [`results/theme_summary_baseline.md`](results/theme_summary_baseline.md).

**What this suggests so far:**
- **Call/audio quality is the biggest named source of complaints** (14.1% of all negatives). It's also the most-discussed aspect.
- **Durability, battery and service are the most negative themes** when they're mentioned (60–66% negative). Those are quality and after-sales problems, not taste.
- **Price, design and fit lean positive.** These aren't where customers are unhappy.
- **The baseline's main weakness:** 41.5% of reviews land in `general_sentiment`, because many complaints don't use obvious keywords ("most of the stuff does not work with my phone"). Closing this gap is the reason to use an LLM.

## How to run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/download_data.py
python scripts/prepare_data.py
python scripts/run_categoriser.py          # auto: Claude if ANTHROPIC_API_KEY is set, else baseline
python scripts/analyse_themes.py --backend baseline
pytest                                     # offline tests; the LLM client is mocked
```
To use Claude, copy `.env.example` to `.env` and add your `ANTHROPIC_API_KEY`. Then run `run_categoriser.py --backend llm` and `analyse_themes.py --backend llm`.

## Next steps
- Build a hand-labelled gold sample to measure baseline accuracy (and LLM accuracy, once a key is available).
- Break down the negative reviews within each theme (what exactly goes wrong) and write ranked recommendations.
