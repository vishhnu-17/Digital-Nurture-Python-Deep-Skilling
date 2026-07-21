# Hands-On 3 – Test Automation Process, Lifecycle & Framework Types

## Task 1: Automation Decision and Test Case Selection

### 17. Criteria for Deciding Whether to Automate

| Criteria | Explanation | Application to `POST /api/courses/` |
|----------|-------------|--------------------------------------|
| Repetitive Execution | Tests executed frequently should be automated to save time. | This endpoint is tested after every code change, making it a good automation candidate. |
| Regression Testing | Features that must be verified after each release are ideal for automation. | Creating a course is a core feature and should be part of regression testing. |
| Stable Functionality | Stable features are easier to automate because they change less often. | The course creation endpoint is expected to remain stable. |
| Data-Driven Testing | Tests requiring multiple input combinations benefit from automation. | Different course names, credits, and departments can be tested automatically. |
| High Business Impact | Critical business functionality should be automated. | Course creation is a core feature of the Course Management API and should always work correctly. |

**Conclusion:**  
The `POST /api/courses/` success scenario is an excellent candidate for automation because it is repetitive, stable, business-critical, and part of regression testing.

---

### 18. Automate or Manual?

| Test Case | Decision | Justification |
|-----------|----------|---------------|
| (a) Regression test for all CRUD endpoints after every code change | **Automate** | Frequently executed and repetitive. |
| (b) Exploratory testing of a new search feature | **Manual** | Requires human observation and creativity. |
| (c) Performance test with 100 concurrent users | **Automate** | Performance tests are executed using automation tools. |
| (d) UI test for the login form | **Automate** | Login is a stable and frequently tested feature. |
| (e) Verify Swagger API documentation is accurate | **Manual** | Requires reviewing documentation for correctness and clarity. |
| (f) Smoke test after deployment | **Automate** | Should run automatically after every deployment to verify the application is available. |

---

### 19. Test Automation ROI

#### Definition

**Return on Investment (ROI)** measures whether the time spent creating and maintaining automated tests is less than repeatedly executing the same tests manually.

---

#### Calculation

- Automation development time = **4 hours**
- Manual execution time = **30 minutes (0.5 hours)**

Break-even point:

```
4 ÷ 0.5 = 8 runs
```

After **8 executions**, automation has saved enough time to recover its initial development cost.

After the **10th run**, assume a **20% maintenance overhead**.

Maintenance per run:

```
20% of 4 hours = 0.8 hours
```

Although maintenance adds extra effort, automation continues to provide long-term savings when the test is executed regularly.

---

### 20. Flaky Tests

#### Definition

A **flaky test** is a test that sometimes passes and sometimes fails without any changes to the application.

---

#### Example

A Selenium test clicks a button immediately after the page loads. Sometimes the button loads slowly, causing the test to fail even though the application works correctly.

---

#### Strategies to Prevent Flaky Tests

1. Use explicit waits (WebDriverWait) instead of time.sleep() so Selenium waits only until elements are ready.
2. Use stable locators, such as IDs or reliable CSS selectors, instead of fragile absolute XPaths.
3. Keep test data and the test environment consistent, ensuring tests don't depend on leftover data or unpredictable external factors.

---

# Task 2: Compare Automation Framework Types

## 21. Automation Framework Comparison

### 1. Linear Framework

**Description**

A Linear Framework executes test cases in a fixed sequence without separating test data or reusable components. It is the simplest automation framework.

**Advantage**
- Easy to learn and implement.

**Disadvantage**
- Difficult to maintain as the project grows.

**Course Management Example**
- Automating a simple login test for a small demo project.

---

### 2. Modular Framework

**Description**

The application is divided into independent modules, and reusable functions are created for each module.

**Advantage**
- Reusable code reduces duplication.

**Disadvantage**
- Initial design requires more planning.

**Course Management Example**
- Separate modules for Login, Courses, Students, and Departments.

---

### 3. Data-Driven Framework

**Description**

Test logic remains the same while test data is stored externally in Excel, CSV, or JSON files.

**Advantage**
- Easily test multiple input combinations.

**Disadvantage**
- Test data management becomes more complex.

**Course Management Example**
- Testing course creation using multiple combinations of course names and credits from a CSV file.

---

### 4. Keyword-Driven Framework

**Description**

Test steps are represented using predefined keywords such as Login, Click, Type, and Verify, allowing non-programmers to create test cases.

**Advantage**
- Easy for non-technical team members to use.

**Disadvantage**
- More complex framework implementation.

**Course Management Example**
- QA analysts create login tests using keywords instead of writing Selenium code.

---

### 5. Hybrid Framework

**Description**

A Hybrid Framework combines Modular, Data-Driven, and Keyword-Driven approaches to maximize flexibility and maintainability.

**Advantage**
- Highly scalable and reusable.

**Disadvantage**
- More complex to design and maintain.

**Course Management Example**
- Reusing page objects while reading login credentials from CSV files and allowing keyword-based test execution.

---

### 22. Recommended Framework

For the Course Management frontend, the requirements are:

- Test login with **50 user/password combinations**
- Reuse login functionality across **20 test cases**
- Support both **technical and non-technical** team members

### Recommendation

A **Hybrid Framework** combining:

- **Modular Framework** for reusable login functionality.
- **Data-Driven Framework** for testing multiple user credentials.
- **Keyword-Driven Framework** so non-technical QA members can create test scenarios.

This combination provides scalability, reusability, and ease of maintenance.

---

### 23. Hybrid Framework Folder Structure

```text
CourseManagementAutomation/
│
├── config/
│   ├── config.py
│   └── settings.json
│
├── data/
│   ├── login_data.csv
│   ├── course_data.csv
│   └── users.xlsx
│
├── pages/
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── course_page.py
│   └── base_page.py
│
├── tests/
│   ├── test_login.py
│   ├── test_courses.py
│   ├── test_students.py
│   └── test_smoke.py
│
├── utilities/
│   ├── browser_utils.py
│   ├── wait_utils.py
│   ├── logger.py
│   └── screenshot.py
│
├── reports/
│
├── screenshots/
│
├── requirements.txt
│
└── pytest.ini
```

### Folder Description

- **config/** – Stores project configuration files.
- **data/** – Contains CSV, Excel, or JSON test data.
- **pages/** – Page Object Model classes.
- **tests/** – Selenium test scripts.
- **utilities/** – Common helper functions.
- **reports/** – Test execution reports.
- **screenshots/** – Screenshots captured during failures.

---
