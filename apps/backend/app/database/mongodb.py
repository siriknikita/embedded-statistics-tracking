import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from datetime import datetime
from app.models.sensor import SensorDataInput, SensorDataOutput


class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database = None

    @classmethod
    async def connect(cls):
        """Connect to MongoDB"""
        mongodb_url = os.getenv("MONGODB_URL")
        db_name = os.getenv("MONGODB_DB_NAME", "embedded-statistics-tracking-dev")
        
        if not mongodb_url:
            raise ValueError("MONGODB_URL environment variable is not set")
        
        cls.client = AsyncIOMotorClient(mongodb_url)
        cls.database = cls.client[db_name]
        print(f"Connected to MongoDB database: {db_name}")

    @classmethod
    async def disconnect(cls):
        """Disconnect from MongoDB"""
        if cls.client:
            cls.client.close()
            print("Disconnected from MongoDB")

    @classmethod
    async def insert_sensor_data(cls, data: SensorDataInput) -> str:
        """Insert sensor data into MongoDB"""
        if not cls.database:
            raise RuntimeError("Database not connected. Call connect() first.")
        
        document = {
            "timestamp": datetime.utcnow(),
            "temperature": data.temperature,
            "humidity": data.humidity,
            "voc": data.voc,
            "light": data.light,
            "sound": data.sound,
            "accelerometer": {
                "x": data.accelerometer.x,
                "y": data.accelerometer.y,
                "z": data.accelerometer.z,
            },
            "gyroscope": {
                "x": data.gyroscope.x,
                "y": data.gyroscope.y,
                "z": data.gyroscope.z,
            },
        }
        
        result = await cls.database.sensor_readings.insert_one(document)
        return str(result.inserted_id)

    @classmethod
    async def get_all_sensor_data(cls) -> List[SensorDataOutput]:
        """Get all sensor data from MongoDB"""
        if not cls.database:
            raise RuntimeError("Database not connected. Call connect() first.")
        
        cursor = cls.database.sensor_readings.find().sort("timestamp", -1)
        documents = await cursor.to_list(length=None)
        
        results = []
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            results.append(SensorDataOutput(**doc))
        
        return results

    @classmethod
    async def clear_all_data(cls) -> int:
        """Clear all sensor data (for testing)"""
        if not cls.database:
            raise RuntimeError("Database not connected. Call connect() first.")
        
        result = await cls.database.sensor_readings.delete_many({})
        return result.deleted_count

