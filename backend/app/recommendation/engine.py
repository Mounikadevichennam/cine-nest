import math
import re
from collections import Counter
from typing import List, Dict, Set, Any
from sqlalchemy.orm import Session, joinedload
from app.models.movie import Movie, Genre, Actor, MovieActor
from app.models.user import User, user_favourite_genres, user_favourite_actors
from app.models.activity import WatchHistory, Like, NotInterested, Rating, SearchHistory
from app.services.tmdb_service import TMDBService

def compute_tfidf_cosine_sims(candidate_texts: List[str], profile_text: str) -> List[float]:
    """Pure-Python TF-IDF Vectorizer and Cosine Similarity calculation."""
    def tokenize(text: str) -> List[str]:
        return re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())

    docs = [tokenize(t) for t in candidate_texts]
    N = len(docs)
    if N == 0:
        return []

    doc_freqs = Counter()
    for doc in docs:
        unique_words = set(doc)
        for w in unique_words:
            doc_freqs[w] += 1

    idfs = {w: math.log((N + 1) / (df + 1)) + 1.0 for w, df in doc_freqs.items()}

    def get_tfidf_vector(tokens: List[str]) -> Dict[str, float]:
        tf = Counter(tokens)
        total = float(len(tokens) or 1)
        return {w: (count / total) * idfs.get(w, 1.0) for w, count in tf.items()}

    profile_vec = get_tfidf_vector(tokenize(profile_text))
    p_norm = math.sqrt(sum(val * val for val in profile_vec.values()))

    sims = []
    for doc in docs:
        doc_vec = get_tfidf_vector(doc)
        d_norm = math.sqrt(sum(val * val for val in doc_vec.values()))
        if p_norm == 0 or d_norm == 0:
            sims.append(0.0)
        else:
            dot = sum(val * doc_vec.get(w, 0.0) for w, val in profile_vec.items())
            sims.append(dot / (p_norm * d_norm))
    return sims

class RecommendationEngine:
    """
    CineNest 100-Point Hybrid Recommendation Engine.
    Combines user onboarding preferences, behavioral signals (likes, ratings, watch completion),
    explicit NotInterested negative filters, recency search interest, and live TMDB candidates.
    """

    @classmethod
    def get_recommendations_for_user(cls, db: Session, user: User, limit: int = 20) -> List[dict]:
        # 1. Fetch live TMDB candidate pool in-memory
        live_candidates = []
        try:
            live_candidates.extend(TMDBService.fetch_trending_live(limit=20))
            live_candidates.extend(TMDBService.fetch_new_releases_live(limit=20))
            for fg in user.favourite_genres:
                live_candidates.extend(TMDBService.fetch_genre_movies_live(fg.name, limit=10))
            for fa in user.favourite_actors:
                live_candidates.extend(TMDBService.fetch_actor_movies_live(fa.name, limit=10))
        except Exception:
            pass

        # Also fetch existing MySQL movie objects
        db_movies = db.query(Movie).options(
            joinedload(Movie.genres),
            joinedload(Movie.movie_actors).joinedload(MovieActor.actor)
        ).filter(Movie.poster_url != None).all()

        # Merge live candidates and DB movies into candidate dicts deduplicated by tmdb_id
        candidate_dict: Dict[int, dict] = {}
        for dbm in db_movies:
            m_dict = {
                "id": dbm.id,
                "tmdb_id": dbm.tmdb_id or dbm.id,
                "title": dbm.title,
                "description": dbm.description or dbm.storyline,
                "storyline": dbm.storyline or dbm.description,
                "release_year": dbm.release_year,
                "imdb_rating": dbm.imdb_rating,
                "poster_url": dbm.poster_url,
                "backdrop_url": dbm.backdrop_url,
                "trailer_url": dbm.trailer_url,
                "language": dbm.language,
                "genres": [{"id": g.id, "name": g.name} for g in dbm.genres],
                "actors": [ma.actor.name.lower() for ma in dbm.movie_actors if ma.actor],
                "db_obj": dbm
            }
            key = dbm.tmdb_id or dbm.id
            candidate_dict[key] = m_dict

        for lc in live_candidates:
            tid = lc.get("tmdb_id") or lc.get("id")
            if tid and tid not in candidate_dict:
                g_objs = lc.get("genres", [])
                g_names = [g["name"].lower() for g in g_objs if isinstance(g, dict) and "name" in g]
                lc_dict = {
                    "id": lc.get("id"),
                    "tmdb_id": tid,
                    "title": lc.get("title"),
                    "description": lc.get("description"),
                    "storyline": lc.get("storyline"),
                    "release_year": lc.get("release_year", 2024),
                    "imdb_rating": lc.get("imdb_rating", 0.0),
                    "poster_url": lc.get("poster_url"),
                    "backdrop_url": lc.get("backdrop_url"),
                    "trailer_url": lc.get("trailer_url"),
                    "language": lc.get("language"),
                    "genres": g_objs,
                    "actors": [],
                    "raw_dict": lc
                }
                candidate_dict[tid] = lc_dict

        if not candidate_dict:
            return []

        # 2. Extract explicit Not Interested negative preference IDs & details
        not_interested_movies = db.query(Movie).options(
            joinedload(Movie.genres),
            joinedload(Movie.movie_actors).joinedload(MovieActor.actor)
        ).join(NotInterested, NotInterested.movie_id == Movie.id).filter(NotInterested.user_id == user.id).all()

        not_interested_tmdb_ids = {m.tmdb_id or m.id for m in not_interested_movies}
        disliked_genres: Set[str] = set()
        disliked_actors: Set[str] = set()
        for nm in not_interested_movies:
            for g in nm.genres:
                disliked_genres.add(g.name.lower())
            for ma in nm.movie_actors:
                if ma.actor:
                    disliked_actors.add(ma.actor.name.lower())

        # Filter out explicit Not Interested candidates
        candidates = [c for tid, c in candidate_dict.items() if tid not in not_interested_tmdb_ids]
        if not candidates:
            return []

        # 3. User profile preferences (Onboarding data)
        pref_lang = (user.preferred_language or "Telugu").lower()

        fav_genres = db.query(Genre.name).join(user_favourite_genres).filter(user_favourite_genres.c.user_id == user.id).all()
        fav_genre_names = {g[0].lower() for g in fav_genres}

        fav_actors = db.query(Actor.name).join(user_favourite_actors).filter(user_favourite_actors.c.user_id == user.id).all()
        fav_actor_names = {a[0].lower() for a in fav_actors}

        # 4. User behavioral feedback signals from DB
        likes_movie_ids = {lk[0] for lk in db.query(Like.movie_id).filter(Like.user_id == user.id).all()}
        ratings_map = {r.movie_id: r.rating for r in db.query(Rating).filter(Rating.user_id == user.id).all()}
        
        watch_records = db.query(WatchHistory).filter(WatchHistory.user_id == user.id).all()
        watch_map = {w.movie_id: (w.completion_percentage, w.watch_count) for w in watch_records}

        recent_searches = [
            s[0].lower() for s in db.query(SearchHistory.search_query).filter(SearchHistory.user_id == user.id).order_by(SearchHistory.searched_at.desc()).limit(5).all()
        ]

        # 5. Pure-Python TF-IDF Plot Similarity
        plots = [c.get("storyline") or c.get("description") or c.get("title") or "movie" for c in candidates]
        profile_text = f"{pref_lang} {' '.join(fav_genre_names)} {' '.join(fav_actor_names)} {' '.join(recent_searches)}"
        tfidf_sims = compute_tfidf_cosine_sims(plots, profile_text)

        # 6. Compute 100-Point Hybrid Score for each candidate
        scored_movies = []
        for idx, item in enumerate(candidates):
            score = 0.0

            # Signal A: Language Match (10 pts)
            lang = (item.get("language") or "").lower()
            if lang and lang == pref_lang:
                score += 10.0

            # Signal B: Genre Match (20 pts)
            g_list = item.get("genres", [])
            m_genres = set()
            for g in g_list:
                if isinstance(g, dict) and "name" in g:
                    m_genres.add(g["name"].lower())
                elif isinstance(g, str):
                    m_genres.add(g.lower())

            matching_genres = m_genres.intersection(fav_genre_names)
            if fav_genre_names:
                score += min(20.0, (len(matching_genres) / max(1, len(fav_genre_names))) * 20.0)
            elif m_genres:
                score += 5.0

            if disliked_genres and m_genres.intersection(disliked_genres):
                score -= 5.0

            # Signal C: Actor Match (15 pts)
            m_actors = set(item.get("actors", []))
            matching_actors = m_actors.intersection(fav_actor_names)
            if fav_actor_names:
                score += min(15.0, (len(matching_actors) / max(1, len(fav_actor_names))) * 15.0)

            if disliked_actors and m_actors.intersection(disliked_actors):
                score -= 5.0

            # Signal D: TF-IDF Plot Similarity (15 pts)
            if idx < len(tfidf_sims):
                score += float(tfidf_sims[idx]) * 15.0

            # Signal E: User Behaviour Feedback (20 pts)
            db_id = item.get("id")
            if db_id in likes_movie_ids:
                score += 10.0

            user_rating = ratings_map.get(db_id)
            if user_rating:
                if user_rating == 5:
                    score += 8.0
                elif user_rating == 4:
                    score += 5.0
                elif user_rating == 3:
                    score += 2.0
                elif user_rating == 2:
                    score -= 5.0
                elif user_rating == 1:
                    score -= 10.0

            watch_info = watch_map.get(db_id)
            if watch_info:
                completion, repeat_count = watch_info
                score += (completion / 100.0) * 5.0
                if repeat_count > 1:
                    score += min(5.0, repeat_count * 2.0)

            # Signal F: Recent Search Interest (10 pts)
            title_lower = (item.get("title") or "").lower()
            if recent_searches:
                for sq in recent_searches:
                    if sq in title_lower or any(sq in g for g in m_genres):
                        score += 5.0
                        break

            # Signal G: Rating (5 pts)
            r_val = float(item.get("imdb_rating") or 0.0)
            score += (min(10.0, max(0.0, r_val)) / 10.0) * 5.0

            # Signal H: Release Year Recency (5 pts)
            y_val = int(item.get("release_year") or 2024)
            year_diff = max(0, 2026 - y_val)
            score += max(0.0, 5.0 - (year_diff * 0.5))

            scored_movies.append((score, item))

        scored_movies.sort(key=lambda x: x[0], reverse=True)

        result_list = []
        for _, item in scored_movies[:limit]:
            raw = item.get("raw_dict")
            db_obj = item.get("db_obj")

            if raw:
                if db_obj:
                    if raw.get("poster_url"): db_obj.poster_url = raw["poster_url"]
                    if raw.get("backdrop_url"): db_obj.backdrop_url = raw["backdrop_url"]
                    if raw.get("trailer_url"): db_obj.trailer_url = raw["trailer_url"]
                    if raw.get("tmdb_id"): db_obj.tmdb_id = raw["tmdb_id"]
                result_list.append(raw)
            elif db_obj:
                poster = db_obj.poster_url or ""
                if not poster or "3z8c8" in poster or "stree2" in poster or "j67X0f1" in poster or "b02m18" in poster:
                    live_enrich = TMDBService.get_tmdb_movie_details_live(db_obj.tmdb_id or db_obj.id)
                    if live_enrich and live_enrich.get("poster_url"):
                        db_obj.poster_url = live_enrich["poster_url"]
                        db_obj.backdrop_url = live_enrich.get("backdrop_url") or db_obj.backdrop_url
                        db_obj.trailer_url = live_enrich.get("trailer_url") or db_obj.trailer_url
                        if live_enrich.get("tmdb_id"):
                            db_obj.tmdb_id = live_enrich["tmdb_id"]
                        result_list.append(live_enrich)
                    else:
                        result_list.append(db_obj)
                else:
                    result_list.append(db_obj)
            else:
                result_list.append(item)

        try:
            db.commit()
        except Exception:
            db.rollback()

        return result_list

    @classmethod
    def get_because_you_watched(cls, db: Session, user: User, limit: int = 10) -> List[Any]:
        """Recommends movies similar to user's most recently watched movie using live TMDB candidates."""
        last_watch = db.query(WatchHistory).filter(WatchHistory.user_id == user.id).order_by(WatchHistory.watched_at.desc()).first()
        if not last_watch:
            return TMDBService.fetch_trending_live(limit=limit)

        target_movie = db.query(Movie).options(joinedload(Movie.genres)).filter(Movie.id == last_watch.movie_id).first()
        if not target_movie:
            return TMDBService.fetch_trending_live(limit=limit)

        target_genre_name = target_movie.genres[0].name if target_movie.genres else "Action"
        return TMDBService.fetch_genre_movies_live(target_genre_name, limit=limit)
