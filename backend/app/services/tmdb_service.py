import httpx
import time
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.config.settings import settings
from app.models.movie import Movie, Genre, Actor, MovieActor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tmdb_service")

KNOWN_LANGUAGES = {
    "te": "Telugu",
    "hi": "Hindi",
    "ta": "Tamil",
    "ml": "Malayalam",
    "kn": "Kannada",
    "en": "English",
    "ko": "Korean",
    "ja": "Japanese",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "zh": "Chinese",
}

GENRE_NAME_TO_ID = {
    "action": 28,
    "adventure": 12,
    "animation": 16,
    "comedy": 35,
    "crime": 80,
    "documentary": 99,
    "drama": 18,
    "family": 10751,
    "fantasy": 14,
    "history": 36,
    "horror": 27,
    "music": 10402,
    "mystery": 9648,
    "romance": 10749,
    "sci-fi": 878,
    "science fiction": 878,
    "thriller": 53,
    "tv movie": 10770,
    "war": 10752,
    "western": 37,
}

GENRE_ID_TO_NAME = {v: k.title() for k, v in GENRE_NAME_TO_ID.items()}

def resolve_language_name(iso_code: str) -> str:
    if not iso_code:
        return "English"
    code = iso_code.lower()
    if code in KNOWN_LANGUAGES:
        return KNOWN_LANGUAGES[code]
    return code.capitalize()

class TMDBService:
    BASE_URL = getattr(settings, "TMDB_BASE_URL", "https://api.themoviedb.org/3")
    _client: Optional[httpx.Client] = None

    @classmethod
    def _get_headers(cls) -> dict:
        return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CineNest/1.0"}

    @classmethod
    def format_tmdb_item_to_dict(cls, item: dict) -> dict:
        """
        Converts a raw TMDB movie item into a clean MovieResponse-compatible dictionary
        IN-MEMORY without touching MySQL database.
        """
        tmdb_id = item.get("id")
        poster_path = item.get("poster_path")
        backdrop_path = item.get("backdrop_path")
        title = item.get("title") or item.get("original_title") or "Untitled Movie"
        orig_title = item.get("original_title")
        orig_lang = item.get("original_language", "en")
        overview = item.get("overview", "")
        release_date_str = item.get("release_date")

        release_year = 2024
        parsed_release_date = None
        if release_date_str:
            try:
                dt = datetime.strptime(release_date_str, "%Y-%m-%d")
                release_year = dt.year
                parsed_release_date = dt.date()
            except ValueError:
                pass

        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=500&q=80"
        backdrop_url = f"https://image.tmdb.org/t/p/w1280{backdrop_path}" if backdrop_path else None

        genres_list = []
        if "genres" in item and isinstance(item["genres"], list):
            for g in item["genres"]:
                if isinstance(g, dict) and "name" in g:
                    genres_list.append({"id": g.get("id", 0), "name": g.get("name")})
        elif "genre_ids" in item and isinstance(item["genre_ids"], list):
            for gid in item["genre_ids"]:
                gname = GENRE_ID_TO_NAME.get(gid, "Drama")
                genres_list.append({"id": gid, "name": gname})

        # Trailer URL extraction if present
        trailer_url = None
        is_official = False
        if "videos" in item and isinstance(item["videos"], dict):
            results = item["videos"].get("results", [])
            for v in results:
                if v.get("site") == "YouTube" and v.get("type") in ["Trailer", "Teaser"]:
                    trailer_url = f"https://www.youtube.com/embed/{v.get('key')}"
                    is_official = bool(v.get("official"))
                    break

        director = None
        if "credits" in item and isinstance(item["credits"], dict):
            crew = item["credits"].get("crew", [])
            for member in crew:
                if member.get("job") == "Director":
                    director = member.get("name")
                    break

        now_str = datetime.now()
        return {
            "id": tmdb_id,
            "tmdb_id": tmdb_id,
            "imdb_id": item.get("imdb_id"),
            "title": title,
            "original_title": orig_title,
            "description": overview,
            "storyline": overview,
            "release_date": parsed_release_date,
            "release_year": release_year,
            "imdb_rating": float(item.get("vote_average", 0.0)),
            "imdb_vote_count": int(item.get("vote_count", 0)),
            "popularity": float(item.get("popularity", 0.0)),
            "poster_url": poster_url,
            "backdrop_url": backdrop_url,
            "trailer_url": trailer_url,
            "video_key": None,
            "video_site": "YouTube" if trailer_url else None,
            "video_type": "Trailer" if trailer_url else None,
            "is_official_trailer": is_official,
            "language": resolve_language_name(orig_lang),
            "original_language": orig_lang,
            "country": "India" if orig_lang in ["te", "hi", "ta", "ml", "kn"] else "USA",
            "production_company": None,
            "director": director,
            "created_at": now_str,
            "updated_at": now_str,
            "genres": genres_list
        }

    @classmethod
    def _get_client(cls) -> httpx.Client:
        if cls._client is None or cls._client.is_closed:
            cls._client = httpx.Client(
                headers=cls._get_headers(),
                timeout=10.0,
                follow_redirects=True
            )
        return cls._client

    @classmethod
    def _safe_get(cls, url: str, params: dict, client: Optional[httpx.Client] = None) -> dict:
        headers = cls._get_headers()
        for attempt in range(3):
            try:
                verify_ssl = (attempt == 0)
                r = httpx.get(url, params=params, headers=headers, timeout=10.0, follow_redirects=True, verify=verify_ssl)
                if r.status_code == 200:
                    return r.json()
            except Exception as e:
                logger.warning(f"TMDB request retry warning ({url}): {e}")
                time.sleep(0.1)
        return {}

    @classmethod
    def search_tmdb_live(cls, query: str, page: int = 1) -> List[dict]:
        """
        Dynamic live TMDB search for movie titles, actor names, genres, languages, and release years.
        Returns list of clean MovieResponse dicts IN-MEMORY without modifying MySQL database.
        """
        api_key = settings.TMDB_API_KEY
        clean_q = query.strip()
        if not clean_q or not api_key:
            return []

        lower_q = clean_q.lower()
        is_year = clean_q.isdigit() and len(clean_q) == 4

        raw_items = []
        with httpx.Client(headers=cls._get_headers(), timeout=10.0, follow_redirects=True) as client:
            # 1. Person / Actor Search on TMDB
            try:
                p_data = cls._safe_get(f"{cls.BASE_URL}/search/person", {"api_key": api_key, "query": clean_q, "page": page}, client=client)
                p_results = p_data.get("results", [])
                if p_results:
                    pid = p_results[0].get("id")
                    c_data = cls._safe_get(f"{cls.BASE_URL}/person/{pid}/movie_credits", {"api_key": api_key}, client=client)
                    cast_movies = c_data.get("cast", [])[:20]
                    raw_items.extend(cast_movies)
            except Exception as e:
                logger.warning(f"Live TMDB actor search error: {e}")

            # 2. Movie Title / Year Search on TMDB
            try:
                m_params = {"api_key": api_key, "query": clean_q, "page": page}
                if is_year:
                    m_params["primary_release_year"] = int(clean_q)
                m_data = cls._safe_get(f"{cls.BASE_URL}/search/movie", m_params, client=client)
                raw_items.extend(m_data.get("results", []))
            except Exception as e:
                logger.warning(f"Live TMDB title search error: {e}")

            # 3. Genre / Language Discover Search if query matches known genre
            try:
                if lower_q in GENRE_NAME_TO_ID:
                    gid = GENRE_NAME_TO_ID[lower_q]
                    disc_data = cls._safe_get(f"{cls.BASE_URL}/discover/movie", {"api_key": api_key, "with_genres": gid, "sort_by": "popularity.desc", "page": page}, client=client)
                    raw_items.extend(disc_data.get("results", []))
            except Exception as e:
                logger.warning(f"Live TMDB genre discover error: {e}")

        # Deduplicate raw items by TMDB ID
        seen_ids = set()
        formatted_list = []
        for it in raw_items:
            mid = it.get("id")
            if mid and mid not in seen_ids:
                seen_ids.add(mid)
                formatted_list.append(cls.format_tmdb_item_to_dict(it))

        return formatted_list

    @classmethod
    def fetch_trending_live(cls, page: int = 1, limit: int = 20) -> List[dict]:
        """Fetches live trending/popular movies from TMDB in-memory."""
        api_key = settings.TMDB_API_KEY
        if not api_key:
            return []

        data = cls._safe_get(f"{cls.BASE_URL}/trending/movie/week", {"api_key": api_key, "page": page})
        results = data.get("results", [])[:limit]
        return [cls.format_tmdb_item_to_dict(it) for it in results]

    @classmethod
    def fetch_new_releases_live(cls, page: int = 1, limit: int = 20) -> List[dict]:
        """Fetches live 2024-2026 new releases from TMDB in-memory."""
        api_key = settings.TMDB_API_KEY
        if not api_key:
            return []

        data = cls._safe_get(
            f"{cls.BASE_URL}/discover/movie",
            {"api_key": api_key, "primary_release_year": 2024, "sort_by": "popularity.desc", "page": page}
        )
        results = data.get("results", [])[:limit]
        return [cls.format_tmdb_item_to_dict(it) for it in results]

    @classmethod
    def fetch_genre_movies_live(cls, genre_name: str, page: int = 1, limit: int = 15) -> List[dict]:
        """Fetches movies matching genre from TMDB in-memory."""
        api_key = settings.TMDB_API_KEY
        clean_g = genre_name.lower().strip()
        gid = GENRE_NAME_TO_ID.get(clean_g)
        if not api_key or not gid:
            return []

        data = cls._safe_get(
            f"{cls.BASE_URL}/discover/movie",
            {"api_key": api_key, "with_genres": gid, "sort_by": "popularity.desc", "page": page}
        )
        results = data.get("results", [])[:limit]
        return [cls.format_tmdb_item_to_dict(it) for it in results]

    @classmethod
    def fetch_actor_movies_live(cls, actor_name: str, page: int = 1, limit: int = 15) -> List[dict]:
        """Fetches movies featuring an actor from TMDB in-memory."""
        api_key = settings.TMDB_API_KEY
        if not api_key or not actor_name:
            return []

        p_data = cls._safe_get(f"{cls.BASE_URL}/search/person", {"api_key": api_key, "query": actor_name, "page": page})
        p_results = p_data.get("results", [])
        if p_results:
            pid = p_results[0].get("id")
            c_data = cls._safe_get(f"{cls.BASE_URL}/person/{pid}/movie_credits", {"api_key": api_key})
            cast_movies = c_data.get("cast", [])[:limit]
            return [cls.format_tmdb_item_to_dict(it) for it in cast_movies]
        return []

    @classmethod
    def get_tmdb_movie_details_live(cls, tmdb_id: int) -> Optional[dict]:
        """Fetches detailed metadata, videos/trailers, and cast for a single movie from TMDB in-memory."""
        api_key = settings.TMDB_API_KEY
        if not api_key or not tmdb_id:
            return None

        res_data = cls._safe_get(
            f"{cls.BASE_URL}/movie/{tmdb_id}",
            {"api_key": api_key, "append_to_response": "credits,videos"}
        )
        if res_data and "id" in res_data:
            return cls.format_tmdb_item_to_dict(res_data)
        return None

    @classmethod
    def ensure_movie_in_db(cls, db: Session, movie_id_or_tmdb_id: int) -> Optional[Movie]:
        """
        On-demand minimal activity reference:
        Checks MySQL for existing movie by id or tmdb_id.
        ONLY if not found in MySQL and user is performing an activity (Like, Rate, Watch, Not-Interested),
        fetches metadata for ONLY THAT SINGLE MOVIE from TMDB and inserts 1 row into MySQL so foreign keys match.
        """
        movie = db.query(Movie).filter(
            (Movie.id == movie_id_or_tmdb_id) | (Movie.tmdb_id == movie_id_or_tmdb_id)
        ).first()

        if movie:
            return movie

        # Fetch single movie from TMDB and insert minimal reference row
        api_key = settings.TMDB_API_KEY
        if not api_key:
            return None

        dd = cls._safe_get(
            f"{cls.BASE_URL}/movie/{movie_id_or_tmdb_id}",
            {"api_key": api_key, "append_to_response": "credits,videos"}
        )
        if not dd or "id" not in dd:
            return None

        try:
            tmdb_id = dd.get("id")
            title = dd.get("title") or dd.get("original_title") or "Untitled Movie"
            poster_path = dd.get("poster_path")
            backdrop_path = dd.get("backdrop_path")
            release_date_str = dd.get("release_date")
            overview = dd.get("overview", "")
            orig_lang = dd.get("original_language", "en")

            release_year = 2024
            parsed_release_date = None
            if release_date_str:
                try:
                    dt = datetime.strptime(release_date_str, "%Y-%m-%d")
                    release_year = dt.year
                    parsed_release_date = dt.date()
                except ValueError:
                    pass

            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
            backdrop_url = f"https://image.tmdb.org/t/p/w1280{backdrop_path}" if backdrop_path else None

            director_name = None
            crew = dd.get("credits", {}).get("crew", [])
            for member in crew:
                if member.get("job") == "Director":
                    director_name = member.get("name")
                    break

            trailer_url = None
            is_official = False
            videos = dd.get("videos", {}).get("results", [])
            for v in videos:
                if v.get("site") == "YouTube" and v.get("type") in ["Trailer", "Teaser"]:
                    trailer_url = f"https://www.youtube.com/embed/{v.get('key')}"
                    is_official = bool(v.get("official"))
                    break

            new_m = Movie(
                tmdb_id=tmdb_id,
                imdb_id=dd.get("imdb_id"),
                title=title,
                original_title=dd.get("original_title"),
                description=overview,
                storyline=overview,
                release_date=parsed_release_date,
                release_year=release_year,
                imdb_rating=float(dd.get("vote_average", 0.0)),
                imdb_vote_count=int(dd.get("vote_count", 0)),
                popularity=float(dd.get("popularity", 0.0)),
                poster_url=poster_url,
                backdrop_url=backdrop_url,
                trailer_url=trailer_url,
                is_official_trailer=is_official,
                language=resolve_language_name(orig_lang),
                original_language=orig_lang,
                country="India" if orig_lang in ["te", "hi", "ta", "ml", "kn"] else "USA",
                director=director_name
            )

            for g in dd.get("genres", []):
                gn = g.get("name")
                if gn:
                    dbg = db.query(Genre).filter(Genre.name == gn).first()
                    if not dbg:
                        dbg = Genre(name=gn)
                        db.add(dbg)
                        db.flush()
                    new_m.genres.append(dbg)

            db.add(new_m)
            db.flush()

            cast_list = dd.get("credits", {}).get("cast", [])[:5]
            for c in cast_list:
                cn = c.get("name")
                ch_name = c.get("character")
                pp = c.get("profile_path")
                purl = f"https://image.tmdb.org/t/p/w185{pp}" if pp else None
                if cn:
                    dba = db.query(Actor).filter(Actor.name == cn).first()
                    if not dba:
                        dba = Actor(name=cn, profile_image_url=purl)
                        db.add(dba)
                        db.flush()
                    ma = MovieActor(movie_id=new_m.id, actor_id=dba.id, character_name=ch_name)
                    db.add(ma)

            db.commit()
            return new_m
        except Exception as e:
            logger.error(f"Error in ensure_movie_in_db for {movie_id_or_tmdb_id}: {e}")
            db.rollback()
            return None
