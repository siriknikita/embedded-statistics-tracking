"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { SensorData } from "@/types/sensor";
import { Thermometer, Droplets, Wind, Sun, Volume2, Gauge } from "lucide-react";

interface SensorCardsProps {
  latestData: SensorData | null;
}

export function SensorCards({ latestData }: SensorCardsProps) {
  if (!latestData) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {[1, 2, 3, 4, 5].map((i) => (
          <Card key={i} className="h-full">
            <CardHeader>
              <CardTitle className="text-xl">Loading...</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">--</div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <Card className="h-full transition-shadow hover:shadow-lg">
        <CardHeader>
          <CardTitle className="text-xl flex items-center gap-2">
            <Thermometer className="h-5 w-5" />
            Temperature
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold">{latestData.temperature.toFixed(2)}°C</div>
        </CardContent>
      </Card>

      <Card className="h-full transition-shadow hover:shadow-lg">
        <CardHeader>
          <CardTitle className="text-xl flex items-center gap-2">
            <Droplets className="h-5 w-5" />
            Humidity
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold">{latestData.humidity.toFixed(2)}%</div>
        </CardContent>
      </Card>

      <Card className="h-full transition-shadow hover:shadow-lg">
        <CardHeader>
          <CardTitle className="text-xl flex items-center gap-2">
            <Wind className="h-5 w-5" />
            VOC Index
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold">{latestData.voc}</div>
        </CardContent>
      </Card>

      <Card className="h-full transition-shadow hover:shadow-lg">
        <CardHeader>
          <CardTitle className="text-xl flex items-center gap-2">
            <Sun className="h-5 w-5" />
            Light
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold">{latestData.light}</div>
          <div className="text-sm text-muted-foreground mt-1">0-4095 range</div>
        </CardContent>
      </Card>

      <Card className="h-full transition-shadow hover:shadow-lg">
        <CardHeader>
          <CardTitle className="text-xl flex items-center gap-2">
            <Volume2 className="h-5 w-5" />
            Sound
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold">{latestData.sound}</div>
          <div className="text-sm text-muted-foreground mt-1">0-4095 range</div>
        </CardContent>
      </Card>

      <Card className="h-full transition-shadow hover:shadow-lg">
        <CardHeader>
          <CardTitle className="text-xl flex items-center gap-2">
            <Gauge className="h-5 w-5" />
            Accelerometer
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-muted-foreground">X:</span>
              <span className="font-semibold">{latestData.accelerometer.x.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Y:</span>
              <span className="font-semibold">{latestData.accelerometer.y.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Z:</span>
              <span className="font-semibold">{latestData.accelerometer.z.toFixed(2)}</span>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="h-full transition-shadow hover:shadow-lg sm:col-span-2 lg:col-span-1">
        <CardHeader>
          <CardTitle className="text-xl flex items-center gap-2">
            <Gauge className="h-5 w-5" />
            Gyroscope
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-muted-foreground">X:</span>
              <span className="font-semibold">{latestData.gyroscope.x.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Y:</span>
              <span className="font-semibold">{latestData.gyroscope.y.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Z:</span>
              <span className="font-semibold">{latestData.gyroscope.z.toFixed(2)}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

