from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# engine = create_engine("postgresql://fazzelis:fazzelis@localhost:5432/rip")
engine = create_engine("postgresql://fazzelis:fazzelis@host.docker.internal:5432/rip")
# engine = create_engine("postgresql://fazzelis:fazzelis@postgresql:5432/rip")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
