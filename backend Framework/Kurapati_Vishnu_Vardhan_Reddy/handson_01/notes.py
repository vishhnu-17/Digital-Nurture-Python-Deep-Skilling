"""
===========================================================
TASK 1 - Understanding the Django Request-Response Cycle
===========================================================

1. Journey of a GET /api/courses/ request
-----------------------------------------

Browser
   |
   |  HTTP GET /api/courses/
   V
Django Server (WSGI/ASGI)
   |
   V
Middleware (Request Phase)
   |
   V
URL Router (urls.py)
   |
   | Matches '/api/courses/' to the appropriate view
   V
View (views.py)
   |
   | Executes business logic
   | If data is needed:
   V
Model (models.py)
   |
   | Django ORM generates SQL query
   | SQL is executed on the database
   V
Database
   |
   | Returns course records
   V
Model
   |
   V
View
   |
   | Formats data (HTML/JSON)
   V
Response Object
   |
   V
Middleware (Response Phase)
   |
   V
Browser receives HTTP Response


===========================================================
2. Middleware
===========================================================

Middleware sits between the web server and the Django view.

Request Flow:
Browser
   ->
Middleware
   ->
URL Router
   ->
View

Response Flow:
View
   ->
Middleware
   ->
Browser

Middleware can inspect or modify both requests and responses.


Two built-in Django middleware classes:

1. django.middleware.security.SecurityMiddleware
   - Adds security-related HTTP headers.
   - Helps enforce HTTPS.
   - Protects against several common security issues.

2. django.contrib.sessions.middleware.SessionMiddleware
   - Enables session support.
   - Allows Django to remember user data across requests.
   - Used for login sessions and shopping carts.


(Other common middleware include AuthenticationMiddleware,
CsrfViewMiddleware, CommonMiddleware, etc.)


===========================================================
3. WSGI vs ASGI
===========================================================

WSGI (Web Server Gateway Interface)
-----------------------------------
- Standard interface for synchronous Python web applications.
- Handles one request per worker at a time.
- Best for traditional web applications.
- Supported by servers like Gunicorn and uWSGI.

ASGI (Asynchronous Server Gateway Interface)
--------------------------------------------
- Successor to WSGI.
- Supports asynchronous programming using async/await.
- Can handle WebSockets, long-lived connections, and many concurrent users.
- Supported by servers like Daphne and Uvicorn.

Which does Django use by default?
---------------------------------
- Django provides WSGI by default.
- Every Django project contains a wsgi.py file.
- Modern Django projects also include asgi.py.

When should ASGI be used?
-------------------------
Use ASGI when the application requires:
- WebSockets
- Real-time chat
- Live notifications
- Streaming responses
- Many concurrent connections
- Async views


===========================================================
4. MVC vs Django's MVT
===========================================================

Traditional MVC:

Model
- Handles data and database.

View
- Displays data to the user.

Controller
- Receives requests and controls application logic.


Django follows the MVT pattern:

Model
- Same as MVC Model.
- Represents database tables and business data.

View
- Acts like the Controller in MVC.
- Receives requests, performs logic, interacts with models,
  and returns responses.

Template
- Equivalent to the View in MVC.
- Responsible for displaying HTML to users.


MVC             Django MVT
--------------------------------------
Model      -->  Model
View       -->  Template
Controller -->  View


Summary:
- MVC Controller = Django View
- MVC View = Django Template
- MVC Model = Django Model
"""