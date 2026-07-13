from flask import Flask,request,jsonify
from config import Config
from extensions import db
import requests
from models import Enrollment,Student
app=Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
print(__name__)

with app.app_context():
    db.create_all()
    
@app.post("/api/students/<int:student_id>/enroll")
def enroll_student(student_id):
    student=Student.query.get(student_id)
    if not student:
        return jsonify({"message":"student not found"}),404 
    data=request.get_json()  
    if not data or "course_id" not in data:
        return jsonify({"message":"course_id is required"}),400 
    course_id=data.get("course_id")
    try:
        response=requests.get(f"http://127.0.0.1:5001/api/courses/{course_id}")
        if response.status_code!=200:
            return jsonify({
            "message":"course not found"
            }),404
        existing=Enrollment.query.filter_by(student_id=student_id,course_id=course_id).first()
        if existing:
            return jsonify({"message":"already enrolled"}),409    
        enrollment=Enrollment(student_id=student_id,course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        return jsonify({
        "message": "Student enrolled successfully"
            }), 201
    except requests.exceptions.ConnectionError:
        return jsonify({
            "message":"course service unavailable"
        }),503    
if __name__=="__main__":
    app.run(host="0.0.0.0",port=5002,debug=True)    