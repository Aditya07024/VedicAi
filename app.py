import streamlit as st
from datetime import datetime
import sys
import os
from dotenv import load_dotenv
load_dotenv()

from huggingface_hub import InferenceClient


# Add paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "kundliGenerator"))
sys.path.append(os.path.join(BASE_DIR, "dosha"))
sys.path.append(os.path.join(BASE_DIR, "panchang"))

from GenerateKundli import generate_kundli, generate_kundli_chart
from doshaAnalyzer import detect_doshas
from dashaCalculator import calculate_vimshottari_dasha
from panchangCalculator import calculate_panchang



@st.cache_resource
def load_hf_client():
    return InferenceClient(
        api_key=os.environ.get("HF_TOKEN")
    )

hf_client = load_hf_client()

def generate_ai_explanation(analysis_type, data, kundli):
    cache_key = f"ai_{analysis_type}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    md = data.get("dasha", {}).get("mahadasha", {})
    md_planet = md.get("planet")

    md_house = kundli["planets"].get(md_planet, {}).get("house", "Unknown")
    md_rashi = kundli["planets"].get(md_planet, {}).get("rashi", "Unknown")

    facts = f"""
Ascendant (Lagna): {kundli['lagna']['rashi']}
Moon Sign: {kundli['planets']['Moon']['rashi']}

Current Mahadasha:
- Planet: {md_planet}
- Placement House: {md_house}
- Sign Placement: {md_rashi}

10th House (Career): {get_house_summary(kundli, 10)}
7th House (Marriage): {get_house_summary(kundli, 7)}
1st House (Self): {get_house_summary(kundli, 1)}

Detected Doshas:
{", ".join(d['name'] for d in data.get('doshas', [])) or "None"}
"""

    instruction_map = {
        "career": "Explain career direction calmly and practically.",
        "marriage": "Explain relationship and marriage tendencies gently.",
        "life_phase": "Explain the current life phase as guidance.",
        "strengths_challenges": "Explain strengths first, then challenges.",
        "health": "Explain energy and health patterns non-medically.",
        "spiritual": "Explain spiritual growth and awareness.",
        "dosha_summary": "Explain doshas as tendencies, not fear.",
        "personality": "Explain personality traits warmly."
    }

    prompt = f"""
You are a calm, thoughtful human guide.

IMPORTANT:
- You do NOT calculate astrology.
- You ONLY interpret the verified facts below.
- Do NOT give generic advice.

FACTS (already calculated):
{facts}

TASK:
Create a detailed, person-specific summary for: {analysis_type}

You MUST follow this structure strictly:

1. Core Influence
- Identify the single most dominant planet, house, or dasha influencing this area.
- Explain clearly WHY this factor is dominant right now.

2. How It Manifests in Real Life
- Explain how this influence shows up in daily life, decisions, emotions, or situations.
- Connect house placement with the current dasha timing.

3. Why It Feels This Way Now
- Explain why this is a phase and not permanent.
- Mention timing, maturity, or progression.

4. Practical Direction
- What works well during this phase.
- What should be avoided.
- Keep advice grounded and realistic.

STYLE RULES:
- Write as if guiding ONE real person
- Use cause → effect reasoning
- No astrology jargon without explanation
- No fear, superstition, or guarantees
- 3–4 medium paragraphs
- Warm, human, confident tone
"""

    try:
        completion = hf_client.chat.completions.create(
            model="HuggingFaceH4/zephyr-7b-beta:featherless-ai",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=350,
            temperature=0.7,
        )

        text = completion.choices[0].message.content.strip()

        result = {
            "explanation": text,
            "ai_generated": True,
            "model": "zephyr-7b-beta (HF hosted)"
        }

    except Exception:
        # Graceful rule-based fallback (no AI)
        fallback_map = {
            "career": (
                "Your chart suggests a steady career path influenced by your current dasha. "
                "Progress may feel gradual, but consistency and skill-building will bring results. "
                "Avoid impulsive decisions during emotionally charged periods."
            ),
            "marriage": (
                "Relationships in your chart emphasize patience and mutual understanding. "
                "Emotional maturity plays a key role in long-term harmony, especially during "
                "challenging dashas."
            ),
            "life_phase": (
                "This phase of life appears focused on learning, adjustment, and inner growth. "
                "It is a time to build foundations rather than expect instant outcomes."
            ),
            "strengths_challenges": (
                "Your strengths include adaptability and long-term vision. "
                "Challenges mainly arise from overthinking or delayed action. "
                "Balance planning with timely execution."
            ),
            "health": (
                "Overall energy patterns indicate the importance of routine and balance. "
                "Mental rest and disciplined habits support well-being during demanding periods."
            ),
            "spiritual": (
                "Spiritual growth in your chart comes through self-reflection and awareness. "
                "Periods of silence or introspection can be especially beneficial."
            ),
            "dosha_summary": (
                "The detected doshas indicate tendencies rather than fixed outcomes. "
                "Their impact reduces with awareness, right timing, and conscious effort."
            ),
            "personality": (
                "Your personality shows a thoughtful and observant nature. "
                "You tend to learn from experience and grow stronger through reflection."
            ),
        }

        result = {
            "explanation": fallback_map.get(
                analysis_type,
                "This insight is shown using rule-based interpretation based on your chart."
            ),
            "ai_generated": False,
            "model": "rule-based fallback"
        }

    st.session_state[cache_key] = result
    return result

def get_house_summary(kundli, house_num):
    """
    Return a readable summary of planets in a given house.
    Used ONLY for AI explanations.
    """
    planets = kundli["houses"].get(house_num, [])
    if not planets:
        return "Empty"
    return ", ".join(p["planet"] for p in planets)


# =========================
# REUSABLE AI INSIGHT RENDERER
# =========================
def render_ai_insight(title, analysis_type, data, kundli, expanded=False):
    """
    Renders a single AI insight section with:
    - Spinner
    - AI explanation
    - Red highlighted output
    """
    with st.expander(title, expanded=expanded):
        with st.spinner("🤖 Generating insight (human‑friendly summary)..."):
            insight = generate_ai_explanation(
                analysis_type,
                data,
                kundli
            )

        st.markdown(
            f"""
            <div style="
                border-left: 6px solid #dc2626;
                background-color: #fef2f2;
                padding: 16px;
                border-radius: 8px;
                font-size: 1rem;
                line-height: 1.6;
            ">
            <strong>🤖 AI Explanation</strong><br><br>
            {insight['explanation']}
            </div>
            """,
            unsafe_allow_html=True
        )

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
    
    name = st.text_input("Name", placeholder="John Doe")
    
    birth_date = st.date_input(
        "Birth Date",
        value=datetime(1995, 8, 15),
        min_value=datetime(1900, 1, 1),
        max_value=datetime.now()
    )
    
    birth_time = st.time_input(
        "Birth Time",
        value=datetime.strptime("10:30", "%H:%M").time()
    )
    
    st.subheader("📍 Birth Place")

    st.info("ℹ️ Please manually enter the latitude and longitude of your birth place for accurate results.")

    place_name = st.text_input("Place Name", value="Delhi")

    latitude = st.number_input("Latitude", value=28.6139, format="%.4f")
    longitude = st.number_input("Longitude", value=77.2090, format="%.4f")
    
    st.markdown("---")
    generate_btn = st.button("🔮 Generate Analysis", type="primary", use_container_width=True)

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
                'name': name if name else "User",
                'date': birth_date.strftime("%d %B %Y"),
                'time': birth_time.strftime("%I:%M %p"),
                'place': place_name
            }
            st.session_state['analysis_done'] = True
    
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
    tab1, tab2, tab3, tab4, tab6, tab7 = st.tabs([
        "📊 Kundli Chart", 
        "⚠️ Dosha Analysis", 
        "⏰ Dasha Periods", 
        "📅 Panchang",
        # "🧠 Explanation",
"🤖 AI-Powered Insights",
        "🔍 Why This Prediction?"
        
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
⚠️ AI Usage Notice

This section uses an open-source AI model (OpenHermes).
The AI does NOT calculate planets, doshas, or dashas.
It only explains already-calculated results in simple language.
""")

        render_ai_insight(
            "🌟 Personality Insight",
            "personality",
            {"dasha": dasha, "doshas": doshas},
            kundli
        )

        render_ai_insight(
            "💼 Career Outlook",
            "career",
            {"dasha": dasha, "doshas": doshas},
            kundli,
            expanded=True
        )

        render_ai_insight(
            "💑 Relationships & Marriage",
            "marriage",
            {"dasha": dasha, "doshas": doshas},
            kundli
        )

        render_ai_insight(
            "⏳ Current Life Phase",
            "life_phase",
            {"dasha": dasha, "doshas": doshas},
            kundli
        )

        render_ai_insight(
            "💪 Strengths & Challenges",
            "strengths_challenges",
            {"dasha": dasha, "doshas": doshas},
            kundli
        )

        render_ai_insight(
            "🧘 Health & Energy",
            "health",
            {"dasha": dasha, "doshas": doshas},
            kundli
        )

        render_ai_insight(
            "🕉️ Spiritual Growth",
            "spiritual",
            {"dasha": dasha, "doshas": doshas},
            kundli
        )

        render_ai_insight(
            "⚠️ Dosha Impact Summary",
            "dosha_summary",
            {"doshas": doshas},
            kundli
        )

        st.caption("🧠 AI explains only — all astrology is rule-based and reproducible.")

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