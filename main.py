from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.weather import router as weather_router
from app.routers.activitySuggestions import router as activity_suggestions_router

app = FastAPI(
    title="Breezeplan API",
    version="1.0.0.v",
    description="API for weather data and activity suggestions."
)

# Enable CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, change to specific frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(weather_router)
app.include_router(activity_suggestions_router)

@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint for the Breezeplan API.
    """
    return {"message": "Welcome to the Breezeplan API!"}