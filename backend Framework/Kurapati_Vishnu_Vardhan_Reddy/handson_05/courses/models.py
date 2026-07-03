from extensions import db
class Department(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    hod=db.Column(db.String(100),nullable=False)
    budget=db.Column(db.Numeric(10,2),nullable=False)
    courses=db.relationship("Course",back_populates="department")
    students=db.relationship("Student",back_populates="department")
    def to_dict(self):
        return{
            "id":self.id,
            "name":self.name,
            "hod": self.hod,
            "budget":self.budget
            
        }
        
    
class Course(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)    
    code =db.Column(db.String(10),nullable=False,unique=True)
    credits=db.Column(db.Integer,nullable=False)
    department_id=db.Column(db.Integer,db.ForeignKey("department.id"),nullable=False)
    department=db.relationship(
        Department,back_populates="courses"
    )
    enrollments=db.relationship("Enrollment",back_populates="course")
    
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "code":self.code,
            "credits":self.credits,
            "department_id":self.department_id
        }
    
class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(100),nullable=False)
    last_name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)    
    year=db.Column(db.Integer,nullable=False)
    dept_id=db.Column(db.Integer,db.ForeignKey("department.id"),nullable=False)
    department=db.relationship("Department",back_populates="students")
    enrollments=db.relationship("Enrollment",back_populates="student")
    def to_dict(self):
     return {
        "id": self.id,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "email": self.email,
        "year":self.year,
        "dept_id": self.dept_id
    }

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id"),
        nullable=False
    )

    enrollment_date = db.Column(db.Date, nullable=False)

    grade = db.Column(db.String(5), nullable=True)   
    student=db.relationship("Student",back_populates="enrollments")
    course= db.relationship("Course",back_populates="enrollments")
    def to_dict(self):
     return {
        "id": self.id,
        "student_id": self.student_id,
        "course_id": self.course_id,
        "grade": self.grade
    }