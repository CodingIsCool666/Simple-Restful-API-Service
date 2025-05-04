# app.py
from flask import Flask
from orm.database import init_db
from routes.student_routes import student_bp

app = Flask(__name__)
app.register_blueprint(student_bp)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8787)
