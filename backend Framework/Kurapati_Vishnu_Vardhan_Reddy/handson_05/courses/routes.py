from flask import Blueprint,jsonify,request
from courses.models import *
courses_bp=Blueprint("courses",__name__,url_prefix="/api/courses")
def make_response_json(data,code):
    return jsonify({"status":"success","data":data}),code
def get_or_404():
    return jsonify({"error":"course not found"}),404
@courses_bp.route("/",methods=["GET"])
def get_courses():
    courses=Course.query.all()
    course_list=[]
    for course in courses:
        course_list.append(course.to_dict())
    return make_response_json(course_list,200)    


@courses_bp.route("/",methods=["POST"])
def create_courses():
    data=request.get_json()
    if data is None:
        return jsonify({"error":"request body must be json"}),400
    if "name" not in data or "code" not in data or "credits" not in data or "department_id" not in data:
        return jsonify({"error": "name,code,credits is required"}),400
    course=Course(name=data["name"], code=data["code"],credits=data["credits"],department_id=data["department_id"])
    db.session.add(course)
    db.session.commit()
    return make_response_json(course.to_dict(),201)

@courses_bp.route("/<int:course_id>",methods=["GET"])
def get_course(course_id):
   course=Course.query.get_or_404(course_id)
   if(course is  None):
       return get_or_404()
   return make_response_json(course.to_dict(),200)

@courses_bp.route("/<int:course_id>",methods=["PUT"])
def update_course(course_id):
    
    course=Course.query.get_or_404(course_id)
    data=request.get_json()
    if data is None:
        return get_or_404()
    if "name" not in data or "code" not in data or "credits" not in data:
        return jsonify({"error": "name,code,credits is required"}),400
    course.name=data["name"]
    course.code=data["code"]
    course.credits=data["credits"]
    course.department_id=data["department_id"]
    db.session.commit()
   
    return make_response_json(course.to_dict(),200)

@courses_bp.route("/<int:course_id>",methods=['DELETE'])
def delete_course(course_id):
   course=Course.query.get_or_404(course_id)
   db.session.delete(course)
   db.session.commit()
   return "",200 

@courses_bp.route("/<int:course_id>/students",methods=['GET'])
def students_in_course(course_id):
    course= Course.query.get_or_404(course_id)
    if course is None:
        return get_or_404()
    students=Student.query.join(Enrollment).filter(Enrollment.course_id==course_id).all()
    students_list=[]
    for student in students:
        students_list.append(student.to_dict())
    return make_response_json(students_list,200)  



