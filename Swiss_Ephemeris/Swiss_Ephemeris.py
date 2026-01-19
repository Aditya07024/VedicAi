import swisseph as swe
from datetime import datetime
import pytz
swe.set_sid_mode(swe.SIDM_LAHIRI)

def get_planetary_positions(date, time, latitude, longitude):
    # Convert to Julian Day (astronomical time format)
    dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
    dt = pytz.timezone('Asia/Kolkata').localize(dt)
    dt_utc = dt.astimezone(pytz.UTC)
    
    jd = swe.julday(
        dt_utc.year, 
        dt_utc.month, 
        dt_utc.day,
        dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
    )
    
    # Calculate positions for all planets
    planets = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mars': swe.MARS,
        'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER,
        'Venus': swe.VENUS,
        'Saturn': swe.SATURN,
        'Rahu': swe.TRUE_NODE,  # North Node
        'Ketu': swe.TRUE_NODE   # South Node (180° from Rahu)
    }
    
    positions = {}
    for planet_name, planet_id in planets.items():
        # Get ecliptic longitude
        result = swe.calc_ut(jd, planet_id)
        longitude = result[0][0]  # Degrees (0-360)
        
        if planet_name == 'Ketu':
            longitude = (longitude + 180) % 360  # Opposite of Rahu
        
        positions[planet_name] = {
            'longitude': longitude,
            'rashi': get_rashi(longitude),
            'nakshatra': get_nakshatra(longitude),
            'degrees': longitude % 30  # Degrees within sign
        }
    
    return positions

def get_rashi(longitude):
    """Convert longitude to Rashi (zodiac sign)"""
    rashis = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 
        'Leo', 'Virgo', 'Libra', 'Scorpio',
        'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    return rashis[int(longitude / 30)]

def get_nakshatra(longitude):
    """Convert longitude to Nakshatra (lunar mansion)"""
    nakshatras = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira',
        'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha', 'Magha',
        'Purva Phalguni', 'Uttara Phalguni', 'Hasta', 'Chitra',
        'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula',
        'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta',
        'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ]
    # Each nakshatra spans 13°20' (13.333°)
    return nakshatras[int(longitude / 13.333333)]

if __name__ == "__main__":
    data = get_planetary_positions(
        "2028-01-15",
        "9:52:00",
        28.6139,
        77.2090
    )

    from pprint import pprint
    # print("\n=== TEST OUTPUT (Delhi, 15 Aug 1995, 10:30 AM IST) ===\n")
    pprint(data)