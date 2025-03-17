from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from src.models.student import db, Student

app = Flask(__name__)

# Database configuration from environment variable
load_dotenv()
DATABASE_HOST=os.getenv('DATABASE_HOST')
DATABASE_PORT=os.getenv('DATABASE_PORT')
DATABASE_PASS=os.getenv('DATABASE_PASS')
DATABASE_USER=os.getenv('DATABASE_USER')
DATABASE_NAME=os.getenv('DATABASE_NAME')

DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # 在此綁定 app

# Endpoint to get all students
@app.route('/api/student', methods=['GET'])
def get_student():
    try:
        students = Student.query.all()
        if students:
            student_list = [student.to_dict() for student in students]
            return jsonify(student_list), 200
        else:
            return "No students found", 404
    except Exception as e:
        return str(e), 500

# Endpoint to add a student
@app.route('/api/student', methods=['POST'])
def add_student():
    try:
        student_data = request.get_json()
        name = student_data.get('name')
        age = student_data.get('age')
        major = student_data.get('major')
        if not all([name, age, major]):
            return "Missing required fields", 400

        new_student = Student(name=name, age=age, major=major)
        db.session.add(new_student)
        db.session.commit()
        return "Student added successfully", 201

    except Exception as e:
        return str(e), 500

@app.route('/api/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return "Student deleted successfully", 200
    return "Student not found", 404

@app.route('/api/student/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return "Student not found", 404
    
    student_data = request.get_json()
    student.name = student_data.get('name', student.name)
    student.age = student_data.get('age', student.age)
    student.major = student_data.get('major', student.major)
    db.session.commit()
    return "Student updated successfully", 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Add initial data if the table is empty
        if Student.query.count() == 0:
            initial_students = [
                Student(name="Alice", age=20, major="Physics"),
                Student(name="Bob", age=21, major="Mathematics"),
                Student(name="Charlie", age=22, major="Computer Science"),
                Student(name="Diana", age=23, major="Biology"),
            ]
            db.session.bulk_save_objects(initial_students)
            db.session.commit()

    app.run(host='0.0.0.0', port=8888)

