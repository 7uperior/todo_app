from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, SessionLoacal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLoacal()
        yield db
    finally:
        db.close()


class Todo(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = Field(
        gt=0,
        lt=6,
        description="The priority must be between 1-5",
    )
    complete: bool


@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()  # noqa: E501
    if todo_model is not None:
        return todo_model
    raise http_exception()


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")
