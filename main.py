from fastapi import FastAPI
from controllers import category_controller,user_controller

app = FastAPI()
app.include_router(category_controller.router)
app.include_router(user_controller.router)
