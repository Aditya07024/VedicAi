#!/bin/bash

# VedicAI macOS Setup Helper

echo "🍎 VedicAI - macOS Setup Helper"
echo "================================"

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install PostgreSQL if not present
if ! command -v psql &> /dev/null; then
    echo "📦 Installing PostgreSQL development tools..."
    brew install postgresql
else
    echo "✓ PostgreSQL already installed"
fi

# Reinstall backend dependencies
echo ""
echo "📦 Reinstalling backend dependencies..."
cd backend

# Remove old venv if it exists
if [ -d "venv" ]; then
    rm -rf venv
    echo "✓ Removed old virtual environment"
fi

# Create fresh venv
python3 -m venv venv
source venv/bin/activate

# Upgrade pip first
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Created backend/.env - Please add your DATABASE_URL and GEMINI_API_KEY"
else
    echo "✓ backend/.env already exists"
fi

cd ..

# Setup frontend
echo ""
echo "📦 Setting up Frontend..."
cd frontend

# Remove old node_modules if needed
if [ -d "node_modules" ]; then
    echo "✓ Frontend dependencies already installed"
else
    npm install
    echo "✓ Frontend dependencies installed"
fi

cd ..

echo ""
echo "================================"
echo "✓ macOS Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your DATABASE_URL and GEMINI_API_KEY"
echo "2. Terminal 1: cd backend && source venv/bin/activate && python main.py"
echo "3. Terminal 2: cd frontend && npm run dev"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "API Documentation: http://localhost:8000/docs"
