import sys
import os

# Add project root and kundliGenerator to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "kundliGenerator"))
from datetime import datetime, timedelta

def calculate_vimshottari_dasha(kundli, current_date=None):
    """
    Calculate Vimshottari Dasha system
    """
    if current_date is None:
        current_date = datetime.now().strftime("%Y-%m-%d")
    
    birth_date_str = kundli['birth_details']['date']
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
    current = datetime.strptime(current_date, "%Y-%m-%d")
    
    # Get Moon's nakshatra from kundli
    moon_nakshatra = kundli['planets']['Moon']['nakshatra']
    
    # Dasha sequence based on nakshatra
    nakshatra_lord_map = {
        'Ashwini': 'Ketu', 'Magha': 'Ketu', 'Mula': 'Ketu',
        'Bharani': 'Venus', 'Purva Phalguni': 'Venus', 'Purva Ashadha': 'Venus',
        'Krittika': 'Sun', 'Uttara Phalguni': 'Sun', 'Uttara Ashadha': 'Sun',
        'Rohini': 'Moon', 'Hasta': 'Moon', 'Shravana': 'Moon',
        'Mrigashira': 'Mars', 'Chitra': 'Mars', 'Dhanishta': 'Mars',
        'Ardra': 'Rahu', 'Swati': 'Rahu', 'Shatabhisha': 'Rahu',
        'Punarvasu': 'Jupiter', 'Vishakha': 'Jupiter', 'Purva Bhadrapada': 'Jupiter',
        'Pushya': 'Saturn', 'Anuradha': 'Saturn', 'Uttara Bhadrapada': 'Saturn',
        'Ashlesha': 'Mercury', 'Jyeshtha': 'Mercury', 'Revati': 'Mercury'
    }
    
    # Dasha periods in years
    dasha_years = {
        'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10,
        'Mars': 7, 'Rahu': 18, 'Jupiter': 16, 
        'Saturn': 19, 'Mercury': 17
    }
    
    # Dasha order (cycles)
    dasha_sequence = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 
                      'Rahu', 'Jupiter', 'Saturn', 'Mercury']
    
    # Find starting planet based on Moon's nakshatra
    starting_planet = nakshatra_lord_map.get(moon_nakshatra, 'Ketu')
    
    # Calculate balance of first dasha
    # Simplified: assume full period for now
    # (Actual calculation requires Moon's exact position within nakshatra)
    
    # Rotate sequence to start from birth nakshatra lord
    start_index = dasha_sequence.index(starting_planet)
    rotated_sequence = dasha_sequence[start_index:] + dasha_sequence[:start_index]
    
    # Calculate which Mahadasha is currently running
    years_since_birth = (current - birth_date).days / 365.25
    
    cumulative_years = 0
    current_mahadasha = None
    mahadasha_start = birth_date
    mahadasha_end = None
    years_remaining = 0
    
    for planet in rotated_sequence:
        planet_years = dasha_years[planet]
        cumulative_years += planet_years
        
        if years_since_birth < cumulative_years:
            current_mahadasha = planet
            years_into_dasha = years_since_birth - (cumulative_years - planet_years)
            years_remaining = planet_years - years_into_dasha
            mahadasha_end = birth_date + timedelta(days=cumulative_years * 365.25)
            mahadasha_start = mahadasha_end - timedelta(days=planet_years * 365.25)
            break
    
    # Calculate Antardasha (sub-period)
    # Simplified version
    antardasha_planet = get_current_antardasha(
        current_mahadasha, 
        years_since_birth - (cumulative_years - dasha_years[current_mahadasha]),
        dasha_years,
        dasha_sequence
    )
    
    return {
        'mahadasha': {
            'planet': current_mahadasha,
            'start_date': mahadasha_start.strftime("%Y-%m-%d"),
            'end_date': mahadasha_end.strftime("%Y-%m-%d"),
            'years_remaining': round(years_remaining, 2),
            'total_years': dasha_years[current_mahadasha]
        },
        'antardasha': antardasha_planet,
        'birth_nakshatra_lord': starting_planet,
        'interpretation': get_dasha_interpretation(current_mahadasha, kundli)
    }

def get_current_antardasha(mahadasha_planet, years_into_mahadasha, dasha_years, dasha_sequence):
    """
    Calculate current Antardasha (simplified)
    """
    # In actual Vimshottari, Antardasha follows the same sequence
    # Each Antardasha duration = (Mahadasha years * Antardasha years) / 120
    
    # Simplified: return next planet in sequence
    index = dasha_sequence.index(mahadasha_planet)
    antardasha_index = (index + int(years_into_mahadasha * 3)) % len(dasha_sequence)
    
    return {
        'planet': dasha_sequence[antardasha_index],
        'note': 'Simplified calculation - actual Antardasha requires precise timing'
    }

def get_dasha_interpretation(planet, kundli):
    """
    Get general interpretation of planetary Dasha
    """
    interpretations = {
        'Sun': {
            'general': 'Period of authority, recognition, and father-related matters',
            'positive': 'Leadership opportunities, career growth, govt. favor',
            'challenges': 'Ego conflicts, health of father, authority disputes'
        },
        'Moon': {
            'general': 'Period of emotions, mother, mind, and public dealings',
            'positive': 'Emotional fulfillment, property gains, popularity',
            'challenges': 'Mental stress, mood swings, mother\'s health'
        },
        'Mars': {
            'general': 'Period of energy, courage, property, and siblings',
            'positive': 'Property acquisition, courage, victory over enemies',
            'challenges': 'Accidents, conflicts, anger issues, surgery'
        },
        'Mercury': {
            'general': 'Period of intellect, communication, business, and learning',
            'positive': 'Business success, education, writing, skill development',
            'challenges': 'Overthinking, nervous issues, communication problems'
        },
        'Jupiter': {
            'general': 'Period of wisdom, expansion, children, and spirituality',
            'positive': 'Marriage, children, spiritual growth, higher education',
            'challenges': 'Over-optimism, weight gain, expenses on good causes'
        },
        'Venus': {
            'general': 'Period of luxury, relationships, arts, and comfort',
            'positive': 'Marriage, romance, artistic success, material comforts',
            'challenges': 'Over-indulgence, relationship complications'
        },
        'Saturn': {
            'general': 'Period of discipline, hard work, karma, and delays',
            'positive': 'Long-term success, discipline, karmic rewards',
            'challenges': 'Delays, obstacles, health issues, hard lessons'
        },
        'Rahu': {
            'general': 'Period of ambition, foreign connections, and sudden changes',
            'positive': 'Foreign opportunities, unconventional success, research',
            'challenges': 'Confusion, deception, sudden upheavals'
        },
        'Ketu': {
            'general': 'Period of spirituality, detachment, and past-life karma',
            'positive': 'Spiritual awakening, research, occult knowledge',
            'challenges': 'Losses, isolation, confusion, health issues'
        }
    }
    
    # Check planet's house position for additional context
    planet_house = None
    for house_num, planets in kundli['houses'].items():
        for p in planets:
            if p['planet'] == planet:
                planet_house = house_num
                break
    
    interp = interpretations.get(planet, {})
    
    if planet_house:
        house_meanings = {
            1: 'self, personality, health',
            2: 'wealth, family, speech',
            3: 'courage, siblings, efforts',
            4: 'mother, property, happiness',
            5: 'children, creativity, education',
            6: 'enemies, debts, health challenges',
            7: 'marriage, partnerships, business',
            8: 'longevity, transformation, occult',
            9: 'luck, father, higher learning',
            10: 'career, status, reputation',
            11: 'gains, friends, aspirations',
            12: 'losses, expenses, spirituality'
        }
        
        interp['house_influence'] = f"Planet in {planet_house}th house emphasizes: {house_meanings.get(planet_house, 'various matters')}"
    
    return interp

def print_dasha_report(dasha_info):
    """
    Print formatted Dasha analysis
    """
    print("\n" + "="*70)
    print("                   VIMSHOTTARI DASHA ANALYSIS")
    print("="*70)
    
    maha = dasha_info['mahadasha']
    print(f"\n🔮 Current Mahadasha: {maha['planet']}")
    print(f"   Period: {maha['start_date']} to {maha['end_date']}")
    print(f"   Duration: {maha['total_years']} years total")
    print(f"   Remaining: {maha['years_remaining']} years")
    
    print(f"\n🌙 Current Antardasha: {dasha_info['antardasha']['planet']}")
    print(f"   Note: {dasha_info['antardasha']['note']}")
    
    print(f"\n📊 Birth Nakshatra Lord: {dasha_info['birth_nakshatra_lord']}")
    
    interp = dasha_info['interpretation']
    print(f"\n📖 {maha['planet']} Mahadasha Interpretation:")
    print(f"   General: {interp.get('general', 'N/A')}")
    print(f"   ✓ Positive: {interp.get('positive', 'N/A')}")
    print(f"   ⚠ Challenges: {interp.get('challenges', 'N/A')}")
    
    if 'house_influence' in interp:
        print(f"   🏠 {interp['house_influence']}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    from GenerateKundli import generate_kundli
    
    birth_datetime = {
        "date": "1995-08-15",
        "time": "10:30:00"
    }
    
    birth_location = {
        "name": "Delhi",
        "latitude": 28.6139,
        "longitude": 77.2090
    }
    
    kundli = generate_kundli(birth_datetime, birth_location)
    
    dasha = calculate_vimshottari_dasha(kundli, "2026-01-19")
    
    print_dasha_report(dasha)