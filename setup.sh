#!/bin/bash

# VedicAI Development Setup Script

echo "🌟 VedicAI FastAPI + React Setup"
echo "================================"

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
echo "✓ Python version: $python_version"

# Setup Backend
echo ""
echo "📦 Setting up Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
echo "⚠️  Please update backend/.env with your DATABASE_URL and GEMINI_API_KEY"
cd ..

# Setup Frontend
echo ""
echo "📦 Setting up Frontend..."
cd frontend
npm install
echo "✓ Frontend dependencies installed"
cd ..

echo ""
echo "================================"
echo "✓ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Update backend/.env with your credentials"
echo "2. Terminal 1: cd backend && source venv/bin/activate && python main.py"
echo "3. Terminal 2: cd frontend && npm run dev"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "API Documentation: http://localhost:8000/docs"
