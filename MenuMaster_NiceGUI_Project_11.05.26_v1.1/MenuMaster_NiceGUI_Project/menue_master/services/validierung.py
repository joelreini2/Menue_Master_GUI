from menue_master.domain.modelle import Rezept, Wochenplan, Zutat, wochentage


def zutat_pruefen(zutat: Zutat) -> None:
    if zutat.name.strip() == "":
        raise ValueError("Der Zutatenname darf nicht leer sein.")
    if zutat.menge <= 0:
        raise ValueError("Die Menge muss grösser als 0 sein.")
    if zutat.einheit.strip() == "":
        raise ValueError("Die Einheit darf nicht leer sein.")


def rezept_pruefen(rezept: Rezept) -> None:
    if rezept.name.strip() == "":
        raise ValueError("Der Rezeptname darf nicht leer sein.")
    for zutat in rezept.zutaten:
        zutat_pruefen(zutat)


def wochenplan_pruefen(wochenplan: Wochenplan) -> None:
    if wochenplan.titel.strip() == "":
        raise ValueError("Der Wochenplan-Titel darf nicht leer sein.")
    if len(wochenplan.eintraege) != 7:
        raise ValueError("Ein Wochenplan muss genau sieben Einträge enthalten.")
    vorhandene_tage = [eintrag.wochentag for eintrag in wochenplan.eintraege]
    if vorhandene_tage != wochentage:
        raise ValueError("Der Wochenplan muss Montag bis Sonntag in der richtigen Reihenfolge enthalten.")
