from fastapi import FastAPI, Path
from typing import Optional


app = FastAPI()

students = {
    1: {
        "name": "John",
        "age": 17,
        "class": "year 12"
    },
    2: {
        "name": "Tim",
        "age": 18,
        "class": "year 15"
    }
}
# @app: Path operation Decoration
# get là Operation
# ("/") là đường dẫn Path
@app.get("/")
# Path operation function
def root():
    return {"message": "Hello "}


def _get_student(student_id: int):
    return students[student_id]
# Đường dẫn động sử dụng {}
@app.get("/get-student/")
def get_student_default():
    return _get_student(1)

@app.get("/get-student/{student_id}")
def get_student_by_id(student_id: int = Path(description="view student with id")):
    return students[student_id]

@app.get("/get-by-name")
def get_student_by_name(name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {'Data': 'Not found'}
