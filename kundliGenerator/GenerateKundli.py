import sys
import os

from datetime import datetime
import pytz

def get_rashi(longitude):
    rashis = [
        "Aries", "Taurus", "Gemini", "Cancer",
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    return rashis[int(longitude // 30)]


def get_nakshatra(longitude):
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
        "Ardra", "Punarvasu", "Pushya", "Ashlesha",
        "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishakha",
        "Anuradha", "Jyeshtha", "Mula",
        "Purva Ashadha", "Uttara Ashadha", "Shravana",
        "Dhanishta", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    return nakshatras[int(longitude / 13.333333)]

# Add Swiss_Ephemeris directory to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWISS_EPHEMERIS_PATH = os.path.join(BASE_DIR, "Swiss_Ephemeris")
sys.path.append(SWISS_EPHEMERIS_PATH)
from Swiss_Ephemeris import get_planetary_positions

# --- Aspects Calculation Stub ---
def calculate_aspects(positions):
    """
    Calculate basic Vedic aspects (Drishti)
    For now, this returns a simple placeholder structure
    to keep the Kundli generation pipeline working.
    """
    aspects = {}

    for planet in positions.keys():
        aspects[planet] = {
            "aspects": [],
            "note": "Detailed Vedic Drishti logic to be implemented"
        }

    return aspects

def generate_kundli(birth_datetime, birth_location):
    """
    Create complete birth chart (Kundli)
    """
    
    # Step 1: Get planetary positions
    positions = get_planetary_positions(
        birth_datetime['date'],
        birth_datetime['time'],
        birth_location['latitude'],
        birth_location['longitude']
    )
    
    # Step 2: Calculate Lagna (Ascendant)
    # This is the zodiac sign rising on eastern horizon at birth time
    lagna = calculate_ascendant(
        birth_datetime,
        birth_location
    )
    
    # Step 3: Assign planets to houses
    # House 1 starts from Lagna
    houses = assign_planets_to_houses(positions, lagna)
    
    # Step 4: Calculate aspects (Drishti)
    aspects = calculate_aspects(positions)
    
    kundli = {
        'birth_details': {
            'date': birth_datetime['date'],
            'time': birth_datetime['time'],
            'place': birth_location['name']
        },
        'lagna': lagna,
        'planets': positions,
        'houses': houses,
        'aspects': aspects
    }
    
    return kundli

def calculate_ascendant(birth_datetime, location):
    """
    Calculate rising sign (Lagna)
    This requires sidereal time calculation
    """
    import swisseph as swe
    
    # Convert to Julian Day
    dt = datetime.strptime(
        f"{birth_datetime['date']} {birth_datetime['time']}", 
        "%Y-%m-%d %H:%M:%S"
    )
    dt = pytz.timezone('Asia/Kolkata').localize(dt)
    dt_utc = dt.astimezone(pytz.UTC)
    
    jd = swe.julday(
        dt_utc.year, dt_utc.month, dt_utc.day,
        dt_utc.hour + dt_utc.minute/60.0 + dt_utc.second/3600.0
    )
    
    # Calculate houses using Placidus system
    houses_result = swe.houses(
        jd,
        location['latitude'],
        location['longitude'],
        b'P'  # Placidus house system
    )
    
    ascendant_longitude = houses_result[1][0]  # First house cusp
    
    return {
        'longitude': ascendant_longitude,
        'rashi': get_rashi(ascendant_longitude),
        'nakshatra': get_nakshatra(ascendant_longitude)
    }

def assign_planets_to_houses(positions, lagna):
    """
    Determine which house each planet falls in
    """
    lagna_longitude = lagna['longitude']
    
    houses = {i: [] for i in range(1, 13)}
    
    for planet, data in positions.items():
        planet_longitude = data['longitude']
        
        # Calculate house number
        # Difference from Lagna determines house
        difference = (planet_longitude - lagna_longitude) % 360
        house_number = int(difference / 30) + 1
        
        houses[house_number].append({
            'planet': planet,
            'longitude': planet_longitude,
            'rashi': data['rashi']
        })
    
    return houses

def generate_kundli_chart(kundli):
    """
    Generate a simple North Indian style text chart for Kundli
    """
    lagna_rashi = kundli['lagna']['rashi']
    houses = kundli['houses']

    chart = {}
    for house_no, planets in houses.items():
        if planets:
            chart[house_no] = ", ".join([p['planet'] for p in planets])
        else:
            chart[house_no] = "-"

    return {
        "lagna": lagna_rashi,
        "house_chart": chart
    }


# --- ASCII North Indian Chart Printer ---
def print_ascii_north_indian_chart(kundli_chart):
    """
    Print an ASCII North Indian style Kundli chart in terminal
    House positions are fixed; planets are shown inside houses
    """
    h = kundli_chart["house_chart"]
    lagna = kundli_chart["lagna"]

    print("\n=== ASCII NORTH INDIAN KUNDLI CHART ===\n")
    print(f"                 [10] {h[10]}")
    print("        -----------------------------")
    print(f"        | [11] {h[11]:<12} | [9] {h[9]:<12} |")
    print("        |-----------------------------|")
    print(f"        | [12] {h[12]:<12} | [8] {h[8]:<12} |")
    print("        -----------------------------")
    print(f" [1] {h[1]:<12}        LAGNA ({lagna})        [7] {h[7]:<12}")
    print("        -----------------------------")
    print(f"        | [2] {h[2]:<12} | [6] {h[6]:<12} |")
    print("        |-----------------------------|")
    print(f"        | [3] {h[3]:<12} | [5] {h[5]:<12} |")
    print("        -----------------------------")
    print(f"                 [4] {h[4]}")

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

    kundli = generate_kundli(birth_datetime, birth_location)

    from pprint import pprint
    print("\n=== GENERATED KUNDLI ===\n")
    pprint(kundli)

    print("\n=== KUNDLI CHART (HOUSE WISE) ===\n")
    kundli_chart = generate_kundli_chart(kundli)
    pprint(kundli_chart)
    print_ascii_north_indian_chart(kundli_chart)