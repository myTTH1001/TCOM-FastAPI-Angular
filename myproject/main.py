from fastapi import FastAPI, Path, UploadFile, File
from core.config import settings
from db.session import engine 
from db.base import Base
from apis.base import api_router
from typing import Annotated


def create_tables():         
	Base.metadata.create_all(bind=engine)

def include_router(app):   
	app.include_router(api_router)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    return app


app = start_application()


@app.get("/")
def home():
    return {"msg":"EYEFIRE_DAY3🚀"}

@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}



# alembic revision --autogenerate -m "Commit migration"     : makemigrations
# alembic upgrade head                                      : migrate
# uvicorn main:app --reload                                 : Runserver