from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):  # 改為繼承 db.Model
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    major = db.Column(db.String(100), nullable=False)

    def __init__(self, name, age, major):
        self.name = name
        self.age = age
        self.major = major

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'major': self.major
        }