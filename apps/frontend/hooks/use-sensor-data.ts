"use client";

import { useState, useEffect, useCallback } from "react";
import { SensorData } from "@/types/sensor";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://your-backend.vercel.app";

export function useSensorData() {
  const [data, setData] = useState<SensorData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_URL}/api/sensors_data`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch sensor data: ${response.statusText}`);
      }
      
      const sensorData: SensorData[] = await response.json();
      setData(sensorData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch sensor data");
      console.error("Error fetching sensor data:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    
    // Poll every 30 seconds
    const interval = setInterval(fetchData, 30000);
    
    return () => clearInterval(interval);
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

