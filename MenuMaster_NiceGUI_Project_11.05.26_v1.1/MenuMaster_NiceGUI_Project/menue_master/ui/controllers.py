from menue_master.domain.modelle import Rezept, Wochenplan
from menue_master.services.einkaufsliste_service import EinkaufslisteService
from menue_master.services.rezept_service import RezeptService
from menue_master.services.wochenplan_service import WochenplanService


class MenuMasterController:
    def __init__(
        self,
        rezept_service: RezeptService,
        wochenplan_service: WochenplanService,
        einkaufsliste_service: EinkaufslisteService,
    ) -> None:
        self.rezept_service = rezept_service
        self.wochenplan_service = wochenplan_service
        self.einkaufsliste_service = einkaufsliste_service
        self.aktueller_wochenplan: Wochenplan = self.wochenplan_service.wochenplan_manuell_erstellen("Neue Woche")

    def rezepte_anzeigen(self) -> list[Rezept]:
        return self.rezept_service.rezepte_anzeigen()

    def wochenplan_manuell_erstellen(self, titel: str) -> Wochenplan:
        self.aktueller_wochenplan = self.wochenplan_service.wochenplan_manuell_erstellen(titel)
        return self.aktueller_wochenplan

    def wochenplan_zufaellig_erstellen(self, titel: str) -> Wochenplan:
        rezepte = self.rezepte_anzeigen()
        self.aktueller_wochenplan = self.wochenplan_service.wochenplan_zufaellig_erstellen(titel, rezepte)
        return self.aktueller_wochenplan

    def rezept_zuordnen(self, wochentag: str, rezept: Rezept | None) -> None:
        self.wochenplan_service.rezept_zuordnen(self.aktueller_wochenplan, wochentag, rezept)

    def wochenplan_speichern(self) -> Wochenplan:
        self.aktueller_wochenplan = self.wochenplan_service.wochenplan_speichern(self.aktueller_wochenplan)
        return self.aktueller_wochenplan

    def einkaufsliste_anzeigen(self) -> list[str]:
        return self.einkaufsliste_service.einkaufsliste_als_zeilen(self.aktueller_wochenplan)

    def gespeicherte_wochenplaene_anzeigen(self) -> list[Wochenplan]:
        return self.wochenplan_service.gespeicherte_wochenplaene_anzeigen()
