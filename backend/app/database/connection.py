import os
import logging
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings

logger = logging.getLogger("db_connection")

def get_engine():
    raw_url = settings.DATABASE_URL.strip() if settings.DATABASE_URL else "sqlite:///./cinenest.db"
    
    is_mysql = raw_url.startswith("mysql://") or raw_url.startswith("mysql+pymysql://")
    
    if is_mysql:
        # Standardize scheme to mysql+pymysql:// for PyMySQL driver compatibility
        if raw_url.startswith("mysql://"):
            raw_url = "mysql+pymysql://" + raw_url[len("mysql://"):]
        
        parsed = urlparse(raw_url)
        hostname = parsed.hostname or ""
        is_localhost = hostname in ["localhost", "127.0.0.1", "0.0.0.0", ""]
        is_production = (
            os.getenv("RENDER") is not None or
            os.getenv("ENVIRONMENT", "").lower() == "production" or
            not is_localhost
        )
        
        query_dict = parse_qs(parsed.query)
        
        # Extract SSL options and construct PyMySQL-compatible connect_args
        ssl_mode = query_dict.pop("ssl-mode", [None])[0] or query_dict.pop("ssl_mode", [None])[0]
        ssl_ca = query_dict.pop("ssl-ca", [None])[0] or query_dict.pop("ssl_ca", [None])[0]
        
        # Reconstruct clean URL without query parameters that trigger PyMySQL TypeErrors
        new_query = urlencode([(k, v) for k, vals in query_dict.items() for v in vals])
        clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
        
        connect_args = {}
        if ssl_ca:
            connect_args["ssl"] = {"ca": ssl_ca}
        elif ssl_mode:
            connect_args["ssl"] = {"ssl_mode": ssl_mode}
        elif not is_localhost:
            # Default SSL configuration for cloud MySQL databases (like Aiven)
            connect_args["ssl"] = {}

        try:
            eng = create_engine(
                clean_url,
                connect_args=connect_args,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False
            )
            with eng.connect() as conn:
                logger.info(f"Successfully connected to MySQL database ({hostname}).")
            return eng, False
        except Exception as e:
            if is_production:
                logger.error(f"CRITICAL: Production MySQL Connection Failed to host '{hostname}': {e}")
                raise RuntimeError(
                    f"Production MySQL Database Connection Failed: {e}. "
                    "Ensure DATABASE_URL is set correctly in Render environment, Aiven MySQL service is active, and SSL/TLS credentials are valid."
                ) from e
            else:
                logger.warning(
                    f"Local MySQL connection to localhost:3306 failed ({e}). "
                    "Falling back to local SQLite database for local development."
                )
                raw_url = "sqlite:///./cinenest.db"

    # Local SQLite database connection
    is_sqlite = raw_url.startswith("sqlite")
    connect_args = {"check_same_thread": False} if is_sqlite else {}
    eng = create_engine(raw_url, connect_args=connect_args, pool_pre_ping=not is_sqlite, echo=False)
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
