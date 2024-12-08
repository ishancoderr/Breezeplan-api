from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
import json
import os

router = APIRouter(prefix="/suggestionEngine", tags=["suggestion"])

class Member(BaseModel):
    gender: str
    age: int

class SuggestionRequest(BaseModel):
    longitude: float
    latitude: float
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

@router.post("/activitySuggestions")
async def outdoor_activity_suggestions(request: SuggestionRequest):
    for suggestion in outdoorActivity:
        activity = suggestion["activity"]
        if activity not in user_feedback:
            print(user_feedback)
            user_feedback[activity] = 0

    return {"success": True, "data": outdoorActivity}

@router.post("/choosenActivityData")
async def chosen_activity_data(request: ChosenActivityRequest):
    activity = request.activity
    if activity not in choosenActivitySuggestions:
        raise HTTPException(status_code=400, detail="Activity not recognized.")

    # Update feedback score
    user_feedback[activity] += 1

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