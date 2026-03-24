# Use Cases

## Akteur
- **Benutzer**: plant Mahlzeiten und betrachtet Rezepte

## Haupt-Use-Cases

### 1. Rezepte anzeigen
Der Benutzer öffnet die Rezeptseite und sieht alle verfügbaren Rezepte mit Zutaten.

### 2. Wochenplan verwalten
Der Benutzer erstellt einen Wochenplan, wählt Rezepte pro Wochentag aus und speichert den Plan.

### 3. Wochenplan zufällig füllen
Der Benutzer lässt einen Wochenplan automatisch durch die Anwendung befüllen.

### 4. Einkaufsliste anzeigen
Der Benutzer öffnet die Einkaufsliste und sieht die aufsummierten Zutaten des letzten Wochenplans.

### 5. Vergangene Wochenpläne anzeigen
Der Benutzer öffnet den Verlauf und sieht bereits gespeicherte Wochenpläne.

---

## Beziehungen
- **Wochenplan verwalten** beinhaltet das Auswählen von Rezepten.
- **Einkaufsliste anzeigen** basiert auf einem bereits gespeicherten Wochenplan.
- **Wochenplan zufällig füllen** ist eine Variante innerhalb des Wochenplan-Screens.

---

## Mermaid-Diagramm

Die Diagrammquelle liegt in:

- `docs/architecture-diagrams/use_case_diagram.mmd`
