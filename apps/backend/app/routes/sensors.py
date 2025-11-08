import logging
from fastapi import APIRouter, HTTPException
from app.models.sensor import SensorDataInput, SensorDataOutput
from app.database.mongodb import MongoDB
from typing import List

logger = logging.getLogger(__name__)
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
        logger.error(f"Error retrieving sensor data: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve sensor data: {str(e)}")


@router.get("/database_info")
async def get_database_info():
    """
    Get information about the MongoDB database and collection.
    Useful for checking if the database exists and how many documents are stored.
    """
    try:
        info = await MongoDB.get_database_info()
        return info
    except Exception as e:
        logger.error(f"Error retrieving database info: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve database info: {str(e)}")

