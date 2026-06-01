from __future__ import annotations

import re


GRAM_TOKENS = {
    "г",
    "гр",
    "грамм",
    "грамма",
    "граммов",
    "gram",
    "grams",
    "g",
    "gr",
    "грам",
    "грами",
    "грамів",
}


def normalize_product_name(value: str) -> str:
    text = value.lower().replace("ё", "е")
    text = re.sub(r"[()\"']", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def cleanup_product_text(value: str) -> str:
    text = normalize_product_name(value)
    parts = [part for part in text.split(" ") if part not in GRAM_TOKENS]
    return " ".join(parts).strip()
