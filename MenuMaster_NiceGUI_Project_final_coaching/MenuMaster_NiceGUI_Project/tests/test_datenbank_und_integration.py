from menue_master.data_access.seed import START_REZEPTE, startdaten_anlegen
from menue_master.domain.modelle import Wochenplan


def test_db_004_startdaten_legen_rezepte_mit_zutaten_an(seeded_session_factory, datenbank):
    """DB-Test: Die Seed-Daten werden in der Testdatenbank angelegt."""
    rezepte = datenbank.alle_rezepte_laden()

    assert len(rezepte) == len(START_REZEPTE)
    assert all(rezept.rezept_id is not None for rezept in rezepte)
    assert all(rezept.zutaten for rezept in rezepte)


def test_db_005_startdaten_werden_nicht_doppelt_angelegt(seeded_session_factory, datenbank):
    """DB-Test: Seed-Daten werden bei erneutem Aufruf nicht dupliziert."""
    startdaten_anlegen(seeded_session_factory)

    rezepte = datenbank.alle_rezepte_laden()

    assert len(rezepte) == len(START_REZEPTE)


def test_db_006_wochenplan_speichern_und_wieder_laden(datenbank):
    """DB-Test: Ein Wochenplan wird gespeichert und vollständig wieder geladen."""
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


def test_int_007_controller_laed_rezepte_aus_der_datenbank(controller):
    """Integrationstest: Controller, RezeptService und Datenbank arbeiten zusammen."""
    rezepte = controller.rezepte_anzeigen()

    assert len(rezepte) == len(START_REZEPTE)
    assert all(rezept.zutaten for rezept in rezepte)


def test_int_008_controller_erstellt_zufaelligen_wochenplan(controller):
    """Integrationstest: Controller erstellt über Services einen zufällig befüllten Plan."""
    plan = controller.wochenplan_zufaellig_erstellen("Zufallswoche")

    assert plan.titel == "Zufallswoche"
    assert len(plan.eintraege) == 7
    assert all(eintrag.rezept is not None for eintrag in plan.eintraege)


def test_int_009_controller_speichert_wochenplan_workflow(controller):
    """Integrationstest: Manueller Workflow mit Zuordnung und Speichern funktioniert."""
    rezepte = controller.rezepte_anzeigen()
    plan = controller.wochenplan_manuell_erstellen("Controller-Testwoche")
    for eintrag, rezept in zip(plan.eintraege, rezepte, strict=False):
        controller.rezept_zuordnen(eintrag.wochentag, rezept)

    gespeicherter_plan = controller.wochenplan_speichern()
    gespeicherte_plaene = controller.gespeicherte_wochenplaene_anzeigen()

    assert gespeicherter_plan.wochenplan_id is not None
    assert gespeicherte_plaene[0].titel == "Controller-Testwoche"


def test_int_010_controller_liefert_einkaufsliste_nach_rezeptzuordnung(controller):
    """Integrationstest: Controller liefert nach Rezeptzuordnung eine Einkaufsliste."""
    rezepte = controller.rezepte_anzeigen()
    plan = controller.wochenplan_manuell_erstellen("Einkaufsliste-Testwoche")
    controller.rezept_zuordnen(plan.eintraege[0].wochentag, rezepte[0])
    controller.rezept_zuordnen(plan.eintraege[1].wochentag, rezepte[1])

    einkaufsliste = controller.einkaufsliste_anzeigen()

    assert einkaufsliste
    assert all(isinstance(zeile, str) for zeile in einkaufsliste)
