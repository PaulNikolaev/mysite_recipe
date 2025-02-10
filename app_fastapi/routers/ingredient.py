from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated
from app_fastapi.db.db_depends import get_db
from app_fastapi.models.recipe import Recipe
from app_fastapi.models.ingredient import Ingredient

router = APIRouter(prefix="/ingredient", tags=["ingredient"])


@router.get("/")
async def get_recipes_by_ingredient(ingredient_name: str, db: Annotated[Session, Depends(get_db)]):
    recipes = db.scalars(
        select(Recipe).join(Ingredient).where(Ingredient.title.ilike(f"%{ingredient_name}%"))
    ).all()

    if recipes is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return recipes
