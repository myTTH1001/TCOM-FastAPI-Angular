from fastapi import FastAPI, Path
from core.config import settings
from db.session import engine 
from db.base_class import Base
from typing import Annotated

def create_tables():         
	Base.metadata.create_all(bind=engine)
        

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    create_tables()
    return app


app = start_application()


@app.get("/home/")
def home():
    return {"msg":"EYEFIRE_DAY3🚀"}


@app.get("/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)], q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results