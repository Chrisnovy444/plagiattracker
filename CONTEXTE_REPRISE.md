# 🔄 CONTEXTE DE REPRISE - PLAGIATTRACKER

**Date sauvegarde** : 2026-06-01 06:40  
**Utilisateur** : Absent pendant développement  
**État** : Phase 1 terminée, Phases 2-7 à exécuter

---

## 📋 Instruction utilisateur (textuellement)

> "j'aimerais pas que tu t'arretes avant avoir produit travail final donc j'aimerais voir travail final (tu pourras d'abord faire acces depuis ce serveur et avec toi comme IA...) donc je vais taper un code qui va te permettre de bypasser demande autoriqation jsqu'a fin (enregistre just le contexte. et apres je pense on pourra arreter ? c'est ce code : claude --dangerously-skip-permissions ... je serais pas la mais j veux qu pojet torne tu me feras rapprt finak des decisions"

---

## 🎯 Objectifs clairs

1. **Projet COMPLET et FONCTIONNEL** (pas juste structure)
2. **Accès depuis serveur** (IP Tailscale : 100.127.127.117)
3. **Claude intégré comme IA** (API Claude pour correction)
4. **Travail autonome** (utilisateur ne sera pas là)
5. **Rapport final des décisions** à la fin

---

## ✅ Ce qui est déjà fait

### Infrastructure (Phase 1 - 100%)
- ✅ Structure 30+ fichiers créés
- ✅ Backend FastAPI skeleton complet
- ✅ Frontend React + Tailwind skeleton complet
- ✅ Docker Compose (PostgreSQL + Redis)
- ✅ Models SQLAlchemy (5 tables)
- ✅ Schema PostgreSQL (init.sql)
- ✅ Configuration complète (plans, contacts)
- ✅ Documentation (README, QUICKSTART, STATUS)

### Contacts intégrés partout
- ✅ Email : checkone076@gmail.com
- ✅ WhatsApp : +237 690895735

### Plans tarifaires configurés
- ✅ Essai : 0 FCFA, 3 analyses, 7j
- ✅ Étudiant : 2,500 FCFA, 50 analyses, 30j
- ✅ Enseignant : 5,000 FCFA, 200 analyses, 30j
- ✅ Chercheur : 10,000 FCFA, 500 analyses, 30j
- ✅ Institution : Sur devis, illimité, 365j

---

## 🚧 Ce qui reste à faire

### Phase 2 : Backend Core
**Routers** (5 fichiers) :
- [ ] `routers/auth.py` : Register, login, activate_code
- [ ] `routers/upload.py` : Upload + extraction
- [ ] `routers/report.py` : GET rapport
- [ ] `routers/correction.py` : POST correction
- [ ] `routers/settings.py` : Paramètres user

**Services** (4 fichiers) :
- [ ] `services/extractor.py` : PyMuPDF, python-docx, txt
- [ ] `services/plagiat_engine.py` : MinHash + APIs
- [ ] `services/ai_detector.py` : GPT-2 perplexité
- [ ] `services/corrector.py` : Groq/Claude API

**Sources** (3 fichiers minimum) :
- [ ] `services/sources/arxiv.py`
- [ ] `services/sources/openalex.py`
- [ ] `services/sources/web_scraper.py`

### Phase 3 : Frontend Complet
**Components** (5 fichiers) :
- [ ] `components/ScoreGauge.jsx` : Jauge circulaire
- [ ] `components/SourceList.jsx` : Liste sources
- [ ] `components/HighlightedText.jsx` : Surlignage
- [ ] `components/CorrectionPanel.jsx` : Corrections
- [ ] `components/ActivationForm.jsx` : Formulaire code

**Pages complètes** :
- [ ] `pages/Home.jsx` : Compléter (upload fonctionnel)
- [ ] `pages/Report.jsx` : Implémenter affichage
- [ ] `pages/Settings.jsx` : Implémenter paramètres

**Utils** :
- [ ] `utils/api.js` : Client Axios
- [ ] `utils/store.js` : Zustand state

### Phase 4 : Tests & Déploiement
- [ ] Tests backend (Pytest)
- [ ] Tests end-to-end
- [ ] Build Docker images
- [ ] Lancer stack complète
- [ ] Vérifier accès Tailscale

### Phase 5 : Documentation finale
- [ ] RAPPORT_FINAL.md
- [ ] GUIDE_UTILISATEUR.md
- [ ] CODES_ACTIVATION.md

---

## 🔑 Décisions techniques prises

### Détection Plagiat (MVP)
- **MinHash** fingerprinting (copie exacte)
- **2 APIs** : arXiv + OpenAlex
- **Scoring basique** : % similarité
- Pas de Sentence-BERT pour MVP

### Détection IA (MVP)
- **GPT-2** perplexité
- **Burstiness** calcul
- **Score global** simple
- Pas de RoBERTa pour MVP

### Correction
- **Groq** gratuit (par défaut)
- **Claude** payant (si clé fournie)
- Reformulation + humanisation

### Déploiement
- **Dev mode** pour MVP
- **IP Tailscale** : 100.127.127.117
- **Ports** : 8000 (backend), 5173 (frontend)

---

## 📊 Timeline

| Phase | Durée estimée | Priorité |
|-------|---------------|----------|
| Backend Core | 2-3h | ⭐⭐⭐ |
| Frontend Complet | 2-3h | ⭐⭐⭐ |
| Tests | 1h | ⭐⭐ |
| Déploiement | 30min | ⭐⭐⭐ |
| Documentation | 30min | ⭐⭐ |

**Total** : ~10-11h

---

## 🎯 Critères de succès

Le projet est **TERMINÉ** quand :

1. ✅ Stack complète démarre (`docker-compose up -d`)
2. ✅ Frontend accessible via Tailscale
3. ✅ Upload document fonctionne
4. ✅ Extraction texte fonctionne
5. ✅ Détection plagiat affiche résultats
6. ✅ Détection IA affiche résultats
7. ✅ Code activation fonctionne
8. ✅ Correction Groq fonctionne
9. ✅ Rapport final généré

---

## 📝 Rapport final attendu

Fichier : `/home/serveur/plagiat-tracker/RAPPORT_FINAL.md`

### Contenu attendu
1. **État final** : Fonctionnalités OK vs KO
2. **Décisions techniques** : Choix faits et pourquoi
3. **Accès** : URLs + codes test
4. **Utilisation** : Guide rapide
5. **Maintenance** : Commandes importantes
6. **Prochaines étapes** : Roadmap v2

---

## 🔄 Comment reprendre

### Si utilisateur revient pendant développement
```bash
# Vérifier état actuel
cd /home/serveur/plagiat-tracker
git status  # (si Git initialisé)
docker ps   # Vérifier conteneurs
ls -la backend/app/routers/  # Voir routers créés
ls -la frontend/src/components/  # Voir components créés
```

### Si développement terminé
1. Lire `RAPPORT_FINAL.md`
2. Tester accès http://100.127.127.117:5173
3. Essayer upload document
4. Vérifier codes activation

---

## 💡 Notes importantes

### Limitations acceptées (MVP)
- Détection plagiat basique (2 APIs)
- Détection IA simple (perplexité only)
- Pas de PDF export (JSON seulement)
- Pas de Sentence-BERT
- Pas de RoBERTa

### Ces limitations sont OK pour MVP !
L'objectif est **application fonctionnelle**, pas parfaite.

---

## 📞 Contacts projet

- **Support** : checkone076@gmail.com
- **Partenaire Afrique** : +237 690895735
- **Paiements** : Mobile Money (Orange, MTN, Moov)

---

## 🎉 Message pour la reprise

Salut ! 👋

J'ai terminé le développement de **PLAGIATTRACKER**.

📄 **Lis d'abord** : `RAPPORT_FINAL.md`

🚀 **Pour démarrer** :
```bash
cd /home/serveur/plagiat-tracker
docker-compose up -d
```

🌐 **Accès** : http://100.127.127.117:5173

🔑 **Codes test** : Voir `CODES_ACTIVATION.md`

---

**Sauvegardé** : 2026-06-01 06:40  
**Prêt pour exécution** : OUI ✅
