import models
from fastapi import status,HTTPException,Depends, APIRouter
from schemas import UserCreate,UserOut
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db : Session = Depends(get_db)):
    #hash the password
    user.password = hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}',response_model=UserOut)
def get_user(id: int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with the {id} is not present!!!")
    return user