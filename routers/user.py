from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
import repository.user as users
import database
import schemas
from typing import List

router = APIRouter(
    prefix='/user',
    tags=['users']
)


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return users.create(request, db)


@router.get('/all', response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(database.get_db)):
    return users.get_all(db)


@router.get("/{id}", response_model=schemas.ShowUser)
def get_single_user(id: int, db: Session = Depends(database.get_db)):
    return users.get_one(id, db)


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(database.get_db)):
    return users.delete(id, db)
