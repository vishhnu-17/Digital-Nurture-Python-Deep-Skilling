import mysql.connector
import time

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="college_db"
)

cursor = conn.cursor(dictionary=True)

start = time.time()

query_count = 1

cursor.execute("""
SELECT
    e.enrollment_id,
    s.first_name,
    s.last_name
FROM enrollments e
JOIN students s
ON e.student_id = s.student_id
""")

rows = cursor.fetchall()

for row in rows:
    print(f"{row['first_name']} {row['last_name']} -> Enrollment {row['enrollment_id']}")

end = time.time()

print(f"\nQueries executed: {query_count}")
print(f"Time taken: {end - start:.6f} seconds")

cursor.close()
conn.close()