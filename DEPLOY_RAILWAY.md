# 🚂 Guide Déploiement Railway - PlagiatTracker

## 📋 Prérequis

1. **Compte Railway** : [railway.app](https://railway.app)
2. **GitHub repo** (recommandé) ou déploiement CLI
3. **API Keys** :
   - Groq API (gratuit) : [console.groq.com](https://console.groq.com)
   - Semantic Scholar (optionnel)
   - PubMed (optionnel)

---

## 🏗️ Architecture Railway

Le projet nécessite **4 services** :

```
┌─────────────────────────────────────────┐
│  RAILWAY PROJECT: plagiattracker       │
├─────────────────────────────────────────┤
│                                         │
│  ┌────────────┐  ┌──────────────┐     │
│  │ PostgreSQL │  │    Redis     │     │
│  │   (DB)     │  │   (Cache)    │     │
│  └────────────┘  └──────────────┘     │
│         ↑               ↑              │
│         │               │              │
│  ┌──────┴───────────────┴───────┐     │
│  │      Backend (FastAPI)       │     │
│  │    Port: $PORT (8000)        │     │
│  └──────────────┬───────────────┘     │
│                 │                      │
│  ┌──────────────┴───────────────┐     │
│  │    Frontend (React/Vite)     │     │
│  │    Port: $PORT (5173)        │     │
│  └──────────────────────────────┘     │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🚀 Méthode 1 : Déploiement via GitHub (Recommandé)

### Étape 1 : Push sur GitHub

```bash
cd /home/serveur/plagiat-tracker

# Initialiser git (si pas fait)
git init
git add .
git commit -m "Initial commit: PlagiatTracker MVP"

# Push vers GitHub
git remote add origin https://github.com/TON-USERNAME/plagiattracker.git
git branch -M main
git push -u origin main
```

### Étape 2 : Créer le projet sur Railway

1. **Connexion** : [railway.app](https://railway.app)
2. **New Project** → **Deploy from GitHub repo**
3. **Sélectionner** : `plagiattracker` repo
4. **Wait** : Railway détecte automatiquement la structure

### Étape 3 : Configurer les services

#### Service 1 : PostgreSQL

1. **Add Service** → **Database** → **PostgreSQL**
2. Railway génère automatiquement :
   - `DATABASE_URL`
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_DB`

#### Service 2 : Redis

1. **Add Service** → **Database** → **Redis**
2. Railway génère `REDIS_URL`

#### Service 3 : Backend (FastAPI)

1. **Add Service** → **GitHub Repo** → **Select `backend/`**
2. **Settings** → **Variables** :

```bash
# Base de données (auto depuis PostgreSQL service)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis (auto depuis Redis service)
REDIS_URL=${{Redis.REDIS_URL}}

# Secret key (générer avec : openssl rand -hex 32)
SECRET_KEY=ton_secret_key_32_chars_minimum

# API Keys
GROQ_API_KEY=gsk-xxxxxxxxxxxx
SEMANTIC_SCHOLAR_API_KEY=  # optionnel
PUBMED_API_KEY=  # optionnel

# Config
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=https://TON-FRONTEND.railway.app

# Contact
SUPPORT_EMAIL=checkone076@gmail.com
PARTNER_PHONE=+237690895735

# Hugging Face
HF_HOME=/app/models
TRANSFORMERS_CACHE=/app/models
```

3. **Settings** → **Build** :
   - **Root Directory** : `backend`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Settings** → **Deploy** :
   - **Health Check** : `/health`

#### Service 4 : Frontend (React)

1. **Add Service** → **GitHub Repo** → **Select `frontend/`**
2. **Settings** → **Variables** :

```bash
VITE_API_URL=https://TON-BACKEND.railway.app
VITE_SUPPORT_EMAIL=checkone076@gmail.com
VITE_PARTNER_PHONE=+237690895735
```

3. **Settings** → **Build** :
   - **Root Directory** : `frontend`
   - **Build Command** : `npm install && npm run build`
   - **Start Command** : `npm run preview -- --host 0.0.0.0 --port $PORT`

4. **Settings** → **Networking** :
   - **Generate Domain** → Copier l'URL publique
   - **Update Backend** `CORS_ORIGINS` avec cette URL

---

## 🛠️ Méthode 2 : Déploiement CLI (Alternative)

### Installer Railway CLI

```bash
# Installation
npm i -g @railway/cli

# Login
railway login

# Init projet
cd /home/serveur/plagiat-tracker
railway init
```

### Déployer

```bash
# Déployer backend
cd backend
railway up

# Déployer frontend
cd ../frontend
railway up
```

---

## 🔧 Configuration Post-Déploiement

### 1. Initialiser la base de données

```bash
# Connecter à PostgreSQL via Railway CLI
railway connect postgres

# Exécuter le script init
\i backend/sql/init.sql
```

**Ou via Dashboard** :
1. PostgreSQL service → **Data** → **Query**
2. Coller contenu de `backend/sql/init.sql`
3. **Execute**

### 2. Générer codes activation

```sql
-- Codes test (à exécuter dans Railway Postgres)
INSERT INTO activation_codes (code, plan_type, analyses_limit, validity_days)
VALUES 
  ('TEST-ETUDIANT-2024', 'student', 50, 30),
  ('TEST-ENSEIGNANT-2024', 'teacher', 200, 30),
  ('TEST-CHERCHEUR-2024', 'researcher', 500, 30);
```

### 3. Tester l'application

```bash
# URL Frontend
https://ton-frontend.railway.app

# URL Backend
https://ton-backend.railway.app/docs

# Health check
curl https://ton-backend.railway.app/health
```

---

## 📊 Monitoring & Logs

### Via Railway Dashboard

1. **Backend Logs** :
   - Service Backend → **Logs**
   - Watch errors, API calls, etc.

2. **Frontend Logs** :
   - Service Frontend → **Logs**
   - Build errors, runtime issues

3. **Metrics** :
   - **CPU** : Devrait rester < 50% en idle
   - **RAM** : Backend ~300-500 MB, Frontend ~100 MB
   - **Network** : Monitoring traffic

### Via CLI

```bash
# Logs backend
railway logs --service backend

# Logs frontend
railway logs --service frontend

# Logs postgres
railway logs --service postgres
```

---

## 💰 Coûts Railway

### Plan Hobby (Gratuit)

- **$5 gratuit/mois**
- **500 heures execution**
- Limite : ~16h/jour

**Services :**
- PostgreSQL : ~$2/mois
- Redis : ~$1/mois
- Backend : ~$1/mois
- Frontend : ~$1/mois

**TOTAL** : ~$5/mois (couvert par gratuit)

### Plan Pro ($20/mois)

- **Illimité**
- Meilleure performance
- Support prioritaire

---

## 🔒 Variables d'environnement complètes

### Backend (.env production)

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Redis
REDIS_URL=redis://default:pass@host:port

# Security
SECRET_KEY=minimum_32_characters_random_string

# APIs
GROQ_API_KEY=gsk-xxxxx
SEMANTIC_SCHOLAR_API_KEY=
PUBMED_API_KEY=

# Config
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=https://plagiattracker.railway.app

# Contact
SUPPORT_EMAIL=checkone076@gmail.com
PARTNER_PHONE=+237690895735

# ML Models
HF_HOME=/app/models
TRANSFORMERS_CACHE=/app/models
```

### Frontend (.env production)

```bash
VITE_API_URL=https://plagiattracker-backend.railway.app
VITE_SUPPORT_EMAIL=checkone076@gmail.com
VITE_PARTNER_PHONE=+237690895735
```

---

## ✅ Checklist Déploiement

### Avant déploiement
- [ ] Créer compte Railway
- [ ] Push code sur GitHub
- [ ] Obtenir Groq API Key
- [ ] Préparer variables d'environnement

### Durant déploiement
- [ ] Créer PostgreSQL service
- [ ] Créer Redis service
- [ ] Déployer Backend
- [ ] Déployer Frontend
- [ ] Configurer variables env
- [ ] Générer domains publics
- [ ] Mettre à jour CORS_ORIGINS

### Après déploiement
- [ ] Initialiser base données
- [ ] Générer codes activation test
- [ ] Tester inscription
- [ ] Tester login
- [ ] Tester upload document
- [ ] Tester analyse plagiat
- [ ] Tester analyse IA
- [ ] Vérifier rapports
- [ ] Tester contact support

---

## 🐛 Troubleshooting

### Backend ne démarre pas

```bash
# Vérifier logs
railway logs --service backend

# Problèmes fréquents :
# 1. DATABASE_URL mal configuré
# 2. SECRET_KEY trop court (< 32 chars)
# 3. Module Python manquant
```

### Frontend 404 errors

```bash
# Vérifier VITE_API_URL
# Format : https://backend.railway.app (sans trailing slash)

# Vérifier CORS backend
# Doit contenir URL frontend exacte
```

### PostgreSQL connection refused

```bash
# Attendre 2-3 min après création service
# PostgreSQL prend du temps à initialiser

# Vérifier service est "Active"
# Dashboard → PostgreSQL → Status
```

### Redis connection timeout

```bash
# Vérifier REDIS_URL format
# redis://default:password@host:port

# Vérifier service Redis actif
```

---

## 📞 Support

### Contact PlagiatTracker
- **Email** : checkone076@gmail.com
- **WhatsApp** : +237 690895735

### Railway Support
- **Docs** : [docs.railway.app](https://docs.railway.app)
- **Discord** : [discord.gg/railway](https://discord.gg/railway)
- **Status** : [status.railway.app](https://status.railway.app)

---

## 🔄 Mise à jour Production

### Via GitHub (Auto-deploy)

```bash
# Local
git add .
git commit -m "Update: description"
git push origin main

# Railway déploie automatiquement ! 🚀
```

### Via CLI

```bash
railway up --service backend
railway up --service frontend
```

---

## 📝 Notes importantes

### Premier déploiement
- Backend prend ~3-5 min (télécharge modèles GPT-2)
- Frontend prend ~2 min
- PostgreSQL init prend ~1 min

### Redémarrages
- Railway redémarre services après crash
- Politique : `ON_FAILURE` (max 10 retries)

### Scaling
- Railway scale automatiquement si besoin
- Plan Hobby limité à 1 instance/service

### Backups
- PostgreSQL backupé automatiquement
- Retention : 7 jours (Hobby), 30 jours (Pro)

---

**Version** : 1.0  
**Date** : 2026-06-01  
**Projet** : PlagiatTracker MVP  
**Contact** : checkone076@gmail.com
