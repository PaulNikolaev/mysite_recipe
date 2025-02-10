from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # Синхронная сессия
from sqlalchemy import select, update
from typing import Annotated
# from sqlalchemy import insert
# from slugify import slugify

from db.db_depends import get_db
# from schemas import CategoryCreate
from models.category import Category

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/")
async def get_all_categories(db: Annotated[Session, Depends(get_db)]):
    categories = db.scalars(select(Category)).all()
    if categories is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found")
    return categories

# @router.post('/', status_code=status.HTTP_201_CREATED)
# async def create_category(create_category: CategoryCreate, db: Annotated[Session, Depends(get_db)]):
#     db.execute(insert(Category).values(
#         title=create_category.title,
#         slug=slugify(create_category.title),
#         description=create_category.description
#     ))
#     db.commit()
#     return {
#         'status_code': status.HTTP_201_CREATED,
#         'transaction': 'Successful',
#     }


# @router.put('/')
# async def update_category(category_id: int, update_category: CategoryCreate, db: Annotated[Session, Depends(get_db)]):
#     category = db.scalar(select(Category).where(Category.id == category_id))
#     if category is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='There is no category found'
#         )
#
#     db.execute(update(Category).where(Category.id == category_id).values(
#         title=update_category.title,
#         slug=slugify(update_category.title),
#         description=update_category.description
#     ))
#     db.commit()
#     return {
#         'status_code': status.HTTP_200_OK,
#         'transaction': 'Category update is successful'
#     }


# @router.delete('/')
# async def delete_category(db: Annotated[Session, Depends(get_db)], category_id: int):
#     category = db.scalar(select(Category).where(Category.id == category_id))
#     if category is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='There is no category found'
#         )
#     db.delete(category)
#     db.commit()
#     return {
#         'status_code': status.HTTP_200_OK,
#         'transaction': 'Category delete is successful'
#     }
