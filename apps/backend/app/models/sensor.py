from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Accelerometer(BaseModel):
    x: float
    y: float
    z: float


class Gyroscope(BaseModel):
    x: float
    y: float
    z: float


class SensorDataInput(BaseModel):
    """Input model matching embedded system JSON format exactly"""
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Humidity percentage")
    voc: int = Field(..., ge=0, description="VOC index (uint32)")
    light: int = Field(..., ge=0, le=4095, description="Light sensor value (0-4095)")
    sound: int = Field(..., ge=0, le=4095, description="Sound sensor value (0-4095)")
    accelerometer: Accelerometer
    gyroscope: Gyroscope


class SensorDataOutput(BaseModel):
    """Output model with timestamp"""
    id: Optional[str] = Field(None, alias="_id")
    timestamp: datetime
    temperature: float
    humidity: float
    voc: int
    light: int
    sound: int
    accelerometer: Accelerometer
    gyroscope: Gyroscope

    class Config:
        populate_by_name = True

