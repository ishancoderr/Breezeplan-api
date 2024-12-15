from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
import json
import os
from app.services.reinforcementLearningAgent import ReinforcementLearningAgent

router = APIRouter(prefix="/suggestionEngine", tags=["suggestion"])

class Member(BaseModel):
    gender: str
    age: int

class SuggestionRequest(BaseModel):
    longitude: float
    latitude: float
    temperature:float
    humidity:float
    windSpeed:float
    precipitation:float
    fitnessLevel: str
    members: List[Member]  
    timeRange: str

class ChosenActivityRequest(BaseModel):
    longitude: float
    latitude: float
    activity: str
    location: str
    timeRange: str

user_feedback = {}



def load_json_file(filename: str):
    file_path = os.path.join(os.path.dirname(__file__), "../testData", filename)
    with open(file_path, "r") as file:
        return json.load(file)

choosenActivitySuggestions = load_json_file("choosenActivityData.json")
outdoorActivity = load_json_file("outdoorActivity.json")

# Initialize the reinforcement learning agent
actions = [activity["activity"] for activity in outdoorActivity]
rl_agent = ReinforcementLearningAgent(actions)

@router.post("/activitySuggestions")
async def outdoor_activity_suggestions(request: SuggestionRequest):

    state = {
        "temperature": request.temperature,
        "humidity": request.humidity,
        "windSpeed": request.windSpeed,
        "precipitation": request.precipitation,
        "members": tuple((member.gender, member.age) for member in request.members),
        "fitnessLevel": request.fitnessLevel,
        "timeRange": request.timeRange
    }

    # Let the RL agent choose an action based on the state
    suggested_action = rl_agent.choose_action(state)

    # Prepare response data for the suggested activity
    suggestion_data = next((activity for activity in outdoorActivity if activity["activity"] == suggested_action), None)

    if not suggestion_data:
        raise HTTPException(status_code=404, detail="No suitable activity found.")

    return JSONResponse(content={"success": True, "data": suggestion_data})

@router.post("/choosenActivityData")
async def chosen_activity_data(request: ChosenActivityRequest):
    activity = request.activity

    if activity not in choosenActivitySuggestions:
        raise HTTPException(status_code=400, detail="Activity not recognized.")

    # Update feedback in the RL agent
    state = {
        "longitude": request.longitude,
        "latitude": request.latitude,
        "fitnessLevel": "N/A",  # Optional for chosen activities
        "timeRange": request.timeRange,
    }
    rl_agent.update_q_value(state, activity, reward=1)  # Reward of +1 for user feedback

    # Fetch activity path details
    activity_details = choosenActivitySuggestions[activity]
    response = {
        "activity": activity,
        "location": request.location,
        "chosenPath": {
            "pathName": activity_details["pathName"],
            "length": activity_details["length"],
            "lighting": activity_details["lighting"],
            "description": activity_details["description"],
        },
        "redirectUrl": activity_details["redirectUrl"],
        "safetyTips": activity_details["safetyTips"],
    }

    return JSONResponse(content={"success": True, "data": response})