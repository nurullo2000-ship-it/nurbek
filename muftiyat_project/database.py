DATABASE_URL = "postgresql://postgres:СЕН_КОЙГОН_ПАРОЛЬ@localhost:5432/fastapi_db"
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://postgres:q1w2e3r4t5@localhost:5432/fastapi_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()