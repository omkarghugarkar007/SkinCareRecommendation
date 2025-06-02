#!/bin/bash

# Colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Starting setup for SkinCare Recommendation System...${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}❌ Python 3 is required but not installed. Please install Python 3.8 or higher and try again.${NC}"
    exit 1
fi

# Create virtual environment
echo -e "${GREEN}🛠 Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo -e "${GREEN}📦 Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "${GREEN}📦 Installing dependencies...${NC}"
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${GREEN}📄 Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit the .env file and add your OpenAI API key.${NC}"
else
    echo -e "${GREEN}✅ .env file already exists.${NC}"
fi

echo -e "\n${GREEN}✨ Setup completed successfully!${NC}"
echo -e "\nTo start the application, run the following commands in separate terminals:"
echo -e "1. ${YELLOW}source venv/bin/activate${NC}"
echo -e "2. ${YELLOW}uvicorn api:app --reload --port 8000${NC}"
echo -e "3. ${YELLOW}streamlit run app.py${NC}"
echo -e "\n🌐 Access the application at ${GREEN}http://localhost:8501${NC}"
