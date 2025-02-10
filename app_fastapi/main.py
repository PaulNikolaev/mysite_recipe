from fastapi import FastAPI
from routers import recipe, category, ingredient
from db.db import engine


app = FastAPI(root_path="/api", title="Recipe API", description="API для работы с рецептами")


@app.get("/")
async def welcome() -> dict:
    return {"message": "My recipe app"}

app.include_router(category.router)
app.include_router(recipe.router)
app.include_router(ingredient.router)