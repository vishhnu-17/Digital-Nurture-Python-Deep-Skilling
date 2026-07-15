create database college_db;
use college_db;
create table departments(
    department_id int primary key auto_increment,
    dept_name varchar(100) not null,
    hod_name varchar(100),
    budget decimal(12,2)
);
create table students(
    student_id int primary key auto_increment,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    email varchar(100) unique not null,
    date_of_birth date,
    department_id int,
    enrollment_year int,
    foreign key (department_id) references departments(department_id)
);
create table courses(
    course_id int primary key auto_increment,
    course_name varchar(150) not null,
    course_code varchar(20) unique,
     credits int,
     department_id int,
     foreign key(department_id) references departments(department_id)
);
describe courses;

create table enrollments(
    enrollment_id int primary key auto_increment,
    student_id int ,
    course_id int,
    enrollement_date date,
    grade varchar(2),
    foreign key (student_id) references students(student_id),
    foreign key (course_id) references courses(course_id)
);

create table professors(
    professor_id int primary key auto_increment,
    prof_name varchar(100) not null,
    email varchar(100) unique,
    department_id int ,
    salary decimal(10,2),
    foreign key (department_id) references departments(department_id)
);

-- 1NF:
-- All tables satisfy First Normal Form because every column stores atomic values.
-- Example: first_name stores one name and email stores one email address.
-- Storing multiple phone numbers in one column would violate 1NF.

-- 2NF:
-- The schema satisfies Second Normal Form.
-- Every non-key attribute depends on the entire key.
-- In the enrollments table, enrollment_date and grade depend on the student-course enrollment,
-- not only on student_id or course_id individually.

-- 3NF:
-- The schema satisfies Third Normal Form.
-- There are no transitive dependencies.
-- Department information is stored only in the departments table.
-- Students reference departments using department_id, avoiding duplication.
-- This reduces redundancy and maintains data consistency.

alter table students add phone_number varchar(15);
alter table courses add max_seats int default 60;
alter table enrollments add constraint grade_check check (grade in ('A','B','C','D','F') or grade is null);

alter table departments rename column hod_name to head_of_dept;
alter table students drop column phone_number;

