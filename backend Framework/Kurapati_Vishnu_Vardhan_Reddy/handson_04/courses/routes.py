from flask import Blueprint,jsonify,request
courses_bp=Blueprint("courses",__name__,url_prefix="/api/courses")
courses=[]
def make_response_json(data,code):
    return jsonify({"status":"success","data":data}),code
@courses_bp.route("/",methods=["GET"])
def get_courses():
    return jsonify(courses)



@courses_bp.route("/",methods=["POST"])
def create_courses():
    data=request.get_json()
    if "name" not in data or "code" not in data or "credits" not in data:
        return jsonify({"error": "name,code,credits is required"}),400
    courses.append(data)
    return make_response_json(data,201)

@courses_bp.route("/<int:course_id>",methods=["GET"])
def get_course(course_id):
    if(len(courses)<=course_id):
        return jsonify({"error": "resource not found"}),404
    return jsonify(courses[course_id])

@courses_bp.route("/<int:course_id>",methods=["PUT"])
def update_course(course_id):
    if(course_id>=len(courses)):
        return jsonify({"error": "resource not found"}),404
    data=request.get_json()
    if "name" not in data or "code" not in data or "credits" not in data:
        return jsonify({"error": "name,code,credits is required"}),400
    courses[course_id]=data
    return make_response_json(data,201)

@courses_bp.route("/<int:course_id>",methods=['DELETE'])
def delete_course(course_id):
    if(course_id>=len(courses)):
        return jsonify({"error": "resource not found"}),404
    del courses[course_id]
    return jsonify({"message":"course deleted successfully"}),200 

