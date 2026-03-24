# Bewertungszuordnung / Erfüllung der Modulanforderungen

## 1. Browserbasierte Anwendung
**Erfüllt durch:**
- NiceGUI als UI-Framework
- Navigation über mehrere Browser-Seiten
- serverseitige Instanziierung der UI-Komponenten in Python

**Sichtbar im Code:**
- `main.py`
- `app/ui/pages.py`

---

## 2. Objektorientierung
**Erfüllt durch:**
- Domänenklassen: `Recipe`, `Ingredient`, `MealPlan`, `ShoppingList`
- Service-Klassen für Fachlogik
- ORM-Klassen für Persistenzmodell

**Sichtbar im Code:**
- `app/models/`
- `app/services/`
- `app/database/models.py`

---

## 3. Validierung
**Erfüllt durch:**
- Validierung von Zutaten, Rezepten und Wochenplänen
- Fehlermeldungen bei ungültigen Eingaben

**Sichtbar im Code:**
- `app/models/recipe.py`
- `app/models/mealplan.py`
- `app/ui/pages.py`

---

## 4. ORM und Datenbank
**Erfüllt durch:**
- SQLite als Datenbank
- SQLAlchemy als ORM
- Speicherung von Rezepten, Zutaten und Wochenplänen

**Sichtbar im Code:**
- `app/database/db.py`
- `app/database/models.py`

---

## 5. Tests
**Erfüllt durch:**
- automatisierte Tests für zentrale Service-Funktionen

**Sichtbar im Code:**
- `tests/test_services.py`

---

## 6. Projektdokumentation
**Erfüllt durch:**
- README
- User Stories
- Use Cases
- Architektur-Beschreibung
- Klassendiagramm / ER-Modell als Mermaid-Dateien
- Bewertungszuordnung

**Sichtbar im Repository:**
- `README.md`
- `docs/`
