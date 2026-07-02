from flask import Blueprint, jsonify, request
from extensions import db
from courses.models import Course, Student, Enrollment



courses_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/api/courses"
)

students_bp = Blueprint(
    "students",
    __name__,
    url_prefix="/api/students"
)

enrollments_bp = Blueprint(
    "enrollments",
    __name__,
    url_prefix="/api/enrollments"
)


def make_response_json(data, status_code):
    return jsonify({
        "status": "success",
        "data": data
    }), status_code


@courses_bp.route("/", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return jsonify(
        [course.to_dict() for course in courses]
    )


@courses_bp.route("/", methods=["POST"])
def create_course():

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    required_fields = ["name", "code", "credits", "department_id"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    course = Course(
        name=data["name"],
        code=data["code"],
        credits=data["credits"],
        department_id=data["department_id"]
    )

    db.session.add(course)
    db.session.commit()

    return jsonify(course.to_dict()), 201


@courses_bp.route("/<int:course_id>", methods=["GET"])
def get_course(course_id):

    course = Course.query.get_or_404(course_id)
    return jsonify(course.to_dict())


@courses_bp.route("/<int:course_id>", methods=["PUT"])
def update_course(course_id):

    course = Course.query.get_or_404(course_id)

    data = request.get_json()

    course.name = data.get("name", course.name)
    course.code = data.get("code", course.code)
    course.credits = data.get("credits", course.credits)
    course.department_id = data.get("department_id", course.department_id)

    db.session.commit()

    return jsonify(course.to_dict())

@courses_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):

    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()

    return jsonify({"message": "Course deleted successfully"})

@courses_bp.route("/<int:course_id>/students/", methods=["GET"])
def get_course_students(course_id):

    course = Course.query.get_or_404(course_id)

    students = (
        db.session.query(Student)
        .join(Enrollment)
        .filter(Enrollment.course_id == course.id)
        .all()
    )

    return jsonify([student.to_dict() for student in students])


@students_bp.route("/", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])


@students_bp.route("/", methods=["POST"])
def create_student():
    data = request.get_json() or {}
    student = Student(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=data.get("email"),
        enrollment_year=data.get("enrollment_year"),
        department_id=data.get("department_id")
    )
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201


@enrollments_bp.route("/", methods=["GET"])
def get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify([enrollment.to_dict() for enrollment in enrollments])


@enrollments_bp.route("/", methods=["POST"])
def create_enrollment():
    data = request.get_json() or {}
    enrollment = Enrollment(
        student_id=data.get("student_id"),
        course_id=data.get("course_id"),
        enrollment_date=data.get("enrollment_date"),
        grade=data.get("grade")
    )
    db.session.add(enrollment)
    db.session.commit()
    return jsonify(enrollment.to_dict()), 201