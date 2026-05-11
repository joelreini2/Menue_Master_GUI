import random

from menue_master.data_access.datenbank_zugriff import DatenbankZugriff
from menue_master.domain.modelle import Rezept, Wochenplan, wochentage
from menue_master.services.validierung import wochenplan_pruefen


class WochenplanService:
    def __init__(self, datenbank: DatenbankZugriff) -> None:
        self.datenbank = datenbank

    def wochenplan_manuell_erstellen(self, titel: str) -> Wochenplan:
        return Wochenplan.leerer_wochenplan(titel)

    def wochenplan_zufaellig_erstellen(self, titel: str, rezepte: list[Rezept]) -> Wochenplan:
        if len(rezepte) == 0:
            raise ValueError("Es gibt keine Rezepte für einen zufälligen Wochenplan.")
        wochenplan = Wochenplan.leerer_wochenplan(titel)
        for eintrag in wochenplan.eintraege:
            eintrag.rezept = random.choice(rezepte)
        return wochenplan

    def rezept_zuordnen(self, wochenplan: Wochenplan, wochentag: str, rezept: Rezept | None) -> None:
        if wochentag not in wochentage:
            raise ValueError("Ungültiger Wochentag.")
        for eintrag in wochenplan.eintraege:
            if eintrag.wochentag == wochentag:
                eintrag.rezept = rezept
                return
        raise ValueError("Wochentag wurde im Wochenplan nicht gefunden.")

    def wochenplan_speichern(self, wochenplan: Wochenplan) -> Wochenplan:
        wochenplan_pruefen(wochenplan)
        return self.datenbank.wochenplan_speichern(wochenplan)

    def gespeicherte_wochenplaene_anzeigen(self) -> list[Wochenplan]:
        return self.datenbank.alle_wochenplaene_laden()
