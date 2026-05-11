"""Einfacher Datenbankzugriff für die Services.

Die Klasse ist absichtlich schlicht gehalten. Sie verwendet SQLAlchemy ORM, aber
versteckt keine komplizierte Architektur hinter zusätzlichen Design Patterns.
"""

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from menue_master.data_access.orm_modelle import (
    RezeptORM,
    RezeptZutatORM,
    WochenplanEintragORM,
    WochenplanORM,
    ZutatORM,
)
from menue_master.domain.modelle import Rezept, Wochenplan, WochenplanEintrag, Zutat, wochentage


class DatenbankZugriff:
    def __init__(self, Session: sessionmaker) -> None:
        self.Session = Session

    def alle_rezepte_laden(self) -> list[Rezept]:
        with self.Session() as session:
            rezepte_orm = session.scalars(select(RezeptORM).order_by(RezeptORM.name)).all()
            return [self._rezept_aus_orm(rezept_orm) for rezept_orm in rezepte_orm]

    def rezept_speichern(self, rezept: Rezept) -> Rezept:
        with self.Session() as session:
            rezept_orm = RezeptORM(name=rezept.name.strip(), beschreibung=rezept.beschreibung.strip())
            for zutat in rezept.zutaten:
                zutat_orm = self._zutat_finden_oder_erstellen(session, zutat.name, zutat.einheit)
                rezept_orm.zutaten.append(RezeptZutatORM(zutat=zutat_orm, menge=zutat.menge))
            session.add(rezept_orm)
            session.commit()
            session.refresh(rezept_orm)
            return self._rezept_aus_orm(rezept_orm)

    def wochenplan_speichern(self, wochenplan: Wochenplan) -> Wochenplan:
        with self.Session() as session:
            wochenplan_orm = WochenplanORM(titel=wochenplan.titel.strip(), gespeichert=True)
            for eintrag in wochenplan.eintraege:
                rezept_id = eintrag.rezept.rezept_id if eintrag.rezept else None
                wochenplan_orm.eintraege.append(
                    WochenplanEintragORM(wochentag=eintrag.wochentag, rezept_id=rezept_id)
                )
            session.add(wochenplan_orm)
            session.commit()
            session.refresh(wochenplan_orm)
            return self._wochenplan_aus_orm(wochenplan_orm)

    def alle_wochenplaene_laden(self) -> list[Wochenplan]:
        with self.Session() as session:
            plaene = session.scalars(select(WochenplanORM).order_by(WochenplanORM.wochenplan_id.desc())).all()
            return [self._wochenplan_aus_orm(plan) for plan in plaene]

    def _zutat_finden_oder_erstellen(self, session, name: str, einheit: str) -> ZutatORM:
        stmt = select(ZutatORM).where(ZutatORM.name == name.strip(), ZutatORM.einheit == einheit.strip())
        zutat = session.scalars(stmt).first()
        if zutat is None:
            zutat = ZutatORM(name=name.strip(), einheit=einheit.strip())
            session.add(zutat)
        return zutat

    def _rezept_aus_orm(self, rezept_orm: RezeptORM) -> Rezept:
        zutaten = [
            Zutat(name=rz.zutat.name, menge=rz.menge, einheit=rz.zutat.einheit)
            for rz in rezept_orm.zutaten
        ]
        return Rezept(
            rezept_id=rezept_orm.rezept_id,
            name=rezept_orm.name,
            beschreibung=rezept_orm.beschreibung,
            zutaten=zutaten,
        )

    def _wochenplan_aus_orm(self, wochenplan_orm: WochenplanORM) -> Wochenplan:
        sortierung = {tag: nr for nr, tag in enumerate(wochentage)}
        eintraege_orm = sorted(wochenplan_orm.eintraege, key=lambda e: sortierung.get(e.wochentag, 99))
        eintraege: list[WochenplanEintrag] = []
        for eintrag_orm in eintraege_orm:
            rezept = self._rezept_aus_orm(eintrag_orm.rezept) if eintrag_orm.rezept else None
            eintraege.append(WochenplanEintrag(wochentag=eintrag_orm.wochentag, rezept=rezept))
        return Wochenplan(
            wochenplan_id=wochenplan_orm.wochenplan_id,
            titel=wochenplan_orm.titel,
            eintraege=eintraege,
        )
