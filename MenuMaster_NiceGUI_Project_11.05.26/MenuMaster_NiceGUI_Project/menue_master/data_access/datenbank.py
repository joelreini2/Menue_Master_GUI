from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from menue_master.data_access.orm_modelle import Base

DATENBANK_DATEI = Path(__file__).resolve().parents[2] / "menue_master.db"


def datenbank_erstellen(datenbank_pfad: str | Path = DATENBANK_DATEI) -> tuple[Engine, sessionmaker]:
    engine = create_engine(f"sqlite:///{datenbank_pfad}", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session
