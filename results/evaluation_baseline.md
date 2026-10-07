# Evaluation: baseline vs gold sample

- Gold reviews: 150 (labelling rules: `data/gold/LABELLING_GUIDE.md`)
- Accuracy: **63.3%**
- Macro F1 (9 themes): **0.597**
- Reviews with a specific gold theme: 92; 19.6% of them were put in `general_sentiment`

## Per theme

| theme              |   gold |   predicted |   correct |   precision |   recall |    f1 |
|:-------------------|-------:|------------:|----------:|------------:|---------:|------:|
| battery_power      |      9 |           9 |         9 |       1     |    1     | 1     |
| audio_call_quality |     16 |          23 |        13 |       0.565 |    0.812 | 0.667 |
| build_durability   |     13 |          10 |         4 |       0.4   |    0.308 | 0.348 |
| fit_comfort        |      7 |           7 |         5 |       0.714 |    0.714 | 0.714 |
| ease_of_use        |      8 |          13 |         1 |       0.077 |    0.125 | 0.095 |
| features_design    |     20 |           5 |         5 |       1     |    0.25  | 0.4   |
| value_price        |     11 |           8 |         8 |       1     |    0.727 | 0.842 |
| service_delivery   |      8 |          13 |         6 |       0.462 |    0.75  | 0.571 |
| general_sentiment  |     58 |          62 |        44 |       0.71  |    0.759 | 0.733 |

## Confusion matrix (rows = gold, columns = predicted)

| gold_theme         |   battery_power |   audio_call_quality |   build_durability |   fit_comfort |   ease_of_use |   features_design |   value_price |   service_delivery |   general_sentiment |
|:-------------------|----------------:|---------------------:|-------------------:|--------------:|--------------:|------------------:|--------------:|-------------------:|--------------------:|
| battery_power      |               9 |                    0 |                  0 |             0 |             0 |                 0 |             0 |                  0 |                   0 |
| audio_call_quality |               0 |                   13 |                  0 |             1 |             0 |                 0 |             0 |                  0 |                   2 |
| build_durability   |               0 |                    1 |                  4 |             0 |             2 |                 0 |             0 |                  1 |                   5 |
| fit_comfort        |               0 |                    0 |                  0 |             5 |             2 |                 0 |             0 |                  0 |                   0 |
| ease_of_use        |               0 |                    2 |                  0 |             0 |             1 |                 0 |             0 |                  0 |                   5 |
| features_design    |               0 |                    3 |                  3 |             1 |             3 |                 5 |             0 |                  0 |                   5 |
| value_price        |               0 |                    1 |                  0 |             0 |             0 |                 0 |             8 |                  2 |                   0 |
| service_delivery   |               0 |                    1 |                  0 |             0 |             0 |                 0 |             0 |                  6 |                   1 |
| general_sentiment  |               0 |                    2 |                  3 |             0 |             5 |                 0 |             0 |                  4 |                  44 |

## Disagreements (55)

| review_id   | text                                                                                                                                                 | sentiment   | gold_theme         | theme              |
|:------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------|:------------|:-------------------|:-------------------|
| r0026       | Great Pocket PC / phone combination.                                                                                                                 | positive    | features_design    | general_sentiment  |
| r0031       | This is a simple little phone to use, but the breakage is unacceptible.                                                                              | negative    | build_durability   | ease_of_use        |
| r0045       | Excellent bluetooth headset.                                                                                                                         | positive    | general_sentiment  | ease_of_use        |
| r0060       | The buttons for on and off are bad.                                                                                                                  | negative    | features_design    | ease_of_use        |
| r0077       | Do Not Buy for D807...wrongly advertised for D807.                                                                                                   | negative    | ease_of_use        | general_sentiment  |
| r0089       | Product was excellent and works better than the verizon one and Boy was it cheaper!                                                                  | positive    | value_price        | service_delivery   |
| r0097       | If you plan to use this in a car forget about it.                                                                                                    | negative    | general_sentiment  | ease_of_use        |
| r0108       | I love my 350 headset.. My Jabra350 bluetooth headset is great, the reception is very good and the ear piece is a comfortable fit.                   | positive    | audio_call_quality | fit_comfort        |
| r0140       | Voice recognition is tremendous!                                                                                                                     | positive    | features_design    | audio_call_quality |
| r0159       | And I just love the colors!                                                                                                                          | positive    | features_design    | general_sentiment  |
| r0169       | doesn't last long.                                                                                                                                   | negative    | build_durability   | general_sentiment  |
| r0175       | The file browser offers all the options that one needs.Handsfree is great.                                                                           | positive    | features_design    | general_sentiment  |
| r0185       | I recently had problems where I could not stay connected for more than 10 minutes before being disconnected.                                         | negative    | ease_of_use        | general_sentiment  |
| r0245       | It defeats the purpose of a bluetooth headset.                                                                                                       | negative    | general_sentiment  | ease_of_use        |
| r0255       | This product had a strong rubber/petroleum smell that was unbearable after a while and caused me to return it                                        | negative    | build_durability   | service_delivery   |
| r0262       | Only had this a month but it's worked flawlessly so far.                                                                                             | positive    | build_durability   | general_sentiment  |
| r0267       | Returned 8 hours later.                                                                                                                              | negative    | general_sentiment  | service_delivery   |
| r0282       | I love this bluetooth!                                                                                                                               | positive    | general_sentiment  | ease_of_use        |
| r0287       | Piece of Junk.                                                                                                                                       | negative    | general_sentiment  | build_durability   |
| r0353       | Their network coverage in Los Angeles is horrible.                                                                                                   | negative    | audio_call_quality | general_sentiment  |
| r0360       | Nice design and quality.                                                                                                                             | positive    | features_design    | build_durability   |
| r0424       | Overall, I am psyched to have a phone which has all my appointments and contacts in and gets great reception.                                        | positive    | features_design    | audio_call_quality |
| r0443       | I would recommend purchasing the Jabra JX-10 series 2 which works flawlessly with my Moto Q, go figure.                                              | positive    | ease_of_use        | general_sentiment  |
| r0479       | The keyboard is really worthwhile in usefulness and is sturdy enough I don't expect any problems.                                                    | positive    | features_design    | build_durability   |
| r0486       | Unfortunately the ability to actually know you are receiving a call is a rather important feature and this phone is pitiful in that respect.         | negative    | features_design    | audio_call_quality |
| r0523       | REALLY UGLY.                                                                                                                                         | negative    | features_design    | general_sentiment  |
| r0524       | horrible, had to switch 3 times.                                                                                                                     | negative    | build_durability   | general_sentiment  |
| r0537       | none of the new ones have ever quite worked properly.                                                                                                | negative    | build_durability   | general_sentiment  |
| r0539       | I've missed numerous calls because of this reason.                                                                                                   | negative    | general_sentiment  | audio_call_quality |
| r0549       | Its a total package.                                                                                                                                 | positive    | general_sentiment  | service_delivery   |
| r0584       | Also difficult to put on.I'd recommend avoiding this product.                                                                                        | negative    | fit_comfort        | ease_of_use        |
| r0592       | What possesed me to get this junk, I have no idea...                                                                                                 | negative    | general_sentiment  | build_durability   |
| r0604       | Sprint charges for this service.                                                                                                                     | negative    | value_price        | service_delivery   |
| r0617       | Steer clear of this product and go with the genuine Palm replacementr pens, which come in a three-pack.                                              | negative    | general_sentiment  | audio_call_quality |
| r0627       | Don't bother - go to the store.                                                                                                                      | negative    | general_sentiment  | service_delivery   |
| r0656       | It felt too light and "tinny.".                                                                                                                      | negative    | build_durability   | general_sentiment  |
| r0667       | its extremely slow and takes forever to do anything with it.                                                                                         | negative    | ease_of_use        | general_sentiment  |
| r0673       | Bluetooth does not work, phone locks up, screens just flash up and now it just makes calls randomly while in my pocket locked.                       | negative    | ease_of_use        | audio_call_quality |
| r0738       | Couldn't use the unit with sunglasses, not good in Texas!                                                                                            | negative    | fit_comfort        | ease_of_use        |
| r0744       | .... Item arrived quickly and works great with my Metro PCS Samsung SCH-r450 slider phone and Sony Premium Sound in ear plugs.                       | positive    | service_delivery   | audio_call_quality |
| r0750       | Then a few days later the a puff of smoke came out of the phone while in use.                                                                        | negative    | build_durability   | ease_of_use        |
| r0756       | They have been around for years and carries the highest quality of anti-glare screen protector that I have found to date.                            | positive    | features_design    | build_durability   |
| r0782       | It's a great tool for entertainment, communication, and data management.Oh, be sure to use ActiveSync 4.2 for optimal data synchronization results!  | positive    | features_design    | ease_of_use        |
| r0790       | A good quality bargain.. I bought this after I bought a cheapy from Big Lots that sounded awful and people on the other end couldn't hear me.        | positive    | value_price        | audio_call_quality |
| r0856       | I have only had it for a few weeks, but so far, so good.                                                                                             | positive    | general_sentiment  | build_durability   |
| r0864       | I received my headset in good time and was happy with it.                                                                                            | positive    | service_delivery   | general_sentiment  |
| r0868       | This is by far the worst purchase I've made on Amazon.                                                                                               | negative    | general_sentiment  | service_delivery   |
| r0893       | The cutouts and buttons are placed perfectly.                                                                                                        | positive    | features_design    | ease_of_use        |
| r0905       | My phone sounded OK ( not great - OK), but my wife's phone was almost totally unintelligible, she couldn't understand a word being said on it.       | negative    | audio_call_quality | general_sentiment  |
| r0926       | However, after about a year, the fliptop started to get loose and wobbly and eventually my screen went black and I couldn't receive and place calls. | negative    | build_durability   | audio_call_quality |
| r0929       | Logitech Bluetooth Headset is a 10!.                                                                                                                 | positive    | general_sentiment  | ease_of_use        |
| r0932       | I have tried these cables with my computer and my iPod and it works just fine.                                                                       | positive    | ease_of_use        | general_sentiment  |
| r0938       | Otherwise, easy to install and use, clear sound.                                                                                                     | positive    | ease_of_use        | audio_call_quality |
| r0939       | nice leather.                                                                                                                                        | positive    | features_design    | general_sentiment  |
| r0986       | The screen does get smudged easily because it touches your ear and face.                                                                             | negative    | features_design    | fit_comfort        |
