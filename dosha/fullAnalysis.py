import sys
import os

# Add project root and module directories to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "kundliGenerator"))
sys.path.append(os.path.join(BASE_DIR, "dosha"))
from GenerateKundli import generate_kundli, print_ascii_north_indian_chart, generate_kundli_chart
from doshaAnalyzer import detect_doshas, print_dosha_report
from dashaCalculator import calculate_vimshottari_dasha, print_dasha_report

def full_astrology_analysis(birth_datetime, birth_location, current_date=None):
    """
    Complete astrological analysis
    """
    print("\n" + "="*70)
    print("           COMPLETE VEDIC ASTROLOGY ANALYSIS")
    print("="*70)
    
    # Generate Kundli
    print("\n🔮 Generating Kundli...")
    kundli = generate_kundli(birth_datetime, birth_location)
    
    # Show chart
    kundli_chart = generate_kundli_chart(kundli)
    print_ascii_north_indian_chart(kundli_chart)
    
    # Dosha Analysis
    print("\n📊 Analyzing Doshas...")
    doshas = detect_doshas(kundli)
    print_dosha_report(doshas)
    
    # Dasha Analysis
    print("\n⏰ Calculating Dasha Periods...")
    dasha = calculate_vimshottari_dasha(kundli, current_date)
    print_dasha_report(dasha)
    
    return {
        'kundli': kundli,
        'doshas': doshas,
        'dasha': dasha
    }

if __name__ == "__main__":
    birth_datetime = {
        "date": "1995-08-15",
        "time": "10:30:00"
    }
    
    birth_location = {
        "name": "Delhi",
        "latitude": 28.6139,
        "longitude": 77.2090
    }
    
    analysis = full_astrology_analysis(
        birth_datetime, 
        birth_location,
        current_date="2026-01-19"
    )