from fastapi import FastAPI 
from app.routers.weather import router as weather_router

app = FastAPI(title="Breezeplan API", version="1.0.0.v")

app.include_router(weather_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Breezeplan API!"}