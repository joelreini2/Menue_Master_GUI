"""Startpunkt der MenuMaster-App.

Hier werden Datenbank, Startdaten, Services, Controller und NiceGUI verbunden.
"""

from nicegui import ui

from menue_master.data_access import DatenbankZugriff, datenbank_erstellen
from menue_master.data_access.seed import startdaten_anlegen
from menue_master.services.einkaufsliste_service import EinkaufslisteService
from menue_master.services.rezept_service import RezeptService
from menue_master.services.wochenplan_service import WochenplanService
from menue_master.ui.controllers import MenuMasterController
from menue_master.ui.pages import seiten_erstellen


def starten() -> None:
    engine, Session = datenbank_erstellen()
    startdaten_anlegen(Session)

    datenbank = DatenbankZugriff(Session)
    controller = MenuMasterController(
        rezept_service=RezeptService(datenbank),
        wochenplan_service=WochenplanService(datenbank),
        einkaufsliste_service=EinkaufslisteService(),
    )

    seiten_erstellen(controller)
    ui.run(title="MenuMaster", reload=False)
