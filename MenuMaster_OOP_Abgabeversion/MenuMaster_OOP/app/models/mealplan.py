"""Domänenklasse für Wochenpläne."""

from dataclasses import dataclass, field
from datetime import datetime

WEEKDAYS = [
    "Montag",
    "Dienstag",
    "Mittwoch",
    "Donnerstag",
    "Freitag",
    "Samstag",
    "Sonntag",
]


@dataclass(slots=True)
class MealPlan:
    id: int | None
    title: str
    assignments: dict[str, int | None] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))

    def validate(self, valid_recipe_ids: set[int]) -> None:
        if not self.title.strip():
            raise ValueError("Der Wochenplan braucht einen Titel.")
        missing_days = [day for day in WEEKDAYS if day not in self.assignments]
        if missing_days:
            raise ValueError("Nicht alle Wochentage sind vorhanden.")
        for recipe_id in self.assignments.values():
            if recipe_id is not None and recipe_id not in valid_recipe_ids:
                raise ValueError("Ungültiges Rezept im Wochenplan.")
