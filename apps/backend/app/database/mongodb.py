import os
import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from datetime import datetime
from app.models.sensor import SensorDataInput, SensorDataOutput

logger = logging.getLogger(__name__)


class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database = None
    _connection_lock = asyncio.Lock()

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
            
            # Ensure collection exists (this also ensures the database exists)
            # MongoDB creates databases and collections lazily, but we'll ensure the collection
            # exists explicitly so we can create indexes reliably
            collection_name = "sensor_readings"
            
            # Check if collection exists
            collections = await cls.database.list_collection_names()
            if collection_name not in collections:
                logger.info(f"Collection '{collection_name}' does not exist. Creating it...")
                # Create collection by inserting a dummy document and immediately deleting it
                # This ensures both the database and collection are created
                dummy_doc = {"_dummy": True, "created_at": datetime.utcnow()}
                result = await cls.database[collection_name].insert_one(dummy_doc)
                await cls.database[collection_name].delete_one({"_id": result.inserted_id})
                logger.info(f"Collection '{collection_name}' and database '{db_name}' created successfully")
            else:
                logger.info(f"Collection '{collection_name}' already exists in database '{db_name}'")
            
            # Create index on timestamp for better query performance
            # This will work now that we've ensured the collection exists
            try:
                await cls.database[collection_name].create_index("timestamp")
                logger.info(f"Index on 'timestamp' field created/verified")
            except Exception as index_error:
                logger.warning(f"Could not create index on 'timestamp': {str(index_error)}")
                
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
    async def ensure_connected(cls):
        """Ensure database is connected. Connect if not already connected.
        This is especially important for serverless environments where the lifespan
        context manager may not run reliably.
        
        Uses asyncio.Lock() to prevent race conditions when multiple concurrent
        tasks try to connect simultaneously."""
        # Fast path: if already connected, return immediately
        if cls.database is not None:
            return
        
        # Acquire lock to ensure only one connection attempt at a time
        async with cls._connection_lock:
            # Double-check after acquiring lock (another task might have connected)
            if cls.database is None:
                logger.info("Database not connected. Connecting now...")
                await cls.connect()

    @classmethod
    async def insert_sensor_data(cls, data: SensorDataInput) -> str:
        """Insert sensor data into MongoDB"""
        await cls.ensure_connected()
        
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
        await cls.ensure_connected()
        
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
        await cls.ensure_connected()
        
        result = await cls.database.sensor_readings.delete_many({})
        return result.deleted_count

    @classmethod
    async def get_database_info(cls) -> dict:
        """Get information about the database and collection"""
        await cls.ensure_connected()
        
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

