import pandas as pd
import numpy as np
from typing import List, Dict
from sqlalchemy.orm import Session, joinedload
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models.movie import Movie, Genre, Actor, MovieActor
from app.models.user import User, user_favourite_genres, user_favourite_actors
from app.models.activity import WatchHistory, Like, NotInterested, Rating, SearchHistory

class RecommendationEngine:
    """
    CineNest 100-Point Hybrid Recommendation Engine.
    Combines onboarding preferences, content TF-IDF plot vectors, user behavioral feedback,
    and search recency signals.
    """

    @classmethod
    def get_recommendations_for_user(cls, db: Session, user: User, limit: int = 20) -> List[Movie]:
        # Eagerly load catalog movies with genres and cast
        movies = db.query(Movie).options(
            joinedload(Movie.genres),
            joinedload(Movie.movie_actors).joinedload(MovieActor.actor)
        ).filter(Movie.poster_url != None).all()

        if not movies:
            return []

        # Get user explicit negative preferences (Not Interested)
        not_interested_ids = {
            ni[0] for ni in db.query(NotInterested.movie_id).filter(NotInterested.user_id == user.id).all()
        }

        # Filter out Not Interested movies
        candidate_movies = [m for m in movies if m.id not in not_interested_ids]
        if not candidate_movies:
            return []

        # User profile signals
        pref_lang = (user.preferred_language or "Telugu").lower()
        
        fav_genres = db.query(Genre.name).join(user_favourite_genres).filter(user_favourite_genres.c.user_id == user.id).all()
        fav_genre_names = {g[0].lower() for g in fav_genres}

        fav_actors = db.query(Actor.name).join(user_favourite_actors).filter(user_favourite_actors.c.user_id == user.id).all()
        fav_actor_names = {a[0].lower() for a in fav_actors}

        # User behavior signals
        likes_ids = {lk[0] for lk in db.query(Like.movie_id).filter(Like.user_id == user.id).all()}
        ratings_map = {r.movie_id: r.rating for r in db.query(Rating).filter(Rating.user_id == user.id).all()}
        watch_records = db.query(WatchHistory).filter(WatchHistory.user_id == user.id).all()
        watch_map = {w.movie_id: (w.completion_percentage, w.watch_count) for w in watch_records}
        
        recent_searches = [
            s[0].lower() for s in db.query(SearchHistory.search_query).filter(SearchHistory.user_id == user.id).order_by(SearchHistory.searched_at.desc()).limit(5).all()
        ]

        # TF-IDF Vectorizer for Storyline / Plot descriptions
        plots = [m.storyline or m.description or m.title or "movie" for m in candidate_movies]
        tfidf = TfidfVectorizer(stop_words='english')
        try:
            tfidf_matrix = tfidf.fit_transform(plots)
            profile_text = f"{pref_lang} {' '.join(fav_genre_names)} {' '.join(fav_actor_names)}"
            profile_vector = tfidf.transform([profile_text])
            tfidf_sims = cosine_similarity(profile_vector, tfidf_matrix)[0]
        except Exception:
            tfidf_sims = [0.0] * len(candidate_movies)

        scored_movies = []
        for idx, movie in enumerate(candidate_movies):
            score = 0.0

            # 1. Language Match (10 pts)
            if movie.language.lower() == pref_lang:
                score += 10.0

            # 2. Genre Match (20 pts)
            m_genres = {g.name.lower() for g in movie.genres}
            matching_genres = m_genres.intersection(fav_genre_names)
            if fav_genre_names:
                score += min(20.0, (len(matching_genres) / max(1, len(fav_genre_names))) * 20.0)
            elif m_genres:
                score += 5.0

            # 3. Actor Match (15 pts)
            m_actors = {ma.actor.name.lower() for ma in movie.movie_actors if ma.actor}
            matching_actors = m_actors.intersection(fav_actor_names)
            if fav_actor_names:
                score += min(15.0, (len(matching_actors) / max(1, len(fav_actor_names))) * 15.0)

            # 4. Description TF-IDF Cosine Similarity (15 pts)
            score += float(tfidf_sims[idx]) * 15.0

            # 5. User Behaviour Feedback (20 pts)
            if movie.id in likes_ids:
                score += 10.0
            
            user_rating = ratings_map.get(movie.id)
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

            watch_info = watch_map.get(movie.id)
            if watch_info:
                completion, repeat_count = watch_info
                score += (completion / 100.0) * 5.0
                if repeat_count > 1:
                    score += min(5.0, repeat_count * 2.0)

            # 6. Recent Interest / Recency Search Effect (10 pts)
            if recent_searches:
                for sq in recent_searches:
                    if sq in movie.title.lower() or any(sq in g for g in m_genres):
                        score += 5.0
                        break
            
            # 7. IMDb/TMDB Rating (5 pts)
            score += ((movie.imdb_rating or 0.0) / 10.0) * 5.0

            # 8. Release Year Recency (5 pts)
            year_diff = max(0, 2026 - movie.release_year)
            score += max(0.0, 5.0 - (year_diff * 0.5))

            scored_movies.append((score, movie))

        # Sort by final score descending
        scored_movies.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored_movies[:limit]]

    @classmethod
    def get_because_you_watched(cls, db: Session, user: User, limit: int = 10) -> List[Movie]:
        """Recommends movies similar to the user's most recently watched movie."""
        last_watch = db.query(WatchHistory).filter(WatchHistory.user_id == user.id).order_by(WatchHistory.watched_at.desc()).first()
        if not last_watch:
            return []
        
        target_movie = db.query(Movie).options(joinedload(Movie.genres)).filter(Movie.id == last_watch.movie_id).first()
        if not target_movie:
            return []
        
        target_genres = {g.id for g in target_movie.genres}
        similar = db.query(Movie).options(joinedload(Movie.genres)).filter(
            Movie.id != target_movie.id,
            Movie.language == target_movie.language
        ).limit(30).all()

        scored = []
        for m in similar:
            m_genres = {g.id for g in m.genres}
            match_count = len(target_genres.intersection(m_genres))
            scored.append((match_count, m))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored[:limit]]
