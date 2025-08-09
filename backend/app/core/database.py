from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# create database engine
if settings.DATABASE_URL.startswith("sqlite"):
    # sqlite configuration
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )
elif settings.DATABASE_URL.startswith("mysql"):
    # mysql configuration
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False
    )
else:
    # postgresql configuration
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False
    )

# create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base class for models
Base = declarative_base()

# dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 