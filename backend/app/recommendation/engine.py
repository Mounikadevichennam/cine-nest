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
            pref_lang = (user.preferred_language or "Telugu").lower()
            # A. Preferred Language top discovery (primary regional candidate pool)
            live_candidates.extend(TMDBService.fetch_language_movies_live(pref_lang, limit=20))

            # B. Favourite Genre candidates in Preferred Language + global
            for fg in user.favourite_genres:
                live_candidates.extend(TMDBService.fetch_language_movies_live(pref_lang, genre_name=fg.name, limit=10))
                live_candidates.extend(TMDBService.fetch_genre_movies_live(fg.name, limit=5))

            # C. Favourite Actor candidates
            for fa in user.favourite_actors:
                live_candidates.extend(TMDBService.fetch_actor_movies_live(fa.name, limit=10))

            # D. Global Trending & New Releases for catalog diversity
            live_candidates.extend(TMDBService.fetch_trending_live(limit=15))
            live_candidates.extend(TMDBService.fetch_new_releases_live(limit=15))
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
            if not tid:
                continue
            if tid in candidate_dict:
                existing = candidate_dict[tid]
                if lc.get("poster_url"):
                    existing["poster_url"] = lc["poster_url"]
                if lc.get("backdrop_url"):
                    existing["backdrop_url"] = lc["backdrop_url"]
                if lc.get("trailer_url"):
                    existing["trailer_url"] = lc["trailer_url"]
                if lc.get("actors"):
                    existing_actors = set(existing.get("actors", []))
                    existing_actors.update(lc["actors"])
                    existing["actors"] = list(existing_actors)
                existing["raw_dict"] = lc
            else:
                g_objs = lc.get("genres", [])
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
                    "actors": lc.get("actors", []),
                    "raw_dict": lc
                }
                candidate_dict[tid] = lc_dict

        if not candidate_dict:
            return []

        # 2. Extract explicit Not Interested negative preference IDs & details
        not_interested_rows = db.query(NotInterested.movie_id, Movie.tmdb_id).outerjoin(Movie, Movie.id == NotInterested.movie_id).filter(NotInterested.user_id == user.id).all()
        not_interested_ids = set()
        for mid, tid in not_interested_rows:
            if mid: not_interested_ids.add(mid)
            if tid: not_interested_ids.add(tid)

        not_interested_movies = db.query(Movie).options(
            joinedload(Movie.genres),
            joinedload(Movie.movie_actors).joinedload(MovieActor.actor)
        ).join(NotInterested, NotInterested.movie_id == Movie.id).filter(NotInterested.user_id == user.id).all()

        fav_genre_set = {g.name.lower() for g in user.favourite_genres}
        fav_actor_set = {a.name.lower() for a in user.favourite_actors}
        disliked_genres: Set[str] = set()
        disliked_actors: Set[str] = set()
        for nm in not_interested_movies:
            for g in nm.genres:
                gn = g.name.lower()
                if gn not in fav_genre_set:
                    disliked_genres.add(gn)
            for ma in nm.movie_actors:
                if ma.actor:
                    an = ma.actor.name.lower()
                    if an not in fav_actor_set:
                        disliked_actors.add(an)

        # Filter out explicit Not Interested candidates
        candidates = [
            c for tid, c in candidate_dict.items() 
            if tid not in not_interested_ids and c.get("id") not in not_interested_ids and c.get("tmdb_id") not in not_interested_ids
        ]
        if not candidates:
            return []

        # 3. User profile preferences (Onboarding data)
        pref_lang = (user.preferred_language or "Telugu").lower()

        fav_genres = db.query(Genre.name).join(user_favourite_genres).filter(user_favourite_genres.c.user_id == user.id).all()
        fav_genre_names = {g[0].lower() for g in fav_genres}

        fav_actors = db.query(Actor.name).join(user_favourite_actors).filter(user_favourite_actors.c.user_id == user.id).all()
        fav_actor_names = {a[0].lower() for a in fav_actors}

        # 4. User behavioral feedback signals from DB (mapped to both internal id and tmdb_id)
        likes_rows = db.query(Like.movie_id, Movie.tmdb_id).outerjoin(Movie, Movie.id == Like.movie_id).filter(Like.user_id == user.id).all()
        likes_ids = set()
        for mid, tid in likes_rows:
            if mid: likes_ids.add(mid)
            if tid: likes_ids.add(tid)

        ratings_rows = db.query(Rating.movie_id, Movie.tmdb_id, Rating.rating).outerjoin(Movie, Movie.id == Rating.movie_id).filter(Rating.user_id == user.id).all()
        ratings_map = {}
        for mid, tid, rval in ratings_rows:
            if mid: ratings_map[mid] = rval
            if tid: ratings_map[tid] = rval

        watch_rows = db.query(WatchHistory.movie_id, Movie.tmdb_id, WatchHistory.completion_percentage, WatchHistory.watch_count).outerjoin(Movie, Movie.id == WatchHistory.movie_id).filter(WatchHistory.user_id == user.id).all()
        watch_map = {}
        for mid, tid, comp, wcount in watch_rows:
            if mid: watch_map[mid] = (comp, wcount)
            if tid: watch_map[tid] = (comp, wcount)

        recent_searches = [
            s[0].lower() for s in db.query(SearchHistory.search_query).filter(SearchHistory.user_id == user.id).order_by(SearchHistory.searched_at.desc()).limit(5).all()
        ]

        from app.models.activity import RecentActivity
        recent_activity_rows = db.query(RecentActivity.movie_id, Movie.tmdb_id, Movie.title).outerjoin(Movie, Movie.id == RecentActivity.movie_id).filter(RecentActivity.user_id == user.id).order_by(RecentActivity.created_at.desc()).limit(10).all()
        recent_activity_titles = [r[2].lower() for r in recent_activity_rows if r[2]]

        # 5. Pure-Python TF-IDF Plot Similarity (15 pts)
        plots = [c.get("storyline") or c.get("description") or c.get("title") or "movie" for c in candidates]
        profile_text = f"{pref_lang} {' '.join(fav_genre_names)} {' '.join(fav_actor_names)} {' '.join(recent_searches)} {' '.join(recent_activity_titles)}"
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
            mid = item.get("id")
            tid = item.get("tmdb_id")
            beh_score = 0.0
            if (mid in likes_ids) or (tid in likes_ids):
                beh_score += 10.0

            user_rating = ratings_map.get(mid) or ratings_map.get(tid)
            if user_rating:
                if user_rating == 5:
                    beh_score += 8.0
                elif user_rating == 4:
                    beh_score += 5.0
                elif user_rating == 3:
                    beh_score += 0.0
                elif user_rating == 2:
                    beh_score -= 5.0
                elif user_rating == 1:
                    beh_score -= 10.0

            watch_info = watch_map.get(mid) or watch_map.get(tid)
            if watch_info:
                completion, repeat_count = watch_info
                beh_score += (completion / 100.0) * 5.0
                if repeat_count > 1:
                    beh_score += min(5.0, (repeat_count - 1) * 2.5)

            score += min(20.0, max(-15.0, beh_score))

            # Signal F: Recent Interest (10 pts)
            title_lower = (item.get("title") or "").lower()
            recent_score = 0.0
            if recent_searches:
                for sq in recent_searches:
                    if sq in title_lower or any(sq in g for g in m_genres):
                        recent_score += 5.0
                        break
            if recent_activity_titles:
                for rt in recent_activity_titles:
                    if rt in title_lower or any(rt in g for g in m_genres):
                        recent_score += 5.0
                        break
            score += min(10.0, recent_score)

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

            # Check poster validity
            p = item.get("poster_url") or ""
            if not p or not p.startswith("http") or "unsplash" in p or "placeholder" in p:
                tid = item.get("tmdb_id") or item.get("id")
                if tid:
                    live_enrich = TMDBService.get_tmdb_movie_details_live(tid)
                    if live_enrich and live_enrich.get("poster_url"):
                        item["poster_url"] = live_enrich["poster_url"]
                        if live_enrich.get("backdrop_url"): item["backdrop_url"] = live_enrich["backdrop_url"]
                        if live_enrich.get("trailer_url"): item["trailer_url"] = live_enrich["trailer_url"]
                        if db_obj:
                            db_obj.poster_url = live_enrich["poster_url"]
                            db_obj.backdrop_url = live_enrich.get("backdrop_url") or db_obj.backdrop_url
                            db_obj.trailer_url = live_enrich.get("trailer_url") or db_obj.trailer_url

            if raw:
                raw["poster_url"] = item.get("poster_url")
                raw["backdrop_url"] = item.get("backdrop_url")
                raw["trailer_url"] = item.get("trailer_url")
                if db_obj:
                    if raw.get("poster_url"): db_obj.poster_url = raw["poster_url"]
                    if raw.get("backdrop_url"): db_obj.backdrop_url = raw["backdrop_url"]
                    if raw.get("trailer_url"): db_obj.trailer_url = raw["trailer_url"]
                    if raw.get("tmdb_id"): db_obj.tmdb_id = raw["tmdb_id"]
                result_list.append(raw)
            elif db_obj:
                poster = db_obj.poster_url or ""
                if not poster or not poster.startswith("http") or "unsplash" in poster or "placeholder" in poster:
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
        pref_lang = user.preferred_language or "Telugu"
        if not last_watch:
            return TMDBService.fetch_language_movies_live(pref_lang, limit=limit)

        target_movie = db.query(Movie).options(joinedload(Movie.genres)).filter(Movie.id == last_watch.movie_id).first()
        if not target_movie:
            return TMDBService.fetch_language_movies_live(pref_lang, limit=limit)

        target_genre_name = target_movie.genres[0].name if target_movie.genres else "Action"
        target_lang = target_movie.language or pref_lang
        movies = TMDBService.fetch_language_movies_live(target_lang, genre_name=target_genre_name, limit=limit)
        if not movies:
            movies = TMDBService.fetch_genre_movies_live(target_genre_name, limit=limit)
        return movies
