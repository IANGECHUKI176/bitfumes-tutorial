from fastapi import APIRouter, Depends, status, HTTPException
import schemas, models
from sqlalchemy.orm import Session
import database
import hashing
import tokenhandler as tkn
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login", status_code=status.HTTP_200_OK)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")

    if not hashing.Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    # generate token and return it
    access_token = tkn.create_access_token(
        data={"sub": user.email}
        # expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
