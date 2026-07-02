from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Student Service Running"

@app.route("/api/students/<int:student_id>/enroll/<int:course_id>", methods=["POST"])
def enroll_student(student_id, course_id):

    response = requests.get(
        f"http://127.0.0.1:5001/api/courses/{course_id}"
    )

    if response.status_code != 200:
        return {
            "message": "Course Service unavailable or course not found"
        }, 503

    return {
        "student_id": student_id,
        "course": response.json(),
        "message": "Enrollment successful"
    }


if __name__ == "__main__":
    app.run(port=5002, debug=True)