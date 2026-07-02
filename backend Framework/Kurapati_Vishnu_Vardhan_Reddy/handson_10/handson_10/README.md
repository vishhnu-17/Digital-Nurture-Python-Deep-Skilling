## Synchronous vs Asynchronous Communication

### Synchronous Communication
- One service directly calls another service and waits for the response.
- Example: Student Service calling Course Service using the `requests` library.

### Asynchronous Communication
- Services communicate through a message broker such as RabbitMQ or Kafka.
- The sender does not wait for an immediate response.
- This approach improves scalability and fault tolerance.