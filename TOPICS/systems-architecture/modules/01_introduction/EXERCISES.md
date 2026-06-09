# Exercises: Module 01 — Introduction to Distributed Systems

## Instructions

Complete each exercise in order. Exercises increase in difficulty.
Submit your answers by editing this file or committing a solutions file.

---

## Easy Exercises (1–3)

### Exercise 1

**Difficulty:** Easy
**Objective:** Recall the 8 Fallacies of Distributed Computing

List all 8 Fallacies of Distributed Computing from memory. For each, write a one-sentence description of the real-world consequence of believing it.

```markdown
1. The network is reliable — consequence: 
2. Latency is zero — consequence: 
3. Bandwidth is infinite — consequence: 
4. The network is secure — consequence: 
5. Topology doesn't change — consequence: 
6. There is one administrator — consequence: 
7. Transport cost is zero — consequence: 
8. The network is homogeneous — consequence: 
```

---

### Exercise 2

**Difficulty:** Easy
**Objective:** Classify databases on the CAP triangle

For each database below, state its CAP classification (CP, AP, or CA), and in one sentence explain what happens to reads/writes when a network partition occurs:

```markdown
1. Single-node PostgreSQL: classification = ?, partition behavior = ?
2. Apache Cassandra (default): classification = ?, partition behavior = ?
3. MongoDB (default write concern): classification = ?, partition behavior = ?
4. Apache ZooKeeper / etcd: classification = ?, partition behavior = ?
5. DynamoDB (eventually consistent reads): classification = ?, partition behavior = ?
```

---

### Exercise 3

**Difficulty:** Easy
**Objective:** Identify synchronous vs. asynchronous communication

For each scenario below, state whether synchronous or asynchronous communication is more appropriate, and give a one-sentence justification:

```markdown
1. User logs in and needs to know if their credentials are valid before proceeding.
   Choice: sync/async? Why?

2. After a successful order, send a "Your order has been placed" email to the customer.
   Choice: sync/async? Why?

3. An analytics service needs to track every user action for later reporting.
   Choice: sync/async? Why?

4. A ride-sharing app needs to know if a driver is available before confirming a booking.
   Choice: sync/async? Why?

5. After a user changes their profile picture, update CDN caches and thumbnail previews.
   Choice: sync/async? Why?
```

---

## Medium Exercises (4–6)

### Exercise 4

**Difficulty:** Medium
**Objective:** Analyze the trade-offs between monolith and microservices

A startup (team of 5 engineers) is building a new project management tool (similar to Trello). They are debating whether to start with a monolith or microservices.

Write a 200-word recommendation to the team. Your answer must:
- State your recommendation clearly
- Give at least 3 specific reasons for your recommendation
- Acknowledge the main counter-argument and explain why it doesn't override your recommendation at this stage
- Name the specific point (team size, scale, or operational maturity) at which the recommendation might change

```markdown
Your recommendation and reasoning:
[Write here]
```

---

### Exercise 5

**Difficulty:** Medium
**Objective:** Reason about the PACELC model

The PACELC model extends CAP by adding a latency/consistency trade-off for normal operation. Consider a global e-commerce site that wants to show users the number of remaining items for a product ("Only 3 left!").

Answer the following:
1. During a network partition between US and EU data centers, what should happen: refuse to show the count (CP), or show a potentially stale count (AP)?
2. During normal operation (no partition), the user is browsing products quickly. What trade-off should the system make: strong consistency (always accurate count) or low latency (slightly stale count)?
3. Based on your answers to 1 and 2, what PACELC classification does your design imply (e.g., PC/EC, PA/EL, PC/EL)?
4. Is there a scenario where showing a slightly incorrect item count could cause a real problem? How would you handle it?

```markdown
Your analysis:
[Write here]
```

---

### Exercise 6

**Difficulty:** Medium
**Objective:** Identify the Distributed Monolith anti-pattern

Read the following architecture description and identify all signs of a distributed monolith:

```
System: "EcomShop" — described as microservices by the team

Services:
- OrderService: Handles order creation. Writes to a shared PostgreSQL database,
  tables: orders, order_items, payments, customers.
- PaymentService: Handles payments. Reads and writes to the same shared PostgreSQL database.
- CustomerService: Handles customer profiles. Same database.
- NotificationService: Before sending any notification, it synchronously calls
  OrderService to get order details, then calls CustomerService to get the customer email.
  If either call fails, no notification is sent.

Deployment: All four services must be deployed together because they share database
migrations. The team has a single deployment pipeline that deploys all services
simultaneously.
```

List every distributed monolith symptom you can identify. For each symptom, name the specific anti-pattern and briefly explain the risk it creates.

```markdown
Symptoms and risks:
[Write here]
```

---

## Hard Exercises (7–8)

### Exercise 7

**Difficulty:** Hard
**Objective:** Implement robust service call error handling

The following Python code makes a call to an external user service. It is fragile — it violates multiple of the 8 Fallacies. Rewrite it to be production-quality.

```python
import requests

def get_user_profile(user_id: int) -> dict:
    response = requests.get(f"http://user-service/api/users/{user_id}")
    user = response.json()
    return user

def get_order_count(user_id: int) -> int:
    response = requests.get(f"http://order-service/api/users/{user_id}/orders")
    orders = response.json()
    return len(orders)

def get_user_dashboard(user_id: int) -> dict:
    user = get_user_profile(user_id)
    order_count = get_order_count(user_id)
    return {"user": user, "order_count": order_count}
```

Your rewrite must:
- Add appropriate timeouts to both calls
- Handle at least 4 distinct failure modes with appropriate behavior for each
- Make the two service calls in parallel (not sequential) to reduce latency
- Be idiomatic Python (use type hints, docstrings)

```python
# Your rewrite here:
```

---

### Exercise 8

**Difficulty:** Hard
**Objective:** Design the right architecture for a given scenario

You are the first engineer at a new healthcare startup. The product is a platform for scheduling medical appointments (patients book appointments with doctors). The MVP needs: patient registration, doctor availability, appointment booking, email confirmation, and billing.

The CTO wants to start with microservices because "that's what Netflix uses". Write a 300-word technical memo to the CTO explaining:
1. Why starting with microservices is likely the wrong choice at this stage
2. What architecture you recommend instead, and why
3. What specific signals or thresholds would change your recommendation (when microservices become appropriate)
4. One concrete risk of following the CTO's recommendation that the CTO may not have considered

```markdown
Your memo:
[Write here]
```

---

## Expert Exercise (9)

### Exercise 9

**Difficulty:** Expert
**Objective:** Reason from first principles about a novel distributed systems scenario

A financial trading platform needs to process stock trade orders. The requirements:
- Each trade must be processed exactly once (duplicate trades cause financial loss)
- The system must acknowledge each trade within 5ms (regulatory requirement)
- During network partitions, the system must remain available (trades must not be refused)
- All trades must be consistent across regions for auditing (regulators require a complete, consistent ledger)

1. Identify the CAP conflict in these requirements. Which two requirements are fundamentally at odds with each other?
2. This is a real problem faced by financial systems. Describe two real-world approaches that industry uses to navigate this contradiction (you may research this — cite your source).
3. Design a system that satisfies the 5ms latency requirement and the "exactly once" requirement, while being explicit about which CAP guarantee you are giving up and how you handle that trade-off operationally.
4. What does the PACELC model add to your analysis that CAP alone doesn't capture?

```markdown
Your analysis:
[Write here]
```
