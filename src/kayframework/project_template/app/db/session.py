from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .database import engine # database.py içinde engine tanımlı olduğunu varsayıyoruz

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()