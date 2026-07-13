"""
API Versioning Strategies

1. URL Versioning
Example:
    /api/v1/courses/
    /api/v2/courses/

Advantages:
- Simple
- Easy to understand
- Easy to test in browsers and Postman
- Most commonly used

Disadvantages:
- URLs change when versions change.


2. Header Versioning

Example:
Accept: application/vnd.api+json;version=1

Advantages:
- Cleaner URLs
- Resource URL remains the same

Disadvantages:
- Harder to test
- Client must always send headers
- Less obvious to developers
"""