import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from datetime import datetime
from app.models.sensor import SensorDataInput, SensorDataOutput

logger = logging.getLogger(__name__)


class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database = None

    @classmethod
    async def connect(cls):
        """Connect to MongoDB and verify connection"""
        mongodb_url = os.getenv("MONGODB_URL")
        db_name = os.getenv("MONGODB_DB_NAME", "embedded-statistics-tracking-dev")
        
        if not mongodb_url:
            raise ValueError("MONGODB_URL environment variable is not set")
        
        cls.client = AsyncIOMotorClient(mongodb_url)
        cls.database = cls.client[db_name]
        
        # Verify connection by pinging the server
        try:
            await cls.client.admin.command('ping')
            logger.info(f"Successfully connected to MongoDB")
            logger.info(f"Database: {db_name}")
            logger.info(f"Collection: sensor_readings (will be created automatically on first insert)")
            
            # Create index on timestamp for better query performance
            # MongoDB will create the collection automatically if it doesn't exist
            try:
                await cls.database.sensor_readings.create_index("timestamp")
                logger.info(f"Index on 'timestamp' field ready (collection will be created on first insert)")
            except Exception as index_error:
                # Index creation might fail if collection doesn't exist yet, which is fine
                logger.debug(f"Index creation note: {str(index_error)}")
        except Exception as e:
            logger.error(f"Failed to verify MongoDB connection: {str(e)}")
            raise

    @classmethod
    async def disconnect(cls):
        """Disconnect from MongoDB"""
        if cls.client:
            cls.client.close()
            print("Disconnected from MongoDB")

    @classmethod
    async def insert_sensor_data(cls, data: SensorDataInput) -> str:
        """Insert sensor data into MongoDB"""
        if cls.database is None:
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
        if cls.database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        
        try:
            cursor = cls.database.sensor_readings.find().sort("timestamp", -1)
            documents = await cursor.to_list(length=None)
            
            results = []
            for doc in documents:
                try:
                    # Convert ObjectId to string - Pydantic will handle _id -> id mapping via alias
                    if "_id" in doc:
                        doc["_id"] = str(doc["_id"])
                    # Use constructor which respects populate_by_name=True
                    results.append(SensorDataOutput(**doc))
                except Exception as e:
                    logger.error(f"Error validating document: {str(e)}, doc: {doc}", exc_info=True)
                    raise
            
            return results
        except Exception as e:
            logger.error(f"Error in get_all_sensor_data: {str(e)}", exc_info=True)
            raise

    @classmethod
    async def clear_all_data(cls) -> int:
        """Clear all sensor data (for testing)"""
        if cls.database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        
        result = await cls.database.sensor_readings.delete_many({})
        return result.deleted_count

    @classmethod
    async def get_database_info(cls) -> dict:
        """Get information about the database and collection"""
        if cls.database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        
        try:
            # Get collection stats
            stats = await cls.database.command("collStats", "sensor_readings")
            collection_count = await cls.database.sensor_readings.count_documents({})
            
            return {
                "database_name": cls.database.name,
                "collection_name": "sensor_readings",
                "document_count": collection_count,
                "exists": collection_count > 0 or stats.get("size", 0) > 0,
                "indexes": await cls.database.sensor_readings.list_indexes().to_list(length=None)
            }
        except Exception as e:
            # Collection might not exist yet
            logger.warning(f"Could not get database info (collection may not exist yet): {str(e)}")
            return {
                "database_name": cls.database.name,
                "collection_name": "sensor_readings",
                "document_count": 0,
                "exists": False,
                "indexes": []
            }

