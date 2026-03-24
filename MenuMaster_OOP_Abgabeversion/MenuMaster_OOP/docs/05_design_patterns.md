# Verwendete Design Patterns

## 1. MVC-nahe Struktur

Die Anwendung trennt Benutzeroberfläche, Logik und Persistenz.

- **Model:** Domänenobjekte + ORM-Klassen
- **View:** NiceGUI-Seiten
- **Controller:** Event-Handler und Services

Das ist keine strenge Framework-MVC-Implementierung, aber für den Kurs eine passende und verständliche Umsetzung.

---

## 2. Service Layer

Die Fachlogik ist in Service-Klassen zusammengefasst:

- `RecipeService`
- `MealPlanService`
- `ShoppingService`

Vorteile:

- weniger Logik direkt in der UI
- besser testbar
- klarere Verantwortlichkeiten

---

## 3. Data Mapper / ORM

SQLAlchemy übernimmt das Mapping zwischen Python-Objekten und Datenbanktabellen.

Vorteile:

- keine direkten SQL-Strings in der Anwendungslogik
- Objekte statt Tabellenlogik im UI-Code
- saubere Trennung der Persistenzschicht

---

## Nicht bewusst verwendet

Folgende komplexere Patterns wurden absichtlich nicht eingebaut:

- Strategy
- Factory
- Observer
- Dependency Injection Framework

Grund: Für dieses Projekt wären sie unnötig und würden den studentischen Rahmen sprengen.
