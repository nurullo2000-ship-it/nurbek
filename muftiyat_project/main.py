from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from database import Base, engine, SessionLocal

app = FastAPI(
    title="Менин API Документациям",
    description="PostgreSQL базасы менен иштеген Swagger API",
    version="1.0.0"
)


# Базанын сессиясын алуу
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Модель (Базадагы таблица)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)


# Таблица жок болсо, автоматтык түрдө түзөт
Base.metadata.create_all(bind=engine)


# Эндпоинт: Колдонуучуларды алуу
@app.get("/users", summary="Бардык колдонуучуларды алуу")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# Эндпоинт: Жаңы колдонуучу кошуу
@app.post("/users", summary="Жаңы колдонуучу түзүү")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    new_user = User(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user