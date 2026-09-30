# CineNest Backend API & Database Engine

FastAPI REST service providing user authentication, profile preferences, normalized MySQL database persistence, administrative CRUD management, and personalized recommendation algorithm scoring.

---

## 🛠 1. MySQL Database Setup Instructions

1. Install **MySQL Server** (v8.0+) or launch a MySQL instance (e.g. PlanetScale, Render MySQL, or local MySQL Workbench).
2. Create the CineNest database instance:
   ```sql
   CREATE DATABASE cinenest_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. Grant user privileges or verify credentials:
   ```sql
   CREATE USER 'cinenest_user'@'localhost' IDENTIFIED BY 'cinenest_password';
   GRANT ALL PRIVILEGES ON cinenest_db.* TO 'cinenest_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

---

## 🔑 2. Required Environment Variables

Create a `.env` file inside `backend/` (copy from `.env.example`):

```env
# Database Connection URL (PyMySQL Driver)
DATABASE_URL=mysql+pymysql://cinenest_user:cinenest_password@localhost:3306/cinenest_db

# Security & Authentication Secrets
JWT_SECRET=your_super_secret_jwt_key_2026_production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Third-Party Data API Key (TMDB - optional ingestion service)
TMDB_API_KEY=your_tmdb_api_key_here

# Allowed Frontend Origins for CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

---

## 🗄 3. Database Initialization Instructions

To automatically create all normalized relational tables (`users`, `profiles`, `movies`, `genres`, `actors`, `movie_genres`, `movie_actors`, `watch_history`, `likes`, `not_interested`, `ratings`, `search_history`, `continue_watching`, `recent_activities`):

Activate your Python virtual environment and run the initialization module:

```bash
cd backend
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

python -m app.database.init_db
```

---

## 🚀 4. How to Start FastAPI Server

Run the development server with live reload:

```bash
uvicorn app.main:app --reload --port 8000
```

Access Interactive API Documentation:
- Swagger UI: `http://localhost:8000/docs`
- Health Endpoint: `http://localhost:8000/api/v1/health`
