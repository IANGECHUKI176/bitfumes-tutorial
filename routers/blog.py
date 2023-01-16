from typing import List
import repository.blog as blogs
import database
import models
import schemas
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
import oauth2

router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)


@router.get('/all', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(database.get_db),
            current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blogs.get_all(db)


@router.get('/{id}', response_model=schemas.ShowBlog)
def get_single_blog(id: int,
                    db: Session = Depends(database.get_db),
                    current_user: schemas.User = Depends(oauth2.get_current_user)
                    ):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id :{id} not found")
    return blog


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog,
           db: Session = Depends(database.get_db),
           current_user: schemas.User = Depends(oauth2.get_current_user)
           ):
    return blogs.create(request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def blog(id: int,
         db: Session = Depends(database.get_db),
         current_user: schemas.User = Depends(oauth2.get_current_user)
         ):
    return blogs.delete(id, db)


@router.put("/{id", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog,
                db: Session = Depends(database.get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)
                ):
    return blogs.update(id, request, db)
