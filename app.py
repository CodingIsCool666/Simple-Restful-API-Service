from flask import Flask, jsonify, request
from sqlalchemy.orm import scoped_session

from orm.models import Student
from orm.database import Session, init_db

app = Flask(__name__)

@app.route('/api/student', methods=['GET'])
def get_student():
    session = scoped_session(Session)
    try:
        student_id = request.args.get("id", type=int)

        if student_id:
            student = session.get(Student, student_id)
            if not student:
                return jsonify({"error": f"Student with ID {student_id} was not found"}), 404
            return jsonify(student.to_dict()), 200
        else:
            students = session.query(Student).all()
            if not students:
                return jsonify({"error": "No students found"}), 404
            return jsonify([student.to_dict() for student in students]), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.remove()


# Endpoint to add a student
@app.route('/api/student', methods=['POST'])
def add_student():
    session = scoped_session(Session)
    try:
        student_data = request.get_json()
        name = student_data.get('name')
        age = student_data.get('age')
        major = student_data.get('major')

        if not all([name, age, major]):
            return jsonify({"error": "Missing required fields"}), 400

        new_student = Student(name=name, age=age, major=major)
        session.add(new_student)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.remove()

    return jsonify({"message": "Student added successfully"}), 201


@app.route('/api/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    session = scoped_session(Session)
    try:
        student = session.get(Student, id)
        if student:
            session.delete(student)
            session.commit()
            return jsonify({"message": "Student deleted successfully"}), 200
        else:
            return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.remove()

@app.route('/api/student/<int:id>', methods=['PUT'])
def update_student(id):
    session = scoped_session(Session)
    try:
        student = session.get(Student, id)
        if not student:
            return jsonify({"error": "Student not found"}), 404

        student_data = request.get_json()
        student.name = student_data.get('name', student.name)
        student.age = student_data.get('age', student.age)
        student.major = student_data.get('major', student.major)

        session.commit()
        return jsonify({"message": "Student updated successfully"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.remove()


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8787)

