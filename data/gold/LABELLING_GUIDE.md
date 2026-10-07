# Gold sample labelling guide

**Sample:** 150 reviews drawn with `reviews.sample(150, random_state=42)` from `data/processed/reviews.csv`
(`scripts/evaluate.py --draw-sample` prints them). Labels were assigned from the review text alone,
without looking at the baseline's labels. One annotator, one pass, so treat the gold set as a careful
reference, not ground truth.

**Rules** (one primary theme per review, from `reviewcat/taxonomy.py`):
1. Pick the aspect that carries the sentiment. If several aspects are named, pick the one the
   complaint (or praise) is mainly about; on a tie, the first one mentioned.
2. No specific product aspect → `general_sentiment`. This includes "Don't buy it", "Piece of junk",
   "works great", recommendations, comparisons with no reason given, and "sending it back" with no reason.
3. Network reception and coverage → `audio_call_quality` (it's what the customer hears on a call).
4. A product that broke, died, smoked or failed over time → `build_durability`, unless it's a
   charger or battery failing to charge → `battery_power`.
5. Cases, holders and headsets that don't fit or are uncomfortable → `fit_comfort`.
6. Connectivity, Bluetooth drop-outs, compatibility with another device, speed and setup → `ease_of_use`.
7. Screen, camera, keyboard, buttons, looks, colours and software features → `features_design`.
8. Price, value, bargains and service fees → `value_price`. Seller, shipping, customer service → `service_delivery`.
