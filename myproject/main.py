from fastapi import FastAPI, UploadFile, HTTPException, status
from core.config import settings
from db.session import engine 
from db.base import Base
from apis.base import api_router
import json, os
from datetime import datetime
from fastapi.responses import FileResponse

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




        









# alembic revision --autogenerate -m "Commit migration"     : makemigrations
# alembic stamp head                                        : Việc sử dụng stampsẽ đặt giá trị phiên bản db cho bản sửa đổi đã chỉ định;
# alembic upgrade head                                      : migrate
# uvicorn main:app --reload                                 : Runserver