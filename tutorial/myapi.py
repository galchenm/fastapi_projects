from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()
students = {
    1: {"name": "John", "age": 20, "class": "year 12"},
    2: {"name": "Jane", "age": 22, "class": "year 11"},
    3: {"name": "Doe", "age": 23, "class": "year 10"},
    4: {"name": "Alice", "age": 21, "class": "year 5"},
    5: {"name": "Alice", "age": 22, "class": "year 6"}
}

class Student(BaseModel):
    name: str
    age: int
    class_name: str

# GET get an info
@app.get("/")
def index():
    return {"name" : "First Data", "second" : 26    }

# Path cannot have a default value, it is always required
@app.get("/students/{student_id}")
def get_student_by_id(
    student_id: int = Path(..., description="The ID of the student you want to view", gt=0)
):
    student = students.get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    return student

# query google.com/search?q=rest+api+methods - it can have a default value
@app.get("/get-by-name")
def get_students_by_name(name: str = Query(None, min_length=1, max_length=50, description="The name of the student you want to search for")):
    result = []
    for student in students:
        if students[student]["name"] == name:
            result.append(students[student])
    if not result:
        raise HTTPException(status_code=404, detail=f"Student with name {name} not found")
    return result

# POST create smth new new
@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"error": "Student with this ID already exists"}
    students[student_id] = student
    return students[student_id]

# PUT update an object
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: Student):
    if student_id not in students:
        return {"error": "Student with this ID does not exist"}
    students[student_id] = student
    return students[student_id]

# DELETE delete smth
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"error": "Student with this ID does not exist"}
    del students[student_id]
    return {"message": "Student deleted successfully"}
