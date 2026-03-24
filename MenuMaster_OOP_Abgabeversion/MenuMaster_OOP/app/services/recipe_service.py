"""Service für Rezepte."""

from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database.models import IngredientORM, RecipeORM
from app.models.recipe import Ingredient, Recipe


class RecipeService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_recipes(self) -> list[Recipe]:
        stmt = select(RecipeORM).options(selectinload(RecipeORM.ingredients)).order_by(RecipeORM.name)
        recipes = self.session.scalars(stmt).all()
        return [self._to_domain(recipe) for recipe in recipes]

    def get_recipe_choices(self) -> dict[str, int]:
        return {recipe.name: recipe.id for recipe in self.get_all_recipes() if recipe.id is not None}

    def import_from_text_file(self, filepath: str | Path) -> int:
        grouped: dict[str, list[Ingredient]] = {}
        with open(filepath, "r", encoding="utf-8") as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line:
                    continue
                parts = [part.strip() for part in line.split(";")]
                if len(parts) != 4:
                    continue
                recipe_name, ingredient_name, amount_text, unit = parts
                amount = float(amount_text.replace(",", "."))
                grouped.setdefault(recipe_name, []).append(Ingredient(ingredient_name, amount, unit))

        created_count = 0
        for recipe_name, ingredients in grouped.items():
            exists = self.session.scalar(select(RecipeORM).where(RecipeORM.name == recipe_name))
            if exists:
                continue
            recipe = Recipe(id=None, name=recipe_name, ingredients=ingredients)
            recipe.validate()
            recipe_orm = RecipeORM(name=recipe.name)
            for ingredient in recipe.ingredients:
                recipe_orm.ingredients.append(
                    IngredientORM(name=ingredient.name, amount=ingredient.amount, unit=ingredient.unit)
                )
            self.session.add(recipe_orm)
            created_count += 1
        self.session.commit()
        return created_count

    @staticmethod
    def _to_domain(recipe_orm: RecipeORM) -> Recipe:
        return Recipe(
            id=recipe_orm.id,
            name=recipe_orm.name,
            ingredients=[
                Ingredient(name=item.name, amount=item.amount, unit=item.unit)
                for item in recipe_orm.ingredients
            ],
        )
