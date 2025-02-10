from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from db.db import Base

class Category(Base):
    """
    Категория рецепта
    """
    __tablename__ = "recipe_category"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, unique=True)
    slug = Column(String(255), nullable=True, unique=True)
    description = Column(Text, nullable=True)

    recipes = relationship("Recipe", back_populates="category")
