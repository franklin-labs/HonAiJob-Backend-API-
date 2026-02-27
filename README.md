# HonaiJob Backend - Architecture Professionnelle & Multi-Agents

Ce dossier contient le backend complet de l'application HonaiJob, construit avec **FastAPI**, **Agno (Phi)** pour l'intelligence artificielle (propulsé par **Groq**), et une architecture en couches prête pour la production.

## 🚀 Fonctionnalités Principales

- **Architecture Multi-Agents (Groq)** : Orchestration intelligente avec les modèles Llama-3.3-70b (Logique) et Llama-3.1-8b (Vitesse).
- **Sourcing d'Emploi Intelligent** : Recherche proactive via DuckDuckGo et Wikipedia avec filtres anti-hallucinations.
- **Support Multi-Clés API** : Chaque utilisateur peut utiliser sa propre clé API Groq via les headers.
- **Authentification Sécurisée** : Google OAuth 2.0 minimaliste et JWT avec Refresh Tokens.
- **Gestion de CV & Projets** : CRUD complet aligné sur les besoins du frontend (JobOffer, Application, UserProject).
- **Base de Données** : Intégration SQLAlchemy (support PostgreSQL/SQLite) avec politique d'obsolescence des offres (15 jours).
- **CORS Configuré** : Prêt pour un déploiement sur des serveurs séparés (Frontend React).

## 🛠️ Structure du Projet

```
backend-honaijob/
├── app/
│   ├── agents/          # Logique des agents Agno, factory et prompts système
│   │   └── prompts/     # Dossier centralisé des prompts systèmes par agent
│   ├── api/             # Routers (auth, agents, projects, applications, jobs)
│   ├── core/            # Configuration globale, sécurité et middleware
│   ├── db/              # Session et base de données
│   ├── models/          # Modèles Pydantic et SQLAlchemy
│   ├── services/        # Logique métier, agrégateur d'offres et matching
│   └── main.py          # Point d'entrée de l'application
├── tests/               # Suite de tests (pytest) couvrant >80% du code
├── AGENTS.MD            # Documentation détaillée de l'IA et des Workflows
├── requirements.txt     # Dépendances du projet (Groq, Agno, DuckDuckGo)
└── .env                 # Variables d'environnement (à créer)
```

## ⚙️ Installation & Configuration

### 1. Prérequis
- Python 3.10+
- Pip (gestionnaire de paquets)
- Accès à une base de données PostgreSQL (ou SQLite par défaut)

### 2. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration des variables d'environnement
Créez un fichier `.env` à la racine du dossier `backend-honaijob/` :

```env
PROJECT_NAME="HonaiJob API"
SECRET_KEY="votre-cle-secrete-jwt"
DATABASE_URL="postgresql://user:password@localhost/honaijob"
GOOGLE_CLIENT_ID="votre-client-id-google"
GOOGLE_CLIENT_SECRET="votre-client-secret-google"

# Configuration Groq (Clé par défaut si l'utilisateur n'en fournit pas)
GROQ_API_KEY="gsk_..."
```

### 4. Lancement de l'application
```bash
uvicorn app.main:app --reload
```
L'API sera accessible sur `http://localhost:8000`.
La documentation Swagger (OpenAPI) est disponible sur `http://localhost:8000/docs`.

## 🧪 Tests & Couverture

Les tests sont écrits avec `pytest` et `pytest-asyncio`. Pour exécuter la suite complète :

```bash
pytest --cov=app tests/
```

## 📦 API & Intégration Frontend

### Headers Spécifiques
- `X-Groq-Api-Key` (Optionnel) : Permet à l'utilisateur d'utiliser son propre quota Groq.

### Routes Clés
- `POST /api/v1/agents/chat` : Interface de discussion avec l'orchestrateur.
- `POST /api/v1/agents/search-jobs` : Recherche d'emploi avec workflow de vérification.
- `GET /api/v1/job-offers/search` : Recherche dans la base de données agrégée proactivement.

---
Développé avec ❤️ par FRANKLIN