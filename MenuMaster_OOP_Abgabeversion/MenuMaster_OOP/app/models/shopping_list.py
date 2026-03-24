"""Domänenklasse für Einkaufslisten."""

from dataclasses import dataclass, field


@dataclass(slots=True)
class ShoppingList:
    items: dict[tuple[str, str], float] = field(default_factory=dict)

    def add_item(self, name: str, unit: str, amount: float) -> None:
        key = (name, unit)
        self.items[key] = self.items.get(key, 0) + amount

    def as_rows(self) -> list[tuple[str, float, str]]:
        return sorted((name, amount, unit) for (name, unit), amount in self.items.items())
