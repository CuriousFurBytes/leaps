# Module 1: Variables and Types — Test

[← Module Home](./README.md) | [Topic Home](../README.md)

**Total Points:** 20  
**Passing Score:** 16 / 20 (80%)  
**Estimated Time:** 40 minutes

---

## Grading Record

| Attempt | Date | Score | Grade | Notes |
|---------|------|-------|-------|-------|
| 1st | — | — / 20 | — | — |
| 2nd | — | — / 20 | — | — |

---

## Section 1: Recall (4 points — 1 pt each)

**Q1.** What does `type(True)` return?

Your answer: _______________

---

**Q2.** What is the output of `10 // 3`? What about `-10 // 3`?

Your answer: _______________

---

**Q3.** What is the correct way to check if a variable `x` is `None`?

a) `if x == None:`  
b) `if x is None:`  
c) `if type(x) == NoneType:`  
d) `if not x:`

Your answer: _______________

---

**Q4.** What does `0.1 + 0.2 == 0.3` evaluate to in Python, and why?

Your answer: _______________

---

## Section 2: Code Reading (6 points — 2 pts each)

**Q5.** What is the output of this code?

```python
x = "Hello, World!"
print(x[7:12])
print(x[-6:])
print(x[::-1])
```

Your answer:

```
[line 1]:
[line 2]:
[line 3]:
```

---

**Q6.** What is the output, and does it demonstrate dynamic typing or static typing?

```python
x = 42
print(type(x).__name__)
x = "now a string"
print(type(x).__name__)
x = [1, 2, 3]
print(type(x).__name__)
```

Your answer:

```
[line 1]:
[line 2]:
[line 3]:
Dynamic or static?
```

---

**Q7.** What are the values of `a`, `b`, and `c` after this code runs?

```python
a, b = 10, 20
a, b = b, a
c = a + b
```

Your answer: a=___ b=___ c=___

---

## Section 3: Concept Application (6 points — 2 pts each)

**Q8.** Explain why this code may produce unexpected results, and fix it:

```python
total = 0.1 + 0.1 + 0.1
if total == 0.3:
    print("Equal!")
else:
    print("Not equal!")
```

Your answer:

_______________

---

**Q9.** What is the difference between `type(x) == int` and `isinstance(x, int)`? Give an example where they produce different results.

Your answer:

_______________

---

**Q10.** Explain the concept of truthiness in Python. List four falsy values and explain what makes them falsy.

Your answer:

_______________

---

## Section 4: Write Code (4 points — 2 pts each)

**Q11.** Write a function `celsius_to_fahrenheit(temp: float) -> float` that converts Celsius to Fahrenheit. Formula: `F = C × 9/5 + 32`. Include type hints and a docstring.

Your answer:

```python

```

---

**Q12.** Write a function `is_palindrome(s: str) -> bool` that returns `True` if the string is a palindrome (reads the same forwards and backwards), ignoring case and spaces.

For example:
- `is_palindrome("racecar")` → `True`
- `is_palindrome("A man a plan a canal Panama")` → `True`
- `is_palindrome("python")` → `False`

Your answer:

```python

```

---

*Check your answers in [ANSWERS.md](./ANSWERS.md) (coming soon)*
