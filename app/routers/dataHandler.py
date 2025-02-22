from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
from app.externalServiceHandler.errorHandler import ErrorHandler
from app.externalServiceHandler.dbConnection import DbConnection
import uuid

router = APIRouter(prefix="/dataHandler", tags=["data"])

# Pydantic models
class LocationInfo(BaseModel):
    pathNameOrLocationName: str
    length: str
    lighting: str
    description: str
    redirectUrl: str
    safetyTips: List[str]

class ActivityData(BaseModel):
    id: str  # Change to string for UUID or MongoDB ObjectId
    activity: str
    description: str
    groupSuitability: str
    timeRequired: str
    image: str
    locationInfo: LocationInfo


@router.post("/addData")
async def add_activity(activity_data: ActivityData):
    db_instance = DbConnection()  # Create an instance of DbConnection
    db_instance.connect()  # Call the connect method
    pass