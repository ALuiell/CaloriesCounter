import argparse
import json
import re
from pathlib import Path


SOURCE_PATH = Path("FoodData_Central_sr_legacy_food_json_2018-04.json")

MACRO_NUTRIENTS = [
    ("Energy", "kcal", "calories_per_100g"),
    ("Protein", "g", "protein_per_100g"),
    ("Total lipid (fat)", "g", "fat_per_100g"),
    ("Carbohydrate, by difference", "g", "carbs_per_100g"),
]

PREPARED_PREFIXES = ("Restaurant,", "Fast foods,", "Babyfood,", "Baby foods,")
EXCLUDED_CATEGORY_PARTS = ("restaurant", "fast food", "baby food")
BRAND_START_RE = re.compile(r"^[A-Z0-9&'.-]{3,},")
BRAND_PHRASE_RE = re.compile(
    r"\b(brand|brands|trademark|mcdonald|burger king|kfc|taco bell|wendy)\b",
    re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find USDA SR Legacy candidates for the starter seed."
    )
    parser.add_argument(
        "--category",
        default="",
        help="Case-insensitive substring filter for foodCategory.description.",
    )
    parser.add_argument(
        "--keyword",
        default="",
        help="Case-insensitive substring filter for description.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of candidates to print.",
    )
    parser.add_argument(
        "--format",
        choices=("table", "json"),
        default="table",
        help="Output format.",
    )
    return parser.parse_args()


def load_foods(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload.get("SRLegacyFoods", [])


def build_nutrient_map(food: dict) -> dict[tuple[str, str], float]:
    nutrients: dict[tuple[str, str], float] = {}
    for item in food.get("foodNutrients", []):
        nutrient = item.get("nutrient") or {}
        name = nutrient.get("name")
        unit_name = nutrient.get("unitName")
        amount = item.get("amount")
        if name and unit_name and amount is not None:
            nutrients[(name, unit_name)] = float(amount)
    return nutrients


def extract_macros(food: dict) -> dict[str, float] | None:
    nutrient_map = build_nutrient_map(food)
    macros: dict[str, float] = {}
    for nutrient_name, unit_name, field_name in MACRO_NUTRIENTS:
        value = nutrient_map.get((nutrient_name, unit_name))
        if value is None:
            return None
        macros[field_name] = value
    return macros


def is_excluded(description: str, category: str) -> bool:
    lowered_category = category.lower()
    lowered_description = description.lower()
    if description.startswith(PREPARED_PREFIXES):
        return True
    if any(part in lowered_category for part in EXCLUDED_CATEGORY_PARTS):
        return True
    if "fast food" in lowered_description or "restaurant" in lowered_description:
        return True
    if BRAND_START_RE.search(description) or BRAND_PHRASE_RE.search(description):
        return True
    return False


def matches_filters(
    description: str,
    category: str,
    category_filter: str,
    keyword_filter: str,
) -> bool:
    if category_filter and category_filter not in category.lower():
        return False
    if keyword_filter and keyword_filter not in description.lower():
        return False
    return True


def build_candidate(food: dict) -> dict | None:
    description = food.get("description") or ""
    category = (food.get("foodCategory") or {}).get("description") or ""
    if not description or not category:
        return None
    if is_excluded(description, category):
        return None

    macros = extract_macros(food)
    if macros is None:
        return None

    return {
        "fdcId": food.get("fdcId"),
        "description": description,
        "foodCategory": category,
        **macros,
    }


def find_candidates(
    foods: list[dict],
    category_filter: str,
    keyword_filter: str,
    limit: int,
) -> list[dict]:
    candidates: list[dict] = []
    normalized_category = category_filter.casefold()
    normalized_keyword = keyword_filter.casefold()

    for food in foods:
        description = food.get("description") or ""
        category = (food.get("foodCategory") or {}).get("description") or ""
        if not matches_filters(
            description.casefold(),
            category.casefold(),
            normalized_category,
            normalized_keyword,
        ):
            continue

        candidate = build_candidate(food)
        if candidate is None:
            continue

        candidates.append(candidate)
        if len(candidates) >= limit:
            break

    return candidates


def format_number(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".")


def truncate(value: str, width: int) -> str:
    if len(value) <= width:
        return value
    return value[: width - 3] + "..."


def print_table(candidates: list[dict]) -> None:
    headers = ["fdcId", "kcal", "protein", "fat", "carbs", "category", "description"]
    rows = []
    for item in candidates:
        rows.append(
            [
                str(item["fdcId"]),
                format_number(item["calories_per_100g"]),
                format_number(item["protein_per_100g"]),
                format_number(item["fat_per_100g"]),
                format_number(item["carbs_per_100g"]),
                truncate(item["foodCategory"], 32),
                truncate(item["description"], 72),
            ]
        )

    widths = [
        max(len(headers[index]), *(len(row[index]) for row in rows))
        if rows
        else len(header)
        for index, header in enumerate(headers)
    ]

    print("  ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    print("  ".join("-" * width for width in widths))
    for row in rows:
        print("  ".join(value.ljust(widths[index]) for index, value in enumerate(row)))


def main() -> int:
    args = parse_args()
    if args.limit < 1:
        raise SystemExit("--limit must be greater than zero")

    foods = load_foods(SOURCE_PATH)
    candidates = find_candidates(foods, args.category, args.keyword, args.limit)

    if args.format == "json":
        print(json.dumps(candidates, ensure_ascii=False, separators=(",", ":")))
    else:
        print_table(candidates)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())