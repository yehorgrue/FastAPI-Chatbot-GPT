from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database
from sqlalchemy.orm import Session

from models.base import Base

from config.config import (
    PG_DB_HOST,
    PG_DB_USERNAME,
    PG_DB_PASSWORD,
    PG_DB_PORT,
    PG_DB_NAME,
    DB_URL,
)
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgresql://{PG_DB_USERNAME}:{PG_DB_PASSWORD}@{PG_DB_HOST}:{PG_DB_PORT}/{PG_DB_NAME}"

database = Database(DB_URL)
engine = create_engine(DB_URL)


# database = Database(DATABASE_URL)
# engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)


def drop_all_tables():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
