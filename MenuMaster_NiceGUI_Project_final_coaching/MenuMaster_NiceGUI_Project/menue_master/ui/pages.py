"""NiceGUI-Seiten für MenuMaster.

Diese Datei erstellt Tabs, Buttons, Eingabefelder und Ansichten für Rezepte, Wochenplan, Einkaufsliste und Historie.
"""

from collections.abc import Callable

from nicegui import ui

from menue_master.ui.controllers import MenuMasterController


RefreshCallback = Callable[[], None]


def seiten_erstellen(controller: MenuMasterController) -> None:
    ui.page_title("MenuMaster")
    refresh_callbacks: list[RefreshCallback] = []

    with ui.header().classes("bg-green-700 text-white"):
        ui.label("🍽️ MenuMaster – Meal Planner").classes("text-2xl font-bold")

    with ui.tabs().classes("w-full") as tabs:
        tab_rezepte = ui.tab("Rezepte")
        tab_wochenplan = ui.tab("Wochenplan")
        tab_einkaufsliste = ui.tab("Einkaufsliste")
        tab_historie = ui.tab("Gespeicherte Pläne")

    with ui.tab_panels(tabs, value=tab_rezepte).classes("w-full p-4"):
        with ui.tab_panel(tab_rezepte):
            rezeptseite(controller)
        with ui.tab_panel(tab_wochenplan):
            wochenplanseite(controller, refresh_callbacks)
        with ui.tab_panel(tab_einkaufsliste):
            einkaufslistenseite(controller, refresh_callbacks)
        with ui.tab_panel(tab_historie):
            historienseite(controller, refresh_callbacks)


def rezeptseite(controller: MenuMasterController) -> None:
    ui.label("Rezepte anzeigen").classes("text-2xl font-bold mb-4")
    with ui.grid(columns="1 sm:2 lg:3").classes("gap-4 w-full"):
        for rezept in controller.rezepte_anzeigen():
            with ui.card().classes("w-full shadow-md rounded-2xl"):
                ui.label(rezept.name).classes("text-lg font-bold")
                ui.label(rezept.beschreibung).classes("text-gray-600")
                ui.separator()
                for zutat in rezept.zutaten:
                    ui.label(f"• {zutat.menge:g} {zutat.einheit} {zutat.name}")


def wochenplanseite(controller: MenuMasterController, refresh_callbacks: list[RefreshCallback]) -> None:
    ui.label("Wochenplan erstellen").classes("text-2xl font-bold mb-4")
    titel_input = ui.input("Titel", value=controller.aktueller_wochenplan.titel).classes("w-full max-w-md")
    meldung = ui.label("").classes("text-green-700")
    rezepte = controller.rezepte_anzeigen()
    rezept_namen = ["(kein Rezept)"] + [r.name for r in rezepte]

    def alle_abhaengigen_ansichten_aktualisieren() -> None:
        for callback in refresh_callbacks:
            callback()

    @ui.refreshable
    def wochenplan_auswahl_anzeigen() -> None:
        with ui.column().classes("gap-3 w-full max-w-2xl"):
            for eintrag in controller.aktueller_wochenplan.eintraege:
                startwert = eintrag.rezept.name if eintrag.rezept else "(kein Rezept)"

                def auswahl_geaendert(e, tag=eintrag.wochentag):
                    name = e.value
                    rezept = next((r for r in rezepte if r.name == name), None)
                    controller.rezept_zuordnen(tag, rezept)
                    alle_abhaengigen_ansichten_aktualisieren()

                with ui.row().classes("items-center gap-4 w-full"):
                    ui.label(eintrag.wochentag).classes("w-28 font-bold")
                    ui.select(rezept_namen, value=startwert, on_change=auswahl_geaendert).classes("w-80")

    def zufaellig() -> None:
        try:
            controller.wochenplan_zufaellig_erstellen(titel_input.value)
            titel_input.value = controller.aktueller_wochenplan.titel
            wochenplan_auswahl_anzeigen.refresh()
            alle_abhaengigen_ansichten_aktualisieren()
            meldung.text = "Zufälliger Wochenplan wurde erstellt."
            ui.notify(meldung.text, type="positive")
        except ValueError as fehler:
            ui.notify(str(fehler), type="negative")

    def speichern() -> None:
        try:
            controller.aktueller_wochenplan.titel = titel_input.value
            controller.wochenplan_speichern()
            wochenplan_auswahl_anzeigen.refresh()
            alle_abhaengigen_ansichten_aktualisieren()
            meldung.text = "Wochenplan wurde gespeichert."
            ui.notify(meldung.text, type="positive")
        except ValueError as fehler:
            ui.notify(str(fehler), type="negative")

    with ui.row().classes("gap-2 my-4"):
        ui.button("Zufällig befüllen", on_click=zufaellig).classes("bg-green-600 text-white")
        ui.button("Speichern", on_click=speichern).classes("bg-blue-600 text-white")

    wochenplan_auswahl_anzeigen()


def einkaufslistenseite(controller: MenuMasterController, refresh_callbacks: list[RefreshCallback]) -> None:
    ui.label("Einkaufsliste generieren").classes("text-2xl font-bold mb-4")

    @ui.refreshable
    def einkaufsliste_anzeigen() -> None:
        with ui.card().classes("w-full max-w-xl shadow-md rounded-2xl"):
            zeilen = controller.einkaufsliste_anzeigen()
            if not zeilen:
                ui.label("Noch keine Zutaten vorhanden. Bitte zuerst einen Wochenplan erstellen.")
            for zeile in zeilen:
                ui.label("• " + zeile)

    ui.button("Aktualisieren", on_click=einkaufsliste_anzeigen.refresh).classes("mb-4")
    refresh_callbacks.append(einkaufsliste_anzeigen.refresh)
    einkaufsliste_anzeigen()


def historienseite(controller: MenuMasterController, refresh_callbacks: list[RefreshCallback]) -> None:
    ui.label("Gespeicherte Wochenpläne anzeigen").classes("text-2xl font-bold mb-4")

    @ui.refreshable
    def historie_anzeigen() -> None:
        plaene = controller.gespeicherte_wochenplaene_anzeigen()
        if not plaene:
            ui.label("Es sind noch keine Wochenpläne gespeichert.")
            return
        with ui.column().classes("gap-4 w-full"):
            for plan in plaene:
                with ui.card().classes("w-full max-w-2xl shadow-md rounded-2xl"):
                    ui.label(plan.titel).classes("text-lg font-bold")
                    for eintrag in plan.eintraege:
                        rezept_name = eintrag.rezept.name if eintrag.rezept else "(kein Rezept)"
                        ui.label(f"{eintrag.wochentag}: {rezept_name}")

    ui.button("Aktualisieren", on_click=historie_anzeigen.refresh).classes("mb-4")
    refresh_callbacks.append(historie_anzeigen.refresh)
    historie_anzeigen()
