# Architektur

## Überblick

MenuMaster ist als einfache browserbasierte Python-Anwendung aufgebaut.

### Schichten

1. **Präsentationsschicht / View**
   - NiceGUI-Seiten in `app/ui/pages.py`
   - Der Browser ist Thin Client und rendert nur die Oberfläche.

2. **Anwendungslogik / Service-Schicht**
   - `RecipeService`
   - `MealPlanService`
   - `ShoppingService`
   - Hier liegt die eigentliche Fachlogik.

3. **Persistenzschicht**
   - SQLite-Datenbank
   - SQLAlchemy ORM-Modelle in `app/database/models.py`

---

## Warum diese Architektur?

Die Struktur ist bewusst einfach gehalten, damit sie zum Unterricht passt:

- UI-Code bleibt übersichtlich.
- Logik kann getrennt getestet werden.
- Datenhaltung ist über ORM sauber von der UI getrennt.
- Das Projekt bleibt klein genug für eine studentische Abgabe.

---

## Verantwortung der wichtigsten Module

### `app/ui/pages.py`
Definiert die Seiten und Navigation. Event-Handler rufen Services auf.

### `app/services/recipe_service.py`
Lädt Rezepte aus der Datenbank und importiert die Startdaten aus der Textdatei.

### `app/services/mealplan_service.py`
Erstellt, validiert und speichert Wochenpläne.

### `app/services/shopping_service.py`
Erzeugt aus einem Wochenplan eine zusammengefasste Einkaufsliste.

### `app/models/`
Enthält die Domänenklassen mit Validierungslogik.

### `app/database/`
Enthält das Datenbank-Setup und die ORM-Mappings.

---

## Steuerung im MVC-Sinn

Die App ist nicht als strenges Enterprise-MVC umgesetzt, aber MVC-nah:

- **Model:** Domänenklassen und ORM-Klassen
- **View:** NiceGUI-Seiten
- **Controller:** Event-Handler in den Seiten zusammen mit den Services

Diese Lösung ist für den Kurs gut geeignet, weil sie verständlich bleibt und dennoch die geforderte Trennung zeigt.
