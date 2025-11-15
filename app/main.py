from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models, schemas, crud

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create", response_model=schemas.URLResponse)
def create(data: schemas.URLCreate, db: Session = Depends(get_db)):
    # IntegrityError is caught and handled in crud.create_url
    return crud.create_url(db, data)

@app.get("/{slug}")
def redirect_url(slug: str, db: Session = Depends(get_db)):
    url = crud.get_url_by_slug(db, slug)
    if not url:
        raise HTTPException(status_code=404, detail="Slug não encontrado")

    crud.increase_hit(db, slug)
    return {"target_url": url.target_url}
