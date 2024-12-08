from fastapi import FastAPI
from app.routers.weather import router as weather_router
from app.routers.activitySuggestions import router as activity_suggestions_router

app = FastAPI(
    title="Breezeplan API",
    version="1.0.0.v",
    description="API for weather data and activity suggestions."
)

app.include_router(weather_router)
app.include_router(activity_suggestions_router)

@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint for the Breezeplan API.
    """
    return {"message": "Welcome to the Breezeplan API!"}