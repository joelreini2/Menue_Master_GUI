# Domain Model und ER-Modell

## Domänenobjekte

### Ingredient
Repräsentiert eine einzelne Zutat mit Name, Menge und Einheit.

### Recipe
Repräsentiert ein Rezept mit Name und einer Liste von Zutaten.

### MealPlan
Repräsentiert einen Wochenplan mit Titel, Erstellungszeitpunkt und Rezeptzuordnung pro Wochentag.

### ShoppingList
Repräsentiert eine zusammengefasste Einkaufsliste. Intern werden Zutaten nach `(Name, Einheit)` gruppiert.

---

## ORM-Entities

### RecipeORM
Tabelle `recipes` – speichert Rezepte.

### IngredientORM
Tabelle `ingredients` – speichert Zutaten zu einem Rezept.

### MealPlanORM
Tabelle `meal_plans` – speichert Wochenpläne.

### MealPlanEntryORM
Tabelle `meal_plan_entries` – speichert die Zuordnung von Wochentag zu Rezept.

---

## Beziehungen

- Ein `RecipeORM` hat **0..n** Zutaten.
- Ein `IngredientORM` gehört genau zu **1** Rezept.
- Ein `MealPlanORM` hat **7** Einträge aus Anwendungssicht.
- Ein `MealPlanEntryORM` gehört genau zu **1** Wochenplan.
- Ein `MealPlanEntryORM` referenziert optional **1** Rezept.

---

## Begründung des Modells

Das Datenmodell ist absichtlich einfach:

- Ein Rezept speichert direkt seine Zutaten.
- Wochenpläne werden separat gespeichert, damit frühere Planungen wieder angezeigt werden können.
- Einkaufsliste wird nicht dauerhaft gespeichert, sondern bei Bedarf aus dem Wochenplan berechnet.

Diese Entscheidung reduziert Komplexität und reicht für den Projektumfang aus.
