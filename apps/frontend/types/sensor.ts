export interface Accelerometer {
  x: number;
  y: number;
  z: number;
}

export interface Gyroscope {
  x: number;
  y: number;
  z: number;
}

export interface SensorData {
  id?: string;
  timestamp: string;
  temperature: number;
  humidity: number;
  voc: number;
  light: number;
  sound: number;
  accelerometer: Accelerometer;
  gyroscope: Gyroscope;
}

