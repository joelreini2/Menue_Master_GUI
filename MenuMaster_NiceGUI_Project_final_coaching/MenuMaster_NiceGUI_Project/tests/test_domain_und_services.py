import pytest

from menue_master.domain.modelle import Rezept, Wochenplan, WochenplanEintrag, Zutat, wochentage
from menue_master.services.einkaufsliste_service import EinkaufslisteService
from menue_master.services.validierung import zutat_pruefen
from menue_master.services.wochenplan_service import WochenplanService


def test_unit_001_zutat_validierung_prueft_gueltige_und_ungueltige_zutaten():
    """Unit-Test: Zutaten werden ohne Datenbank validiert."""
    gueltige_zutat = Zutat("Reis", 80, "g")
    zutat_pruefen(gueltige_zutat)
    assert gueltige_zutat.ist_gueltig() is True

    with pytest.raises(ValueError):
        zutat_pruefen(Zutat("", 80, "g"))


def test_unit_002_wochenplan_service_erstellt_leeren_wochenplan_mit_sieben_tagen():
    """Unit-Test: Der WochenplanService erstellt die Wochentage ohne Datenbankzugriff."""
    service = WochenplanService(datenbank=None)

    wochenplan = service.wochenplan_manuell_erstellen("Woche 1")

    assert wochenplan.titel == "Woche 1"
    assert [eintrag.wochentag for eintrag in wochenplan.eintraege] == wochentage


def test_unit_003_einkaufsliste_service_fasst_gleiche_zutaten_zusammen():
    """Unit-Test: Gleiche Zutaten mit gleicher Einheit werden addiert."""
    rezept_1 = Rezept("Gericht 1", zutaten=[Zutat("Reis", 80, "g"), Zutat("Ei", 1, "Stück")])
    rezept_2 = Rezept("Gericht 2", zutaten=[Zutat("Reis", 120, "g"), Zutat("Ei", 2, "Stück")])
    eintraege = [WochenplanEintrag(tag) for tag in wochentage]
    eintraege[0].rezept = rezept_1
    eintraege[1].rezept = rezept_2
    wochenplan = Wochenplan("Testwoche", eintraege)

    einkaufsliste = EinkaufslisteService().einkaufsliste_erstellen(wochenplan)

    assert einkaufsliste[("reis", "g")] == 200
    assert einkaufsliste[("ei", "stück")] == 3
