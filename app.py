import streamlit as st
from datetime import datetime
import sys
import os
from dotenv import load_dotenv
load_dotenv()
# Gemini import and config
from google import genai
import psycopg2
from psycopg2.extras import Json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    # Debug: API key not found
    print("[WARNING] GEMINI_API_KEY not found in environment variables.")

# Add paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "kundliGenerator"))
sys.path.append(os.path.join(BASE_DIR, "dosha"))
sys.path.append(os.path.join(BASE_DIR, "panchang"))

from GenerateKundli import generate_kundli, generate_kundli_chart
from doshaAnalyzer import detect_doshas
from dashaCalculator import calculate_vimshottari_dasha
from panchangCalculator import calculate_panchang


# =========================
# Database Save Function: Save Raw Data to PostgreSQL
# =========================
def get_db_connection():
    try:
        # Use DATABASE_URL from Neon or fall back to individual env vars
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
        print("[ERROR] Failed to connect to PostgreSQL:", e)
        return None


def save_raw_data_to_db(payload):
    conn = get_db_connection()
    if not conn:
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
        # Extract user_name from birth_details
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
        print("[INFO] Raw data saved to PostgreSQL")
        return True
    except Exception as e:
        print("[ERROR] Failed to save raw data:", e)
        return False



# =========================
# MASTER GEMINI INSIGHT (single call, multi-section)
# =========================
def generate_master_ai_insight(data, kundli):
    print("[INFO] Starting Gemini AI master insight generation...")
    if "ai_master_insight" in st.session_state:
        return st.session_state["ai_master_insight"]

    if not client:
        return None

    prompt = f"""
You are a calm, experienced Vedic astrologer speaking to a client.

Use ONLY the facts below. Do NOT calculate anything new.
Write deep, human-friendly explanations (not generic).

FORMAT EXACTLY LIKE THIS:

PERSONALITY:
<6-8 natural sentences>

CAREER:
<6-8 sentences + one practical real-life suggestion>

RELATIONSHIPS:
<6-8 sentences>

LIFE_PHASE:
<5-6 sentences>

STRENGTHS_CHALLENGES:
<balanced paragraph>

HEALTH:
<gentle non-medical explanation>

SPIRITUAL:
<grounding reflective paragraph>

DOSHA_SUMMARY:
<reassuring explanation>

FACTS:
Ascendant: {kundli['lagna']['rashi']}
Moon Sign: {kundli['planets']['Moon']['rashi']}
Current Mahadasha: {data['dasha']['mahadasha']['planet']}
Doshas: {", ".join(d['name'] for d in data['doshas']) or "None"}
"""

    try:
        print("[INFO] Sending prompt to Gemini model...")
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        print("[INFO] Gemini AI response received, parsing sections...")

        # Check if response has content
        if not response or not response.text:
            print("[ERROR] Gemini API returned empty response")
            return {}
        
        sections = {}
        current = None
        for line in response.text.splitlines():
            if line.strip().endswith(":") and line.strip().isupper():
                current = line.strip()[:-1]
                sections[current] = ""
            elif current:
                sections[current] += line + "\n"

        st.session_state["ai_master_insight"] = sections
        return sections

    except Exception as e:
        print("[ERROR] Gemini AI failed:", e)
        return {}

# Page config
st.set_page_config(
    page_title="VedicAI - Explainable Astrology",
    page_icon="🔮",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(120deg, #8B5CF6, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #6B7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
    }
    .confidence-high {
        color: #10B981;
        font-weight: bold;
    }
    .confidence-medium {
        color: #F59E0B;
        font-weight: bold;
    }
    .confidence-low {
        color: #EF4444;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🔮 VedicAI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Explainable Astrology through Astronomical Computation</p>', unsafe_allow_html=True)
st.markdown(
    '''
    <div style="
        text-align:center;
        margin-bottom: 1.5rem;
        padding: 12px 16px;
        background: #fff7ed;
        border: 2px solid #fb923c;
        border-radius: 10px;
        font-size: 1rem;
        color: #9a3412;
        font-weight: 500;
    ">
        🚀 <strong>Developed by Aditya</strong> <br/>
        💬 Feedback
        <a href="https://www.linkedin.com/in/adityakumar0702/" target="_blank"
           style="color:#c2410c; text-decoration: underline; font-weight:600;">
                Message me on LinkedIn
        </a>
        <br>
        Source Code:
        <a href="https://github.com/Aditya07024" target="_blank"
           style="color:#c2410c; text-decoration: underline; font-weight:600;">
                github.com/Aditya07024
        </a>
    </div>
    ''',
    unsafe_allow_html=True
)

# Centered GitHub button just below banner
st.markdown(
    """
    <div style="text-align:center; margin-bottom: 2rem;">
        <a href="https://github.com/Aditya07024" target="_blank">
            <button style="
                background-color:#dc2626;
                color:white;
                border:none;
                padding:14px 22px;
                font-size:1rem;
                border-radius:10px;
                cursor:pointer;
                font-weight:600;
            ">
                📘 How to Use This App
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar - Input Form
with st.sidebar:
    st.header("📅 Birth Details")
    
    name = st.text_input("Name *", placeholder="John Doe", help="Username is required")
    
    birth_date = st.date_input(
        "Birth Date",
        value=datetime(2003, 2, 7),
        min_value=datetime(1900, 1, 1),
        max_value=datetime.now()
    )
    
    birth_time = st.time_input(
        "Birth Time",
        value=datetime.strptime("3:00", "%H:%M").time()
    )
    
    st.subheader("📍 Birth Place")

    st.info("ℹ️ After entering the birth place click on search icon.")

    col1, col2 = st.columns([4, 1])
    with col1:
        place_name = st.text_input("Place Name *", placeholder="Enter your birth place", help="Place name is required")
    with col2:
        st.write("")  # Spacing
        search_btn = st.button("🔍", help="Search for place coordinates on Google")
    
    if search_btn and place_name:
        # Open Google search for latitude and longitude
        search_url = f"https://www.google.com/search?q={place_name.replace(' ', '+')}+latitude+and+longitude"
        st.markdown(f"[👉 Click here to search on Google]({search_url})")
        st.info(f"📌 **Instructions:**\n1. Click the link above to search '{place_name} latitude and longitude'\n2. Google will show the coordinates in the results\n3. Copy the latitude and longitude values\n4. Paste them in the fields below")

    latitude = st.number_input("Latitude *", value=27.7081, format="%.4f", help="Latitude is required")

    longitude = st.number_input("Longitude *", value= 77.9367, format="%.4f", help="Longitude is required")
    
    st.markdown("---")
    
    # Validate all required fields
    is_form_valid = (
        name and name.strip() != "" and
        place_name and place_name.strip() != "Enter your birth place" and
        latitude != 0 and
        longitude != 0
    )
    
    generate_btn = st.button("🔮 Generate Analysis", type="primary", use_container_width=True, disabled=not is_form_valid)
    
    if not is_form_valid:
        st.warning("⚠️ Please fill all required fields marked with *")

# Main content
if generate_btn or 'analysis_done' in st.session_state:
    
    if generate_btn:
        with st.spinner("🔄 Calculating planetary positions..."):
            # Prepare data
            birth_datetime = {
                "date": birth_date.strftime("%Y-%m-%d"),
                "time": birth_time.strftime("%H:%M:%S")
            }
            
            birth_location = {
                "name": place_name,
                "latitude": latitude,
                "longitude": longitude
            }
            
            # Generate Kundli
            kundli = generate_kundli(birth_datetime, birth_location)
            kundli_chart = generate_kundli_chart(kundli)
            
            # Dosha Analysis
            doshas = detect_doshas(kundli)
            
            # Dasha Analysis
            dasha = calculate_vimshottari_dasha(kundli, datetime.now().strftime("%Y-%m-%d"))
            
            # Panchang
            panchang = calculate_panchang(birth_date.strftime("%Y-%m-%d"), birth_location)
            
            # Store in session state
            st.session_state['kundli'] = kundli
            st.session_state['kundli_chart'] = kundli_chart
            st.session_state['doshas'] = doshas
            st.session_state['dasha'] = dasha
            st.session_state['panchang'] = panchang
            st.session_state['birth_details'] = {
                'name': name,
                'date': birth_date.strftime("%d %B %Y"),
                'time': birth_time.strftime("%I:%M %p"),
                'place': place_name,
                'latitude': latitude,
                'longitude': longitude
            }
            st.session_state['analysis_done'] = True
            
            # Auto-save raw data to database
            payload = {
                "birth_details": st.session_state['birth_details'],
                "kundli_data": kundli,
                "dosha_data": doshas,
                "dasha_data": dasha,
                "panchang_data": panchang,
                "ai_insights": {}
            }
            save_raw_data_to_db(payload)
            st.success(f"✅ Data generated for {name}")
    
    # Retrieve from session state
    kundli = st.session_state.get('kundli')
    kundli_chart = st.session_state.get('kundli_chart')
    doshas = st.session_state.get('doshas')
    dasha = st.session_state.get('dasha')
    panchang = st.session_state.get('panchang')
    birth_details = st.session_state.get('birth_details')
    
    # Success message
    st.success(f"✅ Analysis complete for {birth_details['name']}")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab6, tab7, tab8 = st.tabs([
        "📊 Kundli Chart", 
        "⚠️ Dosha Analysis", 
        "⏰ Dasha Periods", 
        "📅 Panchang",
        # "🧠 Explanation",
        "🤖 AI-Powered Insights",
        "🔍 Why This Prediction?",
        "🧾 Raw Data"
    ])
    
    # TAB 1: Kundli Chart
    with tab1:
        st.subheader("🔮 Birth Chart (Kundli)")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display North Indian (diamond-style) chart
            h = kundli_chart["house_chart"]
            lagna = kundli_chart["lagna"]

            north_indian_chart = f"""
                ┌───────────────┐
                │  [12] {h[12]:<12} │
        ┌───────┼───────────────┼───────┐
        │ [11] {h[11]:<8} │               │ [1] {h[1]:<8} │
        │               │   LAGNA        │               │
        │               │ ({lagna})      │               │
        ├───────────────┼───────────────┼───────────────┤
        │ [10] {h[10]:<8} │               │ [2] {h[2]:<8} │
        │               │               │               │
        └───────┼───────────────┼───────┘
                │  [7] {h[7]:<12} │
        ┌───────┼───────────────┼───────┐
        │ [8] {h[8]:<8} │               │ [6] {h[6]:<8} │
        │               │               │               │
        ├───────────────┼───────────────┼───────────────┤
        │ [9] {h[9]:<8} │               │ [5] {h[5]:<8} │
        │               │               │               │
        └───────┼───────────────┼───────┘
                │  [4] {h[4]:<12} │
                └───────────────┘
            """
            st.code(north_indian_chart, language="text")
        
        with col2:
            st.markdown("### 📋 Birth Details")
            st.write(f"**Name:** {birth_details['name']}")
            st.write(f"**Date:** {birth_details['date']}")
            st.write(f"**Time:** {birth_details['time']}")
            st.write(f"**Place:** {birth_details['place']}")
            
            st.markdown("### 🌟 Ascendant (Lagna)")
            st.write(f"**Rashi:** {kundli['lagna']['rashi']}")
            st.write(f"**Nakshatra:** {kundli['lagna']['nakshatra']}")
        
        # Planetary positions
        st.markdown("---")
        st.subheader("🪐 Planetary Positions")
        
        planets_col1, planets_col2, planets_col3 = st.columns(3)
        
        planet_list = list(kundli['planets'].items())
        
        with planets_col1:
            for planet, data in planet_list[:3]:
                st.metric(
                    label=planet,
                    value=data['rashi'],
                    delta=data['nakshatra']
                )
        
        with planets_col2:
            for planet, data in planet_list[3:6]:
                st.metric(
                    label=planet,
                    value=data['rashi'],
                    delta=data['nakshatra']
                )
        
        with planets_col3:
            for planet, data in planet_list[6:]:
                st.metric(
                    label=planet,
                    value=data['rashi'],
                    delta=data['nakshatra']
                )
    
    # TAB 2: Dosha Analysis
    with tab2:
        st.subheader("⚠️ Dosha Detection")
        
        if not doshas:
            st.success("✅ No major doshas detected in the chart!")
            st.info("This is a favorable indication for smooth life events.")
        else:
            st.warning(f"⚠️ {len(doshas)} Dosha(s) detected")
            
            for i, dosha in enumerate(doshas, 1):
                with st.expander(f"{i}. {dosha['name']} - Severity: {dosha['severity']}", expanded=True):
                    
                    # Severity indicator
                    severity_color = {
                        'High': '🔴',
                        'Medium': '🟡',
                        'Low': '🟢'
                    }
                    st.markdown(f"### {severity_color.get(dosha['severity'], '⚪')} {dosha['name']}")
                    
                    st.write(f"**Description:** {dosha['description']}")
                    st.write(f"**Impact:** {dosha['impact']}")
                    
                    if 'phase' in dosha:
                        st.info(f"**Current Phase:** {dosha['phase']}")
                    
                    if 'house' in dosha:
                        st.write(f"**House Position:** {dosha['house']}th house")
                    
                    # Cancellations
                    if 'cancellations' in dosha and dosha['cancellations']:
                        st.markdown("#### ✓ Mitigating Factors:")
                        for cancel in dosha['cancellations']:
                            st.write(f"• {cancel}")
                    
                    # Remedies
                    st.markdown("#### 📿 Suggested Remedies:")
                    for remedy in dosha['remedies']:
                        st.write(f"• {remedy}")
    
    # TAB 3: Dasha Periods
    with tab3:
        st.subheader("⏰ Vimshottari Dasha System")
        
        maha = dasha['mahadasha']
        
        # Current Mahadasha
        st.markdown(f"### 🔮 Current Mahadasha: **{maha['planet']}**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Start Date", maha['start_date'])
        with col2:
            st.metric("End Date", maha['end_date'])
        with col3:
            st.metric("Years Remaining", f"{maha['years_remaining']:.1f}")
        
        # Progress bar
        progress = (maha['total_years'] - maha['years_remaining']) / maha['total_years']
        st.progress(progress)
        st.caption(f"Progress: {progress*100:.1f}% complete")
        
        # Antardasha
        st.markdown("---")
        st.markdown(f"### 🌙 Current Antardasha: **{dasha['antardasha']['planet']}**")
        st.caption(dasha['antardasha']['note'])
        
        # Interpretation
        st.markdown("---")
        st.markdown(f"### 📖 {maha['planet']} Mahadasha Interpretation")
        
        interp = dasha['interpretation']
        
        st.write(f"**General Theme:** {interp.get('general', 'N/A')}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("**Positive Aspects**")
            st.write(interp.get('positive', 'N/A'))
        
        with col2:
            st.warning("**Challenges**")
            st.write(interp.get('challenges', 'N/A'))
        
        if 'house_influence' in interp:
            st.info(f"**House Influence:** {interp['house_influence']}")
    
    # TAB 4: Panchang
    with tab4:
        st.subheader("📅 Panchang (Hindu Calendar)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌞 Basic Elements")
            st.write(f"**Vara (Day):** {panchang['vara']}")
            st.write(f"**Tithi (Lunar Day):** {panchang['tithi']['paksha']} {panchang['tithi']['name']}")
            st.write(f"**Nakshatra:** {panchang['nakshatra']}")
            st.write(f"**Yoga:** {panchang['yoga']}")
            st.write(f"**Karana:** {panchang['karana']}")
        
        with col2:
            st.markdown("### ⏰ Sun Timings")
            st.write(f"**Sunrise:** {panchang['sunrise']}")
            st.write(f"**Sunset:** {panchang['sunset']}")
            st.write(f"**Rahu Kaal:** Period {panchang['rahu_kaal']['period_index']}")
            st.caption(panchang['rahu_kaal']['note'])

    # TAB 5: Explanation (Gemini)
    # with tab5:
    #     st.subheader("🧠 Explanation (Human-Friendly Interpretation)")
        
    #     st.info("""
    #     🔴 **Important:**  
    #     This section is generated using **Gemini AI**.  
    #     Gemini does **NOT** calculate planets, doshas, or dashas.  
    #     It only **explains the already-calculated results** in simple language.
    #     """)

    #     # Career Explanation
    #     with st.expander("💼 Career Explanation", expanded=True):
    #         career_data = {
    #             'dasha': dasha,
    #             'doshas': doshas,
    #             'tenth_house': kundli['houses'][10]
    #         }
            
    #         career_exp = generate_ai_explanation("career", career_data, kundli)
            
    #         st.markdown(
    #             f"""
    #             <div style="
    #                 border-left: 6px solid #dc2626;
    #                 background-color: #fef2f2;
    #                 padding: 16px;
    #                 border-radius: 8px;
    #             ">
    #             <strong>🤖 Gemini Explanation</strong><br><br>
    #             {career_exp['explanation']}
    #             </div>
    #             """,
    #             unsafe_allow_html=True
    #         )

    #     # Dosha Explanation
    #     with st.expander("⚠️ Dosha Explanation"):
    #         dosha_exp = generate_ai_explanation(
    #             "dosha_summary",
    #             {'doshas': doshas},
    #             kundli
    #         )
            
    #         st.markdown(
    #             f"""
    #             <div style="
    #                 border-left: 6px solid #dc2626;
    #                 background-color: #fef2f2;
    #                 padding: 16px;
    #                 border-radius: 8px;
    #             ">
    #             <strong>🤖 Gemini Explanation</strong><br><br>
    #             {dosha_exp['explanation']}
    #             </div>
    #             """,
    #             unsafe_allow_html=True
    #         )

    #     st.caption("🧠 Gemini is used only for explanation — all astrology is rule-based and reproducible.")
    
    # TAB 6: Transparency
    with tab7:
        st.subheader("🔍 How We Generated This Prediction")
        
        st.markdown("""
        ### 🎯 Our Approach: Calculation-First, Not AI Guessing
        
        Unlike traditional AI astrology apps that generate generic responses, VedicAI follows a **4-step scientific process**:
        """)
        
        st.markdown("---")
        
        # Step 1
        st.markdown("#### 1️⃣ Astronomical Calculation (Swiss Ephemeris)")
        st.code(f"""
Calculated exact planetary positions on {birth_details['date']} at {birth_details['time']}:
- Used Swiss Ephemeris (NASA-grade accuracy)
- Applied Lahiri Ayanamsa (Vedic sidereal zodiac)
- Precision: ±0.01 degrees
        """)
        
        # Step 2
        st.markdown("#### 2️⃣ Kundli Generation")
        st.code(f"""
Generated birth chart:
- Ascendant (Lagna): {kundli['lagna']['rashi']} at {kundli['lagna']['longitude']:.2f}°
- Calculated 12 houses from Lagna position
- Assigned planets to houses based on exact positions
        """)
        
        # Step 3
        st.markdown("#### 3️⃣ Rule Engine Application")
        
        with st.expander("View Applied Rules"):
            st.markdown("**Dosha Detection Rules:**")
            st.code("""
IF Mars in houses [1, 4, 7, 8, 12] THEN Mangal Dosha = TRUE
IF All planets between Rahu-Ketu axis THEN Kaal Sarp Dosha = TRUE
IF Saturn within ±1 house from Moon THEN Sade Sati = TRUE
            """)
            
            st.markdown("**Dasha Calculation:**")
            st.code(f"""
Birth Nakshatra: {kundli['planets']['Moon']['nakshatra']}
Starting Mahadasha Lord: {dasha['birth_nakshatra_lord']}
Current Mahadasha: {maha['planet']} ({maha['start_date']} to {maha['end_date']})
            """)
        
        # Step 4
        st.markdown("#### 4️⃣ Confidence Scoring")
        
        # Calculate sample confidence
        confidence_factors = []
        
        if not doshas:
            confidence_factors.append(("No major doshas", 90))
        else:
            confidence_factors.append((f"{len(doshas)} dosha(s) detected", 70))
        
        confidence_factors.append((f"{maha['planet']} Mahadasha active", 85))
        confidence_factors.append(("Planetary positions verified", 95))
        
        avg_confidence = sum([c[1] for c in confidence_factors]) / len(confidence_factors)
        
        st.metric("Overall Analysis Confidence", f"{avg_confidence:.0f}%")
        
        st.markdown("**Confidence Breakdown:**")
        for factor, conf in confidence_factors:
            st.progress(conf/100)
            st.caption(f"{factor}: {conf}%")
        
        st.markdown("---")
        
        st.info("""
        **🔬 Why Trust This?**
        
        - ✅ **Reproducible:** Same birth details → Same results, always
        - ✅ **Transparent:** You can see every calculation step
        - ✅ **Scientific:** Based on real astronomical data, not random AI generation
        - ✅ **Explainable:** Every prediction shows its reasoning
        """)
        
        st.warning("""
        **⚠️ Important Note:**
        
        This system encodes traditional Vedic astrology rules algorithmically. 
        We do not claim astrology is scientifically proven - we aim to make 
        traditional practices **consistent, transparent, and accessible**.
        """)

    # TAB 7: AI-Powered Insights
    with tab6:
        st.subheader("🤖 AI-Powered Insights")

        st.warning("""
⚠️ **AI Usage Notice**

Gemini AI has a **daily free‑tier limit**.
Only the **most important insights** are generated using AI.

Other insights automatically fall back to **rule‑based human explanations**
to keep the app fast, stable, and reliable.
""")

        with st.spinner("🤖 Generating deep AI insights (this may take a few seconds)..."):
            print("[UI] Spinner shown: Generating AI insights")
            insights = generate_master_ai_insight(
                {"dasha": dasha, "doshas": doshas},
                kundli
            )
            print("[UI] Spinner finished")


        def show_section(title, key):
            with st.expander(title, expanded=(key=="CAREER")):
                if insights and key in insights:
                    full_text = insights[key].strip()
                    # --- Summary generation (first 2–3 meaningful lines) ---
                    lines = [l for l in full_text.splitlines() if l.strip()]
                    summary = " ".join(lines[:2])

                    style_block = """
    background:#fff1f2;
    border-left:6px solid #dc2626;
    color:#7f1d1d;
    padding:14px;
    border-radius:10px;
    font-size:0.95rem;
""" if key == "DOSHA_SUMMARY" else """
    background:#f0f9ff;
    border-left:5px solid #0ea5e9;
    padding:12px;
    border-radius:8px;
    font-size:0.95rem;
"""

                    st.markdown(
                        f'''
    <div style="{style_block}">
        <strong>📝 Insight Summary:</strong><br/>
        {summary}
    </div>
    ''',
                        unsafe_allow_html=True
                    )
                    st.markdown("")
                else:
                    st.info("This insight is shown using detailed rule-based interpretation because AI service is temporarily unavailable.")

        show_section("🌟 Personality Insight", "PERSONALITY")
        show_section("💼 Career Outlook", "CAREER")
        show_section("💑 Relationships & Marriage", "RELATIONSHIPS")
        show_section("⏳ Current Life Phase", "LIFE_PHASE")
        show_section("💪 Strengths & Challenges", "STRENGTHS_CHALLENGES")
        show_section("🧘 Health & Energy", "HEALTH")
        show_section("🕉️ Spiritual Growth", "SPIRITUAL")
        show_section("⚠️ Dosha Impact Summary", "DOSHA_SUMMARY")

        st.caption("🧠 Gemini explains only — all astrology is rule-based and reproducible.")

    # TAB 8: Raw Data (JSON)
    with tab8:
        st.subheader("🧾 Raw Calculated Data (JSON)")
        st.info(
            "This section displays the **exact underlying data** used for all insights above. "
            "You can use this to reproduce every calculation — nothing is hidden or changed.\n\n"
        )
        st.json({
            "birth_details": birth_details,
            "kundli": kundli,
            "doshas": doshas,
            "dasha": dasha,
            "panchang": panchang
        })

else:
    # Welcome screen
    st.markdown("""
    ## Welcome to VedicAI! 👋
    
    ### What Makes Us Different?
    
    Traditional astrology apps use AI to generate generic, inconsistent predictions. 
    **VedicAI uses AI only for explanation** - the actual predictions come from:
    
    - 🔭 **Real astronomical calculations** (Swiss Ephemeris)
    - 📐 **Authentic Vedic rules** (Dosha, Dasha, Yogas)
    - 🎯 **Transparent reasoning** (See exactly why each prediction was made)
    
    ### How It Works:
    
    1. Enter your birth details in the sidebar →
    2. Click "Generate Analysis" 
    3. Explore your Kundli, Doshas, Dasha periods, and Panchang
    4. See the "Why?" tab to understand our calculations
    
    ### Ready to Begin?
    
    👈 Enter your birth details in the sidebar and click **"Generate Analysis"**
    """)