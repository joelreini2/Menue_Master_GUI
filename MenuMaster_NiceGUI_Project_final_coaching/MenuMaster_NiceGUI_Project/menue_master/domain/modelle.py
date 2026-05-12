"""Einfache Domain-Klassen für MenuMaster.

Diese Klassen enthalten bewusst nur gut verständliche Attribute und Methoden.
Sie sind normale Python-Klassen und unabhängig von NiceGUI und der Datenbank.
"""

from dataclasses import dataclass, field

wochentage = [
    "Montag",
    "Dienstag",
    "Mittwoch",
    "Donnerstag",
    "Freitag",
    "Samstag",
    "Sonntag",
]


@dataclass
class Zutat:
    name: str
    menge: float
    einheit: str

    def ist_gueltig(self) -> bool:
        return self.name.strip() != "" and self.menge > 0 and self.einheit.strip() != ""

    def schluessel(self) -> tuple[str, str]:
        return (self.name.strip().lower(), self.einheit.strip().lower())


@dataclass
class Rezept:
    name: str
    beschreibung: str = ""
    zutaten: list[Zutat] = field(default_factory=list)
    rezept_id: int | None = None

    def ist_gueltig(self) -> bool:
        if self.name.strip() == "":
            return False
        return all(zutat.ist_gueltig() for zutat in self.zutaten)

    def zutat_hinzufuegen(self, zutat: Zutat) -> None:
        if not zutat.ist_gueltig():
            raise ValueError("Zutat ist ungültig.")
        self.zutaten.append(zutat)


@dataclass
class WochenplanEintrag:
    wochentag: str
    rezept: Rezept | None = None


@dataclass
class Wochenplan:
    titel: str
    eintraege: list[WochenplanEintrag] = field(default_factory=list)
    wochenplan_id: int | None = None

    def ist_gueltig(self) -> bool:
        if self.titel.strip() == "":
            return False
        tage = [eintrag.wochentag for eintrag in self.eintraege]
        return tage == wochentage

    @classmethod
    def leerer_wochenplan(cls, titel: str) -> "Wochenplan":
        return cls(titel=titel, eintraege=[WochenplanEintrag(tag) for tag in wochentage])
