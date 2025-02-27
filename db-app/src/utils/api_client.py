import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# db configuration
DB_HOST = os.getenv("DB-HOST", "tether-database.postgres.database.azure.com")
DB_NAME = os.getenv("DB-NAME", "your_database_name")
DB_USER = os.getenv("DB-USER", "your_username")
DB_PASSWORD = os.getenv("DB-PASSWORD", "your_password")
DB_PORT = os.getenv("DB-PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dependency for db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()