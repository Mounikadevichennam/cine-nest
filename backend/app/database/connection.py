import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings

logger = logging.getLogger("db_connection")

def get_engine():
    db_url = settings.DATABASE_URL
    if db_url.startswith("mysql"):
        try:
            eng = create_engine(db_url, pool_pre_ping=True, pool_recycle=3600, echo=False)
            with eng.connect() as conn:
                pass
            return eng, False
        except Exception as e:
            logger.warning(f"MySQL connection failed ({e}). Falling back to local SQLite database.")
            db_url = "sqlite:///./cinenest.db"
    
    is_sqlite = db_url.startswith("sqlite")
    connect_args = {"check_same_thread": False} if is_sqlite else {}
    eng = create_engine(db_url, connect_args=connect_args, pool_pre_ping=not is_sqlite, echo=False)
    return eng, is_sqlite

engine, is_sqlite = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
