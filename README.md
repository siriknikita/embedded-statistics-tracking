# Embedded Statistics Tracking

A monorepo application for tracking and visualizing sensor data from an embedded FreeRTOS system. The project consists of a Next.js frontend and a FastAPI backend, both deployable separately to Vercel.

## Project Structure

```
embedded-statistics-tracking/
├── apps/
│   ├── frontend/          # Next.js 14+ application
│   └── backend/           # FastAPI application
├── docs/
│   └── diagrams/          # System architecture and flow diagrams
├── package.json           # Root workspace configuration
└── pnpm-workspace.yaml    # Workspace configuration
```

## Features

- **Real-time Sensor Monitoring**: Display current values from embedded sensors
- **Historical Data Visualization**: Time-series charts using Recharts
- **RESTful API**: FastAPI backend with MongoDB storage
- **Test Data Generation**: Endpoint to seed test data matching exact sensor format
- **Modern UI**: Built with Next.js, Tailwind CSS, and shadcn/ui

## System Architecture

This section provides comprehensive visual documentation of the system architecture, communication flows, data processing, and API endpoints.

### Architecture Overview

The system consists of three main components: an Embedded System (Raspberry Pi Pico W), a Backend API (FastAPI), and a Frontend (Next.js). The embedded system collects sensor data and transmits it to the backend, which stores it in MongoDB. The frontend retrieves and visualizes this data for users.

![System Architecture](docs/diagrams/architecture-diagram.png)

### Communication Flow

The following sequence diagram illustrates the end-to-end communication between all system components, including initialization, sensor reading, data transmission, and frontend polling mechanisms.

![Communication Diagram](docs/diagrams/communication-daigram.png)

### Data Flow

This diagram shows the step-by-step data transformation from raw sensor readings to displayed visualizations, highlighting key technologies and data formats at each stage.

![Data Flow Diagram](docs/diagrams/data-flow-diagram.png)

### API Endpoints Summary

A concise overview of all API endpoints, their purposes, and how they interact with the MongoDB database.

![Endpoints Summary](docs/diagrams/edpoints-summary.png)

## Prerequisites

- Node.js 18+ and pnpm/npm
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) for Python package management
- MongoDB database (connection string required)

## Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd apps/backend
```

2. Install dependencies using `uv`:
```bash
uv sync
```

3. Create a `.env` file:
```bash
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=embedded-statistics-tracking-dev
```

4. Run the development server:
```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd apps/frontend
```

2. Install dependencies:
```bash
npm install
# or
pnpm install
```

3. Create a `.env.local` file:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Run the development server:
```bash
npm run dev
# or
pnpm dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### POST `/api/send_data`
Receive sensor data from the embedded system.

**Request Body:**
```json
{
  "temperature": 22.5,
  "humidity": 50.0,
  "voc": 150,
  "light": 2048,
  "sound": 1024,
  "accelerometer": {"x": 0.1, "y": 0.2, "z": 9.8},
  "gyroscope": {"x": 0.01, "y": 0.02, "z": 0.03}
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Sensor data stored successfully",
  "id": "507f1f77bcf86cd799439011"
}
```

### GET `/api/sensors_data`
Get all sensor data from MongoDB.

**Response:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "timestamp": "2024-01-01T12:00:00Z",
    "temperature": 22.5,
    "humidity": 50.0,
    "voc": 150,
    "light": 2048,
    "sound": 1024,
    "accelerometer": {"x": 0.1, "y": 0.2, "z": 9.8},
    "gyroscope": {"x": 0.01, "y": 0.02, "z": 0.03}
  }
]
```

### POST `/api/seed_test_data`
Generate and insert test sensor data for development/testing.

**Query Parameters:**
- `hours` (optional): Number of hours of historical data (default: 24)
- `interval_minutes` (optional): Interval between data points in minutes (default: 5)

**Example:**
```bash
curl -X POST "http://localhost:8000/api/seed_test_data?hours=24&interval_minutes=5"
```

## Deployment

### Backend Deployment (Vercel)

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Navigate to backend directory:
```bash
cd apps/backend
```

3. Deploy:
```bash
vercel
```

4. Set environment variables in Vercel dashboard:
   - `MONGODB_URL`
   - `MONGODB_DB_NAME`

### Frontend Deployment (Vercel)

1. Navigate to frontend directory:
```bash
cd apps/frontend
```

2. Deploy:
```bash
vercel
```

3. Set environment variable in Vercel dashboard:
   - `NEXT_PUBLIC_API_URL` (your backend URL)

## Embedded System Integration

Update the embedded system code (`personal-project.c`) with your backend URL:

```c
static const char API_HOST[] = "your-backend.vercel.app";
static const char API_PATH[] = "/api/send_data";
```

## Development

### Running Both Services

From the root directory:

```bash
# Terminal 1 - Backend
cd apps/backend && uv run uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd apps/frontend && npm run dev
```

### Testing with Test Data

1. Start the backend server
2. Seed test data:
```bash
curl -X POST "http://localhost:8000/api/seed_test_data?hours=24&interval_minutes=5"
```
3. View data in the frontend dashboard

## Technologies

### Backend
- FastAPI
- Motor (async MongoDB driver)
- Pydantic
- Python 3.11+

### Frontend
- Next.js 14+ (App Router)
- React 19
- TypeScript
- Tailwind CSS
- shadcn/ui
- Recharts

## License

This project is part of the embedded systems course at Lviv National University of Ivan Franko.
