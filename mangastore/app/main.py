from fastapi import FastAPI
from routes import auth_routes, manga_routes, user_routes, order_routes

app = FastAPI(title="Manga Store API")

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(manga_routes.router, prefix="/mangas", tags=["mangas"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(order_routes.router, prefix="/orders", tags=["orders"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Manga Store API"}