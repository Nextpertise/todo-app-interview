# 📌 Todo App (Python + FastAPI + Pydantic)

A simple, object-oriented **TODO application** built with **FastAPI**, **Pydantic**, and an in-memory store. This project serves as a **starting point for technical interviews**, demonstrating best practices in Python API design, object-oriented programming, and dependency management.

## 🚀 Features
- ✅ **FastAPI**-based REST API
- ✅ **Pydantic models** with computed properties
- ✅ **In-memory storage** with a dynamic parent-child TODO relationship
- ✅ **Singleton-based `TodoManager`** for efficient data handling
- ✅ **Unit tests with `unittest`**
- ✅ **Dynamic child resolution** via Pydantic properties

## 🔧 API Endpoints
- `GET /todo` → List all TODOs (including children)
- `POST /todo` → Add a new TODO (optionally linked to a parent)
- `DELETE /todo/{todo_uuid}` → Remove a TODO

## 🛠 Setup & Run
```bash
# Clone the repo
$ git clone https://github.com/Nextpertise/todo-app-interview.git

# Install dependencies
$ poetry install

# Run the FastAPI server
$ cd src
$ poetry run uvicorn main:app --reload

# Run the tests (from the root directory) and set the python path
$ PYTHONPATH=src poetry run pytest
```