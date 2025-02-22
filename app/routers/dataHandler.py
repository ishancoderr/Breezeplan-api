from fastapi import APIRouter,Query, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
from typing import List, Optional
from app.externalServiceHandler.dbConnection import DbConnection
from app.externalServiceHandler.errorHandler import ErrorHandler
import uuid
import datetime
from bson import json_util
import json

router = APIRouter(prefix="/dataHandler", tags=["data"])

class LocationInfo(BaseModel):
    pathNameOrLocationName: str
    length: str
    lighting: str
    description: str
    redirectUrl: str
    safetyTips: List[str]

class ActivityData(BaseModel):
    activity: str
    description: str
    members: List[str]  # Group category instead of names
    temperature: List[str]  # Temperature category instead of value
    timeRequired: List[str]  # Time category instead of range
    groupSuitability: str
    image: str
    locationInfo: LocationInfo
    expDate: datetime.datetime

def get_db_instance():
    db_instance = DbConnection()
    try:
        db_instance.connect()
        db_instance.db.activities.create_index("expDate", expireAfterSeconds=0)
    except Exception as e:
        return ErrorHandler.handle_database_error(e)
    return db_instance

def generate_activity_id(activity: str, location: str):
    # Remove spaces and special characters, and convert to lowercase
    activity_cleaned = activity.replace(" ", "_").lower()
    location_cleaned = location.replace(" ", "_").lower()
    
    # Generate a timestamp
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    
    # Combine into a unique ID
    return f"{activity_cleaned}-{location_cleaned}-{timestamp}"

@router.post("/addData")
async def add_activity(activity_data: ActivityData):
    try:
        db_instance = get_db_instance()
        activity_id = generate_activity_id(activity_data.activity, activity_data.locationInfo.pathNameOrLocationName)
        activity_dict = activity_data.dict()
        activity_dict["id"] = activity_id
        db_instance.db.activities.insert_one(activity_dict)
        return JSONResponse(content={"message": "Activity added successfully", "id": activity_id}, status_code=201)
    except Exception as e:
        return ErrorHandler.handle_database_error(e)

@router.get("/searchData")
async def search_activity(
    activity: Optional[str] = Query(None, description="Filter by activity name"),
    location: Optional[str] = Query(None, description="Filter by location name"),
    description: Optional[str] = Query(None, description="Filter by description")
):
    try:
        db_instance = get_db_instance()
        
        # Build the query dynamically
        query = {}
        if activity:
            query["activity"] = {"$regex": activity, "$options": "i"}
        if location:
            query["locationInfo.pathNameOrLocationName"] = {"$regex": location, "$options": "i"}
        if description:
            query["description"] = {"$regex": description, "$options": "i"}
        
        if query:
            activities = list(db_instance.db.activities.find(query, {"_id": 0}).limit(10))
        else:  
            activities = list(db_instance.db.activities.find({}, {"_id": 0}).limit(10))
        
        activities_json = json.loads(json_util.dumps(activities))
        return JSONResponse(content=activities_json)
    except Exception as e:
        print(f"Error: {str(e)}")
        return ErrorHandler.handle_database_error(e)

@router.put("/editData/{activity_id}")
async def edit_activity(activity_id: str, updated_data: ActivityData):
    try:
        db_instance = get_db_instance()
        update_result = db_instance.db.activities.update_one({"id": activity_id}, {"$set": updated_data.dict()})
        if update_result.matched_count == 0:
            return ErrorHandler.handle_not_found("Activity not found")
        return JSONResponse(content={"message": "Activity updated successfully"})
    except Exception as e:
        return ErrorHandler.handle_database_error(e)

@router.delete("/deleteData/{activity_id}")
async def delete_activity(activity_id: str):
    try:
        db_instance = get_db_instance()
        delete_result = db_instance.db.activities.delete_one({"id": activity_id})
        if delete_result.deleted_count == 0:
            return ErrorHandler.handle_not_found("Activity not found")
        return JSONResponse(content={"message": "Activity deleted successfully"})
    except Exception as e:
        return ErrorHandler.handle_database_error(e)
