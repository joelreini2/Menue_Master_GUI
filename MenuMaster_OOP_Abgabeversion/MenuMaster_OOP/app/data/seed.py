"""Initiales Laden der Rezepte aus der vorhandenen Textdatei."""

from pathlib import Path

from app.database.db import Base, SessionLocal, engine
from app.services.recipe_service import RecipeService


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        recipe_service = RecipeService(session)
        if recipe_service.get_all_recipes():
            return
        source_file = Path(__file__).resolve().parents[2] / "data" / "rezepte.txt"
        if source_file.exists():
            recipe_service.import_from_text_file(source_file)
    finally:
        session.close()
