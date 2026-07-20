from models import *
from sqlalchemy.orm import joinedload
# dept1=Department(department_id=1,department_name="Computer Science")
# dept2 = Department(department_id=2,department_name="Electronics")
# dept3 = Department(department_id=3,department_name="Mechanical")
# session.add_all([dept1,dept2,dept3])
# session.commit()

# student1 = Student(student_id=1,
#     first_name="Arjun",
#     last_name="Reddy",
#     email="arjun.reddy@example.com",
#     department_id=1,enrollment_year=2023
# )

# student2 = Student(student_id=2,
#     first_name="Priya",
#     last_name="Sharma",
#     email="priya.sharma@example.com",
#     department_id=1,enrollment_year=2023
# )

# student3 = Student(student_id=3,
#     first_name="Rahul",
#     last_name="Verma",
#     email="rahul.verma@example.com",
#     department_id=2,enrollment_year=2023
# )

# student4 = Student(student_id=4,
#     first_name="Sneha",
#     last_name="Iyer",
#     email="sneha.iyer@example.com",
#     department_id=2,enrollment_year=2023
# )

# student5 = Student(student_id=5,
#     first_name="Karthik",
#     last_name="Nair",
#     email="karthik.nair@example.com",
#     department_id=3,enrollment_year=2023
# )
# session.add_all([student1,student2,student3,student4,student5])
# session.commit()

# course1=Course(course_name="Database Management System",department_id=1)
# course2 = Course(
#     course_name="Data Structures",
#     department_id=1
# )

# course3 = Course(
#     course_name="Digital Electronics",
#     department_id=2
# )
# session.add_all([course1,course2,course3])
# session.commit()

# enrollment1=Enrollment(student_id=1,course_id=13,grade="A")
# enrollment2 = Enrollment(
#     student_id=2,
#     course_id=13,
#     grade="B"
# )

# enrollment3 = Enrollment(
#     student_id=3,
#     course_id=14,
#     grade="A"
# )

# enrollment4 = Enrollment(
#     student_id=4,
#     course_id=15,
#     grade="B"
# )

# session.add_all([enrollment1,enrollment2,enrollment3,enrollment4])
# session.commit()

# 83
# students=session.query(Student).all()
# for stu in students:
#     if stu.department.department_name=="Computer Science":
#         print(f'{stu.first_name} {stu.department.department_name}')

# students=session.query(Student).join(Department).filter(Department.department_name=='Computer Science')
# for stu in students:
#     print(f'{stu.first_name} {stu.last_name} - {stu.department.department_name}')
    
# 84

enrollments=session.query(Enrollment).join(Student).join(Course).all()
for enrollment in enrollments:
    print(f'{enrollment.student.first_name} {enrollment.student.last_name} enrolled in {enrollment.course.course_name}')
     
#85 
# student=session.query(Student).filter(Student.email=="priya.sharma@example.com").first()
# student.email="priya.verma@example.com"
# session.commit()  

# 86
# enrollment=session.query(Enrollment).filter(Enrollment.enrollment_id==15).first()

# for e in enrollment:
#     e.student.first_name

# session.delete(enrollment)
# session.commit()   

#88
enrollments=session.query(Enrollment).options(
    joinedload(Enrollment.student),
    joinedload(Enrollment.course)
).all()

for e in enrollments:
    print(f'{e.student.student_id} {e.student.first_name} enrolled in {e.course.course_name}')