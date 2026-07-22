# Hands-On 4 – Task 3: Step 58 Comparison

## N+1 Version

- **Queries Executed:** 12
- **Database Round-Trips:** 12
- **Time Taken:** `0.019908` seconds

## JOIN Version

- **Queries Executed:** 1
- **Database Round-Trips:** 1
- **Time Taken:** `0.003991` seconds

## Observation

The JOIN version performs significantly better because all the required data is fetched using a single SQL query instead of executing one query for each enrollment. This reduces the number of database round-trips and improves performance.

## What is a Database Round-Trip?

A database round-trip consists of:

1. Python sends a query to the MySQL server.
2. MySQL executes the query.
3. MySQL returns the result to Python.

## Comparison Table

| Approach | Queries Executed | Database Round-Trips |
|-----------|-----------------:|---------------------:|
| N+1 Query | 12 | 12 |
| JOIN Query | 1 | 1 |

