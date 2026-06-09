# Cheatsheet: Flask vs Django vs FastAPI

> Side-by-side comparisons of common tasks across all three frameworks. Use this as a quick reference while working on exercises or projects.

---

## Table of Contents

- [Hello World](#hello-world)
- [Route with URL Parameter](#route-with-url-parameter)
- [Reading Request Body (JSON)](#reading-request-body-json)
- [Returning JSON](#returning-json)
- [Middleware / Request Hooks](#middleware--request-hooks)
- [Database Model Definition](#database-model-definition)
- [Database Query](#database-query)
- [Authentication Check](#authentication-check)
- [Configuration](#configuration)
- [Running the Dev Server](#running-the-dev-server)
- [Running in Production](#running-in-production)
- [Testing an Endpoint](#testing-an-endpoint)

---

## Hello World

**Flask**

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
```

**Django**

```python
# urls.py
from django.urls import path
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, World!")

urlpatterns = [
    path("", index),
]
```

**FastAPI**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello, World!"}
```

---

## Route with URL Parameter

**Flask**

```python
@app.route("/users/<int:user_id>")
def get_user(user_id: int):
    return {"id": user_id}
```

**Django**

```python
# urls.py
path("users/<int:user_id>/", views.get_user),

# views.py
def get_user(request, user_id):
    return JsonResponse({"id": user_id})
```

**FastAPI**

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):        # type annotation = automatic validation
    return {"id": user_id}
```

---

## Reading Request Body (JSON)

**Flask**

```python
from flask import request

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()      # dict or None if body is not JSON
    name = data["name"]
    return {"created": name}, 201
```

**Django (DRF)**

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["POST"])
def create_user(request):
    name = request.data["name"]    # DRF parses JSON automatically
    return Response({"created": name}, status=201)
```

**FastAPI**

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

@app.post("/users", status_code=201)
def create_user(body: UserCreate):  # Pydantic validates; 422 on bad input
    return {"created": body.name}
```

---

## Returning JSON

**Flask**

```python
from flask import jsonify

@app.route("/data")
def data():
    return jsonify({"key": "value"})
    # OR in Flask 2.2+:
    return {"key": "value"}         # Flask auto-serializes dicts
```

**Django**

```python
from django.http import JsonResponse

def data(request):
    return JsonResponse({"key": "value"})
```

**FastAPI**

```python
@app.get("/data")
def data():
    return {"key": "value"}         # FastAPI always returns JSON
```

---

## Middleware / Request Hooks

**Flask**

```python
@app.before_request
def before():
    # Runs before every request
    pass

@app.after_request
def after(response):
    response.headers["X-Custom"] = "value"
    return response
```

**Django**

```python
# middleware.py
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code before the view
        response = self.get_response(request)
        # Code after the view
        response["X-Custom"] = "value"
        return response

# settings.py
MIDDLEWARE = ["myapp.middleware.CustomMiddleware", ...]
```

**FastAPI**

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Custom"] = "value"
        return response

app.add_middleware(CustomMiddleware)
```

---

## Database Model Definition

**Flask (Flask-SQLAlchemy)**

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
```

**Django**

```python
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = "users"
```

**FastAPI (SQLAlchemy 2.0)**

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
```

---

## Database Query

**Flask (Flask-SQLAlchemy)**

```python
# Get one by primary key
user = db.session.get(User, user_id)

# Filter
users = User.query.filter_by(active=True).all()

# SQLAlchemy 2.0 style (preferred)
from sqlalchemy import select
stmt = select(User).where(User.active == True)
users = db.session.execute(stmt).scalars().all()
```

**Django**

```python
# Get one
user = User.objects.get(pk=user_id)         # raises DoesNotExist if not found

# Filter
users = User.objects.filter(active=True)    # lazy QuerySet

# Get or 404
from django.shortcuts import get_object_or_404
user = get_object_or_404(User, pk=user_id)
```

**FastAPI (SQLAlchemy 2.0 async)**

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
```

---

## Authentication Check

**Flask (Flask-Login)**

```python
from flask_login import login_required, current_user

@app.route("/protected")
@login_required
def protected():
    return f"Hello, {current_user.name}"
```

**Django**

```python
from django.contrib.auth.decorators import login_required

@login_required
def protected(request):
    return HttpResponse(f"Hello, {request.user.username}")
```

**FastAPI (JWT via Depends)**

```python
from fastapi import Depends
from .auth import get_current_user

@app.get("/protected")
def protected(user = Depends(get_current_user)):
    return {"hello": user.name}
```

---

## Configuration

**Flask**

```python
# Using a config class
class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]

app.config.from_object(Config)
```

**Django**

```python
# settings.py — a Python module, import env vars with os.environ or django-environ
import os
DEBUG = os.environ.get("DEBUG", "False") == "True"
DATABASES = {
    "default": {"ENGINE": "django.db.backends.postgresql", "NAME": os.environ["DB_NAME"]}
}
```

**FastAPI (Pydantic Settings)**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Running the Dev Server

**Flask**

```bash
flask --app myapp run --debug
# or
python app.py
```

**Django**

```bash
python manage.py runserver
# With specific host/port:
python manage.py runserver 0.0.0.0:8000
```

**FastAPI**

```bash
uvicorn myapp.main:app --reload
# With host and port:
uvicorn myapp.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Running in Production

**Flask**

```bash
gunicorn "myapp:create_app()" --workers 4 --bind 0.0.0.0:8000
```

**Django**

```bash
gunicorn myproject.wsgi:application --workers 4 --bind 0.0.0.0:8000
```

**FastAPI**

```bash
uvicorn myapp.main:app --workers 4 --host 0.0.0.0 --port 8000
# Or with gunicorn + uvicorn workers:
gunicorn myapp.main:app -k uvicorn.workers.UvicornWorker --workers 4 --bind 0.0.0.0:8000
```

---

## Testing an Endpoint

**Flask**

```python
import pytest
from myapp import create_app

@pytest.fixture
def client():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
```

**Django**

```python
from django.test import TestCase, Client

class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
```

**FastAPI**

```python
import pytest
from fastapi.testclient import TestClient
from myapp.main import app

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}
```
