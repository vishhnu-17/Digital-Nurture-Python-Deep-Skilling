# Hands-On 1 – QA Concepts, Functional Testing & Defect Lifecycle

## Task 1: Map Testing Types to a Real System

### 1. Test Levels for the Course Management API

#### Unit Testing
- **Test Case:** Test the `send_confirmation_email()` function to ensure it sends a confirmation email to the user. 
- **Example:**
  - Input: `student_email="cynthiajmehul@gmail.com`
  - Expected Result: `Sending confirmation to cynthiajmehul@gmail.com`

#### Integration Testing
- **Test Case:** Verify that the `POST /api/courses/` endpoint successfully stores a new course in the database.
- **Components Tested:** FastAPI endpoint + SQLAlchemy + Database.
- **Expected Result:** Course is inserted into the database and `201 Created` is returned.

#### System Testing
- **Test Case:** Verify the complete course management workflow.
- **Steps:**
  1. Login as Admin.
  2. Create a course.
  3. Retrieve the course.
  4. Update the course.
  5. Delete the course.
- **Expected Result:** All operations complete successfully.

#### User Acceptance Testing (UAT)
- **Test Case:** A college administrator verifies that they can manage courses using the application.
- **Expected Result:** The application meets the college's business requirements and is accepted for use.

---

### 2. Functional vs Non-Functional Testing

| Test Case                                      | Type           |
|------------------------------------------------|----------------|
| Create a new course using `POST /api/courses/` | Functional     |
| Retrieve all courses using `GET /api/courses/` | Functional     |
| Reject invalid credits                         | Functional     |
| API responds within 2 seconds                  | Non-Functional |

#### Non-Functional Test Example
**Performance Testing**
- Send multiple requests simultaneously to the Course Management API.
- **Expected Result:** The API should respond within 2 seconds without crashing.

---

### 3. Black-Box vs White-Box Testing

#### Black-Box Testing
Black-box testing verifies the functionality of the application without knowing the internal code or implementation. The tester provides inputs and verifies the outputs based on the requirements.

#### White-Box Testing
White-box testing verifies the internal code, logic, branches, and execution paths. The tester has knowledge of the source code and tests individual functions and code paths.

**Who performs them?**
- **QA Tester:** Black-Box Testing
- **Developer:** White-Box Testing

---

### 4. Formal Test Cases for `POST /api/courses/`

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|--------------|-------------|---------------|------------|-----------------|---------------|-----------|
| TC_001 | Verify that a course is created successfully with valid data. | API server is running and database is connected. | 1. Send a POST request with valid course details.<br>2. Click Send. | Status code **201 Created** is returned and the course is stored in the database. | Status code **201 Created** is returned and the course is stored in the database. | Pass |
| TC_002 | Verify that a course cannot be created with an empty course name. | API server is running. | 1. Send a POST request with an empty course name.<br>2. Click Send. | Status code **400 Bad Request** is returned with an appropriate validation message. | Status code **400 Bad Request** is returned with an appropriate validation message.  |  Pass |
| TC_003 | Verify that a course cannot be created with negative credits. | API server is running. | 1. Send a POST request with negative credits.<br>2. Click Send. | Status code **400 Bad Request** is returned with a validation error. | Status code **400 Bad Request** is returned with a validation error. | Pass |

---

# Task 2: Defect Lifecycle & Severity Classification

## 5. Defect Lifecycle

```
New
 ↓
Assigned
 ↓
Open
 ↓
Fixed
 ↓
Retest
 ↓
Verified
 ↓
Closed
```

### Rejected Path
If the reported issue is not actually a defect or cannot be reproduced, it is marked **Rejected**.

### Deferred Path
If the defect is valid but fixing it is postponed to a future release due to low priority or time constraints, it is marked **Deferred**.

---

## 6. Severity and Priority Classification

| Bug | Severity | Priority | Justification |
|-----|----------|----------|---------------|
| a) `POST /api/courses/` returns **500 Internal Server Error** for all requests. | Critical | P1 | Core functionality is completely broken and users cannot create courses. Immediate fix required. |
| b) Course names longer than 150 characters are silently truncated. | Medium | P3 | Application still works, but data is modified unexpectedly, affecting data integrity. |
| c) Typo on the Swagger `/docs` page. | Low | P4 | Cosmetic issue with no impact on functionality. |
| d) Login occasionally returns **401 Unauthorized** for valid credentials. | High | P2 | Authentication is unreliable and affects users intermittently. Needs prompt investigation. |

---

## 7. Defect Report

**Defect ID:** DEF-001

**Title:** `POST /api/courses/` returns 500 Internal Server Error

**Environment:**
- Windows 11
- Python 3.12
- FastAPI
- SQLite
- Google Chrome

**Build Version:** v1.0

**Severity:** Critical

**Priority:** P1

**Steps to Reproduce:**
1. Start the Course Management API.
2. Open Postman.
3. Send a POST request to `/api/courses/` with valid course data.
4. Observe the response.

**Expected Result:**
The API should create the course successfully and return **201 Created**.

**Actual Result:**
The API returns **500 Internal Server Error** and no course is created.

**Attachments:**
- Screenshot of 500 Internal Server Error.

---

## 8. Severity vs Priority

### Severity
Severity indicates **how serious the defect is** and how much it impacts the application's functionality.

### Priority
Priority indicates **how urgently the defect should be fixed**.

### Example

A typo in the CEO's dashboard title has **Low Severity** because it does not affect functionality. However, if the CEO is demonstrating the application to clients tomorrow, it becomes **High Priority** and should be fixed immediately.

This example shows that **High Severity does not always mean High Priority, and High Priority does not always mean High Severity.**