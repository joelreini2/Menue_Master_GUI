"""ORM-Modelle mit SQLAlchemy.

Die Klassen bilden das ERM ab: Rezept, Zutat, Rezept_Zutat, Wochenplan und
Wochenplan_Eintrag. SQL wird nicht direkt geschrieben, sondern über das ORM erzeugt.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):



class RezeptORM(Base):
    __tablename__ = "rezept"

    rezept_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    beschreibung: Mapped[str] = mapped_column(String(500), default="")

    zutaten: Mapped[list["RezeptZutatORM"]] = relationship(
        back_populates="rezept", cascade="all, delete-orphan"
    )


class ZutatORM(Base):
    __tablename__ = "zutat"

    zutat_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    einheit: Mapped[str] = mapped_column(String(30), nullable=False)

    rezepte: Mapped[list["RezeptZutatORM"]] = relationship(back_populates="zutat")


class RezeptZutatORM(Base):
    __tablename__ = "rezept_zutat"

    rezept_id: Mapped[int] = mapped_column(ForeignKey("rezept.rezept_id"), primary_key=True)
    zutat_id: Mapped[int] = mapped_column(ForeignKey("zutat.zutat_id"), primary_key=True)
    menge: Mapped[float] = mapped_column(Float, nullable=False)

    rezept: Mapped[RezeptORM] = relationship(back_populates="zutaten")
    zutat: Mapped[ZutatORM] = relationship(back_populates="rezepte")


class WochenplanORM(Base):
    __tablename__ = "wochenplan"

    wochenplan_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titel: Mapped[str] = mapped_column(String(120), nullable=False)
    erstellungsdatum: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    gespeichert: Mapped[bool] = mapped_column(Boolean, default=True)

    eintraege: Mapped[list["WochenplanEintragORM"]] = relationship(
        back_populates="wochenplan", cascade="all, delete-orphan"
    )


class WochenplanEintragORM(Base):
    __tablename__ = "wochenplan_eintrag"

    eintrag_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    wochenplan_id: Mapped[int] = mapped_column(ForeignKey("wochenplan.wochenplan_id"), nullable=False)
    rezept_id: Mapped[int | None] = mapped_column(ForeignKey("rezept.rezept_id"), nullable=True)
    wochentag: Mapped[str] = mapped_column(String(20), nullable=False)

    wochenplan: Mapped[WochenplanORM] = relationship(back_populates="eintraege")
    rezept: Mapped[RezeptORM | None] = relationship()
