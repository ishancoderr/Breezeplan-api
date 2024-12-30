from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
import json
import os
from app.services.reinforcementLearningAgent import ReinforcementLearningAgent
from app.services.categorizer import UserInputCategorizer
from app.services.dataSaveService import DataSaveService

router = APIRouter(prefix="/suggestionEngine", tags=["suggestion"])

class Member(BaseModel):
    gender: str
    age: int
    fitnessLevel: str

class SuggestionRequest(BaseModel):
    longitude: float
    latitude: float
    temperature:float
    humidity:float
    windSpeed:float
    precipitation:float
    members: List[Member]  
    timeRange: int
    calories:int

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
        "timeRange": request.timeRange,
        "calories": request.calories,
        "members": [
        (member.gender, member.age, member.fitnessLevel) for member in request.members
        ]
    }
    categorizer = UserInputCategorizer(
        temperature=state['temperature'],
        humidity=state['humidity'],
        wind_speed=state['windSpeed'],
        precipitation=state['precipitation'],
        time_range=state['timeRange'],
        calories=state['calories'],
        members=state['members']
    )

    output_categorization_data = await categorizer.get_encoded_key()
    print(output_categorization_data)
    dataSaver = DataSaveService(
                    output_categorization_data, 
                    output_categorization_data[5],
                    output_categorization_data[8]
                    )
    await dataSaver.save_to_json()
    # Get Q-values for the encoded state
    #encoded_key_str = str(encoded_key)
    #q_values = q_table.get(encoded_key_str)
    suc ='success'
    return JSONResponse(content={"success": True, "data": suc})
    '''
    if not q_values:
        raise HTTPException(status_code=404, detail="No Q-values found for the given state.")

    # Sort activities by Q-values in descending order
    sorted_activities = sorted(q_values.items(), key=lambda x: x[1], reverse=True)
    top_3_activities = [activity[0] for activity in sorted_activities[:3]]

    # Prepare response data for the top 3 activities
    suggestions = [
        activity for activity in outdoorActivity if activity["activity"] in top_3_activities
    ]

    return JSONResponse(content={"success": True, "data": suggestions})
'''
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
 