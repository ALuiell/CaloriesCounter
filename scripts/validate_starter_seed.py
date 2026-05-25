import argparse
import json
import math
import re
from pathlib import Path
from typing import Any


SEED_PATH = Path("data/seeds/starter_products_usda_sr_legacy.json")

REQUIRED_FIELDS = [
    "slug",
    "name_ru",
    "category",
    "state",
    "usda_description",
    "aliases",
    "fdc_id",
    "usda_category",
    "calories_per_100g",
    "protein_per_100g",
    "fat_per_100g",
    "carbs_per_100g",
]

MACRO_FIELDS = [
    "calories_per_100g",
    "protein_per_100g",
    "fat_per_100g",
    "carbs_per_100g",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the USDA starter seed.")
    parser.add_argument(
        "--path",
        type=Path,
        default=SEED_PATH,
        help="Path to starter_products_usda_sr_legacy.json.",
    )
    return parser.parse_args()


def load_seed(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError:
        errors.append(f"Seed file not found: {path}")
        return None
    except json.JSONDecodeError as exc:
        errors.append(f"JSON parse error at line {exc.lineno}, column {exc.colno}: {exc.msg}")
        return None

    if not isinstance(payload, dict):
        errors.append("Root JSON value must be an object.")
        return None
    return payload


def normalize_alias(alias: str) -> str:
    return re.sub(r"\s+", " ", alias.strip().casefold())


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_required_fields(product: dict[str, Any], index: int, errors: list[str]) -> None:
    for field in REQUIRED_FIELDS:
        if field not in product:
            errors.append(f"products[{index}] is missing required field: {field}")


def validate_macro_fields(product: dict[str, Any], index: int, errors: list[str]) -> None:
    for field in MACRO_FIELDS:
        value = product.get(field)
        if not is_number(value) or not math.isfinite(float(value)):
            errors.append(f"products[{index}].{field} must be a finite number.")
            continue
        if value < 0:
            errors.append(f"products[{index}].{field} must not be negative.")


def validate_seed(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    products = payload.get("products")
    if not isinstance(products, list) or not products:
        return ["products must be a non-empty list."]

    slug_owner: dict[str, int] = {}
    fdc_owner: dict[Any, int] = {}
    alias_owner: dict[str, tuple[int, str]] = {}

    for index, product in enumerate(products):
        if not isinstance(product, dict):
            errors.append(f"products[{index}] must be an object.")
            continue

        validate_required_fields(product, index, errors)
        validate_macro_fields(product, index, errors)

        slug = product.get("slug")
        if isinstance(slug, str) and slug:
            previous = slug_owner.setdefault(slug, index)
            if previous != index:
                errors.append(
                    f"products[{index}].slug duplicates products[{previous}].slug: {slug}"
                )

        fdc_id = product.get("fdc_id")
        if fdc_id is not None:
            previous = fdc_owner.setdefault(fdc_id, index)
            if previous != index:
                errors.append(
                    f"products[{index}].fdc_id duplicates products[{previous}].fdc_id: {fdc_id}"
                )

        for field in ("category", "state"):
            value = product.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"products[{index}].{field} must be a non-empty string.")

        aliases = product.get("aliases")
        if not isinstance(aliases, list):
            errors.append(f"products[{index}].aliases must be a non-empty list.")
            continue

        normalized_aliases = [
            (alias, normalize_alias(alias))
            for alias in aliases
            if isinstance(alias, str) and normalize_alias(alias)
        ]
        if not normalized_aliases:
            errors.append(f"products[{index}].aliases must contain at least one alias.")
            continue

        for original_alias, normalized_alias in normalized_aliases:
            previous = alias_owner.setdefault(
                normalized_alias,
                (index, original_alias),
            )
            previous_index, previous_alias = previous
            if previous_index != index:
                errors.append(
                    "alias conflict between "
                    f"products[{previous_index}] ({previous_alias!r}) and "
                    f"products[{index}] ({original_alias!r})"
                )

    return errors


def main() -> int:
    args = parse_args()
    load_errors: list[str] = []
    payload = load_seed(args.path, load_errors)
    if payload is None:
        errors = load_errors
    else:
        errors = load_errors + validate_seed(payload)

    if errors:
        print(f"Validation failed: {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validation passed: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())