# MenuMaster – Rezept- und Wochenplaner

MenuMaster erweitert das bestehende CLI-Projekt zu einer **einfachen browserbasierten Anwendung** mit **NiceGUI**, **objektorientierter Struktur** und **SQLite + SQLAlchemy ORM**.

Die Lösung ist bewusst **klein und kursnah** gehalten. Sie orientiert sich am Pizza-Referenzprojekt, ohne unnötig komplex zu werden.

---

## Projektidee

In vielen Haushalten werden Rezepte, Wochenpläne und Einkaufslisten manuell geführt. Dadurch fehlt schnell die Übersicht, welche Gerichte in der Woche geplant sind und welche Zutaten insgesamt benötigt werden.

Die Anwendung unterstützt deshalb drei Kernaufgaben:

- Rezepte anzeigen
- Wochenpläne speichern
- Einkaufslisten aus Wochenplänen berechnen

---

## Szenario

Eine Benutzerin oder ein Benutzer öffnet die Browser-App, sieht die vorhandenen Rezepte, erstellt einen Wochenplan und lässt daraus automatisch eine Einkaufsliste generieren. Bereits gespeicherte Wochenpläne können später erneut angezeigt werden.

---

## User Stories

### 1. Rezepte anzeigen
**Als Anwender möchte ich alle Rezepte im Browser sehen.**  
**Inputs:** keine  
**Outputs:** Liste von Rezepten mit Zutaten

### 2. Wochenplan erstellen
**Als Anwender möchte ich für jeden Wochentag ein Rezept auswählen können.**  
**Inputs:** Titel des Wochenplans, Rezept pro Tag  
**Outputs:** gespeicherter Wochenplan

### 3. Zufälligen Wochenplan erstellen
**Als Anwender möchte ich einen Wochenplan automatisch füllen lassen können.**  
**Inputs:** vorhandene Rezepte  
**Outputs:** Wochenplan mit zufälligen Rezepten

### 4. Einkaufsliste berechnen
**Als Anwender möchte ich eine zusammengefasste Einkaufsliste für meinen Wochenplan sehen.**  
**Inputs:** gespeicherter Wochenplan  
**Outputs:** Zutaten mit Gesamtmengen

### 5. Vergangene Wochenpläne anzeigen
**Als Anwender möchte ich bereits gespeicherte Wochenpläne nochmals ansehen können.**  
**Inputs:** keine  
**Outputs:** Liste früherer Wochenpläne

Eine ausführlichere Fassung mit Datentypen, Inputs, Outputs und Testfällen steht in [`docs/01_user_stories_testcases.md`](docs/01_user_stories_testcases.md).

---

## Use Cases

### Hauptakteur
- Benutzer / Kunde

### Use Cases
- Rezepte anzeigen
- Wochenplan manuell erstellen
- Wochenplan zufällig füllen
- Wochenplan speichern
- Einkaufsliste für den letzten Wochenplan anzeigen
- Vergangene Wochenpläne anzeigen

Das textuelle Use-Case-Modell und ein Mermaid-Diagramm stehen in [`docs/02_use_cases.md`](docs/02_use_cases.md).

---

## Architektur

Die Anwendung ist einfach in drei Schichten aufgeteilt:

- **UI / View:** NiceGUI-Seiten in `app/ui/pages.py`
- **Application Logic / Controller-Service-Schicht:** Fachlogik in `app/services/`
- **Persistence / Model:** SQLite + SQLAlchemy in `app/database/`

Damit bleibt die Oberfläche übersichtlich, während die Fachlogik testbar und von der Anzeige getrennt ist.

### Verwendete Domänenklassen
- `Recipe`
- `Ingredient`
- `MealPlan`
- `ShoppingList`

### Verwendete ORM-Klassen
- `RecipeORM`
- `IngredientORM`
- `MealPlanORM`
- `MealPlanEntryORM`

### Designentscheidungen
- einfache **MVC-nahe Trennung**
- **Domänenklassen** getrennt von **ORM-Klassen**
- **Services** bündeln Fachlogik
- Browser ist nur Oberfläche, die Logik läuft serverseitig in Python

Detaillierte Architektur- und Diagrammdateien:

- [`docs/03_architektur.md`](docs/03_architektur.md)
- [`docs/architecture-diagrams/uml_class_diagram.mmd`](docs/architecture-diagrams/uml_class_diagram.mmd)
- [`docs/architecture-diagrams/er_diagram.mmd`](docs/architecture-diagrams/er_diagram.mmd)
- [`docs/architecture-diagrams/use_case_diagram.mmd`](docs/architecture-diagrams/use_case_diagram.mmd)

---

## Datenbank / ORM

Verwendet wird eine lokale **SQLite-Datenbank**.

### Tabellen
- `recipes`
- `ingredients`
- `meal_plans`
- `meal_plan_entries`

### Beziehungen
- Ein Rezept hat mehrere Zutaten.
- Ein Wochenplan hat mehrere Einträge.
- Ein Wochenplan-Eintrag verweist optional auf ein Rezept.

Mehr Details stehen in [`docs/04_domain_er_modell.md`](docs/04_domain_er_modell.md).

---

## Design Patterns

Die Anwendung verwendet bewusst nur wenige, verständliche Patterns:

- **MVC-nahe Struktur** für Trennung von UI, Logik und Persistenz
- **Service Layer** für die Kernlogik
- **Data Mapper / ORM** durch SQLAlchemy

Mehr dazu in [`docs/05_design_patterns.md`](docs/05_design_patterns.md).

---

## Screens und Navigation

Implementierte Screens:

- Startseite
- Rezepte
- Wochenplan
- Einkaufsliste
- Verlauf

Navigation und Wireframe-Beschreibung stehen in [`docs/06_screens_navigation.md`](docs/06_screens_navigation.md).

---

## Tests

Es gibt eine kleine, aber sinnvolle Testbasis in `tests/test_services.py`.

Getestet werden insbesondere:

- Import von Rezepten
- Speichern von Wochenplänen
- Berechnung der Einkaufsliste

Die Testfall-Spezifikation steht in [`docs/01_user_stories_testcases.md`](docs/01_user_stories_testcases.md).

---

## Erfüllung der Projektanforderungen

### 1. Browser-based App (NiceGUI)
Die Anwendung läuft im Browser und bietet mehrere Seiten für Rezepte, Wochenplanung, Einkaufsliste und Verlauf.

### 2. Data Validation
Es werden einfache Validierungen durchgeführt:
- Rezeptname darf nicht leer sein
- Zutatenmenge muss grösser als 0 sein
- Einheit darf nicht leer sein
- Wochenplan braucht einen Titel
- Wochenplan darf nur gültige Rezept-IDs enthalten
- Alle Wochentage müssen vorhanden sein

### 3. Database Management via ORM
Die Daten werden in SQLite gespeichert. Der Zugriff erfolgt über SQLAlchemy als ORM.

Eine kompakte Zuordnung zur Bewertung steht in [`docs/07_bewertungszuordnung.md`](docs/07_bewertungszuordnung.md).

---

## Projektstruktur

```text
MenuMaster_OOP/
├── main.py
├── requirements.txt
├── data/
│   └── rezepte.txt
├── app/
│   ├── database/
│   ├── data/
│   ├── models/
│   ├── services/
│   └── ui/
├── docs/
│   ├── architecture-diagrams/
│   └── ui-images/
└── tests/
```

---

## Starten

```bash
pip install -r requirements.txt
python main.py
```

Danach startet die App im Browser.

---

## Hinweise für die Abgabe

- Die Lösung ist bewusst **nicht overengineered**.
- Die App eignet sich gut für eine kurze Live-Demo.
- Die Diagramme sind als **Mermaid-Dateien** abgelegt und können bei Bedarf in Markdown-Tools oder GitHub gerendert werden.
- Die Datei [`docs/08_team_aufteilung_template.md`](docs/08_team_aufteilung_template.md) kann vor der Abgabe noch mit euren Namen ergänzt werden.
