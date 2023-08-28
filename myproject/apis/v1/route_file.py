from fastapi import APIRouter, status
from fastapi import Depends, UploadFile, File
from sqlalchemy.orm import Session
from schemas.avatar import ShowAvatar, CreateAvatar
from db.session import get_db
from db.repository.avatar import upload_avatar
from db.models.avatar import FileImage

router = APIRouter()


@router.post("/avatar/uploads", status_code=status.HTTP_201_CREATED)
async def create_avatar(file: UploadFile = File(...), db: Session= Depends(get_db)):
    name, image = await upload_avatar(file= file)
    avatar = FileImage(name = name, image = image)
    db.add(avatar)
    db.commit()
    return {"Avatar upload Done with path:" : image}
