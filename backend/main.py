from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import Json

# Add parent directory to path for importing astrology modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="VedicAI API",
    description="Explainable Astrology through Astronomical Computation",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== DATABASE ====================
def get_db_connection():
    try:
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            conn = psycopg2.connect(database_url)
        else:
            conn = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host=os.getenv("POSTGRES_HOST", "localhost"),
                port=os.getenv("POSTGRES_PORT", 5432)
            )
        return conn
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        return None

# ==================== PYDANTIC MODELS ====================
class BirthDetails(BaseModel):
    name: str
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM:SS
    place: str
    latitude: float
    longitude: float

class AnalysisRequest(BaseModel):
    birth_details: BirthDetails

class AnalysisResponse(BaseModel):
    birth_details: dict
    kundli: dict
    doshas: list
    dasha: dict
    panchang: dict

# ==================== ROUTES ====================

@app.get("/")
async def root():
    return {
        "message": "VedicAI API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/api/analysis")
async def generate_analysis(request: AnalysisRequest):
    """
    Generate complete astrology analysis
    Takes birth details and returns Kundli, Doshas, Dasha, Panchang
    """
    try:
        # Import astrology modules
        import sys
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(base_dir, "kundliGenerator"))
        sys.path.append(os.path.join(base_dir, "dosha"))
        sys.path.append(os.path.join(base_dir, "panchang"))
        
        from GenerateKundli import generate_kundli, generate_kundli_chart
        from doshaAnalyzer import detect_doshas
        from dashaCalculator import calculate_vimshottari_dasha
        from panchangCalculator import calculate_panchang
        
        # Prepare data
        birth_datetime = {
            "date": request.birth_details.date,
            "time": request.birth_details.time
        }
        
        birth_location = {
            "name": request.birth_details.place,
            "latitude": request.birth_details.latitude,
            "longitude": request.birth_details.longitude
        }
        
        # Generate analysis
        kundli = generate_kundli(birth_datetime, birth_location)
        kundli_chart = generate_kundli_chart(kundli)
        doshas = detect_doshas(kundli)
        dasha = calculate_vimshottari_dasha(kundli, datetime.now().strftime("%Y-%m-%d"))
        panchang = calculate_panchang(request.birth_details.date, birth_location)
        
        # Prepare response
        response = {
            "birth_details": {
                "name": request.birth_details.name,
                "date": request.birth_details.date,
                "time": request.birth_details.time,
                "place": request.birth_details.place,
                "latitude": request.birth_details.latitude,
                "longitude": request.birth_details.longitude
            },
            "kundli": kundli,
            "doshas": doshas,
            "dasha": dasha,
            "panchang": panchang
        }
        
        # Auto-save to database
        save_analysis_to_db({
            "user_name": request.birth_details.name,
            "birth_details": response["birth_details"],
            "kundli_data": kundli,
            "dosha_data": doshas,
            "dasha_data": dasha,
            "panchang_data": panchang,
            "ai_insights": {}
        })
        
        return response
        
    except Exception as e:
        print(f"[ERROR] Analysis generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/insights")
async def generate_ai_insights(request: AnalysisRequest):
    """Generate Gemini AI insights based on analysis"""
    try:
        from google import genai
        
        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            raise HTTPException(status_code=500, detail="Gemini API key not configured")
        
        client = genai.Client(api_key=gemini_key)
        
        # Generate insights using Gemini
        prompt = f"""
You are a Vedic astrologer. Generate insights for:
Name: {request.birth_details.name}
Birth: {request.birth_details.date} at {request.birth_details.time}
Place: {request.birth_details.place}

Provide insights in these sections:
PERSONALITY, CAREER, RELATIONSHIPS, LIFE_PHASE, STRENGTHS_CHALLENGES, HEALTH, SPIRITUAL, DOSHA_SUMMARY
"""
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        
        if response and response.text:
            return {"insights": response.text}
        else:
            return {"insights": None}
            
    except Exception as e:
        print(f"[ERROR] AI insights failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search-place")
async def search_place(query: str):
    """
    Search for place coordinates
    Returns Google Maps search URL
    """
    try:
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}+latitude+and+longitude"
        return {"search_url": search_url, "query": query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== DATABASE FUNCTIONS ====================

def save_analysis_to_db(payload):
    """Save analysis data to PostgreSQL"""
    conn = get_db_connection()
    if not conn:
        print("[WARNING] Could not save to database - no connection")
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vedicai_raw_data (
                id SERIAL PRIMARY KEY,
                user_name TEXT,
                birth_details JSONB,
                kundli_data JSONB,
                dosha_data JSONB,
                dasha_data JSONB,
                panchang_data JSONB,
                ai_insights JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        birth_details = payload.get('birth_details', {})
        user_name = birth_details.get('name', 'Unknown User')
        
        cur.execute(
            """INSERT INTO vedicai_raw_data 
               (user_name, birth_details, kundli_data, dosha_data, dasha_data, panchang_data, ai_insights) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (
                user_name,
                Json(birth_details),
                Json(payload.get('kundli_data')),
                Json(payload.get('dosha_data')),
                Json(payload.get('dasha_data')),
                Json(payload.get('panchang_data')),
                Json(payload.get('ai_insights'))
            )
        )
        
        conn.commit()
        cur.close()
        conn.close()
        print("[INFO] Data saved to PostgreSQL")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save data: {e}")
        return False

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
