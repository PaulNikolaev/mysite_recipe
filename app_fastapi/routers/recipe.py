from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session  # Синхронная сессия
from sqlalchemy import select
from typing import Annotated
from db.db_depends import get_db
from models.recipe import Recipe
from models.category import Category

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/")
async def get_all_recipes(db: Annotated[Session, Depends(get_db)]):
    recipes = db.scalars(select(Recipe).where(Recipe.status == 'published')).all()
    if recipes is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found")
    return recipes


@router.get('/{category_title}')
async def recipe_by_category(db: Annotated[Session, Depends(get_db)], category_title: str):
    category = db.scalar(select(Category).where(Category.title == category_title))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    products_category = db.scalars(
        select(Recipe).where(
            Recipe.category_id == category.id,
            Recipe.status == 'published'
        )
    ).all()

    return products_category


@router.get('/recipe/{recipe_title}')
async def recipe_by_title(db: Annotated[Session, Depends(get_db)], recipe_title: str):
    recipes = db.scalars(
        select(Recipe).where(
            Recipe.title.ilike(f"%{recipe_title}%"),
            Recipe.status == 'published'
        )
    ).all()

    if not recipes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No matching recipes found"
        )

    return recipes

# @router.post('/')
# async def create_recipe():
#     pass

# @router.put('/{recipe_slug}')
# async def update_recipe(recipe_slug: str):
#     pass
#
# @router.delete('/')
# async def delete_recipe(recipe_id: int):
#     pass
