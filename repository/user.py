import schemas
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
import models
import hashing


def create(request: schemas.User, db: Session):
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.encrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all(db: Session):
    users = db.query(models.User).all()
    return users


def get_one(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no user with id:{id}")
    return user


def delete(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id)

    if user.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id :{id} not found")

    # user.delete(synchronize_session=False)
    db.commit()
    return {"deleted": True}
