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
    _connection_lock: Optional[asyncio.Lock] = None
    _lock_loop_id: Optional[int] = None
    _client_loop_id: Optional[int] = None

    @classmethod
    async def _get_connection_lock(cls) -> asyncio.Lock:
        """Get or create the connection lock, ensuring it's created in the current event loop.
        
        This method handles cases where the event loop might have been closed and recreated
        (common in serverless environments), by tracking the loop ID and recreating the lock
        if we're in a different event loop.
        """
        try:
            current_loop = asyncio.get_running_loop()
            current_loop_id = id(current_loop)
            
            # If we don't have a lock, or we're in a different event loop, create a new one
            if cls._connection_lock is None or cls._lock_loop_id != current_loop_id:
                cls._connection_lock = asyncio.Lock()
                cls._lock_loop_id = current_loop_id
        except RuntimeError as e:
            # No running loop - this should not happen in FastAPI async endpoints
            # If it does, we can't create a lock, so we'll raise an error
            logger.error(f"Cannot create connection lock: no running event loop. Error: {e}")
            raise RuntimeError("Cannot create connection lock: no running event loop") from e
        
        return cls._connection_lock

    @classmethod
    async def connect(cls):
        """Connect to MongoDB and verify connection"""
        mongodb_url = os.getenv("MONGODB_URL")
        db_name = os.getenv("MONGODB_DB_NAME", "embedded-statistics-tracking-dev")
        
        if not mongodb_url:
            raise ValueError("MONGODB_URL environment variable is not set")
        
        # Get current event loop ID
        try:
            current_loop = asyncio.get_running_loop()
            current_loop_id = id(current_loop)
        except RuntimeError:
            current_loop_id = None
        
        # Close existing client if it exists and we're in a different event loop
        if cls.client is not None and cls._client_loop_id != current_loop_id:
            try:
                cls.client.close()
            except Exception as e:
                logger.warning(f"Error closing old MongoDB client: {e}")
            cls.client = None
            cls.database = None
        
        cls.client = AsyncIOMotorClient(mongodb_url)
        cls.database = cls.client[db_name]
        cls._client_loop_id = current_loop_id
        
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
            try:
                cls.client.close()
                logger.info("Disconnected from MongoDB")
            except Exception as e:
                logger.warning(f"Error closing MongoDB client: {e}")
            finally:
                cls.client = None
                cls.database = None
                cls._connection_lock = None
                cls._lock_loop_id = None
                cls._client_loop_id = None

    @classmethod
    async def ensure_connected(cls):
        """Ensure database is connected. Connect if not already connected.
        This is especially important for serverless environments where the lifespan
        context manager may not run reliably.
        
        Uses asyncio.Lock() to prevent race conditions when multiple concurrent
        tasks try to connect simultaneously."""
        # Fast path: if already connected, check if we're still in a valid event loop
        if cls.database is not None and cls.client is not None:
            try:
                # Check if we're in a running event loop (required for async operations)
                current_loop = asyncio.get_running_loop()
                current_loop_id = id(current_loop)
                
                # Check if the event loop is closed
                if current_loop.is_closed():
                    logger.warning("Event loop is closed, will reconnect")
                    cls.client = None
                    cls.database = None
                    cls._client_loop_id = None
                # Check if we're in a different event loop than when the client was created
                elif cls._client_loop_id is not None and cls._client_loop_id != current_loop_id:
                    logger.info("Different event loop detected, will reconnect")
                    # Close old client
                    try:
                        cls.client.close()
                    except Exception as e:
                        logger.warning(f"Error closing old client: {e}")
                    cls.client = None
                    cls.database = None
                    cls._client_loop_id = None
                else:
                    # We're in the same event loop, client should be valid
                    return
            except RuntimeError:
                # No running event loop - this shouldn't happen in FastAPI async endpoints
                # but if it does, we need to reconnect
                logger.warning("No running event loop detected, will reconnect")
                cls.client = None
                cls.database = None
                cls._client_loop_id = None
        
        # Acquire lock to ensure only one connection attempt at a time
        lock = await cls._get_connection_lock()
        async with lock:
            # Double-check after acquiring lock (another task might have connected)
            if cls.database is None or cls.client is None:
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
        
        try:
            result = await cls.database.sensor_readings.insert_one(document)
            return str(result.inserted_id)
        except RuntimeError as e:
            # Catch "Event loop is closed" errors and retry with fresh connection
            if "Event loop is closed" in str(e) or "loop is closed" in str(e).lower():
                logger.warning("Event loop closed during operation, reconnecting and retrying...")
                cls.client = None
                cls.database = None
                cls._client_loop_id = None
                await cls.ensure_connected()
                result = await cls.database.sensor_readings.insert_one(document)
                return str(result.inserted_id)
            raise

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
        except RuntimeError as e:
            # Catch "Event loop is closed" errors and retry with fresh connection
            if "Event loop is closed" in str(e) or "loop is closed" in str(e).lower():
                logger.warning("Event loop closed during operation, reconnecting and retrying...")
                cls.client = None
                cls.database = None
                cls._client_loop_id = None
                await cls.ensure_connected()
                cursor = cls.database.sensor_readings.find().sort("timestamp", -1)
                documents = await cursor.to_list(length=None)
                
                results = []
                for doc in documents:
                    if "_id" in doc:
                        doc["_id"] = str(doc["_id"])
                    results.append(SensorDataOutput(**doc))
                
                return results
            raise
        except Exception as e:
            logger.error(f"Error in get_all_sensor_data: {str(e)}", exc_info=True)
            raise

    @classmethod
    async def clear_all_data(cls) -> int:
        """Clear all sensor data (for testing)"""
        await cls.ensure_connected()
        
        try:
            result = await cls.database.sensor_readings.delete_many({})
            return result.deleted_count
        except RuntimeError as e:
            # Catch "Event loop is closed" errors and retry with fresh connection
            if "Event loop is closed" in str(e) or "loop is closed" in str(e).lower():
                logger.warning("Event loop closed during operation, reconnecting and retrying...")
                cls.client = None
                cls.database = None
                cls._client_loop_id = None
                await cls.ensure_connected()
                result = await cls.database.sensor_readings.delete_many({})
                return result.deleted_count
            raise

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
        except RuntimeError as e:
            # Catch "Event loop is closed" errors and retry with fresh connection
            if "Event loop is closed" in str(e) or "loop is closed" in str(e).lower():
                logger.warning("Event loop closed during operation, reconnecting and retrying...")
                cls.client = None
                cls.database = None
                cls._client_loop_id = None
                await cls.ensure_connected()
                try:
                    stats = await cls.database.command("collStats", "sensor_readings")
                    collection_count = await cls.database.sensor_readings.count_documents({})
                    return {
                        "database_name": cls.database.name,
                        "collection_name": "sensor_readings",
                        "document_count": collection_count,
                        "exists": collection_count > 0 or stats.get("size", 0) > 0,
                        "indexes": await cls.database.sensor_readings.list_indexes().to_list(length=None)
                    }
                except Exception as retry_e:
                    logger.warning(f"Could not get database info after retry: {str(retry_e)}")
                    return {
                        "database_name": cls.database.name if cls.database else "unknown",
                        "collection_name": "sensor_readings",
                        "document_count": 0,
                        "exists": False,
                        "indexes": []
                    }
            raise
        except Exception as e:
            # Collection might not exist yet
            logger.warning(f"Could not get database info (collection may not exist yet): {str(e)}")
            return {
                "database_name": cls.database.name if cls.database else "unknown",
                "collection_name": "sensor_readings",
                "document_count": 0,
                "exists": False,
                "indexes": []
            }

