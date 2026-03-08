from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

ENGINE = create_engine("sqlite:///./vaultlight.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)


class Base(DeclarativeBase):
    pass