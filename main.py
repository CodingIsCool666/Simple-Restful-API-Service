from fastapi import FastAPI, HTTPException
import psycopg2
from pydantic import BaseModel

app = FastAPI()

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="db",  # Use 'localhost' if running locally without Docker Compose
        database="postgres",
        user="postgres",
        password="mysecretpassword"
    )
    return conn

# Define Pydantic model for student
class Student(BaseModel):
    first_name: str
    last_name: str

# Get a student by ID
@app.get("/api/student/{student_id}")
def get_student(student_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
    student = cur.fetchone()
    cur.close()
    conn.close()
    
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return {"student_id": student[0], "first_name": student[1], "last_name": student[2]}

# Insert a new student
@app.post("/api/student/")
def insert_student(student: Student):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (first_name, last_name) VALUES (%s, %s) RETURNING student_id", 
                (student.first_name, student.last_name))
    student_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return {"student_id": student_id, "first_name": student.first_name, "last_name": student.last_name}

# Delete a student
@app.delete("/api/student/{student_id}")
def delete_student(student_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    return {"message": "Student deleted"}

# Update a student
@app.put("/api/student/{student_id}")
def update_student(student_id: int, student: Student):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE students SET first_name = %s, last_name = %s WHERE student_id = %s", 
                (student.first_name, student.last_name, student_id))
    conn.commit()
    cur.close()
    conn.close()
    
    return {"student_id": student_id, "first_name": student.first_name, "last_name": student.last_name}
