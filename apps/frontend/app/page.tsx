"use client";

import { useState } from "react";
import { useSensorData } from "@/hooks/use-sensor-data";
import { SensorCards } from "@/components/dashboard/SensorCards";
import { SensorCharts } from "@/components/dashboard/SensorCharts";
import { Button } from "@/components/ui/button";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://your-backend.vercel.app";

export default function Home() {
  const { data, loading, error, refetch } = useSensorData();
  const [generating, setGenerating] = useState(false);

  const handleGenerateRandomData = async () => {
    setGenerating(true);
    try {
      const response = await fetch(`${API_URL}/api/generate_random_data`, {
        method: "POST",
      });
      
      if (!response.ok) {
        throw new Error(`Failed to generate random data: ${response.statusText}`);
      }
      
      // Refresh the sensor data after generating
      await refetch();
    } catch (err) {
      console.error("Error generating random data:", err);
      alert(err instanceof Error ? err.message : "Failed to generate random data");
    } finally {
      setGenerating(false);
    }
  };

  const latestData = data.length > 0 ? data[0] : null;

  return (
    <main className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-16 md:py-24">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6 leading-tight">
            Embedded Statistics
            <br />
            <span className="text-primary">Tracking Dashboard</span>
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground mb-8 max-w-2xl mx-auto leading-relaxed">
            Real-time monitoring of sensor data from embedded FreeRTOS system
          </p>
          <Button 
            onClick={handleGenerateRandomData} 
            disabled={generating || loading}
            size="lg"
            className="mt-4"
          >
            {generating ? "Generating..." : "Generate Random Sensor Data"}
          </Button>
        </div>

        {/* Error State */}
        {error && (
          <div className="mb-8 p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
            <p className="text-destructive">Error: {error}</p>
          </div>
        )}

        {/* Loading State */}
        {loading && data.length === 0 && (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Loading sensor data...</p>
          </div>
        )}

        {/* Real-time Cards */}
        <section id="current-values" className="mb-16">
          <div className="text-center mb-8">
            <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
              Current Values
            </h2>
            <p className="text-muted-foreground text-base md:text-lg max-w-2xl mx-auto">
              Latest sensor readings
            </p>
          </div>
          <SensorCards latestData={latestData} />
        </section>

        {/* Historical Charts */}
        <section id="historical-data">
          <div className="text-center mb-8">
            <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
              Historical Data
            </h2>
            <p className="text-muted-foreground text-base md:text-lg max-w-2xl mx-auto">
              Time-series visualization of sensor data
            </p>
          </div>
          <SensorCharts data={data} />
        </section>
      </div>
    </main>
  );
}
