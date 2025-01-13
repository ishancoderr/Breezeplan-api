from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
import json
import time
from app.services.reinforcementLearningAgent import ReinforcementLearningAgent
from app.services.categorizer import UserInputCategorizer
from app.services.dataSaveService import DataSaveService

router = APIRouter(prefix="/suggestionEngine", tags=["suggestion"])

rl_agent = ReinforcementLearningAgent()

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
    id: int
    activity: str
    tableHash: str
    category: str



user_feedback = {}

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
    dataSaver = DataSaveService(
                    output_categorization_data, 
                    output_categorization_data[5],
                    output_categorization_data[0],
                    output_categorization_data[4]
                    )
    out_hash = await dataSaver.output_hash()
    file_name = await dataSaver.get_file_name(
        output_categorization_data[5],
        output_categorization_data[0],
        output_categorization_data[4]
    )

    file_path = f"data/{file_name}"
    outdoor_activity_path = f"outdoor_activity_data/outdoor_activity_{file_name}"
    #await dataSaver.save_to_json()
    outdoor_file_path_for_method = f"outdoor_activity_{file_name}"

    #create files if not exist
    await dataSaver.create_file_if_not_exists("data", file_name)
    await dataSaver.create_file_if_not_exists("outdoor_activity_data", outdoor_file_path_for_method)

    endPoint = "activitySuggestions"
    file_name_without_extension = file_name.rstrip(".json")
    if out_hash:
        with open(file_path, mode='r') as file:
            data = file.read()
            json_data = json.loads(data)
        if out_hash in json_data:
            print(f"Hash {out_hash} found in {file_path}.")
            output_values = json_data[out_hash].get("values", "No values found")
            print(f"Output values: {output_values}")
            print(f"file_path values: {file_path}")
            sorted_items = sorted(output_values.items(), key=lambda x: x[1], reverse=True)
            top_4 = sorted_items[:4]
            remaining = sorted_items[4:]
            additional_2 = remaining[:2]
            selected_names = [name for name, _ in top_4 + additional_2]
            await rl_agent.update_q_value(selected_names,out_hash,file_path, endPoint)
            print(f"Selected names: {selected_names}")
            with open(outdoor_activity_path, "r") as file:
                data = json.load(file)
                output_values = [activity for activity in data if activity['activity'] in selected_names]
                for activity in output_values:
                    activity['file_name'] = file_name_without_extension 
                    activity['tableHash'] = out_hash
                return {"success": True, "data": output_values}
        else:
            print(f"Hash {out_hash} not found in {file_path}. Saving data to JSON.")
            await dataSaver.save_to_json()
            with open(file_path, mode='r') as file:
                data = file.read()
                json_data = json.loads(data)
            if out_hash in json_data:
                print(f"Hash {out_hash} found in {file_path}.")
                output_values = json_data[out_hash].get("values", "No values found")
                items = sorted(output_values.items())
                six_values = items[:6]
                selected_names = [name for name, _ in six_values ]
                await rl_agent.update_q_value(selected_names, out_hash, file_path, endPoint)
                with open(outdoor_activity_path, "r") as file:
                    data = json.load(file)
                    output_values = [activity for activity in data if activity['activity'] in selected_names] 
                    for activity in output_values:
                        activity['file_name'] = file_name_without_extension 
                        activity['tableHash'] = out_hash  
                    return { "success": True, "data": output_values }
                
            else: 
                return {"success": False, "data": []}


@router.post("/choosenActivityData")
async def chosen_activity_data(request: ChosenActivityRequest):
    selected_activity = request.activity
    table_hash = request.tableHash
    category = request.category
    file_path = f"data/{category}.json"
    endPoint = "choosenActivityData"
    try:
        await rl_agent.update_q_value([selected_activity], table_hash, file_path, endPoint)
        return {"success": True, "message": f"Q-table updated for activity '{selected_activity}-{table_hash}'"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating Q-table: {str(e)}")   





























    # Get Q-values for the encoded state
    #encoded_key_str = str(encoded_key)
    #q_values = q_table.get(encoded_key_str)
    #suc ='success'
    #return JSONResponse(content={"success": True, "data": suc})
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
 '''