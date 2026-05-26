from __future__ import annotations

import re
from dataclasses import dataclass

from app.services.normalization import cleanup_product_text


ITEM_SPLIT_RE = re.compile(r"[,\n]+")
WEIGHT_RE = re.compile(r"(?P<weight>\d+(?:[.,]\d+)?)")


@dataclass
class ParsedFoodItem:
    raw_item_text: str
    product_text: str
    weight_g: float


def parse_food_message(message_text: str) -> list[ParsedFoodItem]:
    items: list[ParsedFoodItem] = []
    for raw_part in ITEM_SPLIT_RE.split(message_text):
        raw_item = raw_part.strip()
        if not raw_item:
            continue

        match = WEIGHT_RE.search(raw_item)
        if not match:
            items.append(ParsedFoodItem(raw_item_text=raw_item, product_text="", weight_g=0))
            continue

        weight_text = match.group("weight").replace(",", ".")
        weight_g = float(weight_text)
        product_text = raw_item[: match.start()] + " " + raw_item[match.end() :]
        product_text = cleanup_product_text(product_text)
        items.append(
            ParsedFoodItem(
                raw_item_text=raw_item,
                product_text=product_text,
                weight_g=weight_g,
            )
        )
    return items
