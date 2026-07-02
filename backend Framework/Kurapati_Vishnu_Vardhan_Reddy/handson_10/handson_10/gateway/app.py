from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "API Gateway Running"

@app.route("/courses/<int:course_id>")
def get_course(course_id):
    response = requests.get(
        f"http://127.0.0.1:5001/api/courses/{course_id}"
    )

    return response.json(), response.status_code

@app.route("/students/<int:student_id>/enroll/<int:course_id>", methods=["POST"])
def enroll_student(student_id, course_id):
    response = requests.post(
        f"http://127.0.0.1:5002/api/students/{student_id}/enroll/{course_id}"
    )

    return response.json(), response.status_code

if __name__ == "__main__":
    app.run(port=5000, debug=True)