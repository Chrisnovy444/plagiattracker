#!/bin/bash

# PLAGIATTRACKER - Startup Script
# Démarre tout automatiquement

set -e

echo "🚀 Démarrage de PLAGIATTRACKER..."
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Création du fichier .env...${NC}"
    cp .env.example .env

    # Generate secure passwords
    DB_PASS=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-32)
    REDIS_PASS=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-32)
    SECRET=$(openssl rand -base64 48 | tr -d "=+/" | cut -c1-48)

    # Update .env
    sed -i "s/your_secure_postgres_password_here/$DB_PASS/g" .env
    sed -i "s/your_secure_redis_password_here/$REDIS_PASS/g" .env
    sed -i "s/your_super_secret_key_min_32_characters_long/$SECRET/g" .env

    echo -e "${GREEN}✅ Fichier .env créé avec mots de passe sécurisés${NC}"
fi

# Start Docker containers
echo -e "${YELLOW}🐳 Démarrage PostgreSQL + Redis...${NC}"
docker-compose up -d postgres redis

# Wait for PostgreSQL
echo -e "${YELLOW}⏳ Attente PostgreSQL...${NC}"
sleep 5

# Check if backend venv exists
if [ ! -d "backend/venv" ]; then
    echo -e "${YELLOW}📦 Création environnement Python...${NC}"
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    cd ..
    echo -e "${GREEN}✅ Environnement Python créé${NC}"
fi

# Start backend
echo -e "${YELLOW}🔧 Démarrage backend FastAPI...${NC}"
cd backend
source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > ../backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../backend.pid
cd ..
echo -e "${GREEN}✅ Backend démarré (PID: $BACKEND_PID)${NC}"

# Wait for backend
sleep 3

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}📦 Installation dépendances frontend...${NC}"
    cd frontend
    npm install
    cd ..
    echo -e "${GREEN}✅ Dépendances frontend installées${NC}"
fi

# Start frontend
echo -e "${YELLOW}🎨 Démarrage frontend React...${NC}"
cd frontend
nohup npm run dev -- --host 0.0.0.0 > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../frontend.pid
cd ..
echo -e "${GREEN}✅ Frontend démarré (PID: $FRONTEND_PID)${NC}"

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 PLAGIATTRACKER démarré avec succès !${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}📋 URLs d'accès :${NC}"
echo -e "   Backend API : ${GREEN}http://localhost:8000${NC}"
echo -e "   API Docs    : ${GREEN}http://localhost:8000/docs${NC}"
echo -e "   Frontend    : ${GREEN}http://localhost:5173${NC}"
echo -e "   Tailscale   : ${GREEN}http://100.127.127.117:5173${NC}"
echo ""
echo -e "${YELLOW}📞 Contact :${NC}"
echo -e "   Email   : ${GREEN}checkone076@gmail.com${NC}"
echo -e "   WhatsApp: ${GREEN}+237 690895735${NC}"
echo ""
echo -e "${YELLOW}🛠️  Commandes utiles :${NC}"
echo -e "   Logs backend  : ${GREEN}tail -f backend.log${NC}"
echo -e "   Logs frontend : ${GREEN}tail -f frontend.log${NC}"
echo -e "   Arrêter tout  : ${GREEN}./stop.sh${NC}"
echo ""
echo -e "${YELLOW}🔑 Codes d'activation test :${NC}"
echo -e "   ${GREEN}docker exec -it plagiat_postgres psql -U plagiat_user -d plagiattracker -c \"SELECT code, plan_type FROM activation_codes WHERE status='active' LIMIT 5;\"${NC}"
echo ""
