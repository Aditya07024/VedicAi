import sys
import os

# Add project root and kundliGenerator to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "kundliGenerator"))

import sys
import os

# Add paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWISS_EPHEMERIS_PATH = os.path.join(BASE_DIR, "Swiss_Ephemeris")
sys.path.append(SWISS_EPHEMERIS_PATH)

def detect_doshas(kundli):
    """
    Detect various doshas in the kundli
    """
    doshas = []
    
    # 1. Mangal Dosha
    mangal_dosha = check_mangal_dosha(kundli)
    if mangal_dosha:
        doshas.append(mangal_dosha)
    
    # 2. Kaal Sarp Dosha
    kaal_sarp = check_kaal_sarp_dosha(kundli)
    if kaal_sarp:
        doshas.append(kaal_sarp)
    
    # 3. Sade Sati
    sade_sati = check_sade_sati(kundli)
    if sade_sati:
        doshas.append(sade_sati)
    
    return doshas

def check_mangal_dosha(kundli):
    """
    Mangal Dosha occurs when Mars is in houses 1, 4, 7, 8, or 12
    """
    mars_house = None
    
    # Find which house Mars is in
    for house_num, planets in kundli['houses'].items():
        for planet in planets:
            if planet['planet'] == 'Mars':
                mars_house = house_num
                break
    
    if mars_house in [1, 4, 7, 8, 12]:
        severity = calculate_mangal_severity(kundli, mars_house)
        
        return {
            'name': 'Mangal Dosha',
            'detected': True,
            'severity': severity,
            'house': mars_house,
            'description': f'Mars is placed in the {mars_house}th house',
            'impact': 'May cause delays or challenges in marriage and relationships',
            'remedies': [
                'Recite Hanuman Chalisa daily',
                'Fast on Tuesdays',
                'Donate red lentils on Tuesdays',
                'Visit Hanuman temple',
                'Wear red coral (after astrological consultation)'
            ],
            'cancellations': check_mangal_cancellations(kundli)
        }
    
    return None

def calculate_mangal_severity(kundli, mars_house):
    """
    Calculate severity based on house and other factors
    """
    # Houses 1, 8, 12 are more severe than 4, 7
    if mars_house in [1, 8, 12]:
        base_severity = 'High'
    else:
        base_severity = 'Medium'
    
    # Check if Mars is in own sign or exalted (reduces severity)
    mars_data = kundli['planets']['Mars']
    mars_rashi = mars_data['rashi']
    
    # Mars owns Aries and Scorpio, exalted in Capricorn
    if mars_rashi in ['Aries', 'Scorpio', 'Capricorn']:
        if base_severity == 'High':
            return 'Medium'
        else:
            return 'Low'
    
    return base_severity

def check_mangal_cancellations(kundli):
    """
    Check for conditions that cancel or reduce Mangal Dosha
    """
    cancellations = []
    
    # 1. If Mars is in own sign
    mars_rashi = kundli['planets']['Mars']['rashi']
    if mars_rashi in ['Aries', 'Scorpio']:
        cancellations.append('Mars in own sign (reduces severity)')
    
    # 2. If Mars is exalted
    if mars_rashi == 'Capricorn':
        cancellations.append('Mars is exalted (reduces severity)')
    
    # 3. If Jupiter aspects Mars (needs aspect calculation - placeholder)
    # cancellations.append('Jupiter aspects Mars (reduces severity)')
    
    return cancellations if cancellations else ['No major cancellations detected']

def check_kaal_sarp_dosha(kundli):
    """
    Kaal Sarp Dosha: All planets on one side of Rahu-Ketu axis
    """
    rahu_long = kundli['planets']['Rahu']['longitude']
    ketu_long = kundli['planets']['Ketu']['longitude']
    
    # Check all planets except Rahu and Ketu
    planets_to_check = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
    
    all_between_rahu_ketu = True
    
    for planet in planets_to_check:
        planet_long = kundli['planets'][planet]['longitude']
        
        # Calculate if planet is between Rahu and Ketu
        # This is a simplified check
        angle_from_rahu = (planet_long - rahu_long) % 360
        
        # If any planet is NOT between Rahu (0°) and Ketu (180°)
        if not (0 < angle_from_rahu < 180):
            all_between_rahu_ketu = False
            break
    
    if all_between_rahu_ketu:
        return {
            'name': 'Kaal Sarp Dosha',
            'detected': True,
            'severity': 'Medium to High',
            'description': 'All planets positioned between Rahu and Ketu axis',
            'impact': 'May cause obstacles, delays, and challenges in life',
            'remedies': [
                'Recite Mahamrityunjaya Mantra',
                'Visit Kaal Sarp Dosha temples (Trimbakeshwar, Ujjain)',
                'Perform Kaal Sarp Dosha Puja',
                'Donate on Nag Panchami',
                'Wear Gomed (Hessonite) after consultation'
            ]
        }
    
    return None

def check_sade_sati(kundli):
    """
    Sade Sati: Saturn transiting 12th, 1st, or 2nd house from Moon
    This requires current Saturn position (transit)
    For birth chart analysis, we check natal positions
    """
    # Get Moon's house
    moon_house = None
    for house_num, planets in kundli['houses'].items():
        for planet in planets:
            if planet['planet'] == 'Moon':
                moon_house = house_num
                break
    
    # Get Saturn's house
    saturn_house = None
    for house_num, planets in kundli['houses'].items():
        for planet in planets:
            if planet['planet'] == 'Saturn':
                saturn_house = house_num
                break
    
    if moon_house and saturn_house:
        # Check if Saturn is in 12th, 1st, or 2nd from Moon
        relative_position = (saturn_house - moon_house) % 12
        
        if relative_position in [0, 1, 11]:  # 1st, 2nd, or 12th house from Moon
            phase = {
                11: 'Rising Phase (12th from Moon)',
                0: 'Peak Phase (1st from Moon)',
                1: 'Setting Phase (2nd from Moon)'
            }
            
            return {
                'name': 'Sade Sati',
                'detected': True,
                'phase': phase.get(relative_position, 'Unknown'),
                'severity': 'Medium',
                'description': f'Saturn in {saturn_house}th house, Moon in {moon_house}th house',
                'impact': 'Period of challenges, tests, and karmic lessons',
                'remedies': [
                    'Recite Shani Stotra or Hanuman Chalisa',
                    'Donate to the needy on Saturdays',
                    'Feed crows and dogs',
                    'Wear blue sapphire (only after proper consultation)',
                    'Light mustard oil lamp on Saturdays'
                ]
            }
    
    return None

def get_planet_house(kundli, planet_name):
    """Helper function to find which house a planet is in"""
    for house_num, planets in kundli['houses'].items():
        for planet in planets:
            if planet['planet'] == planet_name:
                return house_num
    return None

def print_dosha_report(doshas):
    """
    Print a formatted dosha analysis report
    """
    print("\n" + "="*60)
    print("             DOSHA ANALYSIS REPORT")
    print("="*60)
    
    if not doshas:
        print("\n✅ No major doshas detected in the chart!")
        print("\nThis is a favorable indication.")
    else:
        print(f"\n⚠️  {len(doshas)} Dosha(s) detected:\n")
        
        for i, dosha in enumerate(doshas, 1):
            print(f"\n{i}. {dosha['name']}")
            print("-" * 60)
            print(f"   Severity: {dosha['severity']}")
            print(f"   Description: {dosha['description']}")
            print(f"   Impact: {dosha['impact']}")
            
            if 'phase' in dosha:
                print(f"   Phase: {dosha['phase']}")
            
            if 'house' in dosha:
                print(f"   House: {dosha['house']}")
            
            if 'cancellations' in dosha and dosha['cancellations']:
                print(f"\n   ✓ Mitigating Factors:")
                for cancel in dosha['cancellations']:
                    print(f"     • {cancel}")
            
            print(f"\n   📿 Remedies:")
            for remedy in dosha['remedies']:
                print(f"     • {remedy}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    # Test with your existing kundli
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
    
    doshas = detect_doshas(kundli)
    
    print_dosha_report(doshas)