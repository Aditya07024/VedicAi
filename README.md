# VedicAi

An intelligent Vedic astrology platform that generates detailed Kundli (birth charts), analyzes planetary doshas, and provides personalized astrological insights using AI-powered analysis.

🌐 **Live App:** https://vedicai.onrender.com/  

## Overview

VedicAi combines ancient Vedic astrological principles with modern artificial intelligence to provide accurate and meaningful astrological readings. The platform calculates precise planetary positions using Swiss Ephemeris data, analyzes astrological doshas (afflictions), and generates comprehensive Kundli charts with AI-powered interpretations.

## Features

### Core Astrological Calculations

- **Kundli Generation**: Creates detailed birth charts based on date, time, and location of birth
- **Planetary Positions**: Calculates accurate positions of all planets using Swiss Ephemeris
- **Rashi & Nakshatra Mapping**: Determines zodiac signs and lunar mansions for all celestial bodies
- **House Calculations**: Computes all 12 astrological houses

### Dosha Analysis

- **Mangal Dosha**: Detects Mars afflictions in the birth chart
- **Kaal Sarp Dosha**: Identifies Rahu-Ketu axis afflictions
- **Pitra Dosha**: Analyzes ancestral debts
- **Papasamyama**: Evaluates malefic planetary combinations
- **Other Doshas**: Comprehensive detection of various astrological afflictions

### Advanced Features

- **Vimshottari Dasha**: Calculates planetary periods and sub-periods (Mahadashas and Antardashas)
- **Panchang Calculation**: Computes daily astrological almanac data (Tithi, Nakshatra, Yoga, Karana)
- **Kundli Visualization**: Generates interactive visual representations of the birth chart
- **PDF Reports**: Creates downloadable astrological reports
- **AI-Powered Insights**: Uses Google's Gemini API for intelligent interpretation of astrological data
- **Database Storage**: Stores calculations in PostgreSQL for future reference

## Tech Stack

### Backend

- **Python 3.x**: Core programming language
- **Streamlit**: Web application framework for interactive UI
- **Google Gemini API**: AI-powered astrological insights and analysis
- **pyswisseph**: Swiss Ephemeris bindings for accurate astronomical calculations
- **Plotly**: Interactive chart visualization
- **psycopg2**: PostgreSQL database connectivity
- **FPDF**: PDF report generation

### Database

- **PostgreSQL** (Neon): Cloud-hosted relational database
- Stores calculation history and user data

### Deployment

- **Render**: Cloud deployment platform
- **Docker**: Containerization support

## Project Structure

```
VedicAi/
├── app.py                      # Main Streamlit application
├── kundliGenerator/
│   └── GenerateKundli.py      # Kundli calculation and chart generation
├── dosha/
│   ├── doshaAnalyzer.py       # Dosha detection logic
│   ├── dashaCalculator.py     # Vimshottari dasha calculations
│   └── fullAnalysis.py        # Comprehensive astrological analysis
├── panchang/
│   └── panchangCalculator.py  # Panchang (almanac) calculations
├── Swiss_Ephemeris/
│   └── Swiss_Ephemeris.py     # Swiss Ephemeris wrapper
├── frontend/                   # Frontend assets and styling
├── backend/                    # Additional backend utilities
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python runtime version
├── render.yaml                 # Render deployment configuration
└── README.md                   # Project documentation
```

## Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL (or Neon account for cloud database)
- Google Gemini API key
- pip package manager

### Setup Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/Aditya07024/VedicAi.git
   cd VedicAi
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:

   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   DATABASE_URL=postgresql://user:password@host:port/dbname
   # OR individual database settings:
   POSTGRES_DB=your_db_name
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_HOST=your_db_host
   POSTGRES_PORT=5432
   ```

5. **Run the application**

   ```bash
   streamlit run app.py
   ```

6. **Access the application**
   Open your browser and go to `http://localhost:8501`

## Usage

### Generate a Kundli

1. Enter your birth details:
   - Date of birth
   - Time of birth (as accurate as possible)
   - Place of birth
   - Timezone

2. Click "Generate Kundli" to calculate:
   - Planetary positions
   - House placements
   - Rashi and Nakshatra mappings

3. View the results:
   - Interactive birth chart visualization
   - Astrological interpretations via AI
   - Detailed calculations

### Analyze Doshas

- The application automatically detects all applicable doshas
- Each dosha includes:
  - Description and significance
  - Astrological combinations that trigger it
  - Life implications and remedies

### Download Reports

- Generate PDF reports of your complete astrological analysis
- Includes Kundli chart, doshas, dasha periods, and AI insights

## API Integration

### Google Gemini API

The application uses Google's Gemini API to provide intelligent astrological insights:

- Interprets planetary placements
- Analyzes dosha combinations
- Generates personalized guidance

Ensure your API key is properly configured in the `.env` file.

## Database Schema

The application stores the following data in PostgreSQL:

- User input (birth details)
- Calculated planetary positions
- Kundli data (houses, rashis, nakshatras)
- Dosha analysis results
- Dasha periods
- Panchang calculations
- Generated reports

## Deployment

### Deploy to Render

1. Push your code to GitHub
2. Connect your repository to Render
3. Set environment variables in Render dashboard
4. Deploy using the `render.yaml` configuration

### Local Development

Use the provided `setup-macos.sh` script for macOS setup automation.

## Key Modules

### GenerateKundli.py

Calculates the birth chart with all planetary positions and house placements.

### doshaAnalyzer.py

Detects and analyzes various doshas in the birth chart.

### dashaCalculator.py

Computes Vimshottari dasha periods and sub-periods.

### panchangCalculator.py

Calculates daily astrological data (Tithi, Nakshatra, Yoga, Karana).

### Swiss_Ephemeris.py

Wrapper around Swiss Ephemeris library for astronomical calculations.

## Contributing

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with your improvements

## License

This project is open source. Please check the LICENSE file for details.

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

## Disclaimer

VedicAi is designed for educational and entertainment purposes. Astrological readings should not be considered as professional medical, financial, or legal advice. Always consult qualified professionals for important life decisions.

## Acknowledgments

- Swiss Ephemeris for accurate astronomical calculations
- Google Gemini API for AI-powered insights
- Streamlit for the interactive web framework
- The Vedic astrology community for traditional knowledge

---

**Version**: Phase 5  
**Last Updated**: January 2026  
**Repository**: https://github.com/Aditya07024/VedicAi
