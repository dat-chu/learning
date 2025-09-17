# Learning Management Microservice

## 📌 Problem Statement

The system is a **microservice for learning management**, focusing on **user authentication, course management, lessons, and enrollment tracking**.  
It supports authentication & authorization with role-based access control (e.g., `admin`, `user`).

## 🎯 Key Features

- **User Management**: CRUD operations for users (signup, login, update, delete).
- **Course Management**: CRUD operations for courses with metadata.
- **Lesson Management**: Each course contains multiple lessons.
- **Enrollment & Progress Tracking**:
  - Users can enroll in courses.
  - Track lesson completion.
  - Calculate **percentage of lessons completed** for each user in a course.

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy (async)
- **Authentication**: JWT-based auth, role-based authorization
- **Containerization**: Docker & Docker Compose

## 🚀 Development

- Run services with Docker Compose:
  ```bash
  docker compose up --build
  ```
