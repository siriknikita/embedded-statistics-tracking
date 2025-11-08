# Backend - Embedded Statistics Tracking API

FastAPI backend for receiving and serving sensor data from embedded FreeRTOS systems.

## Local Development

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- MongoDB connection string

### Setup

1. **Install dependencies:**
```bash
uv sync
```

2. **Create `.env` file:**
```bash
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=embedded-statistics-tracking-dev
```

3. **Run the server:**

Using uv:
```bash
uv run uvicorn app.main:app --reload
```

Using the start script:
```bash
./start.sh
```

Using the installed script (after `uv sync`):
```bash
uv run start
```

The API will be available at `http://localhost:8000`

## Vercel Deployment

### Environment Variables

Set these in your Vercel project settings:
- `MONGODB_URL` - Your MongoDB connection string
- `MONGODB_DB_NAME` - Database name (default: `embedded-statistics-tracking-dev`)

### Deployment Steps

1. **Install Vercel CLI:**
```bash
npm i -g vercel
```

2. **Navigate to backend directory:**
```bash
cd apps/backend
```

3. **Deploy:**
```bash
vercel
```

4. **Set environment variables in Vercel dashboard:**
   - Go to your project settings
   - Add `MONGODB_URL` and `MONGODB_DB_NAME`

### Vercel Configuration

The `vercel.json` file is configured to:
- Use `@vercel/python` runtime
- Route all requests to `api/index.py`
- The FastAPI app is automatically detected and handled

### Important Notes

- Vercel uses serverless functions, so the app will be deployed as a serverless function
- The `requirements.txt` file is used by Vercel to install dependencies
- The `api/index.py` file is the entry point for Vercel
- MongoDB connection is established on each function invocation (connection pooling is handled by Motor)

## API Endpoints

- `POST /api/send_data` - Receive sensor data from embedded system
- `GET /api/sensors_data` - Get all sensor data
- `POST /api/seed_test_data` - Generate test data (for development)

See the main README.md for detailed API documentation.

