from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from . import models, schemas

def create_url(db: Session, data: schemas.URLCreate):
    new_url = models.URL(
        slug=data.slug,
        target_url=data.target_url
    )
    db.add(new_url)
    try:
        db.commit()
        db.refresh(new_url)
        return new_url
    except IntegrityError:
        db.rollback()
        # Constraint violated: slug already exists (avoid race condition)
        raise HTTPException(status_code=400, detail="Slug já existe")
    except Exception:
        db.rollback()
        raise

def get_url_by_slug(db: Session, slug: str):
    return db.query(models.URL).filter(models.URL.slug == slug).first()

def increase_hit(db: Session, slug: str):
    url = get_url_by_slug(db, slug)
    if url:
        url.hits += 1
        db.commit()
        db.refresh(url)
    return url
