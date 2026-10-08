# Sub-issue drill-down (baseline labels)

194 negative reviews in 4 themes. Rules: `reviewcat/subissues.py`; first match wins. Every assignment: `results/subissues_baseline.csv`.

## audio_call_quality (70 negatives)

| Sub-issue | Reviews | Share | Examples |
|---|---:|---:|---|
| reception_dropped_calls | 14 | 20.0% | “Its reception is very very poor.” / “Could not get strong enough signal.” |
| too_quiet_cant_hear | 13 | 18.6% | “I only hear garbage for audio.” / “Not loud enough and doesn't turn on like it should.” |
| caller_cant_hear_me | 10 | 14.3% | “It didn't work, people can not hear me when I talk.” / “The mic there is a joke, and the volume is quite low.” |
| noise_echo_or_leak | 10 | 14.3% | “Echo Problem....Very unsatisfactory” / “So anyone near you will hear part of your conversation.” |
| poor_sound_general | 10 | 14.3% | “Audio Quality is poor, very poor.” / “Utter crap.. Sound quality is TERRIBLE.” |
| missed_incoming_calls | 4 | 5.7% | “I've missed numerous calls because of this reason.” / “You can not answer calls with the unit, never worked once!” |
| other_unclear | 9 | 12.9% | “I'll be looking for a new earpiece.” / “I cannot make calls at certain places.” |

## battery_power (48 negatives)

| Sub-issue | Reviews | Share | Examples |
|---|---:|---:|---|
| short_battery_life | 19 | 39.6% | “The battery runs down quickly.” / “Battery lasts only a few hours.” |
| charger_fails_or_slow | 17 | 35.4% | “I bought two of them and neither will charge.” / “Does not charge the Cingular (ATT) 8525 phone.” |
| battery_faulty_or_poor | 10 | 20.8% | “The battery is completely useless to me.” / “Who in their right mind is gonna buy this battery?.” |
| other_unclear | 2 | 4.2% | “Rip off---- Over charge shipping.” / “This company charge me a restocking fee and still not given me my refund back.” |

## build_durability (44 negatives)

| Sub-issue | Reviews | Share | Examples |
|---|---:|---:|---|
| vague_quality_or_junk | 17 | 38.6% | “What possesed me to get this junk, I have no idea...” / “This product is very High quality Chinese CRAP!!!!!!” |
| failed_after_short_use | 14 | 31.8% | “Lasted one day and then blew up.” / “They work about 2 weeks then break.” |
| broke_or_cracked | 7 | 15.9% | “The plastic breaks really easy on this clip.” / “Problem is that the ear loops are made of weak material and break easily.” |
| cheap_materials | 6 | 13.6% | “The cable looks so thin and flimsy, it is scary.” / “VERY cheap plastic, creaks like an old wooden floor.” |

## service_delivery (32 negatives)

| Sub-issue | Reviews | Share | Examples |
|---|---:|---:|---|
| customer_support | 11 | 34.4% | “Customer service was terrible.” / “Talk about USELESS customer service.” |
| carrier_network | 7 | 21.9% | “Sprint charges for this service.” / “Sprint - terrible customer service.” |
| returns_refunds_warranty | 7 | 21.9% | “Improper description.... I had to return it.” / “AFTER ARGUING WITH VERIZON REGARDING THE DROPPED CALLS WE RETURNED THE PHONES AFTER TWO DAYS.” |
| retailer_or_listing | 4 | 12.5% | “Don't bother - go to the store.” / “stay away from this store, be careful.” |
| other_unclear | 3 | 9.4% | “Basically the service was very bad.” / “Can't store anything but phone numbers to SIM.” |

## Product failures across all themes

46 of 497 negative reviews (9.3%) say the product doesn't work, broke or died. By the theme the baseline gave them:

| theme              |   negatives |   describes_failure |   failure_share_pct |
|:-------------------|------------:|--------------------:|--------------------:|
| build_durability   |          44 |                  13 |                29.5 |
| general_sentiment  |         194 |                  13 |                 6.7 |
| battery_power      |          48 |                  12 |                25   |
| audio_call_quality |          70 |                   7 |                10   |
| ease_of_use        |          34 |                   1 |                 2.9 |
| features_design    |          22 |                   0 |                 0   |
| fit_comfort        |          27 |                   0 |                 0   |
| service_delivery   |          32 |                   0 |                 0   |
| value_price        |          26 |                   0 |                 0   |
