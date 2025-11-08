"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { SensorData } from "@/types/sensor";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ComposedChart,
} from "recharts";

interface SensorChartsProps {
  data: SensorData[];
}

export function SensorCharts({ data }: SensorChartsProps) {
  // Transform data for charts (reverse to show oldest first)
  const chartData = [...data].reverse().map((item) => ({
    time: new Date(item.timestamp).toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    }),
    timestamp: new Date(item.timestamp).getTime(),
    temperature: item.temperature,
    humidity: item.humidity,
    voc: item.voc,
    light: item.light,
    sound: item.sound,
    accX: item.accelerometer.x,
    accY: item.accelerometer.y,
    accZ: item.accelerometer.z,
    gyroX: item.gyroscope.x,
    gyroY: item.gyroscope.y,
    gyroZ: item.gyroscope.z,
  }));

  if (data.length === 0) {
    return (
      <div className="text-center py-12 text-muted-foreground">
        No sensor data available. Data will appear here once sensors start sending data.
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Temperature & Humidity */}
      <Card className="transition-shadow hover:shadow-lg">
        <CardHeader>
          <CardTitle className="text-2xl">Temperature & Humidity</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <ComposedChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="time"
                tick={{ fontSize: 12 }}
                interval="preserveStartEnd"
              />
              <YAxis yAxisId="left" label={{ value: "Temperature (°C)", angle: -90, position: "insideLeft" }} />
              <YAxis yAxisId="right" orientation="right" label={{ value: "Humidity (%)", angle: 90, position: "insideRight" }} />
              <Tooltip />
              <Legend />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="temperature"
                stroke="#8884d8"
                strokeWidth={2}
                name="Temperature (°C)"
                dot={false}
              />
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="humidity"
                stroke="#82ca9d"
                strokeWidth={2}
                name="Humidity (%)"
                dot={false}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* VOC, Light, Sound */}
      <Card className="transition-shadow hover:shadow-lg">
        <CardHeader>
          <CardTitle className="text-2xl">VOC, Light & Sound</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="time"
                tick={{ fontSize: 12 }}
                interval="preserveStartEnd"
              />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="voc"
                stroke="#ff7300"
                strokeWidth={2}
                name="VOC Index"
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="light"
                stroke="#ffc658"
                strokeWidth={2}
                name="Light (0-4095)"
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="sound"
                stroke="#00ff00"
                strokeWidth={2}
                name="Sound (0-4095)"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Accelerometer */}
      <Card className="transition-shadow hover:shadow-lg">
        <CardHeader>
          <CardTitle className="text-2xl">Accelerometer</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="time"
                tick={{ fontSize: 12 }}
                interval="preserveStartEnd"
              />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="accX"
                stroke="#ff0000"
                strokeWidth={2}
                name="X (m/s²)"
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="accY"
                stroke="#00ff00"
                strokeWidth={2}
                name="Y (m/s²)"
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="accZ"
                stroke="#0000ff"
                strokeWidth={2}
                name="Z (m/s²)"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Gyroscope */}
      <Card className="transition-shadow hover:shadow-lg">
        <CardHeader>
          <CardTitle className="text-2xl">Gyroscope</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="time"
                tick={{ fontSize: 12 }}
                interval="preserveStartEnd"
              />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="gyroX"
                stroke="#ef4444"
                strokeWidth={2}
                name="X (rad/s)"
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="gyroY"
                stroke="#22c55e"
                strokeWidth={2}
                name="Y (rad/s)"
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="gyroZ"
                stroke="#3b82f6"
                strokeWidth={2}
                name="Z (rad/s)"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}

