import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from urllib.parse import quote_plus
from contextlib import contextmanager

logger = logging.getLogger("db_microservice")

load_dotenv()

# db configuration
DB_HOST = os.getenv("DB-HOST", "tether-database.postgres.database.azure.com")
DB_NAME = os.getenv("DB-NAME", "your_database_name")
DB_USER = os.getenv("DB-USER", "your_username")
DB_PASSWORD = os.getenv("DB-PASSWORD", "your_password")
DB_PORT = os.getenv("DB-PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
# logger.debug(f"Connecting to database using: {DATABASE_URL}")

# [1] initialise database connection
try:
    logger.info("Initialising database connection...")
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info("Database connection established")
except Exception as e:
    logger.error(f"Error connecting to database", exc_info=True) 
    raise RuntimeError(f"Database connection failed: {str(e)}") from e

# [2] session management (dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def db_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error("Database session error", exc_info=True)
        raise
    finally:
        db.close()