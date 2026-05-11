from menue_master.data_access.seed import START_REZEPTE, startdaten_anlegen
from menue_master.domain.modelle import Wochenplan


def test_startdaten_legen_rezepte_mit_zutaten_an(seeded_session_factory, datenbank):
    rezepte = datenbank.alle_rezepte_laden()

    assert len(rezepte) == len(START_REZEPTE)
    assert all(rezept.rezept_id is not None for rezept in rezepte)
    assert all(rezept.zutaten for rezept in rezepte)


def test_startdaten_werden_nicht_doppelt_angelegt(seeded_session_factory, datenbank):
    startdaten_anlegen(seeded_session_factory)

    rezepte = datenbank.alle_rezepte_laden()

    assert len(rezepte) == len(START_REZEPTE)


def test_wochenplan_speichern_und_wieder_laden(datenbank):
    rezepte = datenbank.alle_rezepte_laden()
    plan = Wochenplan.leerer_wochenplan("Testwoche")
    for eintrag, rezept in zip(plan.eintraege, rezepte, strict=False):
        eintrag.rezept = rezept

    gespeicherter_plan = datenbank.wochenplan_speichern(plan)
    geladene_plaene = datenbank.alle_wochenplaene_laden()

    assert gespeicherter_plan.wochenplan_id is not None
    assert len(geladene_plaene) == 1
    assert geladene_plaene[0].titel == "Testwoche"
    assert len(geladene_plaene[0].eintraege) == 7
    assert geladene_plaene[0].eintraege[0].wochentag == "Montag"
    assert geladene_plaene[0].eintraege[0].rezept is not None


def test_controller_erstellt_speichert_und_liefert_einkaufsliste(controller):
    rezepte = controller.rezepte_anzeigen()
    plan = controller.wochenplan_manuell_erstellen("Controller-Testwoche")
    for eintrag, rezept in zip(plan.eintraege, rezepte, strict=False):
        controller.rezept_zuordnen(eintrag.wochentag, rezept)

    gespeicherter_plan = controller.wochenplan_speichern()
    einkaufsliste = controller.einkaufsliste_anzeigen()
    gespeicherte_plaene = controller.gespeicherte_wochenplaene_anzeigen()

    assert gespeicherter_plan.wochenplan_id is not None
    assert einkaufsliste
    assert gespeicherte_plaene[0].titel == "Controller-Testwoche"
