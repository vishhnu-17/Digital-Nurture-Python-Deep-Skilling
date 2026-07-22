# Hands-On 4 – Task 3: Step 59 – N+1 Problem at Scale

## Scenario

Assume the application contains **10,000 enrollments**.

## N+1 Query Approach

- 1 query is executed to fetch all enrollments.
- 10,000 additional queries are executed to fetch each student's details.
- **Total Queries Executed:** **10,001**

## JOIN Query Approach

- A single JOIN query retrieves both enrollment and student information.
- **Total Queries Executed:** **1**

## Comparison

| Approach | Total Queries |
|----------|--------------:|
| N+1 Query | 10,001 |
| JOIN Query | 1 |

## Conclusion

The N+1 query approach generates **10,000 unnecessary extra database queries** when processing 10,000 enrollments. These additional database round-trips significantly increase execution time and server load.

Using a **JOIN** retrieves all required data in a single query, eliminating unnecessary database calls and making the application far more efficient and scalable for large datasets.