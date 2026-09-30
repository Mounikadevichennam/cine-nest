import logging
from app.database.connection import engine, Base
from app.models import *  # Ensures all ORM models are registered with Base.metadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("init_db")

def init_db():
    """Initializes the MySQL database by creating all normalized tables if they do not exist."""
    logger.info("Initializing CineNest MySQL Database Schema...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("CineNest Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise e

if __name__ == "__main__":
    init_db()
