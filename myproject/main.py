from fastapi import FastAPI
from core.config import settings
from db.session import engine 
from db.base import Base
from apis.base import api_router
from fastapi.staticfiles import StaticFiles
import requests, time

def create_tables():         
	Base.metadata.create_all(bind=engine)

def include_router(app):   
	app.include_router(api_router)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    return app

def save_system_info_periodically():
    n = 0
    while n<5:
        response = requests.post("http://127.0.0.1:8000/system_info")
        print(response.json())
        time.sleep(5)
        n += 1

app = start_application()

app.mount("/static", StaticFiles(directory="static"), name="static")



import threading


@app.get("/")
def home():
    # threading.Thread(target=save_system_info_periodically()).start()
    return {"msg":"🚀EYEFIRE🚀"}




        









# alembic revision --autogenerate -m "Commit migration"     : makemigrations
# alembic stamp head                                        : Việc sử dụng stampsẽ đặt giá trị phiên bản db cho bản sửa đổi đã chỉ định;
# alembic upgrade head                                      : migrate
# uvicorn main:app --reload                                 : Runserver