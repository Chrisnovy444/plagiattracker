#!/bin/bash

# Script préparation déploiement Railway
# PlagiatTracker MVP

set -e

echo "🚂 Préparation déploiement Railway - PlagiatTracker"
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Vérifications
echo "📋 Vérification prérequis..."

if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git non installé${NC}"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Fichier .env manquant, copie depuis .env.example${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  IMPORTANT : Édite .env avec tes vraies valeurs !${NC}"
    echo ""
fi

echo -e "${GREEN}✅ Prérequis OK${NC}"
echo ""

# 2. Git init (si besoin)
if [ ! -d ".git" ]; then
    echo "📦 Initialisation Git..."
    git init
    git branch -M main
    echo -e "${GREEN}✅ Git initialisé${NC}"
else
    echo -e "${GREEN}✅ Git déjà initialisé${NC}"
fi
echo ""

# 3. Vérifier fichiers Railway
echo "🔧 Vérification fichiers Railway..."

required_files=(
    "railway.json"
    "backend/railway.toml"
    "frontend/railway.toml"
    ".gitignore"
    "DEPLOY_RAILWAY.md"
)

missing=0
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ Manquant : $file${NC}"
        missing=1
    else
        echo -e "${GREEN}✅ $file${NC}"
    fi
done

if [ $missing -eq 1 ]; then
    echo -e "${RED}❌ Fichiers manquants !${NC}"
    exit 1
fi
echo ""

# 4. Test structure projet
echo "📂 Vérification structure..."

required_dirs=(
    "backend/app"
    "backend/sql"
    "frontend/src"
)

for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        echo -e "${RED}❌ Dossier manquant : $dir${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ Structure OK${NC}"
echo ""

# 5. Vérifier variables critiques
echo "🔐 Vérification variables environnement..."

if grep -q "changeme" .env 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Variables par défaut détectées dans .env${NC}"
    echo "   Tu dois changer :"
    echo "   - DB_PASSWORD"
    echo "   - REDIS_PASSWORD"
    echo "   - SECRET_KEY"
    echo "   - GROQ_API_KEY"
    echo ""
    read -p "Continue quand même ? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${GREEN}✅ Variables vérifiées${NC}"
echo ""

# 6. Staging files
echo "📝 Staging fichiers Git..."
git add .

# 7. Commit
echo "💾 Création commit..."

if git diff --cached --quiet; then
    echo -e "${YELLOW}⚠️  Aucun changement à commit${NC}"
else
    git commit -m "Deploy: PlagiatTracker MVP ready for Railway

Features:
- Backend FastAPI (auth, upload, plagiat, AI detection)
- Frontend React + Tailwind
- PostgreSQL + Redis
- Railway config files
- Deployment documentation

Contact: checkone076@gmail.com | +237690895735

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
    echo -e "${GREEN}✅ Commit créé${NC}"
fi
echo ""

# 8. Instructions finales
echo "🎯 Prochaines étapes :"
echo ""
echo "1️⃣  Créer repo GitHub :"
echo "   → https://github.com/new"
echo ""
echo "2️⃣  Ajouter remote :"
echo "   git remote add origin https://github.com/TON-USERNAME/plagiattracker.git"
echo ""
echo "3️⃣  Push code :"
echo "   git push -u origin main"
echo ""
echo "4️⃣  Déployer sur Railway :"
echo "   → https://railway.app/new"
echo "   → Deploy from GitHub repo"
echo "   → Sélectionner 'plagiattracker'"
echo ""
echo "5️⃣  Suivre guide complet :"
echo "   cat DEPLOY_RAILWAY.md"
echo ""
echo -e "${GREEN}✅ Préparation terminée !${NC}"
echo ""
echo "📞 Support : checkone076@gmail.com | WhatsApp: +237690895735"
