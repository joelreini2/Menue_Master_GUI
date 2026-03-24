"""NiceGUI-Seiten für MenuMaster.

Die UI bleibt bewusst einfach und studentisch.
"""

from contextlib import contextmanager

from nicegui import ui

from app.data.seed import initialize_database
from app.database.db import SessionLocal
from app.models.mealplan import WEEKDAYS
from app.services.mealplan_service import MealPlanService
from app.services.recipe_service import RecipeService
from app.services.shopping_service import ShoppingService


@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_app():
    initialize_database()

    @ui.page("/")
    def index_page():
        ui.label("MenuMaster").classes("text-3xl font-bold")
        ui.label("Rezept- und Wochenplaner als Browser-App").classes("text-lg")

        with ui.row().classes("gap-2"):
            ui.button("Rezepte", on_click=lambda: ui.navigate.to("/rezepte"))
            ui.button("Wochenplan", on_click=lambda: ui.navigate.to("/wochenplan"))
            ui.button("Einkaufsliste", on_click=lambda: ui.navigate.to("/einkaufsliste"))
            ui.button("Vergangene Wochenpläne", on_click=lambda: ui.navigate.to("/verlauf"))

    @ui.page("/rezepte")
    def recipes_page():
        ui.button("Zurück", on_click=lambda: ui.navigate.to("/"))
        ui.label("Rezepte").classes("text-2xl font-bold")
        with session_scope() as session:
            recipes = RecipeService(session).get_all_recipes()
        for recipe in recipes:
            with ui.card().classes("w-full max-w-xl"):
                ui.label(recipe.name).classes("text-xl")
                for ingredient in recipe.ingredients:
                    ui.label(f"- {ingredient.amount:g} {ingredient.unit} {ingredient.name}")

    @ui.page("/wochenplan")
    def meal_plan_page():
        ui.button("Zurück", on_click=lambda: ui.navigate.to("/"))
        ui.label("Wochenplan erstellen").classes("text-2xl font-bold")
        title_input = ui.input("Titel des Wochenplans", value="Meine Woche")

        with session_scope() as session:
            recipe_choices = RecipeService(session).get_recipe_choices()

        select_map: dict[str, ui.select] = {}
        for day in WEEKDAYS:
            select_map[day] = ui.select(
                options={None: "Kein Rezept", **{recipe_id: name for name, recipe_id in recipe_choices.items()}},
                label=day,
                value=None,
            ).classes("w-80")

        def save_plan() -> None:
            assignments = {day: select_map[day].value for day in WEEKDAYS}
            with session_scope() as session:
                service = MealPlanService(session)
                try:
                    service.save_meal_plan(title_input.value or "Meine Woche", assignments)
                except ValueError as error:
                    ui.notify(str(error), color="negative")
                    return
            ui.notify("Wochenplan gespeichert.", color="positive")

        def random_fill() -> None:
            with session_scope() as session:
                assignments = MealPlanService(session).create_random_assignments()
            for day, recipe_id in assignments.items():
                select_map[day].value = recipe_id
            ui.notify("Wochenplan zufällig gefüllt.")

        with ui.row().classes("gap-2"):
            ui.button("Zufällig füllen", on_click=random_fill)
            ui.button("Wochenplan speichern", on_click=save_plan)

    @ui.page("/einkaufsliste")
    def shopping_page():
        ui.button("Zurück", on_click=lambda: ui.navigate.to("/"))
        ui.label("Einkaufsliste").classes("text-2xl font-bold")
        with session_scope() as session:
            shopping_list = ShoppingService(session).build_for_latest_meal_plan()
        rows = shopping_list.as_rows()
        if not rows:
            ui.label("Noch keine Einkaufsliste vorhanden. Bitte zuerst einen Wochenplan speichern.")
            return
        with ui.card().classes("w-full max-w-xl"):
            for name, amount, unit in rows:
                ui.label(f"- {amount:g} {unit} {name}")

    @ui.page("/verlauf")
    def history_page():
        ui.button("Zurück", on_click=lambda: ui.navigate.to("/"))
        ui.label("Vergangene Wochenpläne").classes("text-2xl font-bold")
        with session_scope() as session:
            plans = MealPlanService(session).get_all_meal_plans()
            recipe_choices = RecipeService(session).get_recipe_choices()
        recipe_names = {recipe_id: name for name, recipe_id in recipe_choices.items()}
        if not plans:
            ui.label("Noch keine gespeicherten Wochenpläne vorhanden.")
            return
        for plan in plans:
            with ui.card().classes("w-full max-w-xl"):
                ui.label(f"{plan.title} ({plan.created_at})").classes("text-lg font-semibold")
                for day in WEEKDAYS:
                    recipe_id = plan.assignments.get(day)
                    recipe_name = recipe_names.get(recipe_id, "Kein Rezept") if recipe_id else "Kein Rezept"
                    ui.label(f"{day}: {recipe_name}")

    return ui
