"""Service für die Einkaufsliste.

Die Einkaufsliste wird nicht separat gespeichert. Sie wird aus Rezepten und dem
Wochenplan berechnet, damit keine doppelten Daten in der Datenbank entstehen.
"""

from menue_master.domain.modelle import Wochenplan


class EinkaufslisteService:
    """Berechnet Einkaufslisten aus einem Wochenplan."""

    def einkaufsliste_erstellen(self, wochenplan: Wochenplan) -> dict[tuple[str, str], float]:
        """Fasst gleiche Zutaten nach Name und Einheit zusammen."""
        einkaufsliste: dict[tuple[str, str], float] = {}

        for eintrag in wochenplan.eintraege:
            if eintrag.rezept is None:
                continue

            for zutat in eintrag.rezept.zutaten:
                schluessel = zutat.schluessel()
                if schluessel in einkaufsliste:
                    einkaufsliste[schluessel] += zutat.menge
                else:
                    einkaufsliste[schluessel] = zutat.menge

        return einkaufsliste

    def einkaufsliste_als_zeilen(self, wochenplan: Wochenplan) -> list[str]:
        """Gibt die Einkaufsliste als sortierte Textzeilen für die UI zurück."""
        einkaufsliste = self.einkaufsliste_erstellen(wochenplan)
        zeilen: list[str] = []
        for (name, einheit), menge in sorted(einkaufsliste.items()):
            zeilen.append(f"{menge:g} {einheit} {name}")
        return zeilen
