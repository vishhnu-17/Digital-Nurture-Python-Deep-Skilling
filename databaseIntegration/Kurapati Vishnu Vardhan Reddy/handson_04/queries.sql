-- 48
explain select
s.first_name,s.last_name,
c.course_name from enrollments e join students s on
e.student_id=s.student_id join courses c on
c.course_id=e.course_id where s.enrollment_year=2022;
/*
Executed EXPLAIN on the JOIN query before creating indexes.

Step 49:
The students table performs a Full Table Scan (type = ALL)
because enrollment_year is not indexed.

Step 50:
Estimated rows examined:
students     -> 8
enrollments  -> 1
courses      -> 1

The enrollments table uses the student_id index.
The courses table uses the PRIMARY KEY.
The students table will be optimized by adding an index on enrollment_year.
*/

-- TASK 2
create index idx_student_enrollment_year on students(enrollment_year);

create unique index idx_enrollments_student_course on enrollments(student_id,course_id) ;
show index from enrollments;

create index idx_courses_course_code on courses(course_code);
show index from courses;
explain select s.first_name,s.last_name, c.course_name from enrollments e join
students s on e.student_id=s.student_id join courses c on
e.course_id=c.course_id where s.enrollment_year=2022;

-- After creating indexes:
-- The optimizer uses the index on students.enrollment_year
-- instead of performing a full table scan.
-- This reduces the number of rows examined and improves query performance.

-- MySQL does not support partial indexes.
-- Partial indexes with a WHERE clause are a PostgreSQL feature.
-- Hence this step cannot be implemented in MySQL.