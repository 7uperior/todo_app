from fastapi import FastAPI, Depends
import models
from database import engine, SessionLoacal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLoacal()
        yield db
    finally:
        db.close()


@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()
