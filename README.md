# High-Availability E-Commerce Microservices Platform

A production-ready, fintech-grade e-commerce platform built with a microservices architecture. Designed for high availability (HA), resilience, and scalability.

## 🚀 Key Features
- **Microservices Architecture**: 6 distinct services (User, Product, Order, Payment, Inventory, Notification).
- **Polyglot Stack**: Node.js, Python (Flask/FastAPI), Java (Spring Boot) demonstrating interoperability.
- **High Availability**: Configured for horizontal scaling and redundancy.
- **Event-Driven**: Asynchronous communication via Apache Kafka.
- **API Gateway**: NGINX with JWT validation, rate limiting, and load balancing.
- **Observability**: Prometheus & Grafana for metrics, Jaeger for distributed tracing.
- **Resilience**: Circuit breakers (Resilience4j), Retries, Dead Letter Queues.
- **Security**: JWT Auth, RBAC, Data encryption.

## 🏗️ Architecture

| Service | Tech Stack | Database | Port |
|---------|------------|----------|------|
| **API Gateway** | NGINX + Lua | - | 80 |
| **User Service** | Node.js / Express | MongoDB | 3000 |
| **Product Service** | Python / Flask | PostgreSQL | 5000 |
| **Order Service** | Java / Spring Boot | PostgreSQL | 8080 |
| **Payment Service** | Python / FastAPI | PostgreSQL | 8000 |
| **Inventory Service** | Python / Flask | PostgreSQL | 5000 |
| **Notification Service** | Python / FastAPI | Redis | 8000 |

## 🛠️ Infrastructure
- **PostgreSQL**: Primary data store for transactional services.
- **MongoDB**: Replica Set for user data.
- **Redis**: Caching and Token Blacklisting.
- **Kafka**: Event bus for inter-service communication.
- **Zookeeper**: Kafka coordination.

## 🚦 Getting Started

### Prerequisites
- Docker & Docker Compose
- 8GB+ RAM

### Installation & Run

1. **Clone the repository**
2. **Start the stack**
   ```bash
   docker-compose up -d --build
   ```
3. **Verify**
   Run the automated verification script:
   ```bash
   ./scripts/verify_system.sh
   ```

## 📊 Observability
- **Grafana**: `http://localhost:3000` (Default dashboads provisioned)
- **Prometheus**: `http://localhost:9090`
- **Kafka UI**: `http://localhost:8081`
- **Jaeger**: `http://localhost:16686`

## 🧪 API Documentation
All services are accessible through the API Gateway at `http://localhost:80`.

- `POST /api/users/register`: Register new user
- `POST /api/users/login`: Login
- `GET /api/products`: List products
- `POST /api/orders`: Create order
- ... see code for full routes.

## License
MIT
