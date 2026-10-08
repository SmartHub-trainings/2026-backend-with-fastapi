from fastapi import FastAPI
from routes.users_routes import users_router
from routes.products_routes import products_router


app = FastAPI()


app.include_router(users_router,prefix="/users")
app.include_router(products_router,prefix="/products")




