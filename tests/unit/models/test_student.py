from orm.models import Student


def test_student_to_dict():
    """Test converting a Student instance to a dictionary."""
    student = Student(name="Bob", age=23, major="Computer Science")
    student_dict = student.to_dict()

    assert student_dict.get("name") == "Bob"
    assert student_dict.get("age") == 23
    assert student_dict.get("major") == "Computer Science"
    assert "id" in student_dict  # ID should be present, even if None before commit