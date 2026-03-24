"""ORM-Modelle für MenuMaster."""

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class RecipeORM(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    ingredients: Mapped[list["IngredientORM"]] = relationship(
        back_populates="recipe", cascade="all, delete-orphan"
    )
    meal_plan_entries: Mapped[list["MealPlanEntryORM"]] = relationship(
        back_populates="recipe"
    )


class IngredientORM(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(30), nullable=False)

    recipe: Mapped[RecipeORM] = relationship(back_populates="ingredients")


class MealPlanORM(Base):
    __tablename__ = "meal_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[str] = mapped_column(String(30), nullable=False)

    entries: Mapped[list["MealPlanEntryORM"]] = relationship(
        back_populates="meal_plan", cascade="all, delete-orphan"
    )


class MealPlanEntryORM(Base):
    __tablename__ = "meal_plan_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meal_plan_id: Mapped[int] = mapped_column(ForeignKey("meal_plans.id"), nullable=False)
    weekday: Mapped[str] = mapped_column(String(20), nullable=False)
    recipe_id: Mapped[int | None] = mapped_column(ForeignKey("recipes.id"), nullable=True)

    meal_plan: Mapped[MealPlanORM] = relationship(back_populates="entries")
    recipe: Mapped[RecipeORM | None] = relationship(back_populates="meal_plan_entries")
