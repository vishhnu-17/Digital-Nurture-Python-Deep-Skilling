import mysql.connector

import time
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="college_db"
)
cursor=conn.cursor(dictionary=True)
start = time.time()

query_count = 1

cursor.execute("SELECT * FROM enrollments")
enrollments = cursor.fetchall()
# print(enrollments)

start=time.time()
for enrollment in enrollments:
    cursor.execute("select first_name,last_name from students where student_id=%s",(enrollment["student_id"],))
    student=cursor.fetchone()
    print(f'{student["first_name"]} {student["last_name"]}-> enrollement {enrollment["enrollment_id"]}')
    query_count+=1
end=time.time()
print(f"\nQueries executed: {query_count}")
print(f"Time taken: {end-start:.6f} seconds")

cursor.close()
conn.close()    