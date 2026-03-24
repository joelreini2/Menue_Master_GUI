"""Domänenklassen für Rezepte."""

from dataclasses import dataclass, field


@dataclass(slots=True)
class Ingredient:
    name: str
    amount: float
    unit: str

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("Zutatname darf nicht leer sein.")
        if self.amount <= 0:
            raise ValueError("Menge muss grösser als 0 sein.")
        if not self.unit.strip():
            raise ValueError("Einheit darf nicht leer sein.")


@dataclass(slots=True)
class Recipe:
    id: int | None
    name: str
    ingredients: list[Ingredient] = field(default_factory=list)

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("Rezeptname darf nicht leer sein.")
        if not self.ingredients:
            raise ValueError("Ein Rezept braucht mindestens eine Zutat.")
        for ingredient in self.ingredients:
            ingredient.validate()
