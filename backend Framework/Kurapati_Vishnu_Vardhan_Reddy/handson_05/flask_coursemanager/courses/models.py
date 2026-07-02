from extensions import db

class Department(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    head_of_dept = db.Column(db.String(100))
    budget = db.Column(db.Float)
    
    courses = db.relationship(
        "Course",
        back_populates = "department"
            )

    def __repr__(self):
        return f"Department {self.name}"

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "head_of_dept": self.head_of_dept,
            "budget": self.budget
        }

class Course(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    code = db.Column(db.String(100), unique = True, nullable = False)
    credits = db.Column(db.Integer)

    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable = False)

    department = db.relationship(
        "Department",
        back_populates = "courses"
    )
    def __repr__(self):
        return f"Course {self.name}"

    def to_dict(self):
        return{
            "id" : self.id,
            "name" : self.name,
            "code" : self.code,
            "credits" : self.credits,
            "department_id" : self.department_id

        }

class Student(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100), nullable = False)
    last_name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(200), unique = True, nullable = False)
    enrollment_year = db.Column(db.Integer)

    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable = False)

    department = db.relationship("Department")

    enrollments = db.relationship(
        "Enrollment",
        back_populates = "student"
    )
    def __repr__(self):
        return f"Student {self.first_name} {self.last_name}"

    def to_dict(self):
        return{
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "enrollment_year": self.enrollment_year,
            "department_id": self.department_id
        }

class Enrollment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id")
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id")
    )

    enrollment_date = db.Column(db.String(30))

    grade = db.Column(db.String(5))

    student = db.relationship(
        "Student",
        back_populates="enrollments"
    )

    course = db.relationship("Course")

    def __repr__(self):
        return f"Enrollment {self.id}"

    def to_dict(self):
        return{
            "id" : self.id,
            "student_id" : self.student_id,
            "course_id" : self.course_id,
            "enrollment_date" : self.enrollment_date,
            "grade" : self.grade
        }

    

