from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter, status          #modified
from schemas.user import ShowUser
from schemas.user import UserCreate
from db.session import get_db
from db.repository.user import create_new_user

router = APIRouter()


@router.post("/")
def create_user(user : UserCreate,db: Session = Depends(get_db)):
    try:
        user = create_new_user(user=user,db=db)
        return user 
    except Exception as e:
        print(e)
    return None