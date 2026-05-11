import pytest

from menue_master.data_access import DatenbankZugriff, datenbank_erstellen
from menue_master.data_access.seed import startdaten_anlegen
from menue_master.services.einkaufsliste_service import EinkaufslisteService
from menue_master.services.rezept_service import RezeptService
from menue_master.services.wochenplan_service import WochenplanService
from menue_master.ui.controllers import MenuMasterController


@pytest.fixture
def session_factory(tmp_path):
    datenbank_pfad = tmp_path / "test_menue_master.db"
    _engine, Session = datenbank_erstellen(datenbank_pfad)
    return Session


@pytest.fixture
def seeded_session_factory(session_factory):
    startdaten_anlegen(session_factory)
    return session_factory


@pytest.fixture
def datenbank(seeded_session_factory):
    return DatenbankZugriff(seeded_session_factory)


@pytest.fixture
def controller(datenbank):
    return MenuMasterController(
        rezept_service=RezeptService(datenbank),
        wochenplan_service=WochenplanService(datenbank),
        einkaufsliste_service=EinkaufslisteService(),
    )
