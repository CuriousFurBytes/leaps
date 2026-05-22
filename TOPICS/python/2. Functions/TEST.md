# Module 2: Functions — Test

[← Module Home](./README.md) | [Topic Home](../README.md)

**Total Points:** 25  
**Passing Score:** 20 / 25 (80%)  
**Estimated Time:** 50 minutes

---

## Grading Record

| Attempt | Date | Score | Grade | Notes |
|---------|------|-------|-------|-------|
| 1st | — | — / 25 | — | — |
| 2nd | — | — / 25 | — | — |

---

## Section 1: Recall (5 points — 1 pt each)

**Q1.** What does LEGB stand for in Python's scoping rules?

Your answer: _______________

---

**Q2.** What is the output of this code?

```python
def f(x, y=10):
    return x + y

print(f(5))
print(f(5, 20))
print(f(y=3, x=1))
```text

Your answer:

```text
line 1:
line 2:
line 3:
```text

---

**Q3.** What is the difference between `*args` and `**kwargs`?

Your answer: _______________

---

**Q4.** What does a function return if it has no `return` statement?

Your answer: _______________

---

**Q5.** What is a closure?

Your answer: _______________

---

## Section 2: Code Reading (8 points — 2 pts each)

**Q6.** What is the output of this code? Explain the scope behavior.

```python
x = "global"

def outer():
    x = "outer"
    def inner():
        print(x)
    return inner

f = outer()
f()
print(x)
```text

Your answer: _______________

---

**Q7.** This code has a bug. Identify it and write the fix.

```python
def add_to_list(item, result=[]):
    result.append(item)
    return result

print(add_to_list("a"))
print(add_to_list("b"))
print(add_to_list("c"))
```text

What is the actual output? What was the intended output? What is the fix?

Your answer: _______________

---

**Q8.** What is the output of this code? Explain what a closure is doing here.

```python
def make_multiplier(n):
    return lambda x: x * n

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))
print(triple(5))
print(double(triple(2)))
```text

Your answer: _______________

---

**Q9.** What is wrong with this code? Fix it.

```python
functions = []
for i in range(5):
    functions.append(lambda: i)

print([f() for f in functions])
```text

Your answer: _______________

---

## Section 3: Concept Application (7 points)

**Q10 (3 pts).** Explain the difference between these two approaches. When would you use each?

```python
# Approach A
result = sorted(words, key=lambda w: (len(w), w.lower()))

# Approach B
def sort_key(w):
    return (len(w), w.lower())

result = sorted(words, key=sort_key)
```text

Your answer: _______________

---

**Q11 (2 pts).** Write a function `apply_twice(func, value)` that applies `func` to `value` twice and returns the result. Then use it to:
- Double a number twice (result should be 4x original)
- Apply `.strip()` twice to a string (should be idempotent)

```python
def apply_twice(func, value):
    # your code here

# Test:
print(apply_twice(lambda x: x * 2, 5))    # 20
print(apply_twice(str.strip, "  hello  ")) # "hello"
```text

Your answer:

```python

```text

---

**Q12 (2 pts).** Write a function `count_calls(func)` that wraps any function and counts how many times it's been called. The wrapper should have a `.call_count` attribute.

```python
def count_calls(func):
    # your code here

@count_calls
def add(a, b):
    return a + b

add(1, 2)
add(3, 4)
add(5, 6)
print(add.call_count)   # 3
```text

Your answer:

```python

```text

---

## Section 4: Design (5 points)

**Q13 (5 pts).** Design a `memoize` decorator that:
- Caches the return value of a function based on its arguments
- Works for functions with any number of positional arguments
- Stores a `cache_hits` counter on the wrapper function
- Has a `clear_cache()` method on the wrapper

Show it working with a Fibonacci function.

Your answer:

```python

```text

---

## Bonus (5 pts)

**B1 (2 pts).** Explain what `functools.partial` does and write an equivalent `partial` function yourself.

**B2 (3 pts).** Write a `type_checked` decorator that validates function arguments against their type hints at call time (look up `typing.get_type_hints()` and `inspect.signature()`).

---

*Check your answers in [ANSWERS.md](./ANSWERS.md) (coming soon)*
