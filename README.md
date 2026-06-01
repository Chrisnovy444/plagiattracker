# 🔍 PLAGIATTRACKER

**Détecteur de plagiat + contenu IA + correction automatique**

[![Status](https://img.shields.io/badge/status-in_development-yellow)](https://github.com)
[![License](https://img.shields.io/badge/license-proprietary-red)](LICENSE)

---

## 🎯 Vision

Application web professionnelle permettant la détection de :
- **Plagiat académique** (copie exacte + paraphrase)
- **Contenu généré par IA** (GPT, Claude, etc.)
- **Correction automatique** (citation, reformulation, humanisation)

---

## ✨ Fonctionnalités

### Core
- ✅ Upload documents (PDF, DOCX, TXT)
- ✅ Détection plagiat multi-sources (5 APIs académiques + web)
- ✅ Détection IA (perplexité, burstiness, RoBERTa)
- ✅ Rapport visuel avec passages surlignés
- ✅ Export PDF professionnel

### Avancé
- ✅ Correction automatique (Groq API)
- ✅ Re-vérification post-correction
- ✅ Système d'activation par codes
- ✅ Plans tarifaires multi-segments
- ✅ Cache intelligent (Redis)
- ✅ Traitement asynchrone

---

## 🏗️ Architecture

```
Frontend (React + Tailwind)
    ↓ HTTPS REST
Backend (FastAPI)
    ├─ Module extraction (PyMuPDF, python-docx)
    ├─ Module plagiat (MinHash, Sentence-BERT, APIs)
    ├─ Module IA (GPT-2, RoBERTa)
    ├─ Module correction (Groq)
    └─ Module rapport (PDF)
    ↓
Infrastructure
    ├─ PostgreSQL (Supabase)
    ├─ Redis (Upstash)
    └─ Storage (MinIO/S3)
```

---

## 💰 Plans tarifaires

| Plan | Prix (FCFA) | Analyses/mois | Validité |
|------|-------------|---------------|----------|
| **Essai** | 0 | 3 | 7 jours |
| **Étudiant** | 2,500 | 50 | 30 jours |
| **Enseignant** | 5,000 | 200 | 30 jours |
| **Chercheur** | 10,000 | 500 | 30 jours |
| **Institution** | Sur devis | Illimité | 365 jours |

---

## 📞 Contact & Support

| Canal | Contact | Usage |
|-------|---------|-------|
| **Email** | checkone076@gmail.com | Support technique, réclamations |
| **WhatsApp** | +237 690895735 | Achat licence (Afrique) |
| **Méthodes paiement** | Mobile Money, Virement, Cash | Via partenaire |

---

## 🚀 Quick Start (Dev)

### Prérequis
- Docker + Docker Compose
- Node.js 18+
- Python 3.11+

### Installation

```bash
# Cloner le repo
git clone https://github.com/yourorg/plagiat-tracker.git
cd plagiat-tracker

# Lancer l'infrastructure
docker-compose up -d

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### URLs
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📂 Structure du projet

```
plagiat-tracker/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entrypoint
│   │   ├── models.py               # SQLAlchemy models
│   │   ├── routers/                # API endpoints
│   │   └── services/               # Business logic
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── pages/                  # Home, Report, Settings
│   │   ├── components/             # UI components
│   │   └── utils/                  # API client
│   ├── package.json
│   └── Dockerfile
│
├── docs/                           # Documentation
├── docker-compose.yml
└── README.md
```

---

## 🛠️ Technologies

### Backend
- FastAPI (API REST)
- SQLAlchemy (ORM)
- PyMuPDF (PDF extraction)
- Sentence-Transformers (embeddings)
- Transformers (Hugging Face)

### Frontend
- React 18
- Tailwind CSS
- Vite
- React-PDF

### Infrastructure
- PostgreSQL (Supabase)
- Redis (Upstash)
- Docker

### APIs externes
- arXiv, OpenAlex, CrossRef, Semantic Scholar, PubMed
- Groq (correction)
- BeautifulSoup (web scraping)

---

## 🔐 Sécurité

- ✅ HTTPS obligatoire
- ✅ Validation codes activation
- ✅ Rate limiting (Redis)
- ✅ Sanitization inputs
- ✅ CORS configuré
- ✅ Suppression auto documents (30j)

---

## 📊 Statut développement

### Phase 1 : Infrastructure ⏳ EN COURS
- [x] Structure projet
- [ ] Docker Compose
- [ ] Backend squelette
- [ ] Frontend squelette

### Phase 2 : MVP Core
- [ ] Module extraction
- [ ] Détection plagiat (2 APIs)
- [ ] Détection IA (GPT-2)
- [ ] Interface upload
- [ ] Rapport JSON

### Phase 3 : Features avancées
- [ ] 5 APIs académiques complètes
- [ ] Web scraping
- [ ] Sentence-BERT
- [ ] RoBERTa classifier
- [ ] Correction Groq
- [ ] Export PDF

### Phase 4 : Production
- [ ] Système activation codes
- [ ] Dashboard admin
- [ ] Tests end-to-end
- [ ] Déploiement cloud
- [ ] Documentation utilisateur

---

## 📝 License

**Proprietary** - Tous droits réservés  
© 2026 PLAGIATTRACKER

---

## 🤝 Contribution

Projet privé - Pas de contributions externes acceptées pour le moment.

---

## 📞 Support

Pour toute question :
- 📧 checkone076@gmail.com
- 📱 +237 690895735 (WhatsApp)

---

**Version** : 0.1.0-alpha  
**Dernière mise à jour** : 2026-06-01
