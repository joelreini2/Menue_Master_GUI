import pytest

from menue_master.domain.modelle import Rezept, Wochenplan, WochenplanEintrag, Zutat, wochentage
from menue_master.services.einkaufsliste_service import EinkaufslisteService
from menue_master.services.validierung import rezept_pruefen, wochenplan_pruefen, zutat_pruefen


def test_zutat_gueltig():
    zutat = Zutat("Reis", 80, "g")
    zutat_pruefen(zutat)
    assert zutat.ist_gueltig() is True


@pytest.mark.parametrize(
    "zutat",
    [Zutat("", 80, "g"), Zutat("Reis", 0, "g"), Zutat("Reis", 80, "")],
)
def test_zutat_ungueltig(zutat):
    with pytest.raises(ValueError):
        zutat_pruefen(zutat)


def test_rezept_pruefen():
    rezept = Rezept("Omelette", zutaten=[Zutat("Ei", 2, "Stück")])
    rezept_pruefen(rezept)
    assert rezept.ist_gueltig() is True


def test_leerer_wochenplan_hat_sieben_tage():
    wochenplan = Wochenplan.leerer_wochenplan("Woche 1")
    assert [eintrag.wochentag for eintrag in wochenplan.eintraege] == wochentage


def test_wochenplan_ohne_titel_ungueltig():
    wochenplan = Wochenplan.leerer_wochenplan("")
    with pytest.raises(ValueError):
        wochenplan_pruefen(wochenplan)


def test_einkaufsliste_fasst_gleiche_zutaten_zusammen():
    rezept_1 = Rezept("Gericht 1", zutaten=[Zutat("Reis", 80, "g"), Zutat("Ei", 1, "Stück")])
    rezept_2 = Rezept("Gericht 2", zutaten=[Zutat("Reis", 120, "g"), Zutat("Ei", 2, "Stück")])
    eintraege = [WochenplanEintrag(tag) for tag in wochentage]
    eintraege[0].rezept = rezept_1
    eintraege[1].rezept = rezept_2
    wochenplan = Wochenplan("Testwoche", eintraege)

    einkaufsliste = EinkaufslisteService().einkaufsliste_erstellen(wochenplan)

    assert einkaufsliste[("reis", "g")] == 200
    assert einkaufsliste[("ei", "stück")] == 3
