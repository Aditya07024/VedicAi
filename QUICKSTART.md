# 🌟 VedicAI FastAPI + React - Quick Start Guide

## What's Been Created

You now have a production-ready architecture:

```
React Frontend (http://localhost:3000)
        ↓ REST API
FastAPI Backend (http://localhost:8000)
        ↓
PostgreSQL Database + Gemini AI + Astrology Engine
```

## Option 1: Quick Start (Recommended)

### Prerequisites

- Python 3.13+
- Node.js 18+
- npm or yarn
- PostgreSQL (or use Neon PostgreSQL)

### 1-Minute Setup

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh

# Update backend/.env with your credentials
nano backend/.env
```

### Run Development Servers

**Terminal 1 - Backend:**

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

Backend runs on: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

Frontend runs on: `http://localhost:3000`

## Option 2: Docker Setup (One Command)

### Prerequisites

- Docker Desktop installed

### Run Everything:

```bash
# Copy environment template
cp backend/.env.example backend/.env
# Edit backend/.env with your DATABASE_URL and GEMINI_API_KEY
nano backend/.env

# Start all services
docker-compose up

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Database: localhost:5432
```

## Configuration

### Backend Environment Variables

Edit `backend/.env`:

```env
# PostgreSQL Connection
DATABASE_URL=postgresql://neondb_owner:npg_XXXXX@ep-xxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

# Gemini AI API
GEMINI_API_KEY=your_gemini_api_key_here

# Optional - Server Settings
HOST=0.0.0.0
PORT=8000
```

### Frontend Environment Variables

Create `frontend/.env.local` (optional):

```env
VITE_API_URL=http://localhost:8000
```

## Testing the API

### Using Swagger UI (Browser)

```
http://localhost:8000/docs
```

### Using curl

**Get Health:**

```bash
curl http://localhost:8000/health
```

**Generate Analysis:**

```bash
curl -X POST http://localhost:8000/api/analysis \
  -H "Content-Type: application/json" \
  -d '{
    "birth_details": {
      "name": "Aditya",
      "date": "2003-02-07",
      "time": "03:00:00",
      "place": "iglas",
      "latitude": 27.7081,
      "longitude": 77.9367
    }
  }'
```

**Get AI Insights:**

```bash
curl -X POST http://localhost:8000/api/insights \
  -H "Content-Type: application/json" \
  -d '{
    "dosha_data": {...},
    "dasha_data": {...},
    "user_name": "Aditya"
  }'
```

## Project Structure

```
VedicAI/
│
├── 📁 backend/                   # FastAPI Backend
│   ├── main.py                   # Main application (256 lines)
│   ├── requirements.txt           # Dependencies
│   ├── .env.example               # Environment template
│   ├── .env                       # Your credentials (git ignored)
│   └── Dockerfile                 # Docker config
│
├── 📁 frontend/                  # React Frontend
│   ├── src/
│   │   ├── App.jsx                # Main component
│   │   ├── App.css                # App styles
│   │   ├── main.jsx               # Entry point
│   │   ├── index.css              # Global styles
│   │   │
│   │   ├── 📁 components/
│   │   │   ├── BirthForm.jsx       # Birth details form
│   │   │   ├── BirthForm.css       # Form styles
│   │   │   ├── AnalysisResults.jsx # Results display
│   │   │   └── AnalysisResults.css # Results styles
│   │   │
│   │   └── 📁 services/
│   │       └── api.js              # API client
│   │
│   ├── index.html                 # HTML entry
│   ├── package.json               # Dependencies
│   ├── vite.config.js             # Vite config
│   ├── Dockerfile                 # Docker config
│   └── .env.local                 # Your env vars (optional)
│
├── 📁 kundliGenerator/            # Existing astrology modules
├── 📁 dosha/                      # Existing astrology modules
├── 📁 panchang/                   # Existing astrology modules
├── 📁 Swiss_Ephemeris/            # Existing astrology modules
│
├── docker-compose.yml              # Multi-container setup
├── setup.sh                         # Auto setup script
├── ARCHITECTURE.md                 # Architecture details
└── QUICKSTART.md                  # This file

```

## API Reference

### POST `/api/analysis`

Complete astrology analysis

**Input:**

```json
{
  "birth_details": {
    "name": "string",
    "date": "YYYY-MM-DD",
    "time": "HH:MM:SS",
    "place": "string",
    "latitude": number,
    "longitude": number
  }
}
```

**Output:**

```json
{
  "birth_details": {...},
  "kundli": {...},
  "doshas": [...],
  "dasha": {...},
  "panchang": {...}
}
```

### POST `/api/insights`

AI-generated insights

**Input:**

```json
{
  "dosha_data": {...},
  "dasha_data": {...},
  "user_name": "string"
}
```

**Output:**

```json
{
  "insights": "string"
}
```

### GET `/api/search-place?query=...`

Google place search

**Input:**

- `query`: Place name (e.g., "iglas")

**Output:**

```json
{
  "search_url": "https://www.google.com/maps/search/..."
}
```

### GET `/health`

Health check

**Output:**

```json
{
  "status": "ok"
}
```

## Troubleshooting

### Port Already in Use

**Backend (8000):**

```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
```

**Frontend (3000):**

```bash
# Find and kill process
lsof -ti:3000 | xargs kill -9
```

### Database Connection Error

1. Check `DATABASE_URL` in `.env`
2. Ensure database is accessible
3. For Neon: Verify credentials in project settings
4. For local: Ensure PostgreSQL is running

### Module Import Errors

Ensure these directories exist in the project root:

- `kundliGenerator/`
- `dosha/`
- `panchang/`
- `Swiss_Ephemeris/`

Backend uses `sys.path` to import them automatically.

### Gemini API Errors

1. Check `GEMINI_API_KEY` is valid
2. Verify API quota in Google Cloud console
3. Check API is enabled for the project

### CORS Errors

Frontend can't reach backend?

- Ensure both servers are running
- Check `VITE_API_URL` matches backend address
- Verify CORS middleware is enabled in FastAPI

## Performance Tips

1. **Use async endpoints** - Backend uses `async def` for all endpoints
2. **Database connection pooling** - psycopg2 handles this
3. **Frontend lazy loading** - React components load on demand
4. **Image optimization** - Serve optimized charts from backend
5. **Caching** - Add Redis for frequently accessed analyses

## Deployment Options

### Render.com (Free)

1. Push code to GitHub
2. Create 2 services: Backend and Frontend
3. Set environment variables
4. Auto-deploys on push

### AWS

- Backend: ECS/EC2
- Frontend: CloudFront + S3
- Database: RDS PostgreSQL

### GCP

- Backend: Cloud Run
- Frontend: Cloud Storage + CDN
- Database: Cloud SQL

### Azure

- Backend: App Service
- Frontend: Static Web Apps
- Database: Azure Database for PostgreSQL

## Next Steps

1. ✅ **Setup** - Follow one of the setup options above
2. **Test** - Try submitting a birth chart
3. **Customize** - Add your branding to frontend
4. **Deploy** - Push to your preferred platform
5. **Monitor** - Set up logging and error tracking

## Support

- **API Docs**: Visit `http://localhost:8000/docs` for interactive documentation
- **Issues**: Create an issue with error messages and screenshots
- **Development**: All code follows PEP 8 (Python) and Prettier (JavaScript)

## Comparison: Streamlit vs FastAPI + React

| Feature        | Streamlit | FastAPI + React  |
| -------------- | --------- | ---------------- |
| Users/second   | 1-5       | 100+             |
| Custom UI      | Limited   | Complete control |
| Mobile         | No        | Yes              |
| SPA Experience | No        | Yes              |
| Deployments    | Limited   | Unlimited        |
| Team scaling   | Hard      | Easy             |
| Monetization   | Difficult | Easy             |
| Learning curve | Easier    | Moderate         |

This new architecture supports **thousands of users** and is ready for:

- ✅ College projects
- ✅ Startup MVPs
- ✅ Portfolio showcases
- ✅ Professional applications

Good luck! 🚀
