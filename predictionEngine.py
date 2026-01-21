"""
predictionEngine.py
-------------------
Rule-based, deterministic prediction engine.
NO Streamlit code should exist in this file.
"""

def generate_predictions(kundli, dasha, doshas):
    """
    Generate structured, time-bound predictions
    based on verified Kundli, Dasha, and Dosha data.
    """

    predictions = {
        "career": generate_career_prediction(kundli, dasha, doshas),
        "marriage": generate_marriage_prediction(kundli, dasha, doshas)
    }

    return predictions


def generate_career_prediction(kundli, dasha, doshas):
    tenth_house = kundli["houses"].get(10, [])
    mahadasha = dasha["mahadasha"]["planet"]

    confidence = 70
    outlook = "Moderately Favorable"

    if mahadasha in ["Sun", "Mars", "Jupiter"]:
        confidence += 10
        outlook = "Favorable"

    if any(d["name"] == "Mangal Dosha" for d in doshas):
        confidence -= 5

    return {
        "area": "Career",
        "outlook": outlook,
        "confidence": max(0, min(confidence, 100)),
        "factors": [
            {
                "name": "10th House",
                "description": f"Planets present: {', '.join(p['planet'] for p in tenth_house) or 'None'}",
                "strength": 70,
                "weight": 0.4
            },
            {
                "name": "Current Mahadasha",
                "description": mahadasha,
                "strength": 75,
                "weight": 0.6
            }
        ],
        "timeline": [
            {
                "period": "Next 6 months",
                "prediction": "Gradual progress with learning opportunities",
                "confidence": confidence
            },
            {
                "period": "6–12 months",
                "prediction": "Stability and role clarity improve",
                "confidence": confidence
            }
        ],
        "recommendations": [
            "Focus on skill-building",
            "Avoid impulsive job changes",
            "Maintain consistency in efforts"
        ]
    }


def generate_marriage_prediction(kundli, dasha, doshas):
    seventh_house = kundli["houses"].get(7, [])
    mahadasha = dasha["mahadasha"]["planet"]

    confidence = 65
    outlook = "Needs Patience"

    if mahadasha in ["Venus", "Jupiter", "Moon"]:
        confidence += 10
        outlook = "Supportive Period"

    if any(d["name"] == "Mangal Dosha" for d in doshas):
        confidence -= 10

    return {
        "area": "Marriage",
        "outlook": outlook,
        "confidence": max(0, min(confidence, 100)),
        "factors": [
            {
                "name": "7th House",
                "description": f"Planets present: {', '.join(p['planet'] for p in seventh_house) or 'None'}",
                "strength": 65
            },
            {
                "name": "Current Mahadasha",
                "description": mahadasha,
                "strength": 70
            }
        ],
        "timeline": [
            {
                "period": "Next 12 months",
                "prediction": "Emotional clarity improves before commitments"
            }
        ],
        "recommendations": [
            "Communicate expectations clearly",
            "Avoid rushed decisions",
            "Focus on emotional compatibility"
        ]
    }