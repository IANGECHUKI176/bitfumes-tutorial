from sqlalchemy.orm import Session
import models
import schemas
from fastapi import status, HTTPException


def get_all(db: Session):
    blog = db.query(models.Blog).all()
    return blog


def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=2)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if blog.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id :{id} not found")
    
    blog.delete(synchronize_session=False)
    db.commit()
    return {"deleted": True}


def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if blog.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no blog with this id {id} found")
    blog.update(request.dict())
    db.commit()
    return "updated"
