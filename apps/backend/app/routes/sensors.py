from fastapi import APIRouter, HTTPException
from app.models.sensor import SensorDataInput, SensorDataOutput
from app.database.mongodb import MongoDB
from typing import List

router = APIRouter(prefix="/api", tags=["sensors"])


@router.post("/send_data", status_code=200)
async def send_data(data: SensorDataInput):
    """
    Receive sensor data from embedded system and store in MongoDB.
    Matches exact JSON format from embedded FreeRTOS system.
    """
    try:
        record_id = await MongoDB.insert_sensor_data(data)
        return {
            "status": "success",
            "message": "Sensor data stored successfully",
            "id": record_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store sensor data: {str(e)}")


@router.get("/sensors_data", response_model=List[SensorDataOutput])
async def get_sensors_data():
    """
    Get all sensor data from MongoDB.
    Returns all records sorted by timestamp (newest first).
    """
    try:
        data = await MongoDB.get_all_sensor_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve sensor data: {str(e)}")

