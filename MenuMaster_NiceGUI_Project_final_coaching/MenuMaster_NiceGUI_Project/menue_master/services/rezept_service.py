"""Service für Rezept-Aktionen.

Der Service hält die Rezeptlogik von UI und Datenbanktechnik getrennt.
"""

from menue_master.data_access.datenbank_zugriff import DatenbankZugriff
from menue_master.domain.modelle import Rezept
from menue_master.services.validierung import rezept_pruefen


class RezeptService:
    """Bietet Rezeptfunktionen für Controller und Tests an."""

    def __init__(self, datenbank: DatenbankZugriff) -> None:
        self.datenbank = datenbank

    def rezepte_anzeigen(self) -> list[Rezept]:
        """Lädt alle Rezepte über den Datenbankzugriff."""
        return self.datenbank.alle_rezepte_laden()

    def rezept_speichern(self, rezept: Rezept) -> Rezept:
        """Validiert und speichert ein Rezept."""
        rezept_pruefen(rezept)
        return self.datenbank.rezept_speichern(rezept)
