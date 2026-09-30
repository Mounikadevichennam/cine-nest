# CineNest — Personalized OTT Subscriber & Recommendation System

[![Frontend: React + Vite](https://img.shields.io/badge/Frontend-React%20%2B%20Vite%20%2B%20Tailwind-blue)](https://vitejs.dev/)
[![Backend: FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%2B%20Python-green)](https://fastapi.tiangolo.com/)
[![Database: MySQL](https://img.shields.io/badge/Database-MySQL-orange)](https://www.mysql.com/)
[![Recommendation: scikit-learn](https://img.shields.io/badge/Recommendation-TF--IDF%20%2B%20Cosine%20Similarity-purple)](https://scikit-learn.org/)

CineNest is an end-to-end regional OTT movie streaming and recommendation prototype built with a clean monorepo architecture. CineNest solves generic content recommendation problems by integrating first-time onboarding preferences, metadata matching, scikit-learn plot vector similarities, behavioral feedback, and recency decay scoring.

---

## 🏛 1. System Monorepo Architecture

```
CineNest/
├── frontend/                     # React.js + Vite + Tailwind CSS SPA
│   ├── src/
│   │   ├── components/           # Reusable OTT UI components & Admin tables
│   │   ├── pages/                # Subscriber & Admin portal page views
│   │   ├── services/             # Centralized Axios API client layer
│   │   ├── context/              # AuthContext (JWT) & ProfileContext
│   │   ├── App.jsx               # React Router with Protected User/Admin Guards
│   │   └── main.jsx
│   ├── package.json
│   └── .env.example              # VITE_API_BASE_URL
│
├── backend/                      # Python FastAPI REST Server
│   ├── app/
│   │   ├── main.py               # Server entry point & CORS
│   │   ├── config/               # Settings & Pydantic environment configuration
│   │   ├── database/             # SQLAlchemy engine & table initializers
│   │   ├── models/               # ORM relational models (UserRole, Movie, Activity)
│   │   ├── schemas/              # Pydantic validation DTOs
│   │   ├── routes/               # Modular REST endpoints (/auth, /users, /movies, /admin, /recommendations)
│   │   ├── services/             # Business logic & TMDB regional ingestion pipeline
│   │   ├── recommendation/       # Scikit-learn 100-Point Hybrid Scoring Engine
│   │   └── auth/                 # JWT security & require_admin / require_user guards
│   ├── requirements.txt
│   └── .env.example              # DATABASE_URL, JWT_SECRET, TMDB_API_KEY
│
├── data/                         # Recommendation vector datasets & Ingestion README
├── docs/                         # Architecture, Database, & Recommendation Documentation
├── .gitignore
└── README.md
```

---

## 🌟 2. Key Features

- **Regional Language Priority**: Built for Indian OTT audiences with strong representation across 6 languages: **Telugu, Hindi, Tamil, Malayalam, Kannada, and English**.
- **100-Point Hybrid Recommendation Engine**:
  - Language Match: 10 pts
  - Genre Match: 20 pts
  - Actor Match: 15 pts
  - Description TF-IDF Cosine Similarity: 15 pts
  - User Behavioral Feedback: 20 pts (Watch completion, Likes, Ratings)
  - Search Interest / Recency: 10 pts
  - IMDb/TMDB Rating: 5 pts
  - Release Year: 5 pts
  - **Explicit Negative Preference**: `NotInterested` content is penalized and filtered out.
- **Role-Based Access Control (RBAC)**:
  - `USER`: Subscribers accessing catalog, onboarding, search, player, and recommendations.
  - `ADMIN`: Strict administrator portal (`/admin/*`) with stats, catalog CRUD, poster, and trailer updates.
- **TMDB Integration**: Asynchronous regional movie ingestion pipeline built with `httpx` (poster required, 2016–2026 feature films).

---

## 🚀 3. Local Setup Guide

### Prerequisites
- Node.js (v18+) & npm
- Python (v3.10+)
- MySQL Server (v8.0+) or SQLite fallback for local dev

### Step 1: Backend Setup
```bash
cd backend
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python -m app.database.init_db
python -m app.database.seed_data
uvicorn app.main:app --reload --port 8000
```

### Step 2: Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 4. Deployment Instructions
- **Frontend → Vercel**: Deploy from `frontend/` directory with `VITE_API_BASE_URL`.
- **Backend → Render**: Deploy from `backend/` directory with `DATABASE_URL`, `JWT_SECRET`, `TMDB_API_KEY`.
- **Database → MySQL**: PlanetScale / Render MySQL / Aiven.
