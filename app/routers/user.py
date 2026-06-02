from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):

    #hashed password - user.password
    #hashed_password = pwd_context.hash(user.password)
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    user_query = db.query(models.User).filter(models.User.email==user.email).first()

    if user_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email already exists")

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"the user with id {id} doesn't exist")

    return user