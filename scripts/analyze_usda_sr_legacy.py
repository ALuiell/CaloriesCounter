import json
import re
from collections import Counter
from pathlib import Path


SOURCE_PATH = Path("FoodData_Central_sr_legacy_food_json_2018-04.json")
JSON_REPORT_PATH = Path("data/analysis/usda_sr_legacy_analysis.json")
MD_REPORT_PATH = Path("docs/usda-analysis.md")

MACRO_NUTRIENTS = [
    ("Energy", "kcal", "calories_per_100g"),
    ("Protein", "g", "protein_per_100g"),
    ("Total lipid (fat)", "g", "fat_per_100g"),
    ("Carbohydrate, by difference", "g", "carbs_per_100g"),
]

BRAND_UPPER_RE = re.compile(r"^[A-Z0-9&'\.-]{3,},")
PREPARED_PREFIXES = ("Restaurant,", "Fast foods,", "Babyfood,")
EXCLUDED_CATEGORIES = {"Meals, Entrees, and Side Dishes", "Restaurant Foods"}

INTERESTING_CATEGORIES = [
    "Vegetables and Vegetable Products",
    "Fruits and Fruit Juices",
    "Cereal Grains and Pasta",
    "Legumes and Legume Products",
    "Dairy and Egg Products",
    "Poultry Products",
    "Beef Products",
    "Pork Products",
    "Finfish and Shellfish Products",
    "Fats and Oils",
]


def load_foods() -> list[dict]:
    with SOURCE_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload["SRLegacyFoods"]


def build_nutrient_map(food: dict) -> dict[tuple[str, str], float]:
    result: dict[tuple[str, str], float] = {}
    for item in food.get("foodNutrients", []):
        nutrient = item.get("nutrient", {})
        key = (nutrient.get("name"), nutrient.get("unitName"))
        amount = item.get("amount")
        if key[0] and key[1] and amount is not None:
            result[key] = float(amount)
    return result


def classify_description(description: str, category: str) -> str | None:
    if description.startswith(PREPARED_PREFIXES):
        return "prepared_or_restaurant"
    if BRAND_UPPER_RE.search(description):
        return "brand_like"
    if category in EXCLUDED_CATEGORIES:
        return "excluded_category"
    return None


def sample_by_category(foods: list[dict], category: str, limit: int = 6) -> list[str]:
    result: list[str] = []
    for food in foods:
        food_category = (food.get("foodCategory") or {}).get("description", "UNKNOWN")
        if food_category != category:
            continue
        description = food.get("description", "")
        if classify_description(description, food_category):
            continue
        result.append(description)
        if len(result) >= limit:
            break
    return result


def build_analysis(foods: list[dict]) -> dict:
    category_counts = Counter(
        (food.get("foodCategory") or {}).get("description", "UNKNOWN")
        for food in foods
    )

    macro_coverage = Counter()
    flags = Counter()
    exclusion_counts = Counter()
    kept_foods: list[dict] = []

    for food in foods:
        description = food.get("description", "")
        category = (food.get("foodCategory") or {}).get("description", "UNKNOWN")
        nutrient_map = build_nutrient_map(food)

        for nutrient_name, unit_name, field_name in MACRO_NUTRIENTS:
            if (nutrient_name, unit_name) in nutrient_map:
                macro_coverage[field_name] += 1

        lowered = description.lower()
        if "raw" in lowered:
            flags["contains_raw"] += 1
        if "cooked" in lowered:
            flags["contains_cooked"] += 1
        if "canned" in lowered:
            flags["contains_canned"] += 1
        if "without salt" in lowered:
            flags["contains_without_salt"] += 1
        if "(includes foods for usda" in lowered:
            flags["contains_usda_distribution_note"] += 1

        reason = classify_description(description, category)
        if reason:
            exclusion_counts[reason] += 1
        else:
            kept_foods.append(food)

    kept_category_counts = Counter(
        (food.get("foodCategory") or {}).get("description", "UNKNOWN")
        for food in kept_foods
    )

    interesting_samples = {
        category: sample_by_category(foods, category)
        for category in INTERESTING_CATEGORIES
    }

    recommendations = [
        "Do not query the 211 MB source file at runtime from the bot.",
        "Keep USDA as a source dataset and import only the normalized fields you need.",
        "For level 1, use a curated starter table with Russian names and aliases.",
        "Build a second-stage importer that writes normalized products into SQLite.",
        "Treat dry/cooked/raw variants as separate products when calories differ materially.",
        "Filter out restaurant, fast-food, baby-food, and obvious brand-heavy records before broad import.",
    ]

    return {
        "source_file": SOURCE_PATH.name,
        "total_foods": len(foods),
        "total_categories": len(category_counts),
        "top_categories": category_counts.most_common(20),
        "macro_coverage": dict(macro_coverage),
        "description_flags": dict(flags),
        "filtered_candidate_counts": {
            "kept_after_basic_filter": len(kept_foods),
            "excluded_after_basic_filter": sum(exclusion_counts.values()),
            "excluded_breakdown": dict(exclusion_counts),
        },
        "top_categories_after_basic_filter": kept_category_counts.most_common(20),
        "interesting_category_samples": interesting_samples,
        "recommendations": recommendations,
    }


def write_reports(analysis: dict) -> None:
    JSON_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_REPORT_PATH.write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    top_categories_lines = "\n".join(
        f"- {name}: {count}"
        for name, count in analysis["top_categories"][:10]
    )
    filtered_categories_lines = "\n".join(
        f"- {name}: {count}"
        for name, count in analysis["top_categories_after_basic_filter"][:10]
    )
    recommendation_lines = "\n".join(
        f"- {item}" for item in analysis["recommendations"]
    )

    sample_sections = []
    for category, samples in analysis["interesting_category_samples"].items():
        lines = "\n".join(f"- {sample}" for sample in samples) or "- No sample found"
        sample_sections.append(f"### {category}\n{lines}")

    md = f"""# USDA SR Legacy Analysis

## Summary

- Source file: `{analysis["source_file"]}`
- Total foods: `{analysis["total_foods"]}`
- Total categories: `{analysis["total_categories"]}`

## Macro Coverage

- Calories (`Energy`, `kcal`): `{analysis["macro_coverage"]["calories_per_100g"]}`
- Protein (`Protein`, `g`): `{analysis["macro_coverage"]["protein_per_100g"]}`
- Fat (`Total lipid (fat)`, `g`): `{analysis["macro_coverage"]["fat_per_100g"]}`
- Carbs (`Carbohydrate, by difference`, `g`): `{analysis["macro_coverage"]["carbs_per_100g"]}`

All 4 core values exist for all `{analysis["total_foods"]}` records, so the main problem is not missing macros. The real problem is record noise, naming style, and product normalization.

## Top Categories

{top_categories_lines}

## Description Signals

- Contains `raw`: `{analysis["description_flags"].get("contains_raw", 0)}`
- Contains `cooked`: `{analysis["description_flags"].get("contains_cooked", 0)}`
- Contains `canned`: `{analysis["description_flags"].get("contains_canned", 0)}`
- Contains `without salt`: `{analysis["description_flags"].get("contains_without_salt", 0)}`
- Contains USDA distribution note: `{analysis["description_flags"].get("contains_usda_distribution_note", 0)}`

## Basic Filter Result

- Kept after basic filter: `{analysis["filtered_candidate_counts"]["kept_after_basic_filter"]}`
- Excluded after basic filter: `{analysis["filtered_candidate_counts"]["excluded_after_basic_filter"]}`
- Excluded prepared or restaurant: `{analysis["filtered_candidate_counts"]["excluded_breakdown"].get("prepared_or_restaurant", 0)}`
- Excluded brand-like: `{analysis["filtered_candidate_counts"]["excluded_breakdown"].get("brand_like", 0)}`
- Excluded category-level noise: `{analysis["filtered_candidate_counts"]["excluded_breakdown"].get("excluded_category", 0)}`

## Top Categories After Basic Filter

{filtered_categories_lines}

## Useful Samples

{"\n\n".join(sample_sections)}

## Recommendations

{recommendation_lines}
"""

    MD_REPORT_PATH.write_text(md, encoding="utf-8")


def main() -> None:
    foods = load_foods()
    analysis = build_analysis(foods)
    write_reports(analysis)
    print(f"Wrote {JSON_REPORT_PATH}")
    print(f"Wrote {MD_REPORT_PATH}")


if __name__ == "__main__":
    main()
