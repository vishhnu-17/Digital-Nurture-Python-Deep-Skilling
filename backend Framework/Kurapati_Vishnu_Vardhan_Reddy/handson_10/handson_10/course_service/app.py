from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///course.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()

    if Course.query.count() == 0:
        course = Course(name="Python Backend")
        db.session.add(course)
        db.session.commit()

@app.route("/")
def home():
    return "Course Service Running"

@app.route("/api/courses/<int:course_id>")
def get_course(course_id):
    course = Course.query.get(course_id)

    if course is None:
        return {"message": "Course not found"}, 404

    return {
        "id": course.id,
        "name": course.name
    }


if __name__ == "__main__":
    app.run(port=5001, debug=True)