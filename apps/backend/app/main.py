import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.database.mongodb import MongoDB
from app.routes import sensors, test_data

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup
    await MongoDB.connect()
    yield
    # Shutdown
    await MongoDB.disconnect()


app = FastAPI(
    title="Embedded Statistics Tracking API",
    description="API for receiving and serving sensor data from embedded FreeRTOS system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sensors.router)
app.include_router(test_data.router)


@app.get("/")
async def root():
    return {
        "message": "Embedded Statistics Tracking API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/send_data": "Receive sensor data from embedded system",
            "GET /api/sensors_data": "Get all sensor data",
            "POST /api/seed_test_data": "Generate test data (for development)"
        }
    }

