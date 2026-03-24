# User Stories, Datentypen und Testfälle

## User Story 1 – Rezepte anzeigen
**Als Anwender möchte ich alle Rezepte im Browser sehen.**

**Beschreibung**  
Die Anwendung zeigt alle in der Datenbank vorhandenen Rezepte mit ihren Zutaten an.

**Inputs**
- keine

**Outputs**
- `list[Recipe]`
- Anzeige von Rezeptname und Zutaten im Browser

**Wichtige Datentypen**
- `Recipe`
- `Ingredient`

**Testfälle**
- Es sind Rezepte vorhanden -> alle Rezepte werden angezeigt.
- Es sind keine Rezepte vorhanden -> die Liste bleibt leer oder zeigt keine Karten.

---

## User Story 2 – Wochenplan erstellen
**Als Anwender möchte ich für jeden Wochentag ein Rezept auswählen können.**

**Beschreibung**  
Für jeden Wochentag kann ein Rezept oder kein Rezept gewählt werden. Der Wochenplan wird gespeichert.

**Inputs**
- Titel als `str`
- Zuordnung `dict[str, int | None]`

**Outputs**
- gespeicherter `MealPlan`

**Wichtige Datentypen**
- `MealPlan`
- `dict[str, int | None]`

**Testfälle**
- Gültiger Titel und gültige Rezept-IDs -> Wochenplan wird gespeichert.
- Leerer Titel -> Fehlermeldung.
- Ungültige Rezept-ID -> Fehlermeldung.
- Fehlender Wochentag -> Fehlermeldung.

---

## User Story 3 – Zufälligen Wochenplan erstellen
**Als Anwender möchte ich einen Wochenplan automatisch füllen lassen können.**

**Beschreibung**  
Die Anwendung verteilt vorhandene Rezepte zufällig auf die sieben Wochentage.

**Inputs**
- vorhandene Rezeptliste aus der Datenbank

**Outputs**
- `dict[str, int | None]` mit sieben Wochentagen

**Testfälle**
- Es gibt Rezepte -> für alle Wochentage wird eine Rezept-ID gesetzt.
- Es gibt keine Rezepte -> alle Wochentage erhalten `None`.

---

## User Story 4 – Einkaufsliste berechnen
**Als Anwender möchte ich eine zusammengefasste Einkaufsliste für meinen Wochenplan sehen.**

**Beschreibung**  
Die Zutaten aller Rezepte eines Wochenplans werden nach Name und Einheit zusammengefasst.

**Inputs**
- `meal_plan_id` als `int` oder aktueller Wochenplan

**Outputs**
- `ShoppingList`
- Zeilenform `list[tuple[str, float, str]]`

**Wichtige Datentypen**
- `ShoppingList`
- `tuple[str, str] -> float`

**Testfälle**
- Zwei Rezepte mit derselben Zutat und Einheit -> Menge wird addiert.
- Leerer Wochenplan -> leere Einkaufsliste.
- Kein gespeicherter Wochenplan -> leere Einkaufsliste.

---

## User Story 5 – Vergangene Wochenpläne anzeigen
**Als Anwender möchte ich bereits gespeicherte Wochenpläne nochmals ansehen können.**

**Beschreibung**  
Die Anwendung liest alle gespeicherten Wochenpläne aus der Datenbank und zeigt sie sortiert an.

**Inputs**
- keine

**Outputs**
- `list[MealPlan]`

**Testfälle**
- Es gibt gespeicherte Pläne -> diese werden angezeigt.
- Es gibt noch keine Pläne -> Hinweistext wird angezeigt.

---

## Bereits umgesetzte automatisierte Tests

Die Datei `tests/test_services.py` deckt aktuell diese Fälle ab:

1. Rezeptimport aus Textdatei
2. Speichern und Laden eines Wochenplans
3. Zusammenfassen der Einkaufsliste

---

## Sinnvolle Erweiterungen für weitere Tests

- Validierung von `Ingredient.validate()`
- Validierung von `Recipe.validate()`
- Validierung von `MealPlan.validate()`
- Test für zufällige Wochenplanerstellung ohne Rezepte
- Test für Verlauf mit mehreren gespeicherten Wochenplänen
