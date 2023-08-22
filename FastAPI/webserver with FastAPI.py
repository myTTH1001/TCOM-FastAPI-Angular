from fastapi import FastAPI, Path
from typing import Optional


app = FastAPI()

students = {
    1: {
        "name": "John",
        "age": 17,
        "class": "year 12"
    }
}

@app.get("/")
def root():
    return {"message": "Hello "}

@app.get("/get-student/{student_id}")
# lỗi dòng này khi em thêm default=None anh ạ
def get_student(student_id: int):
    return students[student_id]

@app.get("/get-by-name")
def get_student(*,name: Optional[str] =None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {'Data': 'Not found'}