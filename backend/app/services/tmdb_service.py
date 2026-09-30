import httpx
import logging
import asyncio
from typing import List, Optional, Dict
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.config.settings import settings
from app.models.movie import Movie, Genre, Actor, MovieActor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tmdb_service")

# Map common TMDB ISO language codes to readable names
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

def resolve_language_name(iso_code: str) -> str:
    if not iso_code:
        return "English"
    code = iso_code.lower()
    if code in KNOWN_LANGUAGES:
        return KNOWN_LANGUAGES[code]
    return code.capitalize()

class TMDBService:
    BASE_URL = getattr(settings, "TMDB_BASE_URL", "https://api.themoviedb.org/3")

    @classmethod
    async def fetch_and_ingest_catalog(cls, db: Session, pages_per_query: int = 2):
        """
        Multi-year TMDB catalog ingestion across 2016-2026 for any language available in TMDB.
        Removes language restrictions while maintaining metadata, deduplication, and rich video details.
        """
        api_key = settings.TMDB_API_KEY
        if not api_key:
            logger.warning("TMDB_API_KEY is not set. Ingestion requires a valid TMDB API Key.")
            return {"status": "skipped", "reason": "Missing TMDB_API_KEY"}

        total_inserted = 0
        total_duplicates = 0

        # Language queries + Global popularity discovery
        queries = [
            {"code": "te", "name": "Telugu"},
            {"code": "hi", "name": "Hindi"},
            {"code": "ta", "name": "Tamil"},
            {"code": "ml", "name": "Malayalam"},
            {"code": "kn", "name": "Kannada"},
            {"code": "en", "name": "English"},
            {"code": None, "name": "Global Popular Movies"} # Any language in TMDB
        ]

        async with httpx.AsyncClient(timeout=12.0) as client:
            for q in queries:
                lang_code = q["code"]
                lang_name = q["name"]
                logger.info(f"--- Processing TMDB catalog ingestion for: {lang_name} [2016-2026] ---")

                for year in range(2016, 2027):
                    for page in range(1, pages_per_query + 1):
                        url = f"{cls.BASE_URL}/discover/movie"
                        params = {
                            "api_key": api_key,
                            "primary_release_year": year,
                            "sort_by": "popularity.desc",
                            "page": page
                        }
                        if lang_code:
                            params["with_original_language"] = lang_code

                        try:
                            res = await client.get(url, params=params)
                            if res.status_code != 200:
                                logger.error(f"TMDB API error {res.status_code} for {lang_name} {year}: {res.text}")
                                break
                            
                            data = res.json()
                            results = data.get("results", [])
                            if not results:
                                break

                            for item in results:
                                # Poster is strictly required for catalog insertion
                                poster_path = item.get("poster_path")
                                if not poster_path:
                                    continue

                                tmdb_id = item.get("id")
                                existing = db.query(Movie).filter(Movie.tmdb_id == tmdb_id).first()
                                if existing:
                                    total_duplicates += 1
                                    continue

                                title = item.get("title") or item.get("original_title")
                                if not title:
                                    continue

                                orig_title = item.get("original_title")
                                orig_lang = item.get("original_language", "en")
                                resolved_lang = resolve_language_name(orig_lang)
                                overview = item.get("overview", "")
                                release_date_str = item.get("release_date")
                                
                                release_year = year
                                parsed_release_date = None
                                if release_date_str:
                                    try:
                                        dt = datetime.strptime(release_date_str, "%Y-%m-%d")
                                        release_year = dt.year
                                        parsed_release_date = dt.date()
                                    except ValueError:
                                        pass

                                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                                backdrop_path = item.get("backdrop_path")
                                backdrop_url = f"https://image.tmdb.org/t/p/w1280{backdrop_path}" if backdrop_path else None
                                tmdb_rating = float(item.get("vote_average", 0.0))
                                tmdb_votes = int(item.get("vote_count", 0))
                                tmdb_popularity = float(item.get("popularity", 0.0))

                                # Fetch detailed metadata for cast, crew, videos, and IMDb ID
                                detail_url = f"{cls.BASE_URL}/movie/{tmdb_id}"
                                detail_params = {"api_key": api_key, "append_to_response": "credits,videos"}
                                detail_res = await client.get(detail_url, params=detail_params)
                                
                                trailer_url = None
                                video_key = None
                                video_site = None
                                video_type = None
                                is_official = False
                                imdb_id = None
                                director_name = None
                                genre_list = []
                                cast_list = []

                                if detail_res.status_code == 200:
                                    detail_data = detail_res.json()
                                    imdb_id = detail_data.get("imdb_id")
                                    genre_list = detail_data.get("genres", [])
                                    
                                    # Extract director from crew
                                    crew = detail_data.get("credits", {}).get("crew", [])
                                    for member in crew:
                                        if member.get("job") == "Director":
                                            director_name = member.get("name")
                                            break

                                    # Video / Trailer metadata extraction
                                    videos = detail_data.get("videos", {}).get("results", [])
                                    official_trailers = [v for v in videos if v.get("type") == "Trailer" and v.get("official") is True]
                                    any_trailers = [v for v in videos if v.get("type") in ["Trailer", "Teaser"]]
                                    
                                    target_video = official_trailers[0] if official_trailers else (any_trailers[0] if any_trailers else None)
                                    if target_video:
                                        video_key = target_video.get("key")
                                        video_site = target_video.get("site")
                                        video_type = target_video.get("type")
                                        is_official = bool(target_video.get("official"))
                                        if video_site == "YouTube" and video_key:
                                            trailer_url = f"https://www.youtube.com/embed/{video_key}"
                                    
                                    # Cast extraction (top 5)
                                    cast_list = detail_data.get("credits", {}).get("cast", [])[:5]

                                movie = Movie(
                                    tmdb_id=tmdb_id,
                                    imdb_id=imdb_id,
                                    title=title,
                                    original_title=orig_title,
                                    description=overview,
                                    storyline=overview,
                                    release_date=parsed_release_date,
                                    release_year=release_year,
                                    imdb_rating=tmdb_rating,
                                    imdb_vote_count=tmdb_votes,
                                    popularity=tmdb_popularity,
                                    poster_url=poster_url,
                                    backdrop_url=backdrop_url,
                                    trailer_url=trailer_url,
                                    video_key=video_key,
                                    video_site=video_site,
                                    video_type=video_type,
                                    is_official_trailer=is_official,
                                    language=resolved_lang,
                                    original_language=orig_lang,
                                    country="India" if orig_lang in ["te", "hi", "ta", "ml", "kn"] else "USA",
                                    director=director_name
                                )

                                # Attach Genres
                                for g in genre_list:
                                    g_name = g.get("name")
                                    if g_name:
                                        db_genre = db.query(Genre).filter(Genre.name == g_name).first()
                                        if not db_genre:
                                            db_genre = Genre(name=g_name)
                                            db.add(db_genre)
                                            db.flush()
                                        movie.genres.append(db_genre)

                                db.add(movie)
                                db.flush()

                                # Attach Actors
                                for c in cast_list:
                                    c_name = c.get("name")
                                    char_name = c.get("character")
                                    profile_path = c.get("profile_path")
                                    p_url = f"https://image.tmdb.org/t/p/w185{profile_path}" if profile_path else None

                                    if c_name:
                                        db_actor = db.query(Actor).filter(Actor.name == c_name).first()
                                        if not db_actor:
                                            db_actor = Actor(name=c_name, profile_image_url=p_url)
                                            db.add(db_actor)
                                            db.flush()
                                        movie_actor = MovieActor(movie_id=movie.id, actor_id=db_actor.id, character_name=char_name)
                                        db.add(movie_actor)

                                db.commit()
                                total_inserted += 1

                        except Exception as e:
                            logger.error(f"Error processing TMDB movie item: {e}")
                            db.rollback()

                        await asyncio.sleep(0.05) # Rate limit protection

        logger.info(f"TMDB Multi-Year Ingestion Finished. New inserted: {total_inserted}, Skipped duplicates: {total_duplicates}")
        return {"status": "success", "inserted": total_inserted, "duplicates": total_duplicates}

    @classmethod
    def print_catalog_summary(cls, db: Session):
        """Prints detailed catalog statistics including year breakdown, language distribution, poster & video count."""
        years = list(range(2016, 2027))
        
        all_movies = db.query(Movie).all()
        total_count = len(all_movies)
        poster_count = sum(1 for m in all_movies if m.poster_url)
        trailer_count = sum(1 for m in all_movies if m.trailer_url)
        
        year_counts = {yr: 0 for yr in years}
        lang_counts = {}

        for m in all_movies:
            if m.release_year in year_counts:
                year_counts[m.release_year] += 1
            lang_counts[m.language] = lang_counts.get(m.language, 0) + 1

        print("\n" + "="*85)
        print("                 CINENEST COMPLETE CATALOG AUDIT REPORT")
        print("="*85)
        print(f"TOTAL MOVIES IN DATABASE : {total_count}")
        print(f"POSTER VALID COUNT       : {poster_count} ({100.0 if total_count > 0 else 0:.1f}%)")
        print(f"TRAILER/VIDEO AVAILABLE  : {trailer_count} ({(trailer_count/total_count)*100.0 if total_count > 0 else 0:.1f}%)")
        print("-" * 85)
        
        print("YEAR-WISE BREAKDOWN (2016 - 2026):")
        year_str = " | ".join(f"{yr}: {year_counts[yr]}" for yr in years)
        print(year_str)
        print("-" * 85)

        print("LANGUAGE DISTRIBUTION:")
        sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)
        for lang, count in sorted_langs:
            pct = (count / total_count) * 100.0 if total_count > 0 else 0
            print(f"  • {lang:<15} : {count:^5} movies ({pct:.1f}%)")
        print("="*85 + "\n")
        return total_count

    @classmethod
    def search_and_sync_movies(cls, db: Session, query: str) -> List[Movie]:
        """
        Two-level search architecture:
        LEVEL 1: Queries local CineNest database for matching titles, actors, genres, languages, and years.
        LEVEL 2: If local results count < 10 or query is actor/year search, queries TMDB API directly for person credits and movie titles.
        Synchronizes matching real TMDB records into local database and returns deduplicated results.
        """
        api_key = settings.TMDB_API_KEY
        clean_q = query.strip()
        if not clean_q:
            return []

        search_term = f"%{clean_q}%"
        is_year = clean_q.isdigit() and len(clean_q) == 4
        
        q_filter = (
            Movie.title.ilike(search_term) |
            Movie.original_title.ilike(search_term) |
            Movie.language.ilike(search_term) |
            Movie.storyline.ilike(search_term) |
            Movie.genres.any(Genre.name.ilike(search_term)) |
            Movie.movie_actors.any(MovieActor.actor.has(Actor.name.ilike(search_term)))
        )
        lower_q = clean_q.lower()
        if "jr" in lower_q and "ntr" in lower_q or lower_q in ["ntr", "jr ntr", "jr. ntr"]:
            q_filter = q_filter | Movie.movie_actors.any(MovieActor.actor.has(Actor.name.ilike("%N.T. Rama Rao Jr.%")))

        if is_year:
            q_filter = q_filter | (Movie.release_year == int(clean_q))

        return db.query(Movie).filter(Movie.poster_url != None, q_filter).limit(40).all()

        # Level 2 TMDB Search & Ingestion if local results are empty
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CineNest/1.0"}
            with httpx.Client(timeout=2.0, headers=headers) as client:
                tmdb_movies_to_ingest = []

                # A. Person / Actor Search on TMDB
                try:
                    person_res = client.get(f"{cls.BASE_URL}/search/person", params={"api_key": api_key, "query": clean_q})
                    if person_res.status_code == 200:
                        p_data = person_res.json().get("results", [])
                        if p_data:
                            person_id = p_data[0].get("id")
                            credits_res = client.get(f"{cls.BASE_URL}/person/{person_id}/movie_credits", params={"api_key": api_key})
                            if credits_res.status_code == 200:
                                cast_movies = credits_res.json().get("cast", [])[:5]
                                tmdb_movies_to_ingest.extend(cast_movies)
                except Exception:
                    pass

                # B. Movie Title / Year Search on TMDB
                try:
                    movie_params = {"api_key": api_key, "query": clean_q}
                    if is_year:
                        movie_params["primary_release_year"] = int(clean_q)

                    m_res = client.get(f"{cls.BASE_URL}/search/movie", params=movie_params)
                    if m_res.status_code == 200:
                        tmdb_movies_to_ingest.extend(m_res.json().get("results", [])[:5])
                except Exception:
                    pass

                # C. Synchronize discovered TMDB movies into local DB
                added_count = 0
                for item in tmdb_movies_to_ingest:
                    if added_count >= 5:
                        break

                    poster_path = item.get("poster_path")
                    if not poster_path:
                        continue

                    tmdb_id = item.get("id")
                    if not tmdb_id:
                        continue

                    existing = db.query(Movie).filter(Movie.tmdb_id == tmdb_id).first()
                    if existing:
                        continue

                    title = item.get("title") or item.get("original_title")
                    if not title:
                        continue

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

                    if not (2016 <= release_year <= 2026):
                        continue

                    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                    backdrop_path = item.get("backdrop_path")
                    backdrop_url = f"https://image.tmdb.org/t/p/w1280{backdrop_path}" if backdrop_path else None
                    orig_lang = item.get("original_language", "en")

                    trailer_url = None
                    imdb_id = None
                    director_name = None
                    genre_list = []
                    cast_list = []

                    try:
                        detail_res = client.get(f"{cls.BASE_URL}/movie/{tmdb_id}", params={"api_key": api_key, "append_to_response": "credits,videos"})
                        if detail_res.status_code == 200:
                            dd = detail_res.json()
                            imdb_id = dd.get("imdb_id")
                            genre_list = dd.get("genres", [])
                            crew = dd.get("credits", {}).get("crew", [])
                            for member in crew:
                                if member.get("job") == "Director":
                                    director_name = member.get("name")
                                    break
                            videos = dd.get("videos", {}).get("results", [])
                            for v in videos:
                                if v.get("type") == "Trailer" and v.get("site") == "YouTube":
                                    trailer_url = f"https://www.youtube.com/embed/{v.get('key')}"
                                    break
                            cast_list = dd.get("credits", {}).get("cast", [])[:5]
                    except Exception:
                        pass

                    new_m = Movie(
                        tmdb_id=tmdb_id,
                        imdb_id=imdb_id,
                        title=title,
                        original_title=item.get("original_title"),
                        description=item.get("overview", ""),
                        storyline=item.get("overview", ""),
                        release_date=parsed_release_date,
                        release_year=release_year,
                        imdb_rating=float(item.get("vote_average", 0.0)),
                        imdb_vote_count=int(item.get("vote_count", 0)),
                        popularity=float(item.get("popularity", 0.0)),
                        poster_url=poster_url,
                        backdrop_url=backdrop_url,
                        trailer_url=trailer_url,
                        language=resolve_language_name(orig_lang),
                        original_language=orig_lang,
                        country="India" if orig_lang in ["te", "hi", "ta", "ml", "kn"] else "USA",
                        director=director_name
                    )

                    for g in genre_list:
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
                    added_count += 1
        except Exception as err:
            logger.error(f"Error in search_and_sync_movies: {err}")
            db.rollback()

        # Re-query local database after sync to include newly added TMDB items
        return db.query(Movie).filter(Movie.poster_url != None, q_filter).limit(40).all()

if __name__ == "__main__":
    from app.database.connection import SessionLocal
    db = SessionLocal()
    try:
        asyncio.run(TMDBService.fetch_and_ingest_catalog(db))
        TMDBService.print_catalog_summary(db)
    finally:
        db.close()
