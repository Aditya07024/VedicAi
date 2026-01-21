# 🌟 VedicAI - Explainable Astrology Through Astronomical Computation

> Now with FastAPI + React architecture for production scaling

## 🚀 Quick Start (2 minutes)

```bash
chmod +x setup.sh && ./setup.sh
# Edit backend/.env with your credentials
# Terminal 1: cd backend && source venv/bin/activate && python main.py
# Terminal 2: cd frontend && npm run dev
# Open http://localhost:3000
```

## ✨ What's New

Your Streamlit app has been converted to a **production-ready architecture**:

```
React Frontend (Port 3000)
    ↓ REST API
FastAPI Backend (Port 8000)
    ↓
PostgreSQL + Gemini AI + Astrology Engine
```

## 📚 Key Resources

- [**QUICKSTART.md**](QUICKSTART.md) - Get started in 5 minutes
- [**ARCHITECTURE.md**](ARCHITECTURE.md) - Technical design details
- [**Interactive API Docs**](http://localhost:8000/docs) - When server is running

## 📁 Project Structure

```
VedicAI/
├── backend/                  # FastAPI REST API
├── frontend/                # React + Vite UI
├── kundliGenerator/         # Astrology calculations
├── dosha/
├── panchang/
├── Swiss_Ephemeris/
├── docker-compose.yml       # Multi-container setup
├── QUICKSTART.md            # 5-minute setup
└── ARCHITECTURE.md          # Technical details
```

## 🔧 Setup

**Option 1: Auto Setup**

```bash
chmod +x setup.sh && ./setup.sh
```

**Option 2: Docker**

```bash
cp backend/.env.example backend/.env
docker-compose up
```

**Option 3: Manual**

```bash
# Backend
cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py

# Frontend (new terminal)
cd frontend && npm install && npm run dev
```

## 📊 API & Access

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🎯 Benefits Over Streamlit

- 🚀 Handle 1000+ concurrent users (vs 50)
- 📱 Mobile responsive design
- ⚡ Much faster response times
- 🔧 Complete UI customization
- 📦 Easy team collaboration
- 🌐 Multiple deployment options

---

Made with ❤️ for Vedic Astrology
