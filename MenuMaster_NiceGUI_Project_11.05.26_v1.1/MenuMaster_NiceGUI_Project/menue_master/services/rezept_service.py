from menue_master.data_access.datenbank_zugriff import DatenbankZugriff
from menue_master.domain.modelle import Rezept
from menue_master.services.validierung import rezept_pruefen


class RezeptService:
    def __init__(self, datenbank: DatenbankZugriff) -> None:
        self.datenbank = datenbank

    def rezepte_anzeigen(self) -> list[Rezept]:
        return self.datenbank.alle_rezepte_laden()

    def rezept_speichern(self, rezept: Rezept) -> Rezept:
        rezept_pruefen(rezept)
        return self.datenbank.rezept_speichern(rezept)
