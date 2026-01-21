#!/bin/bash
# Production Deployment Helper Script

echo "🚀 VedicAI Production Deployment Setup"
echo "======================================"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Git Setup
echo -e "${BLUE}Step 1: Git Repository${NC}"
if [ ! -d ".git" ]; then
    read -p "Git repo initialized? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git init
        git add .
        git commit -m "Initial commit: FastAPI + React VedicAI"
        echo -e "${GREEN}✓ Git repository initialized${NC}"
    fi
else
    echo -e "${GREEN}✓ Git repository exists${NC}"
fi

# 2. Environment Setup
echo -e "\n${BLUE}Step 2: Environment Variables${NC}"
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠️  Creating backend/.env from template${NC}"
    cp backend/.env.example backend/.env
    echo -e "${YELLOW}Please edit backend/.env with your credentials:${NC}"
    echo "  - DATABASE_URL: PostgreSQL connection string"
    echo "  - GEMINI_API_KEY: Your Gemini API key"
    read -p "Press Enter once you've updated backend/.env..."
else
    echo -e "${GREEN}✓ backend/.env exists${NC}"
fi

# 3. Build Check
echo -e "\n${BLUE}Step 3: Build Verification${NC}"
echo -e "${YELLOW}Building backend...${NC}"
cd backend
pip install -r requirements.txt > /dev/null 2>&1 && echo -e "${GREEN}✓ Backend dependencies installed${NC}" || echo "Backend build error"
cd ..

echo -e "${YELLOW}Building frontend...${NC}"
cd frontend
npm install > /dev/null 2>&1 && echo -e "${GREEN}✓ Frontend dependencies installed${NC}" || echo "Frontend build error"
npm run build > /dev/null 2>&1 && echo -e "${GREEN}✓ Frontend built successfully${NC}" || echo "Frontend build error"
cd ..

# 4. Deployment Options
echo -e "\n${BLUE}Step 4: Select Deployment Platform${NC}"
echo "1) Render.com (Recommended - Free)"
echo "2) AWS (ECS/Lambda)"
echo "3) Heroku"
echo "4) DigitalOcean App Platform"
echo "5) Manual Docker Setup"

read -p "Select option (1-5): " deploy_option

case $deploy_option in
    1)
        echo -e "\n${YELLOW}Render.com Deployment${NC}"
        echo "1. Push code to GitHub"
        echo "2. Go to https://render.com"
        echo "3. Create new Web Service for backend:"
        echo "   - Branch: main"
        echo "   - Start Command: cd backend && pip install -r requirements.txt && python main.py"
        echo "   - Environment: Add DATABASE_URL and GEMINI_API_KEY"
        echo "4. Create new Static Site for frontend:"
        echo "   - Branch: main"
        echo "   - Build Command: cd frontend && npm install && npm run build"
        echo "   - Publish Directory: frontend/dist"
        ;;
    2)
        echo -e "\n${YELLOW}AWS ECS Deployment${NC}"
        echo "1. Install AWS CLI"
        echo "2. Create ECR repository: aws ecr create-repository --repository-name vedicai"
        echo "3. Build and push:"
        echo "   docker-compose build"
        echo "   docker tag vedicai:latest <account>.dkr.ecr.<region>.amazonaws.com/vedicai:latest"
        echo "   docker push <account>.dkr.ecr.<region>.amazonaws.com/vedicai:latest"
        echo "4. Create ECS task and service"
        ;;
    3)
        echo -e "\n${YELLOW}Heroku Deployment${NC}"
        echo "1. Install Heroku CLI"
        echo "2. Create Procfile with: web: cd backend && gunicorn main:app"
        echo "3. heroku create vedicai"
        echo "4. heroku config:set DATABASE_URL=..."
        echo "5. heroku config:set GEMINI_API_KEY=..."
        echo "6. git push heroku main"
        ;;
    4)
        echo -e "\n${YELLOW}DigitalOcean App Platform${NC}"
        echo "1. Push to GitHub"
        echo "2. Go to DigitalOcean Apps"
        echo "3. Create app from GitHub repo"
        echo "4. Configure services (backend & frontend)"
        echo "5. Deploy"
        ;;
    5)
        echo -e "\n${YELLOW}Manual Docker Setup${NC}"
        echo "1. docker-compose build"
        echo "2. docker-compose push (to your registry)"
        echo "3. Deploy to any Docker-compatible host"
        ;;
esac

echo -e "\n${GREEN}✓ Deployment setup complete!${NC}"
