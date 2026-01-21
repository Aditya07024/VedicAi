#!/usr/bin/env python3
"""
Quick test to verify Gemini API integration.
Run this before starting the Streamlit app.
"""

import os
from dotenv import load_dotenv

print("[TEST] Testing Gemini API integration...")
print("=" * 60)

# Load environment
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    print("❌ [FAIL] GEMINI_API_KEY not found in .env file")
    print("\nSolution:")
    print("1. Create a .env file in the project root")
    print("2. Add: GEMINI_API_KEY=your_actual_key")
    print("3. Get your key from: https://ai.google.dev/")
    exit(1)

print("✅ [PASS] GEMINI_API_KEY found in environment")
print(f"   Key starts with: {GEMINI_API_KEY[:10]}...")

# Test client initialization
try:
    from google import genai
    print("✅ [PASS] google.genai imported successfully")
except ImportError as e:
    print(f"❌ [FAIL] Could not import google.genai: {e}")
    exit(1)

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("✅ [PASS] Gemini client initialized successfully")
except Exception as e:
    print(f"❌ [FAIL] Could not initialize Gemini client: {e}")
    exit(1)

# Test a simple API call
try:
    print("\n[TEST] Making a test API call...")
    test_prompt = "Respond with just one word: hello"
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=test_prompt
    )
    
    print(f"✅ [PASS] API call successful!")
    print(f"   Response: {response.text.strip()}")
    
except Exception as e:
    print(f"❌ [FAIL] API call failed: {type(e).__name__}: {str(e)}")
    print("\nPossible solutions:")
    print("1. Check your GEMINI_API_KEY is correct")
    print("2. Verify you have API quota available")
    print("3. Check your internet connection")
    exit(1)

print("\n" + "=" * 60)
print("✅ All tests passed! Gemini API is ready to use.")
print("\nYou can now run: streamlit run app.py")
