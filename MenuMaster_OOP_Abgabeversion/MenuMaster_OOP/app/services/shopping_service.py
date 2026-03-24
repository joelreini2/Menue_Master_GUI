"""Service für Einkaufslisten."""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database.models import MealPlanORM, RecipeORM
from app.models.shopping_list import ShoppingList


class ShoppingService:
    def __init__(self, session: Session):
        self.session = session

    def build_for_latest_meal_plan(self) -> ShoppingList:
        latest_plan = self.session.scalar(
            select(MealPlanORM).order_by(MealPlanORM.id.desc()).limit(1)
        )
        if latest_plan is None:
            return ShoppingList()
        return self.build_for_meal_plan_id(latest_plan.id)

    def build_for_meal_plan_id(self, meal_plan_id: int) -> ShoppingList:
        meal_plan = self.session.scalar(
            select(MealPlanORM)
            .options(selectinload(MealPlanORM.entries))
            .where(MealPlanORM.id == meal_plan_id)
        )
        shopping_list = ShoppingList()
        if meal_plan is None:
            return shopping_list

        recipe_ids = [entry.recipe_id for entry in meal_plan.entries if entry.recipe_id is not None]
        if not recipe_ids:
            return shopping_list

        recipes = self.session.scalars(
            select(RecipeORM)
            .options(selectinload(RecipeORM.ingredients))
            .where(RecipeORM.id.in_(recipe_ids))
        ).all()
        recipe_map = {recipe.id: recipe for recipe in recipes}

        for entry in meal_plan.entries:
            if entry.recipe_id is None:
                continue
            recipe = recipe_map[entry.recipe_id]
            for ingredient in recipe.ingredients:
                shopping_list.add_item(ingredient.name, ingredient.unit, ingredient.amount)
        return shopping_list
