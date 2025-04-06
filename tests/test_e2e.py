import requests
import pytest
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orm.models import Student

load_dotenv()
DATABASE_HOST = os.getenv('DATABASE_HOST', 'postgres')
DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')
DATABASE_PASS = os.getenv('DATABASE_PASS', 'postgres')
DATABASE_USER = os.getenv('DATABASE_USER', 'postgres')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'postgres')
DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

SERVICE_PORT = os.getenv('SERVICE_PORT', '8888')
BASE_URL = f"http://127.0.0.1:{SERVICE_PORT}/api/student"

@pytest.fixture(scope="function", autouse=True)
def reset_db():
    """
    Connect to database and delete all students before each test
    """
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Delete all students before each test
    try:
        session.query(Student).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"An error occurred while resetting the database: {e}")
    finally:
        session.close()

    yield

def test_get_empty_students():
    """Test GET when the database is empty."""
    response = requests.get(BASE_URL)
    assert response.status_code == 404
    assert response.json() == {"error": "No students found"}

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
