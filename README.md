# DRF Theatre Service

The **DRF Theatre Service** is a Django REST Framework-based application designed to manage theatre-related operations such as plays, performances, reservations, and payments. It provides a robust API for managing theatre data and integrates with external payment services like Stripe for handling transactions.

---

## Features

- **Plays Management**: Manage plays, including their genres and associated actors.
- **Performance Scheduling**: Schedule performances in theatre halls with zone-based seating.
- **Reservations**: Allow users to reserve tickets for performances.
- **Payments**: Integrate with Stripe for secure payment processing.
- **API Documentation**: Automatically generated API documentation using DRF-Spectacular.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/drf-theatre-service.git
   cd drf-theatre-service
   ```

2. Install dependencies using [Poetry](https://python-poetry.org/):
   ```bash
   poetry install
   ```

3. Set up the environment variables:
   ```bash
   cp .env.example .env
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

---

## Running the Project with Docker Compose

To run the project using Docker Compose, follow these steps:

1. **Ensure Docker and Docker Compose are installed**:
   - Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) on your system.

2. **Set up environment variables**:
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Fill in the required variables in the `.env` file. See the description of each variable below.

3. **Build and start the containers**:
   - Run the following command to build and start the containers:
     ```bash
     docker-compose up --build
     ```

4. **Access the application**:
   - The application will be available at [http://localhost](http://localhost).
   - The API documentation can be accessed at:
     - Swagger UI: [http://localhost/api/schema/swagger-ui/](http://localhost/api/schema/swagger-ui/)
     - ReDoc: [http://localhost/api/schema/redoc/](http://localhost/api/schema/redoc/)

5. **Access additional services**:
   - **PostgreSQL**: Available on port `5432`.
   - **pgAdmin**: Available at [http://localhost:5050](http://localhost:5050).
   - **RedisInsight**: Available at [http://localhost:5540](http://localhost:5540).

---

## Environment Variables

The `.env.example` file contains the following variables. Here's what each variable does:

### Email Configuration
- **`EMAIL_BACKEND`**: The backend used for sending emails (e.g., `django.core.mail.backends.smtp.EmailBackend`).
- **`EMAIL_HOST`**: The SMTP server for sending emails.
- **`EMAIL_HOST_USER`**: The username for the SMTP server.
- **`EMAIL_HOST_PASSWORD`**: The password for the SMTP server.
- **`EMAIL_PORT`**: The port for the SMTP server (e.g., `587` for TLS).

### Google OAuth Configuration
- **`GOOGLE_OAUTH_CLIENT_ID`**: The client ID for Google OAuth integration.
- **`GOOGLE_OAUTH_CLIENT_SECRET`**: The client secret for Google OAuth integration.

### Database Configuration
- **`POSTGRES_HOST`**: The hostname for the PostgreSQL database (e.g., `db` for the Docker service).
- **`POSTGRES_PORT`**: The port for the PostgreSQL database (default: `5432`).
- **`POSTGRES_DB`**: The name of the PostgreSQL database.
- **`POSTGRES_USER`**: The username for the PostgreSQL database.
- **`POSTGRES_PASSWORD`**: The password for the PostgreSQL database.

### pgAdmin Configuration
- **`PGADMIN_DEFAULT_EMAIL`**: The default email for accessing pgAdmin.
- **`PGADMIN_DEFAULT_PASSWORD`**: The default password for accessing pgAdmin.

### Django Configuration
- **`SECRET_KEY`**: The secret key for the Django application. This should be a long, random string.
- **`DJANGO_SETTINGS_MODULE`**: The settings module for the Django application (default: `config.settings`).
- **`DEBUG`**: Whether to run the application in debug mode (`True` or `False`).

### Stripe Configuration
- **`STRIPE_PUBLISHABLE_KEY`**: The publishable key for Stripe integration.
- **`STRIPE_SECRET_KEY`**: The secret key for Stripe integration.
- **`STRIPE_WEBHOOK_SECRET`**: The webhook secret for Stripe to verify incoming webhook requests.

### Payment Configuration
- **`PAYMENT_SESSION_EXPIRATION_MINUTES`**: The expiration time (in minutes) for payment sessions (default: `30`).
- **`PAYMENT_CURRENCY`**: The currency for payments (e.g., `usd`).

### Frontend URLs
- **`FRONTEND_SUCCESS_URL`**: The URL to redirect users to after a successful payment.
- **`FRONTEND_CANCEL_URL`**: The URL to redirect users to after a canceled payment.

---

By configuring these variables in the `.env` file, you can customize the behavior of the application and ensure it integrates correctly with external services like Stripe, PostgreSQL, and email providers.

## Dependencies

This project uses the following dependencies, defined in `pyproject.toml`:

### Core Dependencies
- **Django**: The web framework used for building the application.
- **Django REST Framework (DRF)**: Provides tools for building RESTful APIs.
- **DRF-Spectacular**: Used for generating OpenAPI documentation for the API.
- **django-filter**: Adds filtering capabilities to DRF views.
- **python-decouple**: Manages environment variables for configuration.

### Database
- **psycopg2**: PostgreSQL adapter for Python, used for database interactions.

### Payments
- **Stripe**: Integration with Stripe for payment processing.

### Development Tools
- **black**: A code formatter for maintaining consistent code style.
- **flake8**: A linting tool for enforcing Python coding standards.
- **isort**: Automatically sorts imports in Python files.

### Why These Dependencies Were Used
- **Django and DRF**: Provide a robust framework for building scalable web applications and APIs.
- **DRF-Spectacular**: Simplifies API documentation generation, ensuring consistency and ease of use.
- **django-filter**: Enhances API usability by enabling filtering capabilities.
- **psycopg2**: Ensures efficient interaction with the PostgreSQL database.
- **Stripe**: Offers a secure and reliable payment processing solution.
- **Testing Tools**: Ensure the application is thoroughly tested and reliable.
- **Development Tools**: Maintain code quality and consistency across the project.

---

## API Documentation

The API documentation is automatically generated using **DRF-Spectacular**. Once the server is running, you can access the documentation at:

- Swagger UI: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
- ReDoc: [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)

---

## In Progress Tasks

### Features
- [ ] Scheduled job to release tickets for unpaid orders.
- [ ] Optimize relationships for the Ticket table (link Ticket to ZonePrice, instead of linking to Performance and Zone).
- [ ] Optimization of ReservationService and closer integration with PaymentService (now payment for Reservation is created outside the transaction in which Reservation is created).
- [ ] Handling the case when one user tries to create two Reservations at the same time (now two Reservations will be created, but a user cannot have two Reservations with PENDING Payment).
- [ ] Additional check of payment session status when processing webhook
- [ ] Pagination
- [ ] Reservation cancellation functionality
- [ ] Response caching
- [ ] Social auth authentication

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push them to your fork.
4. Submit a pull request with a detailed description of your changes.

---

## Contact

For questions or support, please contact [yaroslav.zhuravlov.dev@gmail.com](mailto:yaroslav.zhuravlov.dev@gmail.com).