from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.db import Base


class Ingredient(Base):
    """
    Ингредиент для рецепта
    """
    __tablename__ = 'recipe_ingredient'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    amount = Column(Integer, nullable=False, default=1)
    quantity = Column(String(50), nullable=False, default="грамм")
    recipe_id = Column(Integer, ForeignKey('recipe_recipe.id', ondelete='CASCADE'), nullable=False)

    recipe = relationship("Recipe", back_populates="ingredients")

    def __repr__(self):
        return f"{self.title} — {self.amount} {self.quantity}"