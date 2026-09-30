# CineNest Recommendation Engine Specification

## 100-Point Conceptual Scoring Breakdown

| Parameter | Weight | Description |
| :--- | :--- | :--- |
| **Language** | 10 pts | Exact match with onboarding/profile preferred language |
| **Genre** | 20 pts | +1 pt per matching genre |
| **Actor** | 15 pts | +1 pt per matching actor |
| **TF-IDF Plot Similarity** | 15 pts | Cosine similarity on storyline embeddings |
| **User Behavior** | 20 pts | Completion rate & repeat watching |
| **Recency / Search** | 10 pts | Recent interest boost |
| **IMDb Rating** | 5 pts | Normalized IMDb rating factor |
| **Release Year** | 5 pts | Recency decay factor |

**Negative Adjustment**: `is_not_interested = True` penalizes matching genres/movies.
