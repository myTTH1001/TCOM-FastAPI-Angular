from pydantic import BaseModel
from fastapi import UploadFile, File


class CreateAvatar(BaseModel):
    name: str

class ShowAvatar(BaseModel):
    name:str 
    image:str

    class Config():
        from_attributes = True