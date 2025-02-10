from fastapi import FastAPI
from app_fastapi.routers import recipe, category, ingredient
from app_fastapi.db.db import engine


app = FastAPI(title="Recipe API", description="API для работы с рецептами")


@app.get("/")
async def welcome() -> dict:
    return {"message": "My recipe app"}

app.include_router(category.router)
app.include_router(recipe.router)
app.include_router(ingredient.router)