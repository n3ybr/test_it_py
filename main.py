from fastapi import FastAPI
from controllers import category_controller

app = FastAPI()
app.include_router(category_controller.router)
