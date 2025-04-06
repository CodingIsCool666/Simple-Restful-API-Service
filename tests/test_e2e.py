import requests
import pytest
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from orm.models import Student


BASE_URL = "http://127.0.0.1:8787/api/student"

load_dotenv()
DATABASE_HOST=os.getenv('DATABASE_HOST', 'postgres')
DATABASE_PORT=os.getenv('DATABASE_PORT', '5432')
DATABASE_PASS=os.getenv('DATABASE_PASS', 'postgres')
DATABASE_USER=os.getenv('DATABASE_USER', 'postgres')
DATABASE_NAME=os.getenv('DATABASE_NAME', 'postgres')

# 建立連線 URL
DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

# 創建資料庫引擎
engine = create_engine(DATABASE_URL)

# 創建 session
Session = sessionmaker(bind=engine)
session = Session()


@pytest.fixture(scope="function", autouse=True)
def reset_db():
    """Reset the database before each test by deleting all students."""
    try:
        # 直接刪除所有學生資料
        deleted = session.query(Student).delete()
        session.commit()
        print(f"{deleted} student(s) deleted successfully!")

    except Exception as e:
        session.rollback()
        print(f"An error occurred while deleting students: {e}")
    finally:
        session.close()

def test_get_empty_students():
    """Test GET when the database is empty."""
    response = requests.get(BASE_URL)
    assert response.status_code == 404
    assert response.json() == {'error': 'No students found'}

def test_add_student():
    """Test adding a student using POST."""
    data = {"name": "John Doe", "age": 25, "major": "Physics"}
    response = requests.post(BASE_URL, json=data)
    assert response.status_code == 201
    assert response.json() == {"message": "Student added successfully"}

def test_get_students():
    """Test GET after adding students."""
    test_add_student()  # Ensure at least one student exists
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    students = response.json()
    assert len(students) > 0
    assert students[0]["name"] == "John Doe"

def test_delete_student():
    """Test DELETE a student by ID."""
    test_add_student()  # Add a student first
    response = requests.get(BASE_URL)
    student_id = response.json()[0]["id"]

    delete_response = requests.delete(f"{BASE_URL}/{student_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Student deleted successfully"}

    # Verify deletion
    get_response = requests.get(BASE_URL)
    assert get_response.status_code == 404  # Should be empty now

def test_update_student():
    """Test updating a student's details using PUT."""
    test_add_student()  # Add a student first
    response = requests.get(BASE_URL)
    student_id = response.json()[0]["id"]

    updated_data = {"name": "Jane Doe", "age": 30, "major": "Math"}
    put_response = requests.put(f"{BASE_URL}/{student_id}", json=updated_data)
    assert put_response.status_code == 200
    assert put_response.json() == {"message": "Student updated successfully"}
    # Verify update
    get_response = requests.get(BASE_URL)
    student = get_response.json()[0]
    assert student["name"] == "Jane Doe"
    assert student["age"] == 30
    assert student["major"] == "Math"
