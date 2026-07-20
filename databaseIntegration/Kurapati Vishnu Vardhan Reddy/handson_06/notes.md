# Task 3 - Eager Loading

## Before `joinedload()`

- One query fetched the `enrollments` table.
- Additional queries were executed for each related `student` and `course`.
- This resulted in the **N+1 query problem**, where one initial query is followed by multiple additional queries.

## After `joinedload()`

- Related `student` and `course` data are fetched together using SQL `JOIN`s.
- Only **one SQL query** is executed.
- The N+1 query problem is eliminated.
- Query performance is significantly improved by reducing the number of database round trips.