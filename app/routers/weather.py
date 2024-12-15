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
            transformed_output = {
                "locationName": forecast_data["location"]["name"],  # Dynamically retrieve the location name
                "longitude": f'{round(forecast_data["location"]["lon"] * 100000)} meters',
                "latitude": f'{round(forecast_data["location"]["lat"] * 100000)} meters',
                "temperature": f'{round(forecast_data["current"]["temp_c"])} Celsius',
                "humidity": f'{forecast_data["current"]["humidity"]} %',
                "windSpeed": f'{round(forecast_data["current"]["wind_kph"] / 3.6)} m/s',
                "precipitation": f'{forecast_data["current"]["precip_mm"]} mm'
            }
            return transformed_output
        else:
            return {"error": f"Error: {response.status_code}, {response.text}"}


        