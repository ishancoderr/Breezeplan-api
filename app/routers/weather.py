from fastapi import APIRouter
import httpx
from pydantic import BaseModel

router = APIRouter(prefix="/weather", tags=["Weather"])

#weather api ===> https://www.weatherapi.com/my/

class WeatherRoutes:
    @router.post("/weatherData")
    async def get_weather_data(latitude: float, longitude: float): 
        base_url = "http://api.weatherapi.com/v1/forecast.json"
        api_key = "ad4fd6881cf24aeb98395308242911"  # Replace with your actual API key
        days = 3

        params = {
            "key": api_key,
            "q": f"{latitude},{longitude}",
            "days": days,
            "aqi": "yes",
            "alerts": "yes"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(base_url, params=params)

        if response.status_code == 200:
            forecast_data = response.json()
            return forecast_data
        else:
            return {"error": f"Error: {response.status_code}, {response.text}"}


        