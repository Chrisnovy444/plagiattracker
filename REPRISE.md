# 🔄 PLAGIATTRACKER — Fichier de reprise rapide

> **Ce fichier est le SEUL à lire pour reprendre le projet.**  
> Dis à Claude : "lis /home/serveur/plagiat-tracker/REPRISE.md et reprends"

---

## 📍 État actuel (mise à jour : 2026-06-01)

**Version** : 2.0 (toutes fonctionnalités implémentées)  
**Statut** : 🟡 En cours de premier démarrage  
**Dernière action** : Installation dépendances Python + configuration Bedrock

---

## 🔑 Credentials (TOUS dans `.env.production`)

| Service | Statut | Fichier |
|---------|--------|---------|
| GitHub (`ghp_...`) | ✅ | `.env.production` + git remote |
| Supabase (URL + key + password) | ✅ | `.env.production` |
| Upstash Redis (URL + token) | ✅ | `.env.production` |
| Railway token | ✅ | `.env.production` |
| Vercel token (`vcp_...`) | ✅ | `.env.production` |
| AWS Bedrock (token + region) | ✅ | `.env` + `.env.production` + env système |
| Groq | ❌ Non fourni | — |

**⚠️ Ne jamais commit `.env.production` — il est dans `.gitignore`**

---

## 🏗️ Architecture en place

```
plagiat-tracker/
├── backend/           ← FastAPI (Python 3.10, venv)
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models.py (5 tables SQLAlchemy)
│   │   ├── database.py
│   │   ├── routers/ (auth, upload, report)
│   │   └── services/
│   │       ├── extractor.py (PDF/DOCX/TXT)
│   │       ├── plagiat_engine.py (MinHash + Sentence-BERT)
│   │       ├── ai_detector.py (GPT-2 + RoBERTa + heuristiques fallback)
│   │       ├── corrector.py (Claude Bedrock + Groq fallback)
│   │       └── sources/ (arxiv, openalex, crossref, semantic_scholar, pubmed, web_scraper)
│   ├── requirements.txt (complet avec torch)
│   ├── requirements-light.txt (sans torch, pour serveur 8 Go RAM)
│   └── venv/
├── frontend/          ← React 18 + Vite + Tailwind (thème vert/orange)
│   ├── src/pages/ (Home, Report, Settings)
│   ├── src/components/ (ScoreGauge, SourceList, CorrectionPanel, HighlightedText, Navbar, Footer)
│   └── src/utils/ (api.js, store.js)
├── docker-compose.yml ← PostgreSQL 15 + Redis 7
├── .env               ← Config dev local (DB localhost:5433, Redis localhost:6380)
├── .env.production    ← TOUS les tokens cloud
├── start.sh / stop.sh
└── REPRISE.md         ← CE FICHIER
```

---

## 🟢 Infra qui tourne

- **PostgreSQL** : Docker `plagiat_postgres` sur `localhost:5433` — 5 tables + codes activation
- **Redis** : Docker `plagiat_redis` sur `localhost:6380`
- **Git** : Remote `origin` → `github.com/Chrisnovy444/plagiattracker` (token dans URL)

---

## 🎯 Pour démarrer l'app

```bash
cd /home/serveur/plagiat-tracker/backend
source venv/bin/activate
pip install -r requirements-light.txt  # ou requirements.txt si assez de RAM
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (autre terminal) :
cd /home/serveur/plagiat-tracker/frontend
npm run dev -- --host 0.0.0.0
```

**URLs** :
- Backend : http://localhost:8000 (API docs : /docs)
- Frontend : http://localhost:5173
- Tailscale : http://100.127.127.117:5173

---

## 📝 Décisions techniques clés

1. **Correction IA** : Claude via AWS Bedrock (token Bearer), Groq en fallback
2. **Détection IA** : Mode dégradé (heuristiques) si torch pas installé, mode complet si oui
3. **Auth** : Codes d'activation (pas JWT pour MVP), SHA256 passwords
4. **Monétisation** : Plans FCFA (trial/student/teacher/researcher/institution)
5. **Contact** : checkone076@gmail.com + WhatsApp +237 690895735

---

## 📂 Fichiers de référence

| Besoin | Fichier |
|--------|---------|
| **Reprendre le projet** | `/home/serveur/plagiat-tracker/REPRISE.md` (CE FICHIER) |
| **Tous les tokens** | `/home/serveur/plagiat-tracker/.env.production` |
| **Config dev locale** | `/home/serveur/plagiat-tracker/.env` |
| **Rapport final V1** | `/home/serveur/plagiat-tracker/RAPPORT_FINAL.md` |
| **Fonctionnalités V2** | `/home/serveur/plagiat-tracker/FEATURES_COMPLETED.md` |
| **Historique sessions** | `/home/serveur/BILAN/02_HISTORIQUE/SESSIONS.md` |
| **Discussion complète** | `/home/serveur/BILAN/02_HISTORIQUE/discussions/2026-06-01_plagiattracker_complete.md` |
| **Déploiement Railway** | `/home/serveur/plagiat-tracker/DEPLOY_RAILWAY.md` |
| **État projet BILAN** | `/home/serveur/BILAN/01_ETAT/projet_plagiattracker.md` |

---

## ⏭️ Prochaines étapes

1. ✅ ~~Installer dépendances Python~~
2. ✅ ~~Lancer backend (uvicorn)~~ — **TOURNE port 8000**
3. ✅ ~~Lancer frontend (vite)~~ — **TOURNE port 5173**
4. 🔄 Test end-to-end : inscription → upload → analyse → rapport
5. ⬜ Tester correction via Bedrock
6. ⬜ Déploiement cloud (Railway backend + Vercel frontend)
7. ⬜ Obtenir clé Groq (optionnel, fallback)

---

## 💡 Pour la prochaine session Claude

**Commande à donner** :
> "Lis /home/serveur/plagiat-tracker/REPRISE.md et continue le projet plagiattracker"

Claude saura exactement où on en est sans 10 minutes de fouille.

---

**Dernière mise à jour** : 2026-06-01  
**Par** : Session Claude Code #6
