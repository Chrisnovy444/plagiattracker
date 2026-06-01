# ⚡ Railway Quickstart - 5 minutes

## 🎯 Déploiement ultra-rapide

### 1️⃣ Préparer le projet (local)

```bash
cd /home/serveur/plagiat-tracker
./prepare_deploy.sh
```

### 2️⃣ Push vers GitHub

```bash
# Créer repo sur https://github.com/new
# Nom suggéré : plagiattracker

# Push
git remote add origin https://github.com/TON-USERNAME/plagiattracker.git
git push -u origin main
```

### 3️⃣ Déployer sur Railway

1. **Connexion** : [railway.app](https://railway.app) (GitHub auth)

2. **New Project** → **Deploy from GitHub repo**

3. **Ajouter services** :

```
┌─ PostgreSQL ──────────────┐
│ (auto-config)             │
└───────────────────────────┘

┌─ Redis ───────────────────┐
│ (auto-config)             │
└───────────────────────────┘

┌─ Backend ─────────────────┐
│ Root: backend             │
│ Build: requirements.txt   │
│ Start: uvicorn app.main   │
└───────────────────────────┘

┌─ Frontend ────────────────┐
│ Root: frontend            │
│ Build: npm install+build  │
│ Start: npm run preview    │
└───────────────────────────┘
```

### 4️⃣ Variables Backend

**Settings → Variables** :

```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
SECRET_KEY=generate_avec_openssl_rand_hex_32
GROQ_API_KEY=gsk-TON-CLE-ICI
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=https://TON-FRONTEND.railway.app
SUPPORT_EMAIL=checkone076@gmail.com
PARTNER_PHONE=+237690895735
```

### 5️⃣ Variables Frontend

**Settings → Variables** :

```bash
VITE_API_URL=https://TON-BACKEND.railway.app
VITE_SUPPORT_EMAIL=checkone076@gmail.com
VITE_PARTNER_PHONE=+237690895735
```

### 6️⃣ Init Database

**PostgreSQL → Query** :

```sql
-- Copier/coller contenu de backend/sql/init.sql
-- Puis exécuter

-- Ajouter codes test
INSERT INTO activation_codes (code, plan_type, analyses_limit, validity_days)
VALUES 
  ('TEST-2024-STUDENT', 'student', 50, 30),
  ('TEST-2024-TEACHER', 'teacher', 200, 30);
```

### 7️⃣ Test

```bash
# Health check
curl https://ton-backend.railway.app/health

# Ouvrir app
https://ton-frontend.railway.app
```

---

## 🔑 API Keys nécessaires

### Groq (REQUIS - Gratuit)

1. → [console.groq.com](https://console.groq.com)
2. **Sign up** (gratuit)
3. **API Keys** → **Create API Key**
4. Copier `gsk-xxxxxx`
5. Coller dans Railway `GROQ_API_KEY`

### Semantic Scholar (Optionnel)

- API publique, pas de clé requise
- Limite : 100 req/5min

### PubMed (Optionnel)

- API publique
- Email requis dans query params

---

## 💰 Coût

### Plan Hobby (GRATUIT)

- **$5 gratuit/mois**
- Suffisant pour 4 services
- ~500h execution/mois

**Coût réel** :
- PostgreSQL : $2
- Redis : $1
- Backend : $1
- Frontend : $1
- **TOTAL** : $5/mois → **COUVERT** ✅

---

## ✅ Checklist

- [ ] Code pushé sur GitHub
- [ ] Groq API key obtenue
- [ ] 4 services créés sur Railway
- [ ] Variables backend configurées
- [ ] Variables frontend configurées
- [ ] CORS_ORIGINS mis à jour
- [ ] Database initialisée
- [ ] Codes test créés
- [ ] Health check OK
- [ ] App accessible

---

## 🚨 Dépannage rapide

### Backend crash
```bash
# Vérifier logs
railway logs --service backend

# Causes fréquentes :
# - SECRET_KEY < 32 chars
# - DATABASE_URL vide
# - Groq API key invalide
```

### Frontend 404
```bash
# Vérifier VITE_API_URL
# Format : https://backend.railway.app
# (sans /api, sans trailing slash)

# Vérifier CORS backend
# Doit contenir frontend URL exacte
```

### Cannot connect to DB
```bash
# Attendre 2-3 min
# PostgreSQL init peut être long

# Vérifier service "Active"
```

---

## 📞 Support

- **Email** : checkone076@gmail.com
- **WhatsApp** : +237 690895735

---

## 📚 Documentation complète

→ `DEPLOY_RAILWAY.md` (guide détaillé)

---

**Temps total** : ~5-10 minutes  
**Coût** : $0 (plan Hobby gratuit)  
**Prêt pour production** : ✅
