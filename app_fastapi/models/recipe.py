from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from db.db import Base


class Recipe(Base):
    __tablename__ = "recipe_recipe"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=True)
    description = Column(Text, nullable=False)
    cooking_time = Column(Integer, nullable=False)
    servings = Column(Integer, default=1, nullable=False)
    thumbnail = Column(String(255), default="images/thumbnails/default.jpg", nullable=True)
    status = Column(String(10), default="published", nullable=False)
    create = Column(DateTime, default=datetime.utcnow)
    update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fixed = Column(Boolean, default=False)

    category_id = Column(Integer, ForeignKey("recipe_category.id"))
    category = relationship("Category", back_populates="recipes")

    ingredients = relationship("Ingredient", back_populates="recipe", cascade="all, delete-orphan")


