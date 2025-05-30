# SQLAlchemy, Alembic, and PostgreSQL Project with Docker

This project demonstrates a Python application using SQLAlchemy for ORM, Alembic for database migrations, and PostgreSQL as the database. The entire environment is containerized using Docker and Docker Compose, with Python dependencies managed by Poetry.

## Prerequisites

- **Git:**
- **Docker:**
- **Docker Compose:**

_(Poetry is used for Python dependency management within the Docker image, so you do not need to install Poetry on your host machine to run these Dockerized steps.)_

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/yarqui/pythonweb-06.git
    cd pythonweb-06
    ```

## Running the Application and Database

1.  **Build and Start Docker Services:**
    This command will build the application Docker image (if it doesn't exist or if `Dockerfile` changes) and start both the PostgreSQL database container and your application container in detached mode.
    ```bash
    docker-compose up --build -d
    ```
    Wait for the database service to initialize. You can check the status with:
    ```bash
    docker-compose ps
    ```
    You should see both `db` and `app` services running, and the `db` service should indicate it's `(healthy)`.

## Executing Project Tasks

All the following commands should be run from your project root directory on your host machine. They use `docker-compose exec` to run commands inside the running `app` container.

1.  **Apply Database Migrations**
    This command uses Alembic to apply all pending migrations, which will create the necessary tables in your PostgreSQL database based on your SQLAlchemy models.

    ```bash
    docker-compose exec app poetry run alembic upgrade head
    ```

2.  **Seed the Database with Initial Data**
    This command runs the `seed.py` script, which populates your database tables with randomly generated data.

    ```bash
    docker-compose exec app poetry run python -m src.seed
    ```

3.  **Run Select Queries**
    This command runs the `my_select.py` script, which executes 10 predefined queries against the database and prints their results to the console.
    ```bash
    docker-compose exec app poetry run python -m src.my_select
    ```
    Review the output in your terminal to see the results of each query.

## Accessing the Database Directly

If you want to connect directly to the PostgreSQL database (e.g., to inspect tables, running manual queries with `psql`):

```bash
docker-compose exec db psql -U admin -d myappdb
```
