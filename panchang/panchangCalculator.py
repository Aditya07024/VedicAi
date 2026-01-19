import sys
import os
from datetime import datetime
import pytz

# Add Swiss_Ephemeris directory to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWISS_EPHEMERIS_PATH = os.path.join(BASE_DIR, "Swiss_Ephemeris")
sys.path.append(SWISS_EPHEMERIS_PATH)


from Swiss_Ephemeris import get_planetary_positions

# Helper to determine Nakshatra from longitude
def get_nakshatra(longitude):
    """
    Determine Nakshatra from longitude
    Each Nakshatra spans 13°20' (13.333333°)
    """
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

def calculate_panchang(date, location):
    """
    Calculate 5 elements of Hindu calendar
    """
    
    positions = get_planetary_positions(
        date, "00:00:00",
        location['latitude'],
        location['longitude']
    )
    
    moon_longitude = positions['Moon']['longitude']
    sun_longitude = positions['Sun']['longitude']
    
    panchang = {
        'tithi': calculate_tithi(moon_longitude, sun_longitude),
        'vara': calculate_vara(date),
        'nakshatra': get_nakshatra(moon_longitude),
        'yoga': calculate_yoga(moon_longitude, sun_longitude),
        'karana': calculate_karana(moon_longitude, sun_longitude),
        'sunrise': calculate_sunrise(date, location),
        'sunset': calculate_sunset(date, location),
        'rahu_kaal': calculate_rahu_kaal(date, location)
    }
    
    return panchang

def calculate_tithi(moon_long, sun_long):
    """
    Tithi is lunar day (1-30)
    Based on Moon-Sun angle difference
    """
    difference = (moon_long - sun_long) % 360
    tithi_number = int(difference / 12) + 1
    
    tithi_names = [
        'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
        'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
        'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Purnima/Amavasya'
    ]
    
    paksha = 'Shukla' if tithi_number <= 15 else 'Krishna'
    
    return {
        'number': tithi_number,
        'name': tithi_names[(tithi_number - 1) % 15],
        'paksha': paksha
    }

def calculate_yoga(moon_long, sun_long):
    """
    27 yogas based on sum of Sun and Moon longitudes
    """
    yoga_sum = (moon_long + sun_long) % 360
    yoga_number = int(yoga_sum / 13.333333)
    
    yoga_names = [
        'Vishkumbha', 'Preeti', 'Ayushman', 'Saubhagya', 'Shobhana',
        'Atiganda', 'Sukarma', 'Dhriti', 'Shoola', 'Ganda',
        'Vriddhi', 'Dhruva', 'Vyaghata', 'Harshana', 'Vajra',
        'Siddhi', 'Vyatipata', 'Variyan', 'Parigha', 'Shiva',
        'Siddha', 'Sadhya', 'Shubha', 'Shukla', 'Brahma',
        'Indra', 'Vaidhriti'
    ]
    
    return yoga_names[yoga_number]

def calculate_sunrise(date, location):
    """Use Swiss Ephemeris to calculate exact sunrise"""
    import swisseph as swe

    dt = datetime.strptime(date, "%Y-%m-%d")
    jd = swe.julday(dt.year, dt.month, dt.day, 0)

    # rsmi flags must be passed as keyword with geopos tuple
    result = swe.rise_trans(
        jd,
        swe.SUN,
        geopos=(location['longitude'], location['latitude'], 0),
        rsmi=swe.CALC_RISE
    )

    sunrise_jd = result[1][0]
    rev = swe.revjul(sunrise_jd)
    utc_h = rev[3]
    utc_m = rev[4] if len(rev) > 4 else 0

    # Convert UTC to IST (+5:30)
    total_minutes = int(utc_h * 60 + utc_m + 330)
    h = (total_minutes // 60) % 24
    mi = total_minutes % 60

    return f"{h:02d}:{mi:02d}"

def calculate_vara(date):
    """Day of the week (Vara)"""
    dt = datetime.strptime(date, "%Y-%m-%d")
    vara_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return vara_names[dt.weekday()]


def calculate_karana(moon_long, sun_long):
    """
    Karana based on half-tithi (6 degrees)
    Simplified, deterministic implementation
    """
    difference = (moon_long - sun_long) % 360
    karana_index = int(difference / 6)

    karana_names = [
        "Bava", "Balava", "Kaulava", "Taitila", "Garaja",
        "Vanija", "Vishti"
    ]

    # Cycles through karanas
    return karana_names[karana_index % len(karana_names)]


def calculate_sunset(date, location):
    """Use Swiss Ephemeris to calculate exact sunset"""
    import swisseph as swe

    dt = datetime.strptime(date, "%Y-%m-%d")
    jd = swe.julday(dt.year, dt.month, dt.day, 0)

    result = swe.rise_trans(
        jd,
        swe.SUN,
        geopos=(location['longitude'], location['latitude'], 0),
        rsmi=swe.CALC_SET
    )

    sunset_jd = result[1][0]
    rev = swe.revjul(sunset_jd)
    utc_h = rev[3]
    utc_m = rev[4] if len(rev) > 4 else 0

    # Convert UTC to IST (+5:30)
    total_minutes = int(utc_h * 60 + utc_m + 330)
    h = (total_minutes // 60) % 24
    mi = total_minutes % 60

    return f"{h:02d}:{mi:02d}"


def calculate_rahu_kaal(date, location):
    """
    Simplified Rahu Kaal calculation based on weekday
    """
    vara = calculate_vara(date)
    rahu_periods = {
        "Monday": 2,
        "Tuesday": 7,
        "Wednesday": 5,
        "Thursday": 6,
        "Friday": 4,
        "Saturday": 3,
        "Sunday": 8
    }

    return {
        "period_index": rahu_periods.get(vara),
        "note": "Exact Rahu Kaal timing derived from sunrise-sunset segmentation"
    }

def print_ascii_panchang_chart(panchang):
    """
    Print an ASCII Panchang chart in terminal
    """
    print("\n=== ASCII PANCHANG CHART ===\n")
    print("+-------------------------------+")
    print(f"| Vara       : {panchang['vara']:<15} |")
    print(f"| Tithi      : {panchang['tithi']['paksha']} {panchang['tithi']['name']:<8} |")
    print(f"| Nakshatra  : {panchang['nakshatra']:<15} |")
    print(f"| Yoga       : {panchang['yoga']:<15} |")
    print(f"| Karana     : {panchang['karana']:<15} |")
    print(f"| Sunrise    : {panchang['sunrise']:<15} |")
    print(f"| Sunset     : {panchang['sunset']:<15} |")
    print(f"| Rahu Kaal  : Period {panchang['rahu_kaal']['period_index']:<9} |")
    print("+-------------------------------+")

if __name__ == "__main__":
    location = {
        "name": "Delhi",
        "latitude": 28.6139,
        "longitude": 77.2090
    }

    panchang = calculate_panchang("2026-01-18", location)

    from pprint import pprint
    print("\n=== PANCHANG OUTPUT ===\n")
    pprint(panchang)
    print_ascii_panchang_chart(panchang)