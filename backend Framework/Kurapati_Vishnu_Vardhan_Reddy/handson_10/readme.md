# Hands-on 10 – Microservices Architecture

## Service Decomposition

The Course Management API can be decomposed into the following independent microservices.

| Service Name | Responsibility | Endpoints it Owns | Database it Owns |
|--------------|----------------|-------------------|------------------|
| Auth Service | User registration, login, JWT authentication | `/register`, `/login` | `users.db` |
| Course Service | Manage departments and courses | `/courses`, `/departments` | `courses.db` |
| Student Service | Manage students and enrollments | `/students`, `/enrollments` | `students.db` |
| Notification Service | Send email notifications | `/send-email` | `notifications.db` |

## Why this decomposition?

- Each service has a single responsibility.
- Each service owns its own database.
- Services can be developed, deployed, and scaled independently.
- Failure in one service does not directly affect the others.


## Synchronous Communication (HTTP)

In synchronous communication, one service directly calls another service over HTTP and waits for an immediate response.

### Advantages
- Easy to implement and understand.
- Immediate response from the called service.
- Suitable for real-time operations.

### Disadvantages
- Tight coupling between services.
- If one service is unavailable, dependent requests fail.
- Increased response time due to network latency.

---

## Asynchronous Communication (Message Queue)

In asynchronous communication, services exchange messages through a message broker such as RabbitMQ or Kafka instead of communicating directly.

### Advantages
- Loose coupling between services.
- Better scalability.
- Improved fault tolerance.
- Services continue processing even if another service is temporarily unavailable.

### Disadvantages
- More complex architecture.
- Eventual consistency instead of immediate consistency.
- Requires additional infrastructure.

---

## When to use RabbitMQ or Kafka

Message queues are suitable when immediate responses are not required.

Examples include:
- Sending confirmation emails
- SMS notifications
- Logging
- Audit records
- Order processing
- Background jobs
- Analytics