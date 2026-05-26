# USDA SR Legacy Analysis

## Purpose

This document summarizes what the project currently knows about the USDA SR Legacy dataset and how that affects implementation decisions.

## Summary

- Source file: `FoodData_Central_sr_legacy_food_json_2018-04.json`
- Total foods: `7793`
- Total categories: `25`

## Macro Coverage

- Calories (`Energy`, `kcal`): `7793`
- Protein (`Protein`, `g`): `7793`
- Fat (`Total lipid (fat)`, `g`): `7793`
- Carbs (`Carbohydrate, by difference`, `g`): `7793`

All 4 core values exist for all `7793` records, so the main problem is not missing macros. The real problem is record noise, naming style, and product normalization.

## Top Categories

- Beef Products: 954
- Vegetables and Vegetable Products: 814
- Baked Products: 517
- Lamb, Veal, and Game Products: 464
- Poultry Products: 383
- Beverages: 366
- Sweets: 358
- Fruits and Fruit Juices: 355
- Baby Foods: 345
- Pork Products: 336

## Description Signals

- Contains `raw`: `1433`
- Contains `cooked`: `1806`
- Contains `canned`: `499`
- Contains `without salt`: `265`
- Contains USDA distribution note: `57`

## Basic Filter Result

- Kept after basic filter: `7213`
- Excluded after basic filter: `580`
- Excluded prepared or restaurant: `371`
- Excluded brand-like: `98`
- Excluded category-level noise: `111`

## Top Categories After Basic Filter

- Beef Products: 954
- Vegetables and Vegetable Products: 814
- Baked Products: 517
- Lamb, Veal, and Game Products: 464
- Poultry Products: 383
- Beverages: 366
- Sweets: 357
- Fruits and Fruit Juices: 355
- Pork Products: 335
- Dairy and Egg Products: 291

## Useful Samples

### Vegetables and Vegetable Products
- Seaweed, Canadian Cultivated EMI-TSUNOMATA, dry
- Seaweed, Canadian Cultivated EMI-TSUNOMATA, rehydrated
- Potatoes, hash brown, refrigerated, unprepared
- Potatoes, hash brown, refrigerated, prepared, pan-fried in canola oil
- Sweet Potatoes, french fried, frozen as packaged, salt added in processing
- Tomato and vegetable juice, low sodium

### Fruits and Fruit Juices
- Lemons, raw, without peel
- Lemon juice, raw
- Lemon juice from concentrate, canned or bottled
- Lemon peel, raw
- Prickly pears, raw
- Plums, dried (prunes), stewed, without added sugar

### Cereal Grains and Pasta
- Vital wheat gluten
- Cornmeal, degermed, enriched, yellow
- Cornmeal, yellow, self-rising, bolted, plain, enriched
- Cornmeal, yellow, self-rising, bolted, with wheat flour added, enriched
- Cornmeal, yellow, self-rising, degermed, enriched
- Millet, cooked

### Legumes and Legume Products
- Chicken, meatless, breaded, fried
- Tofu yogurt
- Papad
- Beans, baked, canned, no salt added
- Beans, chili, barbecue, ranch style, cooked
- Luncheon slices, meatless

### Dairy and Egg Products
- Whipped topping, frozen, low fat
- Cream substitute, powdered, light
- Milk, buttermilk, fluid, cultured, reduced fat
- Cheese, cottage, lowfat, 1% milkfat, lactose reduced
- Cheese, parmesan, low sodium
- Cheese, cottage, lowfat, 1% milkfat, with vegetables

### Poultry Products
- Turkey, wing, smoked, cooked, with skin, bone removed
- Turkey, drumstick, smoked, cooked, with skin, bone removed
- Turkey, light or dark meat, smoked, cooked, skin and bone removed
- Turkey, light or dark meat, smoked, cooked, with skin, bone removed
- Quail, cooked, total edible
- Pheasant, cooked, total edible

### Beef Products
- Beef, retail cuts, separable fat, raw
- Beef, retail cuts, separable fat, cooked
- Beef, brisket, whole, separable lean only, all grades, raw
- Beef, grass-fed, ground, raw
- Beef, flank, steak, separable lean only, trimmed to 0" fat, choice, raw
- Beef, flank, steak, separable lean only, trimmed to 0" fat, choice, cooked, braised

### Pork Products
- Pork, cured, bacon, cooked, broiled, pan-fried or roasted, reduced sodium
- Pork, fresh, composite of trimmed leg, loin, shoulder, and spareribs, (includes cuts to be cured), separable lean and fat, raw
- Pork, fresh, backfat, raw
- Pork, fresh, belly, raw
- Pork, fresh, separable fat, raw
- Pork, fresh, leg (ham), rump half, separable lean and fat, raw

### Finfish and Shellfish Products
- Mollusks, scallop, (bay and sea), cooked, steamed
- Mollusks, snail, raw
- Turtle, green, raw
- Jellyfish, dried, salted
- Frog legs, raw
- Fish, mackerel, salted

### Fats and Oils
- Creamy dressing, made with sour cream and/or buttermilk and oil, reduced calorie
- Vegetable oil-butter spread, reduced calorie
- Salad dressing, blue or roquefort cheese dressing, light
- Salad dressing, french dressing, reduced calorie
- Mayonnaise, made with tofu
- Salad dressing, blue or roquefort cheese dressing, fat-free

## Recommendations

- Do not query the 211 MB source file at runtime from the bot.
- Keep USDA as a source dataset and import only the normalized fields you need.
- For level 1, use a curated starter table with Russian names and aliases.
- Build a second-stage importer that writes normalized products into SQLite.
- Treat dry/cooked/raw variants as separate products when calories differ materially.
- Filter out restaurant, fast-food, baby-food, and obvious brand-heavy records before broad import.

## Related Files

- [Starter Products](F:\Python\CaloriesCounter\docs\starter-products.md)
- [Seed Expansion Candidates](F:\Python\CaloriesCounter\docs\seed-expansion-candidates.md)
- [Documentation Standard](F:\Python\CaloriesCounter\docs\documentation-standard.md)
