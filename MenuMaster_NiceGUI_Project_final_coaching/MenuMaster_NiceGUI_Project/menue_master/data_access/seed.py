"""Startdaten für MenuMaster.

Die Beispielrezepte werden nur angelegt, wenn die Datenbank noch leer ist.
"""

from sqlalchemy import select

from menue_master.data_access.datenbank_zugriff import DatenbankZugriff
from menue_master.data_access.orm_modelle import RezeptORM
from menue_master.domain.modelle import Rezept, Zutat


START_REZEPTE = [
    Rezept("Spaghetti Bolognese", "Ein einfaches Pasta-Gericht", [Zutat("Spaghetti", 100, "g"), Zutat("Hackfleisch", 100, "g"), Zutat("Tomatensauce", 100, "ml"), Zutat("Zwiebel", 0.5, "Stück")]),
    Rezept("Gemüsepfanne", "Schnelles Gemüsegericht", [Zutat("Paprika", 0.5, "Stück"), Zutat("Zucchini", 0.5, "Stück"), Zutat("Karotte", 1, "Stück"), Zutat("Reis", 80, "g")]),
    Rezept("Omelette", "Einfaches Omelette", [Zutat("Ei", 2, "Stück"), Zutat("Milch", 50, "ml"), Zutat("Käse", 30, "g")]),
    Rezept("Salat", "Frischer Salat", [Zutat("Blattsalat", 50, "g"), Zutat("Tomate", 1, "Stück"), Zutat("Gurke", 0.25, "Stück")]),
    Rezept("Bratwurst mit Kartoffeln", "Deftiges Gericht", [Zutat("Bratwurst", 2, "Stück"), Zutat("Kartoffeln", 200, "g"), Zutat("Senf", 20, "g")]),
    Rezept("Hähnchen mit Reis", "Einfaches Reisgericht", [Zutat("Hähnchenbrust", 150, "g"), Zutat("Reis", 80, "g"), Zutat("Brokkoli", 100, "g")]),
    Rezept("Pizza Margherita", "Pizza mit Tomate und Mozzarella", [Zutat("Pizzateig", 1, "Stück"), Zutat("Tomatensauce", 80, "ml"), Zutat("Mozzarella", 100, "g")]),
    Rezept("Nudelsuppe", "Warme Suppe", [Zutat("Nudeln", 60, "g"), Zutat("Karotte", 0.5, "Stück"), Zutat("Sellerie", 30, "g"), Zutat("Gemüsebrühe", 500, "ml")]),
    Rezept("Fisch mit Gemüse", "Fischgericht", [Zutat("Fischfilet", 150, "g"), Zutat("Zucchini", 0.5, "Stück"), Zutat("Paprika", 0.5, "Stück")]),
    Rezept("Pfannkuchen", "Süsses Gericht", [Zutat("Mehl", 100, "g"), Zutat("Milch", 200, "ml"), Zutat("Ei", 1, "Stück")]),
]


def startdaten_anlegen(Session) -> None:
    with Session() as session:
        anzahl = len(session.scalars(select(RezeptORM)).all())
    if anzahl > 0:
        return

    datenbank = DatenbankZugriff(Session)
    for rezept in START_REZEPTE:
        datenbank.rezept_speichern(rezept)
