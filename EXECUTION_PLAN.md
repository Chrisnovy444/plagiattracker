# 🎯 PLAN D'EXÉCUTION AUTONOME - PLAGIATTRACKER

**Date** : 2026-06-01  
**Demande utilisateur** : Projet COMPLET et FONCTIONNEL  
**Mode** : Travail autonome sans interruption  
**Objectif** : Application opérationnelle avec Claude intégré comme IA

---

## 📋 Contexte sauvegardé

### Demande exacte utilisateur
> "j'aimerais pas que tu t'arretes avant avoir produit travail final donc j'aimerais voir travail final (tu pourras d'abord faire acces depuis ce serveur et avec toi comme IA...) donc je vais taper un code qui va te permettre de bypasser demande autoriqation jsqu'a fin (enregistre just le contexte. et apres je pense on pourra arreter ? c'est ce code : claude --dangerously-skip-permissions ... je serais pas la mais j veux qu pojet torne tu me feras rapprt finak des decisions"

### Interprétation
1. ✅ Projet COMPLET (pas juste infrastructure)
2. ✅ Accès depuis serveur (localhost ou IP Tailscale)
3. ✅ Claude intégré comme IA du système (API Claude pour correction)
4. ✅ Travail autonome (utilisateur absent)
5. ✅ Rapport final des décisions à la fin

---

## 🚀 Plan d'exécution complet

### Phase 1 : Infrastructure (✅ FAIT)
- [x] Docker Compose
- [x] Models SQLAlchemy
- [x] Backend FastAPI skeleton
- [x] Frontend React skeleton
- [x] Documentation

### Phase 2 : Backend Core (2-3h)
- [ ] **Routers API**
  - [ ] `auth.py` : Register, login, activate code
  - [ ] `upload.py` : Upload fichier + extraction
  - [ ] `report.py` : GET rapports
  - [ ] `correction.py` : POST corrections
  - [ ] `settings.py` : Paramètres user

- [ ] **Services Core**
  - [ ] `extractor.py` : PyMuPDF + python-docx + txt
  - [ ] `plagiat_engine.py` : MinHash fingerprinting + scoring
  - [ ] `ai_detector.py` : GPT-2 perplexité + burstiness
  - [ ] `corrector.py` : Intégration Groq/Claude API

- [ ] **API Sources (simplified)**
  - [ ] `arxiv.py` : Recherche arXiv
  - [ ] `openalex.py` : Recherche OpenAlex
  - [ ] `web_scraper.py` : BeautifulSoup basique

### Phase 3 : Frontend Complet (2-3h)
- [ ] **Components**
  - [ ] `ScoreGauge.jsx` : Jauge circulaire (Recharts)
  - [ ] `SourceList.jsx` : Liste sources trouvées
  - [ ] `HighlightedText.jsx` : Surlignage passages
  - [ ] `CorrectionPanel.jsx` : Boutons correction
  - [ ] `ActivationForm.jsx` : Formulaire activation code

- [ ] **Pages complètes**
  - [ ] `Home.jsx` : Upload + activation (COMPLET)
  - [ ] `Report.jsx` : Affichage rapport complet
  - [ ] `Settings.jsx` : Gestion clés API

- [ ] **State Management**
  - [ ] Zustand store : user, documents, reports
  - [ ] API client (Axios)

### Phase 4 : Intégration & Tests (1-2h)
- [ ] Tests backend (Pytest)
- [ ] Tests frontend (composants)
- [ ] Tests end-to-end (upload → rapport)
- [ ] Vérification codes activation
- [ ] Vérification détection plagiat basique
- [ ] Vérification détection IA basique

### Phase 5 : Déploiement Local (30min)
- [ ] Générer .env avec passwords sécurisés
- [ ] Build Docker images
- [ ] Lancer stack complète
- [ ] Vérifier accès http://100.127.127.117:5173 (Tailscale)
- [ ] Créer script démarrage automatique

### Phase 6 : Intégration Claude (1h)
- [ ] Configuration Claude API key
- [ ] Correction automatique via Claude
- [ ] Humanisation contenu IA
- [ ] Reformulation plagiat

### Phase 7 : Documentation & Rapport (30min)
- [ ] README utilisateur final
- [ ] Guide activation codes
- [ ] Rapport final décisions
- [ ] Backup fichiers importants

---

## 🔧 Décisions techniques à prendre

### 1. Détection Plagiat (MVP)
**Approche simplifiée** :
- MinHash fingerprinting (copie exacte)
- 2 APIs seulement (arXiv + OpenAlex) pour MVP
- Scoring basique (% similarité)

**Approche complète** :
- MinHash + Sentence-BERT (paraphrase)
- 5 APIs académiques
- Web scraping
- Scoring avancé

**DÉCISION** : Approche simplifiée pour MVP fonctionnel

### 2. Détection IA (MVP)
**Approche simplifiée** :
- GPT-2 perplexité seulement
- Calcul burstiness
- Score global

**Approche complète** :
- GPT-2 + RoBERTa classifier
- Burstiness + cross-entropy
- Score par phrase + section

**DÉCISION** : Approche simplifiée pour MVP fonctionnel

### 3. Correction (MVP)
**Option 1** : Groq gratuit seulement
**Option 2** : Claude API (clé utilisateur requise)
**Option 3** : Les deux

**DÉCISION** : Option 3 - Les deux (Groq par défaut, Claude si clé fournie)

### 4. Frontend Build
**Option 1** : Dev mode (Vite dev server)
**Option 2** : Production build (Vite build + Nginx)

**DÉCISION** : Dev mode pour MVP, production pour v2

### 5. Accès
**Option 1** : localhost seulement
**Option 2** : IP Tailscale (100.127.127.117)
**Option 3** : Domaine (avec Caddy)

**DÉCISION** : Option 2 - IP Tailscale pour accès mobile

---

## 🎯 MVP Fonctionnel (objectif réaliste 6-8h)

### Ce qui DOIT fonctionner
1. ✅ Upload document (PDF/DOCX/TXT)
2. ✅ Extraction texte
3. ✅ Détection plagiat basique (arXiv + OpenAlex)
4. ✅ Détection IA basique (GPT-2 perplexité)
5. ✅ Affichage rapport (scores + sources)
6. ✅ Système activation codes (validation)
7. ✅ Correction basique (Groq API)
8. ✅ Export rapport (JSON, PDF v2)
9. ✅ Accès via Tailscale

### Ce qui peut attendre v2
- Sentence-BERT (paraphrase avancée)
- RoBERTa classifier (IA avancée)
- Web scraping
- 3 autres APIs académiques
- Export PDF professionnel
- Dashboard utilisateur
- Historique analyses

---

## 📊 Timeline estimée

| Phase | Durée | Cumul |
|-------|-------|-------|
| ~~Phase 1 : Infrastructure~~ | ~~2h~~ | ~~2h~~ ✅ |
| Phase 2 : Backend Core | 2-3h | 5h |
| Phase 3 : Frontend Complet | 2-3h | 8h |
| Phase 4 : Tests | 1h | 9h |
| Phase 5 : Déploiement | 30min | 9h30 |
| Phase 6 : Claude intégration | 1h | 10h30 |
| Phase 7 : Documentation | 30min | 11h |

**Total estimé** : ~10-11h de développement continu

---

## 🔑 Clés API requises

### Obligatoires
- [x] PostgreSQL password (généré auto)
- [x] Redis password (généré auto)
- [x] SECRET_KEY (généré auto)

### Optionnelles (pour fonctionnalités avancées)
- [ ] GROQ_API_KEY (gratuit, pour correction)
- [ ] SEMANTIC_SCHOLAR_API_KEY (gratuit)
- [ ] PUBMED_API_KEY (gratuit)
- [ ] CLAUDE_API_KEY (payant, si utilisateur veut meilleure correction)

**DÉCISION** : Démarrer sans clés optionnelles, fonctionner en mode dégradé

---

## 🚀 Commandes d'exécution

### Setup automatique
```bash
cd /home/serveur/plagiat-tracker

# Générer .env sécurisé
cat > .env << EOF
DB_PASSWORD=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 32)
SECRET_KEY=$(openssl rand -base64 48)
DATABASE_URL=postgresql://plagiat_user:\$(cat .env | grep DB_PASSWORD | cut -d= -f2)@postgres:5432/plagiattracker
REDIS_URL=redis://:\$(cat .env | grep REDIS_PASSWORD | cut -d= -f2)@redis:6379/0
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=http://localhost:5173,http://100.127.127.117:5173
SUPPORT_EMAIL=checkone076@gmail.com
PARTNER_PHONE=+237690895735
GROQ_API_KEY=
CLAUDE_API_KEY=
EOF

# Lancer stack complète
docker-compose up -d

# Installer backend dependencies
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Lancer backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &

# Installer frontend dependencies
cd ../frontend
npm install

# Lancer frontend
npm run dev -- --host 0.0.0.0 &
```

### Vérification
```bash
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:5173

# PostgreSQL
docker exec -it plagiat_postgres psql -U plagiat_user -d plagiattracker -c "SELECT COUNT(*) FROM activation_codes;"

# Codes test
docker exec -it plagiat_postgres psql -U plagiat_user -d plagiattracker -c "SELECT code, plan_type FROM activation_codes WHERE status='active' LIMIT 5;"
```

---

## 📝 Rapport final à générer

### Structure rapport
```markdown
# PLAGIATTRACKER - RAPPORT FINAL

## 1. État du projet
- ✅ Fonctionnalités implémentées
- ⚠️ Limitations connues
- 📝 TODO pour v2

## 2. Décisions techniques
- Architecture finale
- APIs choisies
- Modèles IA utilisés

## 3. Accès & Utilisation
- URLs d'accès
- Codes activation test
- Guide utilisateur rapide

## 4. Maintenance
- Commandes démarrage
- Logs & debugging
- Backup & restauration

## 5. Évolutions futures
- Roadmap v2
- Fonctionnalités avancées
- Optimisations
```

---

## ⚠️ Notes importantes

### Limitations acceptées pour MVP
1. **Détection plagiat** : Basique (2 APIs seulement)
2. **Détection IA** : Perplexité seulement (pas RoBERTa)
3. **Correction** : Groq gratuit (pas Claude par défaut)
4. **Export** : JSON seulement (pas PDF)
5. **Auth** : Basique (pas JWT complet)

### Ce qui est prioritaire
1. ✅ Application qui tourne
2. ✅ Upload + extraction fonctionnent
3. ✅ Scores affichés (même basiques)
4. ✅ Codes activation validés
5. ✅ Accès via Tailscale

---

## 🎯 Définition du "TERMINÉ"

Le projet est considéré **TERMINÉ** quand :

1. ✅ `docker-compose up -d` démarre tout
2. ✅ Frontend accessible http://100.127.127.117:5173
3. ✅ Backend accessible http://100.127.127.117:8000
4. ✅ Upload document fonctionne
5. ✅ Rapport s'affiche avec scores
6. ✅ Code activation fonctionne
7. ✅ Documentation complète existe
8. ✅ Rapport final généré

---

**Prêt à exécuter** : OUI  
**Mode** : Autonome  
**Durée estimée** : 10-11h  
**Rapport final** : `/home/serveur/plagiat-tracker/RAPPORT_FINAL.md`
