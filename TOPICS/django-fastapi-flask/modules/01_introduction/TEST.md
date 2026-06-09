# Test: Module 01 — Introduction

**Instructions:** Answer all questions. Write your answers directly below each question in the `> Answer:` block. Bonus questions are optional and can raise your score above 100%.

**Total Points:** 37 pts (Easy: 5 × 1pt + Medium: 5 × 2pts + Hard: 4 × 3pts + Expert: 2 × 5pts)
**Bonus Available:** 5 pts

---

## Section 1: Easy Questions (1 pt each)

**Q1.** What does WSGI stand for, and which PEP number defines it for Python 3?

> Answer:

---

**Q2.** List the five most commonly used HTTP methods and the CRUD operation each corresponds to.

> Answer:

---

**Q3.** What is the HTTP status code for each of the following situations?
(a) A resource was found and returned successfully
(b) A new resource was created
(c) The client sent a malformed request
(d) The client is not authenticated
(e) The server encountered an unexpected error

> Answer:

---

**Q4.** In one sentence each: what is Flask, what is Django, and what is FastAPI?

> Answer:

---

**Q5.** What is the function signature of a minimal WSGI application? Name the two parameters and briefly explain what each contains.

> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Explain the difference between WSGI and ASGI. Your answer must include: (a) the programming model difference (synchronous vs asynchronous), (b) one concrete scenario where ASGI provides a meaningful advantage over WSGI, and (c) one type of connection that ASGI supports but WSGI does not.

> Answer:

---

**Q7.** Compare Flask and Django across these four dimensions: (a) built-in database support, (b) routing configuration style, (c) target use case, and (d) out-of-the-box API documentation.

> Answer:

---

**Q8.** What is the "application factory pattern" in Flask and why does it matter for testing? You do not need to show code, but describe the concept clearly.

> Answer:

---

**Q9.** HTTP is described as a "stateless protocol." What does this mean, and what mechanisms do web applications use to work around this statelessness?

> Answer:

---

**Q10.** Why is running `flask run` or `uvicorn main:app --reload` unsuitable for a production deployment? Name at least two specific problems with these development servers in production.

> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** The following Flask application has three bugs. Find and fix each one, and explain what each bug would cause at runtime.

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/greet", methods=["GET"])
def greet():
    name = request.json["name"]
    return f"Hello, {name}!"

@app.route("/items/<item_id>")
def get_item(item_id):
    items = {1: "apple", 2: "banana"}
    return items[item_id]

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
```

> Answer:

---

**Q12.** Write a FastAPI endpoint that:
- Route: `POST /users`
- Accepts a JSON body with fields: `username` (string, 3–50 chars), `email` (valid email format), `age` (integer, 18 or older)
- Returns `{"id": 1, "username": ..., "email": ..., "age": ...}` with status 201 on success
- FastAPI/Pydantic should handle all validation automatically (no manual if/else validation)

Show the complete Pydantic model and route function.

> Answer:

---

**Q13.** Explain the historical progression of Python web serving: from CGI to mod_python to WSGI to ASGI. For each step, describe the key limitation that motivated the transition to the next step.

> Answer:

---

**Q14.** You are deploying a FastAPI application. Explain the difference between these two deployment commands and when you would use each:

```bash
# Option A
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Option B
gunicorn main:app -k uvicorn.workers.UvicornWorker --workers 4 --bind 0.0.0.0:8000
```

> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** A team is choosing between Flask and FastAPI for a new project. The project is a REST API for a machine learning model serving system. Expected characteristics: 500 requests/second at peak, most requests involve calling the model (100–500ms CPU-bound work), WebSocket connections for streaming results, team of 3 Python engineers with 2 years of web development experience.

Design your recommendation. Include: (a) your framework choice and justification, (b) the deployment architecture (server type, worker count, process manager), (c) one thing about the chosen framework you would need to be careful about given the CPU-bound nature of the ML inference work, and (d) how you would handle the WebSocket streaming requirement.

> Answer:

---

**Q16.** The following is a complete minimal WSGI application:

```python
def application(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"Hello"]
```

Without using Flask, Django, or FastAPI — using only Python's standard library and the `wsgiref` module — extend this into a WSGI application that:

1. Routes `GET /` to return `{"message": "ok"}` as JSON
2. Routes `POST /echo` to read the JSON request body and return it unchanged
3. Returns `{"error": "not found"}` with status 404 for all other paths
4. Returns `{"error": "method not allowed"}` with status 405 if the method is wrong for a known path

Show the complete implementation. Your code must be runnable.

> Answer:

---

## Bonus Question (+5 pts)

**Bonus 1.** (+5 pts) ASGI supports three `scope["type"]` values for different connection types. Name all three, describe what each represents, and give a concrete example of when each would be used in a real application.

> Answer:
