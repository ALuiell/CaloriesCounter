# Seed Expansion Candidates

Отчет подготовлен для расширения `data/seeds/starter_products_usda_sr_legacy.json`. Seed-файл на этом шаге не менялся.

Метод: для каждого выбранного продукта был выполнен поиск через `scripts/find_usda_candidates.py` с фильтрами `--category` и `--keyword`; затем из локального `FoodData_Central_sr_legacy_food_json_2018-04.json` выбраны generic USDA SR Legacy записи без брендов, restaurant/fast food/baby food и без лишних canned/salted/prepared вариантов, когда был простой raw/cooked/plain вариант.

## Summary

| USDA category | Кандидатов |
| --- | ---: |
| Vegetables and Vegetable Products | 10 |
| Fruits and Fruit Juices | 10 |
| Dairy and Egg Products | 10 |
| Cereal Grains and Pasta | 12 |
| Legumes and Legume Products | 16 |
| Всего | 58 |

## Vegetables and Vegetable Products

| Русское название | Будущий slug | Категория проекта | State | USDA fdcId | USDA description | USDA category | calories_per_100g | protein_per_100g | fat_per_100g | carbs_per_100g | Почему выбран / неоднозначность |
| --- | --- | --- | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| шпинат | `spinach_raw` | овощи | сырой продукт | 168462 | Spinach, raw | Vegetables and Vegetable Products | 23 | 2.86 | 0.39 | 3.63 | Самая простая запись для шпината, без frozen/canned/salted. Неоднозначность: есть cooked-вариант, но для базового овоща raw лучше как нейтральная точка. |
| кабачок цукини | `zucchini_raw` | овощи | сырой продукт | 169291 | Squash, summer, zucchini, includes skin, raw | Vegetables and Vegetable Products | 17 | 1.21 | 0.32 | 3.11 | Generic raw zucchini с кожурой, лучше canned/frozen вариантов. Неоднозначность: в русском "кабачок" шире, чем zucchini. |
| свекла вареная | `beets_boiled` | овощи | готовый продукт | 169146 | Beets, cooked, boiled, drained | Vegetables and Vegetable Products | 44 | 1.68 | 0.18 | 9.96 | Простая вареная свекла без соли, ближе к частому пользовательскому запросу "свекла". Неоднозначность: есть raw-вариант для отдельного slug. |
| баклажан сырой | `eggplant_raw` | овощи | сырой продукт | 169228 | Eggplant, raw | Vegetables and Vegetable Products | 25 | 0.98 | 0.18 | 5.88 | Самая generic запись без маринада и приготовления. Неоднозначность: в реальном питании чаще нужен cooked-вариант. |
| спаржа | `asparagus_raw` | овощи | сырой продукт | 168389 | Asparagus, raw | Vegetables and Vegetable Products | 20 | 2.2 | 0.12 | 3.88 | Простая raw-запись, без frozen/canned/salt. Неоднозначность: cooked boiled тоже хорош для отдельного уточнения. |
| сельдерей стеблевой | `celery_raw` | овощи | сырой продукт | 169988 | Celery, raw | Vegetables and Vegetable Products | 14 | 0.69 | 0.17 | 2.97 | Generic raw celery; не соус и не смесь овощей. Неоднозначность: USDA не уточняет "стеблевой" в названии, но это наиболее ожидаемая интерпретация. |
| редис | `radish_raw` | овощи | сырой продукт | 169276 | Radishes, raw | Vegetables and Vegetable Products | 16 | 0.68 | 0.1 | 3.4 | Самый простой raw-вариант обычного редиса, не oriental/pickled. Неоднозначность: нет существенной. |
| батат запеченный | `sweet_potato_baked` | овощи | готовый продукт | 168483 | Sweet potato, cooked, baked in skin, flesh, without salt | Vegetables and Vegetable Products | 90 | 2.01 | 0.15 | 20.7 | Plain baked sweet potato без соли и без french fried/puffs. Неоднозначность: есть raw и boiled варианты; baked выбран как частая съедобная форма. |
| тыква вареная | `pumpkin_boiled` | овощи | готовый продукт | 168449 | Pumpkin, cooked, boiled, drained, without salt | Vegetables and Vegetable Products | 20 | 0.72 | 0.07 | 4.9 | Plain cooked pumpkin без canned pie mix и без соли. Неоднозначность: raw pumpkin тоже доступна, но cooked полезнее как дефолт. |
| фасоль стручковая вареная | `green_beans_boiled` | овощи | готовый продукт | 169141 | Beans, snap, green, cooked, boiled, drained, without salt | Vegetables and Vegetable Products | 35 | 1.89 | 0.28 | 7.88 | Plain cooked green snap beans, без canned и salted. Неоднозначность: это овощная стручковая фасоль, не зрелые бобовые. |

## Fruits and Fruit Juices

| Русское название | Будущий slug | Категория проекта | State | USDA fdcId | USDA description | USDA category | calories_per_100g | protein_per_100g | fat_per_100g | carbs_per_100g | Почему выбран / неоднозначность |
| --- | --- | --- | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| арбуз | `watermelon_raw` | фрукты и ягоды | сырой продукт | 167765 | Watermelon, raw | Fruits and Fruit Juices | 30 | 0.61 | 0.15 | 7.55 | Простая raw-запись без сиропов и соков. Неоднозначность: нет существенной. |
| дыня канталупа | `cantaloupe_raw` | фрукты и ягоды | сырой продукт | 169092 | Melons, cantaloupe, raw | Fruits and Fruit Juices | 34 | 0.84 | 0.19 | 8.16 | Generic raw melon для частого запроса "дыня". Неоднозначность: канталупа не покрывает все сорта дыни. |
| ананас | `pineapple_raw` | фрукты и ягоды | сырой продукт | 169124 | Pineapple, raw, all varieties | Fruits and Fruit Juices | 50 | 0.54 | 0.12 | 13.1 | Raw all varieties лучше canned/juice/syrup. Неоднозначность: нет существенной. |
| манго | `mango_raw` | фрукты и ягоды | сырой продукт | 169910 | Mangos, raw | Fruits and Fruit Juices | 60 | 0.82 | 0.38 | 15 | Простая raw-запись, не nectar и не dried sweetened. Неоднозначность: нет существенной. |
| грейпфрут | `grapefruit_raw` | фрукты и ягоды | сырой продукт | 173033 | Grapefruit, raw, pink and red and white, all areas | Fruits and Fruit Juices | 32 | 0.63 | 0.1 | 8.08 | Сводная raw-запись по цветам и регионам лучше отдельных juice/canned. Неоднозначность: усредняет разные сорта. |
| лимон | `lemon_raw` | фрукты и ягоды | сырой продукт | 167746 | Lemons, raw, without peel | Fruits and Fruit Juices | 29 | 1.1 | 0.3 | 9.32 | Plain raw lemon без кожуры, ближе к обычному учету мякоти/сока. Неоднозначность: не включает цедру. |
| лайм | `lime_raw` | фрукты и ягоды | сырой продукт | 168155 | Limes, raw | Fruits and Fruit Juices | 30 | 0.7 | 0.2 | 10.5 | Простая raw-запись. Неоднозначность: нет существенной. |
| малина | `raspberry_raw` | фрукты и ягоды | сырой продукт | 167755 | Raspberries, raw | Fruits and Fruit Juices | 52 | 1.2 | 0.65 | 11.9 | Raw berries без canned/frozen sweetened/puree. Неоднозначность: нет существенной. |
| ежевика | `blackberry_raw` | фрукты и ягоды | сырой продукт | 173946 | Blackberries, raw | Fruits and Fruit Juices | 43 | 1.39 | 0.49 | 9.61 | Raw berries лучше canned syrup/frozen. Неоднозначность: нет существенной. |
| черешня | `sweet_cherries_raw` | фрукты и ягоды | сырой продукт | 171719 | Cherries, sweet, raw | Fruits and Fruit Juices | 63 | 1.06 | 0.2 | 16 | Plain sweet raw cherries, без canned/dried/syrup. Неоднозначность: для "вишня" нужен отдельный sour cherries candidate. |

## Dairy and Egg Products

| Русское название | Будущий slug | Категория проекта | State | USDA fdcId | USDA description | USDA category | calories_per_100g | protein_per_100g | fat_per_100g | carbs_per_100g | Почему выбран / неоднозначность |
| --- | --- | --- | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| молоко цельное 3.25% | `milk_whole_3_25pct` | молочные продукты | готовый продукт | 171265 | Milk, whole, 3.25% milkfat, with added vitamin D | Dairy and Egg Products | 61 | 3.15 | 3.25 | 4.8 | Базовое цельное молоко, дополняет уже имеющиеся 1% и 2%. Неоднозначность: fortified vitamin D, но это generic SR Legacy запись. |
| молоко обезжиренное | `milk_nonfat` | молочные продукты | готовый продукт | 171269 | Milk, nonfat, fluid, with added vitamin A and vitamin D (fat free or skim) | Dairy and Egg Products | 34 | 3.37 | 0.08 | 4.96 | Базовое skim/nonfat молоко, не protein fortified и не powdered. Неоднозначность: fortified vitamins. |
| яичный белок сырой | `egg_white_raw` | яйца | сырой продукт | 172183 | Egg, white, raw, fresh | Dairy and Egg Products | 52 | 10.9 | 0.17 | 0.73 | Простая fresh raw запись, полезна для частого учета белков отдельно. Неоднозначность: нет cooked-варианта в этом candidate. |
| яичный желток сырой | `egg_yolk_raw` | яйца | сырой продукт | 172184 | Egg, yolk, raw, fresh | Dairy and Egg Products | 322 | 15.9 | 26.5 | 3.59 | Простая fresh raw запись, дополняет whole egg. Неоднозначность: нет cooked-варианта в этом candidate. |
| сливки 36% | `heavy_cream` | молочные продукты | готовый продукт | 170859 | Cream, fluid, heavy whipping | Dairy and Egg Products | 340 | 2.84 | 36.1 | 2.84 | Generic heavy cream без подсластителей и добавок. Неоднозначность: "whipping" может отличаться от русских сливок по жирности. |
| сыр пармезан | `parmesan` | молочные продукты | готовый продукт | 170848 | Cheese, parmesan, hard | Dairy and Egg Products | 392 | 35.8 | 25 | 3.22 | Hard parmesan лучше grated/reduced-fat/low-sodium как базовый сыр. Неоднозначность: нет существенной. |
| сыр швейцарский | `swiss_cheese` | молочные продукты | готовый продукт | 171251 | Cheese, swiss | Dairy and Egg Products | 393 | 27 | 31 | 1.44 | Plain cheese entry без low-fat/low-sodium. Неоднозначность: сортовое название обобщает несколько близких сыров. |
| сыр гауда | `gouda` | молочные продукты | готовый продукт | 171241 | Cheese, gouda | Dairy and Egg Products | 356 | 24.9 | 27.4 | 2.22 | Простая запись для популярного сыра без вариантов жирности. Неоднозначность: нет существенной. |
| сыр рикотта цельномолочная | `ricotta_whole_milk` | молочные продукты | готовый продукт | 170851 | Cheese, ricotta, whole milk | Dairy and Egg Products | 150 | 7.54 | 10.2 | 7.27 | Plain whole milk ricotta; более нейтрально, чем part skim, если жирность не уточнена. Неоднозначность: для нежирной рикотты нужен отдельный slug. |
| сыр сливочный | `cream_cheese` | молочные продукты | готовый продукт | 173418 | Cheese, cream | Dairy and Egg Products | 350 | 6.15 | 34.4 | 5.52 | Plain cream cheese, без low-fat/fat-free. Неоднозначность: не равно плавленому сыру. |

## Cereal Grains and Pasta

| Русское название | Будущий slug | Категория проекта | State | USDA fdcId | USDA description | USDA category | calories_per_100g | protein_per_100g | fat_per_100g | carbs_per_100g | Почему выбран / неоднозначность |
| --- | --- | --- | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| перловка сухая | `barley_pearled_dry` | крупы и гарниры | сухой продукт | 170284 | Barley, pearled, raw | Cereal Grains and Pasta | 352 | 9.91 | 1.16 | 77.7 | Plain pearled barley raw, нужная сухая пара к cooked. Неоднозначность: "raw" в USDA соответствует сухой крупе. |
| перловка вареная | `barley_pearled_cooked` | крупы и гарниры | готовый продукт | 170285 | Barley, pearled, cooked | Cereal Grains and Pasta | 123 | 2.26 | 0.44 | 28.2 | Plain cooked pearled barley, без соли и добавок. Неоднозначность: нет существенной. |
| булгур сухой | `bulgur_dry` | крупы и гарниры | сухой продукт | 170688 | Bulgur, dry | Cereal Grains and Pasta | 342 | 12.3 | 1.33 | 75.9 | Простая dry запись, нужна из-за сильной разницы с cooked. Неоднозначность: нет существенной. |
| булгур вареный | `bulgur_cooked` | крупы и гарниры | готовый продукт | 170287 | Bulgur, cooked | Cereal Grains and Pasta | 83 | 3.08 | 0.24 | 18.6 | Plain cooked bulgur, хороший дефолт для обычного запроса "булгур". Неоднозначность: нет существенной. |
| кускус сухой | `couscous_dry` | крупы и гарниры | сухой продукт | 169699 | Couscous, dry | Cereal Grains and Pasta | 376 | 12.8 | 0.64 | 77.4 | Простая dry запись, без seasoning. Неоднозначность: нет существенной. |
| кускус готовый | `couscous_cooked` | крупы и гарниры | готовый продукт | 169700 | Couscous, cooked | Cereal Grains and Pasta | 112 | 3.79 | 0.16 | 23.2 | Plain cooked couscous, лучший дефолт для блюда без уточнения сухого веса. Неоднозначность: нет существенной. |
| киноа сухая | `quinoa_dry` | крупы и гарниры | сухой продукт | 168874 | Quinoa, uncooked | Cereal Grains and Pasta | 368 | 14.1 | 6.07 | 64.2 | Plain uncooked quinoa, нужна сухая пара к cooked. Неоднозначность: в названии USDA "uncooked", в seed лучше state "сухой продукт". |
| киноа вареная | `quinoa_cooked` | крупы и гарниры | готовый продукт | 168917 | Quinoa, cooked | Cereal Grains and Pasta | 120 | 4.4 | 1.92 | 21.3 | Plain cooked quinoa, без смесей с пастой. Неоднозначность: нет существенной. |
| пшено сухое | `millet_dry` | крупы и гарниры | сухой продукт | 169702 | Millet, raw | Cereal Grains and Pasta | 378 | 11 | 4.22 | 72.8 | Plain millet raw, подходит как сухая крупа. Неоднозначность: "millet" шире русского "пшено". |
| пшено вареное | `millet_cooked` | крупы и гарниры | готовый продукт | 168871 | Millet, cooked | Cereal Grains and Pasta | 119 | 3.51 | 1 | 23.7 | Plain cooked millet, полезно как готовая каша/гарнир. Неоднозначность: способ приготовления без молока и масла. |
| мука пшеничная цельнозерновая | `whole_wheat_flour` | крупы и гарниры | сухой продукт | 168893 | Wheat flour, whole-grain (Includes foods for USDA's Food Distribution Program) | Cereal Grains and Pasta | 340 | 13.2 | 2.5 | 72 | Generic whole-grain wheat flour, без self-rising/enriched white вариантов. Неоднозначность: includes USDA distribution note, но продукт generic. |
| кукурузная крупа желтая | `cornmeal_yellow` | крупы и гарниры | сухой продукт | 168867 | Cornmeal, degermed, enriched, yellow | Cereal Grains and Pasta | 370 | 7.11 | 1.75 | 79.4 | Базовый yellow cornmeal, лучше self-rising и mixed wheat flour вариантов. Неоднозначность: enriched/degermed; цельнозернового plain cornmeal в выдаче не было среди лучших generic. |

## Legumes and Legume Products

| Русское название | Будущий slug | Категория проекта | State | USDA fdcId | USDA description | USDA category | calories_per_100g | protein_per_100g | fat_per_100g | carbs_per_100g | Почему выбран / неоднозначность |
| --- | --- | --- | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| фасоль черная сухая | `black_beans_dry` | бобовые | сухой продукт | 173734 | Beans, black, mature seeds, raw | Legumes and Legume Products | 341 | 21.6 | 1.42 | 62.4 | Plain mature black beans raw, нужна сухая пара к cooked. Неоднозначность: "raw" означает сухие зрелые бобы. |
| фасоль черная вареная | `black_beans_cooked` | бобовые | готовый продукт | 173735 | Beans, black, mature seeds, cooked, boiled, without salt | Legumes and Legume Products | 132 | 8.86 | 0.54 | 23.7 | Plain boiled black beans without salt, не canned. Неоднозначность: есть black turtle beans, но эта запись более общая. |
| фасоль пинто сухая | `pinto_beans_dry` | бобовые | сухой продукт | 175199 | Beans, pinto, mature seeds, raw (Includes foods for USDA's Food Distribution Program) | Legumes and Legume Products | 347 | 21.4 | 1.23 | 62.6 | Plain mature pinto beans raw, сухая пара к cooked. Неоднозначность: includes USDA distribution note, но без бренда/готового блюда. |
| фасоль пинто вареная | `pinto_beans_cooked` | бобовые | готовый продукт | 175200 | Beans, pinto, mature seeds, cooked, boiled, without salt | Legumes and Legume Products | 143 | 9.01 | 0.65 | 26.2 | Plain boiled pinto beans without salt, лучше canned. Неоднозначность: нет существенной. |
| фасоль navy сухая | `navy_beans_dry` | бобовые | сухой продукт | 173745 | Beans, navy, mature seeds, raw | Legumes and Legume Products | 337 | 22.3 | 1.5 | 60.8 | Plain mature navy beans raw, сухая пара к cooked. Неоднозначность: русское название лучше уточнить позже как "мелкая белая фасоль". |
| фасоль navy вареная | `navy_beans_cooked` | бобовые | готовый продукт | 173746 | Beans, navy, mature seeds, cooked, boiled, without salt | Legumes and Legume Products | 140 | 8.23 | 0.62 | 26 | Plain boiled navy beans without salt, не canned. Неоднозначность: русское название требует алиасов "белая мелкая фасоль". |
| фасоль лима сухая | `lima_beans_dry` | бобовые | сухой продукт | 174252 | Lima beans, large, mature seeds, raw | Legumes and Legume Products | 338 | 21.5 | 0.69 | 63.4 | Plain large mature lima beans raw, сухая пара к cooked. Неоднозначность: есть baby/thin seeded lima beans, выбран large как более общий вариант. |
| фасоль лима вареная | `lima_beans_cooked` | бобовые | готовый продукт | 174253 | Lima beans, large, mature seeds, cooked, boiled, without salt | Legumes and Legume Products | 115 | 7.8 | 0.38 | 20.9 | Plain boiled large lima beans without salt, не canned. Неоднозначность: есть baby lima beans с другой калорийностью. |
| соевые бобы сухие | `soybeans_dry` | бобовые | сухой продукт | 174270 | Soybeans, mature seeds, raw | Legumes and Legume Products | 446 | 36.5 | 19.9 | 30.2 | Plain mature soybeans raw, лучше roasted/salted. Неоднозначность: "raw" здесь сухие зрелые бобы, не зеленая эдамаме. |
| соевые бобы вареные | `soybeans_cooked` | бобовые | готовый продукт | 174271 | Soybeans, mature cooked, boiled, without salt | Legumes and Legume Products | 172 | 18.2 | 8.97 | 8.36 | Plain boiled mature soybeans without salt. Неоднозначность: description пропускает слово "seeds", но категория и макросы соответствуют mature soybeans. |
| тофу твердый | `tofu_firm` | бобовые | готовый продукт | 172448 | Tofu, firm, prepared with calcium sulfate and magnesium chloride (nigari) | Legumes and Legume Products | 78 | 9.04 | 4.17 | 2.85 | Generic firm tofu без бренда, не fried и не fermented. Неоднозначность: tofu технологически prepared, но это базовый legume product. |
| горох колотый вареный | `split_peas_cooked` | бобовые | готовый продукт | 172429 | Peas, split, mature seeds, cooked, boiled, without salt | Legumes and Legume Products | 118 | 8.34 | 0.39 | 21.1 | Plain boiled split peas without salt. Неоднозначность: dry split peas не попали в выдачу скрипта по выбранному keyword, можно искать отдельно позже. |
| маш сухой | `mung_beans_dry` | бобовые | сухой продукт | 174256 | Mung beans, mature seeds, raw | Legumes and Legume Products | 347 | 23.9 | 1.15 | 62.6 | Plain mature mung beans raw, сухая пара к cooked. Неоднозначность: не cellophane noodles и не sprouts. |
| маш вареный | `mung_beans_cooked` | бобовые | готовый продукт | 174257 | Mung beans, mature seeds, cooked, boiled, without salt | Legumes and Legume Products | 105 | 7.02 | 0.38 | 19.2 | Plain boiled mung beans without salt. Неоднозначность: не проростки маша. |
| бобы фава вареные | `fava_beans_cooked` | бобовые | готовый продукт | 173753 | Broadbeans (fava beans), mature seeds, cooked, boiled, without salt | Legumes and Legume Products | 110 | 7.6 | 0.4 | 19.6 | Plain boiled fava beans without salt, не canned. Неоднозначность: русские алиасы могут быть "конские бобы"/"бобы фава". |
| арахисовая паста без соли | `peanut_butter_smooth_unsalted` | бобовые | готовый продукт | 172470 | Peanut butter, smooth style, without salt | Legumes and Legume Products | 598 | 22.2 | 51.4 | 22.3 | Generic smooth peanut butter without salt, лучше fortified/reduced-fat/salted. Неоднозначность: это processed продукт, но USDA относит его к Legumes and Legume Products. |

## Validation

Текущий seed после подготовки отчета нужно валидировать командой:

```powershell
python scripts/validate_starter_seed.py
```