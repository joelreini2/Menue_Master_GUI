"""Service für Wochenpläne."""

import random
from datetime import datetime

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, selectinload

from app.database.models import MealPlanEntryORM, MealPlanORM, RecipeORM
from app.models.mealplan import MealPlan, WEEKDAYS


class MealPlanService:
    def __init__(self, session: Session):
        self.session = session

    def create_random_assignments(self) -> dict[str, int | None]:
        recipe_ids = self.session.scalars(select(RecipeORM.id)).all()
        if not recipe_ids:
            return {day: None for day in WEEKDAYS}
        return {day: random.choice(recipe_ids) for day in WEEKDAYS}

    def save_meal_plan(self, title: str, assignments: dict[str, int | None]) -> MealPlan:
        valid_recipe_ids = set(self.session.scalars(select(RecipeORM.id)).all())
        meal_plan = MealPlan(id=None, title=title, assignments=assignments)
        meal_plan.validate(valid_recipe_ids)

        meal_plan_orm = MealPlanORM(
            title=meal_plan.title,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
        for day in WEEKDAYS:
            meal_plan_orm.entries.append(
                MealPlanEntryORM(weekday=day, recipe_id=assignments.get(day))
            )
        self.session.add(meal_plan_orm)
        self.session.commit()
        return self.get_latest_meal_plan()

    def get_latest_meal_plan(self) -> MealPlan | None:
        stmt = (
            select(MealPlanORM)
            .options(selectinload(MealPlanORM.entries))
            .order_by(desc(MealPlanORM.id))
            .limit(1)
        )
        meal_plan_orm = self.session.scalar(stmt)
        if meal_plan_orm is None:
            return None
        return self._to_domain(meal_plan_orm)

    def get_all_meal_plans(self) -> list[MealPlan]:
        stmt = (
            select(MealPlanORM)
            .options(selectinload(MealPlanORM.entries))
            .order_by(desc(MealPlanORM.id))
        )
        return [self._to_domain(item) for item in self.session.scalars(stmt).all()]

    @staticmethod
    def _to_domain(meal_plan_orm: MealPlanORM) -> MealPlan:
        assignments = {entry.weekday: entry.recipe_id for entry in meal_plan_orm.entries}
        return MealPlan(
            id=meal_plan_orm.id,
            title=meal_plan_orm.title,
            assignments=assignments,
            created_at=meal_plan_orm.created_at,
        )
