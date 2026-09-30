import logging
from sqlalchemy.orm import Session
from app.database.connection import engine, SessionLocal
from app.models import Movie, Genre, Actor, MovieActor, User, UserRole, Profile
from app.auth.security import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed_data")

DEMO_MOVIES = [
    {
        "title": "RRR",
        "language": "Telugu",
        "release_year": 2022,
        "release_date": "2022-03-25",
        "imdb_rating": 8.8,
        "imdb_vote_count": 165000,
        "poster_url": "https://image.tmdb.org/t/p/w500/nEufeZlyAODFndB5mZFiVh9eJe.jpg",
        "trailer_url": "https://www.youtube.com/embed/f_vbAtFSS48",
        "storyline": "A fearless revolutionary and an officer in the British force join hands to fight against tyranny in colonial India.",
        "description": "Epic period action drama directed by S.S. Rajamouli.",
        "genres": ["Action", "Drama", "History"],
        "cast": [("N.T. Rama Rao Jr.", "Komaram Bheem"), ("Ram Charan", "Alluri Sitarama Raju"), ("Alia Bhatt", "Sita")]
    },
    {
        "title": "Pushpa 2: The Rule",
        "language": "Telugu",
        "release_year": 2024,
        "release_date": "2024-12-05",
        "imdb_rating": 8.5,
        "imdb_vote_count": 89000,
        "poster_url": "https://image.tmdb.org/t/p/w500/1X64qnd9c8w0t6eO1nK3Zq41W3t.jpg",
        "trailer_url": "https://www.youtube.com/embed/gKizDojsdvs",
        "storyline": "The clash between Pushpa Raj and SP Bhanwar Singh Shekhawat continues as Pushpa consolidates his red sandalwood smuggling empire.",
        "description": "High-octane mass action thriller starring Allu Arjun.",
        "genres": ["Action", "Crime", "Drama"],
        "cast": [("Allu Arjun", "Pushpa Raj"), ("Rashmika Mandanna", "Srivalli"), ("Fahadh Faasil", "Bhanwar Singh Shekhawat")]
    },
    {
        "title": "Kalki 2898 AD",
        "language": "Telugu",
        "release_year": 2024,
        "release_date": "2024-06-27",
        "imdb_rating": 8.1,
        "imdb_vote_count": 78000,
        "poster_url": "https://image.tmdb.org/t/p/w500/sN0FhW1o3m4o3o3z8c8z3c8z3c8.jpg",
        "trailer_url": "https://www.youtube.com/embed/k86x27z2t4s",
        "storyline": "A modern avatar of Vishnu descends to Earth to protect humanity from dark forces in a post-apocalyptic future.",
        "description": "Futuristic sci-fi mythological epic starring Prabhas, Amitabh Bachchan, and Kamal Haasan.",
        "genres": ["Sci-Fi", "Action", "Fantasy"],
        "cast": [("Prabhas", "Bhairava"), ("Amitabh Bachchan", "Ashwatthama"), ("Deepika Padukone", "SUM-80")]
    },
    {
        "title": "Kantara",
        "language": "Kannada",
        "release_year": 2022,
        "release_date": "2022-09-30",
        "imdb_rating": 8.3,
        "imdb_vote_count": 95000,
        "poster_url": "https://image.tmdb.org/t/p/w500/j67X0f1P0t3R9c8c8c8c8c8c8c8.jpg",
        "trailer_url": "https://www.youtube.com/embed/6o1R5x22Y58",
        "storyline": "When greed paves the way for a conflict between villagers and an evil landlord, a hero rises to protect divine land rights.",
        "description": "Folklore divine thriller directed by and starring Rishab Shetty.",
        "genres": ["Action", "Drama", "Thriller"],
        "cast": [("Rishab Shetty", "Shiva"), ("Sapthami Gowda", "Leela"), ("Kishore", "Murali")]
    },
    {
        "title": "Manjummel Boys",
        "language": "Malayalam",
        "release_year": 2024,
        "release_date": "2024-02-22",
        "imdb_rating": 8.6,
        "imdb_vote_count": 42000,
        "poster_url": "https://image.tmdb.org/t/p/w500/m500M3z8c8c8c8c8c8c8c8c8c8c.jpg",
        "trailer_url": "https://www.youtube.com/embed/3z8c8c8c8c8",
        "storyline": "A group of friends try to rescue their companion from the dangerous Guna Caves in Kodaikanal.",
        "description": "True-event survival thriller blockbuster from Malayalam cinema.",
        "genres": ["Adventure", "Drama", "Thriller"],
        "cast": [("Soubin Shahir", "Kuttan"), ("Sreenath Bhasi", "Subhash"), ("Balalu Menon", "Sixer")]
    },
    {
        "title": "Leo",
        "language": "Tamil",
        "release_year": 2023,
        "release_date": "2023-10-19",
        "imdb_rating": 7.9,
        "imdb_vote_count": 82000,
        "poster_url": "https://image.tmdb.org/t/p/w500/b02m18x2R3z8c8c8c8c8c8c8c8c.jpg",
        "trailer_url": "https://www.youtube.com/embed/Po3jIG6Qd80",
        "storyline": "A mild-mannered cafe owner in Himachal Pradesh becomes a target of dangerous gangsters who believe he is a former assassin.",
        "description": "Lokesh Cinematic Universe action thriller starring Thalapathy Vijay.",
        "genres": ["Action", "Crime", "Thriller"],
        "cast": [("Vijay", "Parthiban / Leo Das"), ("Trisha Krishnan", "Sathya"), ("Sanjay Dutt", "Antony Das")]
    },
    {
        "title": "Stree 2",
        "language": "Hindi",
        "release_year": 2024,
        "release_date": "2024-08-15",
        "imdb_rating": 7.8,
        "imdb_vote_count": 55000,
        "poster_url": "https://image.tmdb.org/t/p/w500/stree2poster123456789.jpg",
        "trailer_url": "https://www.youtube.com/embed/stree2trailer",
        "storyline": "The town of Chanderi faces a new menace in Sarkata, requiring Vicky and Stree to unite once again.",
        "description": "Horror-comedy blockbuster starring Rajkummar Rao and Shraddha Kapoor.",
        "genres": ["Comedy", "Horror"],
        "cast": [("Rajkummar Rao", "Vicky"), ("Shraddha Kapoor", "Untitled Maiden"), ("Pankaj Tripathi", "Rudra")]
    },
    {
        "title": "Dune: Part Two",
        "language": "English",
        "release_year": 2024,
        "release_date": "2024-03-01",
        "imdb_rating": 8.5,
        "imdb_vote_count": 320000,
        "poster_url": "https://image.tmdb.org/t/p/w500/1pdfLPoWuVh2ghUToChJOVLEjG3.jpg",
        "trailer_url": "https://www.youtube.com/embed/Way9Dexny3w",
        "storyline": "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.",
        "description": "Denis Villeneuve's epic sci-fi masterpiece.",
        "genres": ["Sci-Fi", "Adventure", "Action"],
        "cast": [("Timothée Chalamet", "Paul Atreides"), ("Zendaya", "Chani"), ("Rebecca Ferguson", "Lady Jessica")]
    }
]

def seed_database():
    db = SessionLocal()
    try:
        logger.info("Seeding CineNest Demonstration Data...")
        
        # 1. Seed Admin Account
        admin = db.query(User).filter(User.email == "admin@cinenest.com").first()
        if not admin:
            admin = User(
                name="CineNest Admin",
                email="admin@cinenest.com",
                password_hash=hash_password("Admin@123"),
                role=UserRole.ADMIN,
                preferred_language="Telugu"
            )
            db.add(admin)
            db.flush()

            admin_prof = Profile(
                user_id=admin.id,
                profile_name="Administrator",
                avatar="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80"
            )
            db.add(admin_prof)

        # 2. Seed Demo User Account
        user = db.query(User).filter(User.email == "mounika@cinenest.com").first()
        if not user:
            user = User(
                name="Mounika",
                email="mounika@cinenest.com",
                password_hash=hash_password("User@123"),
                role=UserRole.USER,
                preferred_language="Telugu"
            )
            db.add(user)
            db.flush()

            user_prof = Profile(
                user_id=user.id,
                profile_name="Mounika",
                avatar="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80"
            )
            db.add(user_prof)

        # 3. Seed Movie Catalog
        for m_data in DEMO_MOVIES:
            existing = db.query(Movie).filter(Movie.title == m_data["title"]).first()
            if existing:
                continue

            movie = Movie(
                title=m_data["title"],
                language=m_data["language"],
                release_year=m_data["release_year"],
                imdb_rating=m_data["imdb_rating"],
                imdb_vote_count=m_data["imdb_vote_count"],
                poster_url=m_data["poster_url"],
                trailer_url=m_data["trailer_url"],
                storyline=m_data["storyline"],
                description=m_data["description"],
                country="India" if m_data["language"] != "English" else "USA"
            )

            # Genres
            for g_name in m_data["genres"]:
                g = db.query(Genre).filter(Genre.name == g_name).first()
                if not g:
                    g = Genre(name=g_name)
                    db.add(g)
                    db.flush()
                if g not in movie.genres:
                    movie.genres.append(g)

            db.add(movie)
            db.flush()

            # Cast
            for a_name, char_name in m_data["cast"]:
                a = db.query(Actor).filter(Actor.name == a_name).first()
                if not a:
                    a = Actor(name=a_name)
                    db.add(a)
                    db.flush()
                ma = MovieActor(movie_id=movie.id, actor_id=a.id, character_name=char_name)
                db.add(ma)

        db.commit()
        logger.info("CineNest Seed Data successfully created!")

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
