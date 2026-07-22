use college_db;

    -- 35
     select * from students where student_id in(
     select student_id from enrollments group by student_id having count(*)> 
     (select avg(c) from(select count(*) as c from enrollments group by student_id) t));

     -- 36
    select course_id from enrollments having min(grade)='A' and max(grade)='A';


    select c.course_id,c.course_name from courses c where not exists(
        select 1 from enrollments e where e.course_id=c.course_id and (e.grade!='A' or e.grade is null)
    );


    -- 37
    select prof_name from professors p where salary=(
    select max(salary) as maxi from professors p1 where p1.department_id=p.department_id group by department_id ) ;

    -- 38
    select department_id,avg_sal from 
    (select department_id,avg(salary) as avg_sal from professors group by department_id ) as dept_avg where avg_sal>85000;

    -- 39
    create view vw_student_enrollment_summary as
    select s.student_id,concat(s.first_name," ",s.last_name) as full_name,d.dept_name,count(e.course_id),avg(
        case 
          when e.grade='A' then 4
          when e.grade='B' then 3
          when e.grade='C' then 2
          WHEN e.grade='D' THEN 1
          WHEN e.grade='F' THEN 0  
       end       
    ) as gpa from 
    students s join enrollments e on s.student_id=e.student_id join
     departments d on
    s.department_id=d.department_id
     group by s.student_id,full_name,d.dept_name;

     -- 40
    create view vw_course_stats as
    select c.course_name,c.course_code,count(e.course_id) as total_enrollments, avg(
        case 
           when e.grade='A' then 4
          when e.grade='B' then 3
          when e.grade='C' then 2
          WHEN e.grade='D' THEN 1
          WHEN e.grade='F' THEN 0  
       end          
     ) as gpa from courses c
     left join enrollments e on c.course_id=e.course_id group by c.course_code,c.course_name;

    -- 41
    select * from vw_student_enrollment_summary where gpa>3;

    -- 42
    update vw_student_enrollment_summary set full_name="vishnu" where student_id=1;

    -- 43
    drop view vw_student_enrollment_summary;
    create view vw_student_enrollment_summary as
    select * from students where department_id=1;

    update vw_student_enrollment_summary set enrollment_year=2023 where
    student_id=1;

    select * from vw_student_enrollment_summary;

    -- 44
    DELIMITER $$
    create procedure sp_enroll_student(
        in p_student_id int, in p_course_id int , in p_enrollment_date date
    )
    BEGIN 
      DECLARE p_count int default 0;
      select count(*) into p_count from enrollments where course_id=p_course_id and student_id=p_student_id;
      IF p_count>0 THEN 
         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Student is already enrolled in this course';
      ELSE 
        insert into enrollments(course_id,student_id,enrollment_date) values(p_course_id,p_student_id,p_enrollment_date);   
      END IF;
    END $$  

    DELIMITER ;      

    call sp_enroll_student(2,2,'2025-10-19');

    -- 45
    CREATE TABLE department_transfer_log(
        log_id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT,
        old_department_id INT,
        new_department_id INT,
        transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    DELIMITER $$

    CREATE PROCEDURE sp_transfer_student(
        IN p_student_id INT,
        IN p_new_department_id INT
    )
    BEGIN
        DECLARE p_old_department_id INT;

        DECLARE EXIT HANDLER FOR SQLEXCEPTION
        BEGIN
            ROLLBACK;
        END;

        SELECT department_id
        INTO p_old_department_id
        FROM students
        WHERE student_id = p_student_id;

        START TRANSACTION;

        UPDATE students
        SET department_id = p_new_department_id
        WHERE student_id = p_student_id;

        INSERT INTO department_transfer_log
        (student_id, old_department_id, new_department_id)
        VALUES
        (p_student_id, p_old_department_id, p_new_department_id);

        COMMIT;
    END $$

    DELIMITER ;

    call sp_transfer_student(5,2);

    -- 46 test with invalid 
    call sp_transfer_student(5,100);

-- 47
START transaction;
insert into enrollments (student_id,course_id,enrollment_date,grade) values 
(7,1,"2026-01-10","A");
savepoint sp1;
insert into enrollments (student_id,course_id,enrollment_date,grade) values 
(10,1,"2026-01-11","F");
rollback to sp1;
commit; 