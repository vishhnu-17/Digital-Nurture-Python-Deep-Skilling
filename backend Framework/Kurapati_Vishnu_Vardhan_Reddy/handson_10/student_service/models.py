from extensions import db

class Student(db.Model):
    __tablename__="students"
    
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    enrollment_year = db.Column(db.Integer, nullable=False)
    enrollments=db.relationship("Enrollment",back_populates="student",cascade="all, delete-orphan")
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "enrollment_year": self.enrollment_year
        }

class Enrollment(db.Model):
    __tablename__="enrollments"
    id = db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey("students.id"),nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    student=db.relationship("Student",back_populates="enrollments")            
    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "course_id": self.course_id
        }    