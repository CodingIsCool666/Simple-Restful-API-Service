# Simple Restful API Service

This repository contains a simple RESTful API built with **Flask** and **SQLAlchemy**. It exposes endpoints for creating, reading, updating, and deleting student records stored in a PostgreSQL database.

## Features
- CRUD endpoints for students
- PostgreSQL database integration via SQLAlchemy
- Dockerfile and Docker Compose setup
- Unit and end-to-end tests using pytest

## Requirements
- Python 3.11
- PostgreSQL database (or use Docker Compose)
- `pip` for installing dependencies

## Installation
Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file or set the following environment variables for database configuration:

```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASS=postgres
DATABASE_NAME=postgres
```

## Running the Application

### Directly with Python
Ensure PostgreSQL is running and the environment variables are set, then start the Flask app:

```bash
python app.py
```

The API will be available at `http://localhost:8888/api/student`.

### Using Docker Compose
You can also run the app and database with Docker Compose:

```bash
docker-compose up --build
```

## API Endpoints

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | `/api/student` | Get all students (returns 404 if none). |
| POST | `/api/student` | Add a new student (JSON with `name`, `age`, `major`). |
| PUT | `/api/student/<id>` | Update a student's information. |
| DELETE | `/api/student/<id>` | Delete a student by ID. |

## Running Tests
With the application and database running, execute the tests with:

```bash
pytest
```

This runs both the unit tests and the end-to-end tests that interact with the running API.

