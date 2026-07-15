# Task 42 – Updating a Multi-Table View

## Observation

An attempt to update the `vw_student_enrollment_summary` view failed because it is a **multi-table view** created using `JOIN` operations and aggregate functions (`COUNT()` and `AVG()`).

## Why it is not updatable

The view contains data from multiple tables (`students`, `departments`, and `enrollments`) and also includes calculated columns. When an `UPDATE` statement is executed, MySQL cannot determine how the changes should be applied to the underlying tables or how calculated values should be modified.

For example, the `full_name` column is generated using:

```sql
CONCAT(first_name, ' ', last_name)
```

If we execute:

```sql
UPDATE vw_student_enrollment_summary
SET full_name = 'John Smith'
WHERE student_id = 1;
```

MySQL cannot determine how to split `"John Smith"` into `first_name` and `last_name`.

Similarly, values such as `COUNT(course_id)` and `GPA` are computed using aggregate functions and are **derived values**, not actual columns stored in the database. Therefore, they cannot be updated directly.

## Conclusion

Multi-table views containing `JOIN`s and aggregate functions are generally **not updatable**. To allow updates through a view, it should typically be based on a **single table** and avoid aggregate functions or computed columns.