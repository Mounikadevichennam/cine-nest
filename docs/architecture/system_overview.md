# CineNest System Architecture & Deployment Blueprint

```
[ React SPA (Vercel) ] <---> [ FastAPI REST API (Render) ] <---> [ MySQL / DB Server ]
                                       |
                           [ 100-Pt Hybrid Recommendation Engine ]
                                (scikit-learn / TF-IDF / Cosine)
```

## Security & RBAC Enforcement
1. **Authentication**: JWT tokens passed in `Authorization: Bearer <token>` headers.
2. **User Role Authorization**:
   - `UserRole.USER`: Public endpoints and personalized subscriber feeds (`/api/v1/recommendations/*`, `/api/v1/movies/*`, `/api/v1/users/*`).
   - `UserRole.ADMIN`: Administrative CRUD endpoints (`/api/v1/admin/*`). Protected via `Depends(require_admin)` which inspects JWT payload and raises `403 Forbidden` for regular subscribers.
