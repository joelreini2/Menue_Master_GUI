"""Service für Wochenplan-Aktionen.

Hier liegt die Logik zum Erstellen, Befüllen, Zuordnen und Speichern von Wochenplänen.
"""

import random

from menue_master.data_access.datenbank_zugriff import DatenbankZugriff
from menue_master.domain.modelle import Rezept, Wochenplan, wochentage
from menue_master.services.validierung import wochenplan_pruefen


class WochenplanService:
    """Bündelt alle fachlichen Aktionen rund um Wochenpläne."""

    def __init__(self, datenbank: DatenbankZugriff) -> None:
        self.datenbank = datenbank

    def wochenplan_manuell_erstellen(self, titel: str) -> Wochenplan:
        """Erstellt einen leeren Wochenplan mit Montag bis Sonntag."""
        return Wochenplan.leerer_wochenplan(titel)

    def wochenplan_zufaellig_erstellen(self, titel: str, rezepte: list[Rezept]) -> Wochenplan:
        """Füllt jeden Wochentag zufällig mit einem vorhandenen Rezept."""
        if len(rezepte) == 0:
            raise ValueError("Es gibt keine Rezepte für einen zufälligen Wochenplan.")
        wochenplan = Wochenplan.leerer_wochenplan(titel)
        for eintrag in wochenplan.eintraege:
            eintrag.rezept = random.choice(rezepte)
        return wochenplan

    def rezept_zuordnen(self, wochenplan: Wochenplan, wochentag: str, rezept: Rezept | None) -> None:
        """Ordnet einem Wochentag ein Rezept zu oder setzt ihn leer."""
        if wochentag not in wochentage:
            raise ValueError("Ungültiger Wochentag.")
        for eintrag in wochenplan.eintraege:
            if eintrag.wochentag == wochentag:
                eintrag.rezept = rezept
                return
        raise ValueError("Wochentag wurde im Wochenplan nicht gefunden.")

    def wochenplan_speichern(self, wochenplan: Wochenplan) -> Wochenplan:
        """Validiert und speichert einen Wochenplan in der Datenbank."""
        wochenplan_pruefen(wochenplan)
        return self.datenbank.wochenplan_speichern(wochenplan)

    def gespeicherte_wochenplaene_anzeigen(self) -> list[Wochenplan]:
        return self.datenbank.alle_wochenplaene_laden()
