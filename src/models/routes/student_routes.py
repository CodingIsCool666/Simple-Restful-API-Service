from flask import Blueprint, request, jsonify
from src.models.student import db, Student

student_bp = Blueprint('student', __name__, url_prefix='/api/student')

@student_bp.route('', methods=['GET'])
def get_students():
    try:
        students = Student.query.all()
        if not students:
            return "No students found", 404
        return jsonify([s.to_dict() for s in students]), 200
    except Exception as e:
        return str(e), 500

@student_bp.route('', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        name, age, major = data.get('name'), data.get('age'), data.get('major')
        if not all([name, age, major]):
            return "Missing required fields", 400

        student = Student(name=name, age=age, major=major)
        db.session.add(student)
        db.session.commit()
        return "Student added successfully", 201
    except Exception as e:
        return str(e), 500

@student_bp.route('/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return "Student not found", 404
    db.session.delete(student)
    db.session.commit()
    return "Student deleted successfully", 200

@student_bp.route('/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return "Student not found", 404
    data = request.get_json()
    student.name = data.get('name', student.name)
    student.age = data.get('age', student.age)
    student.major = data.get('major', student.major)
    db.session.commit()
    return "Student updated successfully", 200
