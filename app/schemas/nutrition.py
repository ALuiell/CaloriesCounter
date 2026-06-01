from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RecognizedItem:
    product_id: int
    product_source: str
    raw_item_text: str
    product_text: str
    display_name: str
    weight_g: float
    calories: float
    protein_g: float
    fat_g: float
    carbs_g: float


@dataclass
class CalculationResult:
    recognized_items: list[RecognizedItem] = field(default_factory=list)
    unrecognized_items: list[str] = field(default_factory=list)
    assistant_enabled: bool = False

    @property
    def has_any_items(self) -> bool:
        return bool(self.recognized_items or self.unrecognized_items)

    @property
    def total_calories(self) -> float:
        return sum(item.calories for item in self.recognized_items)

    @property
    def total_protein(self) -> float:
        return sum(item.protein_g for item in self.recognized_items)

    @property
    def total_fat(self) -> float:
        return sum(item.fat_g for item in self.recognized_items)

    @property
    def total_carbs(self) -> float:
        return sum(item.carbs_g for item in self.recognized_items)
