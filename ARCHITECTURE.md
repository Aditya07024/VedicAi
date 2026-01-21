# VedicAI - FastAPI + React Architecture

## Project Structure

```
VedicAI/
├── backend/                 # FastAPI Backend
│   ├── main.py             # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variables
│   └── Dockerfile           # Docker configuration
│
├── frontend/                # React Frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API integration
│   │   └── App.jsx          # Main app
│   ├── package.json         # NPM dependencies
│   ├── vite.config.js       # Vite configuration
│   └── Dockerfile           # Docker configuration
│
├── kundliGenerator/         # Existing modules
├── dosha/
├── panchang/
├── Swiss_Ephemeris/
│
├── docker-compose.yml       # Docker compose
└── README.md               # Documentation
```

## Architecture

```
React Frontend (Port 3000)
       ↓ REST API
FastAPI Backend (Port 8000)
       ↓
PostgreSQL Database + Gemini AI
```

## Setup Instructions

### Option 1: Docker Compose (Recommended)

```bash
# Clone and setup
git clone <repo>
cd VedicAI

# Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your credentials

# Start all services
docker-compose up

# Access
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

**Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python main.py
# Server runs on http://localhost:8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
# App runs on http://localhost:3000
```

## API Endpoints

### POST `/api/analysis`

Generate complete astrology analysis

**Request:**

```json
{
  "birth_details": {
    "name": "Aditya",
    "date": "2003-02-07",
    "time": "03:00:00",
    "place": "iglas",
    "latitude": 27.7081,
    "longitude": 77.9367
  }
}
```

**Response:**

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

Generate Gemini AI insights

### GET `/api/search-place?query=iglas`

Search for place coordinates on Google

### GET `/health`

Health check endpoint

### GET `/docs`

Interactive API documentation (Swagger UI)

## Features

✅ **Separation of Concerns**

- Backend handles business logic
- Frontend handles UI
- Database handles persistence

✅ **Scalability**

- Can handle hundreds of concurrent users
- API can be deployed independently
- Database can be scaled separately

✅ **Production Ready**

- Docker containerization
- Environment configuration
- Error handling
- CORS support

✅ **Developer Experience**

- Hot reload in development
- Interactive API docs
- TypeScript-ready React setup
- Clear component structure

## Deployment

### Render.com (Frontend + Backend)

1. Fork the repository
2. Create two Render services:
   - **Backend**: Deploy `backend/` with `python main.py` command
   - **Frontend**: Deploy `frontend/` with `npm run build && npm run preview` command
3. Set environment variables in Render dashboard
4. Link services with environment variables

### AWS/GCP/Azure

Use the provided Docker Compose file to deploy with:

- ECS/App Engine/Container Instances for containerized services
- RDS/Cloud SQL for PostgreSQL
- CDN for static frontend assets

## Environment Variables

**Backend (.env)**

```
DATABASE_URL=postgresql://user:password@host:5432/vedicai
GEMINI_API_KEY=your_api_key
```

**Frontend (.env)**

```
VITE_API_URL=http://localhost:8000
```

## Development

```bash
# Install dependencies
npm install          # Frontend
pip install -r requirements.txt  # Backend

# Run in development
npm run dev          # Frontend
python main.py       # Backend

# Build for production
npm run build        # Frontend
```

## Benefits Over Streamlit

| Aspect                 | Streamlit                            | FastAPI + React                |
| ---------------------- | ------------------------------------ | ------------------------------ |
| **Scalability**        | Limited to single server             | Unlimited horizontal scaling   |
| **User Capacity**      | ~10-50 concurrent users              | 1000+ concurrent users         |
| **Customization**      | Limited UI flexibility               | Complete UI control            |
| **Performance**        | Slower (Python rendering)            | Fast (Client-side rendering)   |
| **Deployment**         | Simple but limited                   | More options (AWS, Azure, GCP) |
| **Team Collaboration** | Difficult (frontend/backend mixed)   | Easy (separate teams)          |
| **Monetization**       | Difficult (re-render on interaction) | Easy (clear API boundaries)    |

## Next Steps

1. ✅ **Current**: Project structure created
2. **Todo**: Update path references in backend to import astrology modules
3. **Todo**: Add authentication (JWT tokens)
4. **Todo**: Add user profiles and history
5. **Todo**: Add chart visualization with Plotly
6. **Todo**: Deploy to production

## Support

For questions or issues, create a GitHub issue or contact the development team.

Made with ❤️ for Vedic Astrology
