import random
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Query
from app.models.sensor import SensorDataInput, Accelerometer, Gyroscope
from app.database.mongodb import MongoDB
from typing import Dict

router = APIRouter(prefix="/api", tags=["test-data"])


def generate_test_sensor_data(base_time: datetime, variation: float = 0.1) -> SensorDataInput:
    """
    Generate realistic test sensor data matching exact embedded system format.
    Values are realistic and have slight variations.
    """
    # Temperature: 18-25°C with small random variation
    temp = round(random.uniform(20.0, 23.0) + random.uniform(-variation, variation), 2)
    
    # Humidity: 40-60% with small random variation
    hum = round(random.uniform(45.0, 55.0) + random.uniform(-variation, variation), 2)
    
    # VOC: 0-500 (typical range)
    voc = random.randint(0, 500)
    
    # Light: 0-4095 (ADC range)
    light = random.randint(100, 3000)
    
    # Sound: 0-4095 (ADC range)
    sound = random.randint(50, 2000)
    
    # Accelerometer: small variations around gravity (9.8 m/s²) or near zero
    acc_x = round(random.uniform(-0.5, 0.5), 2)
    acc_y = round(random.uniform(-0.5, 0.5), 2)
    acc_z = round(random.uniform(9.5, 10.0), 2)  # Z typically shows gravity
    
    # Gyroscope: small angular velocity variations
    gyro_x = round(random.uniform(-0.1, 0.1), 2)
    gyro_y = round(random.uniform(-0.1, 0.1), 2)
    gyro_z = round(random.uniform(-0.1, 0.1), 2)
    
    return SensorDataInput(
        temperature=temp,
        humidity=hum,
        voc=voc,
        light=light,
        sound=sound,
        accelerometer=Accelerometer(x=acc_x, y=acc_y, z=acc_z),
        gyroscope=Gyroscope(x=gyro_x, y=gyro_y, z=gyro_z)
    )


@router.post("/generate_random_data")
async def generate_random_data() -> Dict:
    """
    Generate a single random sensor reading and store it in the database.
    Useful for testing and demonstration purposes.
    
    Returns:
        Dictionary with status and the inserted record ID
    """
    try:
        # Generate a single random sensor reading with current timestamp
        test_data = generate_test_sensor_data(datetime.utcnow())
        
        # Insert into database using the standard insert method
        record_id = await MongoDB.insert_sensor_data(test_data)
        
        return {
            "status": "success",
            "message": "Random sensor data generated and stored successfully",
            "id": record_id,
            "data": {
                "temperature": test_data.temperature,
                "humidity": test_data.humidity,
                "voc": test_data.voc,
                "light": test_data.light,
                "sound": test_data.sound,
                "accelerometer": {
                    "x": test_data.accelerometer.x,
                    "y": test_data.accelerometer.y,
                    "z": test_data.accelerometer.z,
                },
                "gyroscope": {
                    "x": test_data.gyroscope.x,
                    "y": test_data.gyroscope.y,
                    "z": test_data.gyroscope.z,
                },
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate random data: {str(e)}")


@router.post("/seed_test_data")
async def seed_test_data(
    hours: int = Query(24, ge=1, le=168, description="Number of hours of historical data"),
    interval_minutes: int = Query(5, ge=1, le=60, description="Interval between data points in minutes")
) -> Dict:
    """
    Generate and insert test sensor data matching exact embedded system format.
    
    Args:
        hours: Number of hours of historical data to generate (default: 24)
        interval_minutes: Interval between data points in minutes (default: 5)
    
    Returns:
        Dictionary with count of inserted records
    """
    try:
        # Calculate number of records to generate
        num_records = (hours * 60) // interval_minutes
        
        if num_records > 10000:
            raise HTTPException(
                status_code=400,
                detail=f"Too many records requested ({num_records}). Maximum is 10000."
            )
        
        # Generate data points going back in time
        now = datetime.utcnow()
        inserted_count = 0
        
        for i in range(num_records):
            # Calculate timestamp (going back in time)
            timestamp_offset = timedelta(minutes=interval_minutes * (num_records - i - 1))
            record_time = now - timestamp_offset
            
            # Generate test data
            test_data = generate_test_sensor_data(record_time)
            
            # Insert into database with custom timestamp
            document = {
                "timestamp": record_time,
                "temperature": test_data.temperature,
                "humidity": test_data.humidity,
                "voc": test_data.voc,
                "light": test_data.light,
                "sound": test_data.sound,
                "accelerometer": {
                    "x": test_data.accelerometer.x,
                    "y": test_data.accelerometer.y,
                    "z": test_data.accelerometer.z,
                },
                "gyroscope": {
                    "x": test_data.gyroscope.x,
                    "y": test_data.gyroscope.y,
                    "z": test_data.gyroscope.z,
                },
            }
            
            await MongoDB.database.sensor_readings.insert_one(document)
            inserted_count += 1
        
        return {
            "status": "success",
            "message": f"Generated and inserted {inserted_count} test records",
            "records_inserted": inserted_count,
            "hours": hours,
            "interval_minutes": interval_minutes
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to seed test data: {str(e)}")

