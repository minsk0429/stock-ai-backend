from fastapi import FastAPI
from app.api import price, ai

app = FastAPI()

app.include_router(price.router)
app.include_router(ai.router)
