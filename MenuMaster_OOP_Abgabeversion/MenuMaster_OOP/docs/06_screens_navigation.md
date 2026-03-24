# Screens und Navigation

## Implementierte Screens

### 1. Startseite (`/`)
Funktion als einfacher Einstiegspunkt mit Navigation zu allen Hauptbereichen.

### 2. Rezeptseite (`/rezepte`)
Zeigt alle importierten Rezepte mit Zutaten.

### 3. Wochenplanseite (`/wochenplan`)
Erlaubt:
- Titel eingeben
- pro Wochentag ein Rezept wählen
- Wochenplan zufällig füllen
- Wochenplan speichern

### 4. Einkaufsliste (`/einkaufsliste`)
Zeigt die berechnete Einkaufsliste des zuletzt gespeicherten Wochenplans.

### 5. Verlauf (`/verlauf`)
Zeigt alle gespeicherten Wochenpläne mit Datum und gewählten Rezepten.

---

## Navigation

Die Navigation ist absichtlich flach und einfach:

- Startseite -> Rezepte
- Startseite -> Wochenplan
- Startseite -> Einkaufsliste
- Startseite -> Verlauf
- jede Unterseite -> Zurück zur Startseite

---

## Einfacher Wireframe (textuell)

```text
[Startseite]
  |-- Rezepte
  |-- Wochenplan
  |-- Einkaufsliste
  `-- Verlauf
```

```text
[Wochenplan]
  Titel: [____________]
  Montag:      [Select]
  Dienstag:    [Select]
  Mittwoch:    [Select]
  Donnerstag:  [Select]
  Freitag:     [Select]
  Samstag:     [Select]
  Sonntag:     [Select]

  [Zufällig füllen] [Wochenplan speichern]
```

---

## Warum nur wenige Screens?

Im Projekt steht nicht die Menge an UI im Vordergrund, sondern die saubere Umsetzung von:

- OOP
- ORM
- Validierung
- browserbasierter Anwendung

Daher wurde bewusst eine kleine, gut demonstrierbare Navigation gewählt.
