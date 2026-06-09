# Test: Module 02 — Messaging and Queues

**Instructions:** Answer all questions. Write your answers directly below each question.

**Total Points:** 37 pts (Easy: 5 + Medium: 10 + Hard: 12 + Expert: 10)
**Bonus Available:** 5 pts

> [!NOTE]
> This test will be expanded when Module 02 README is written in full.
> The questions below are placeholders indicating coverage areas.

---

## Section 1: Easy Questions (1 pt each)

**Q1.** What is the difference between a point-to-point queue and a publish/subscribe topic?

> Answer:

**Q2.** Name the three delivery semantic tiers.

> Answer:

**Q3.** What is a dead-letter queue?

> Answer:

**Q4.** In Kafka, what does "consumer lag" mean?

> Answer:

**Q5.** What is a Kafka partition and why does it matter for ordering guarantees?

> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Why must consumers using at-least-once delivery be idempotent?

> Answer:

**Q7.** Explain the trade-off between Kafka and RabbitMQ. When would you choose each?

> Answer:

**Q8.** Describe how Kafka consumer groups enable horizontal scaling.

> Answer:

**Q9.** What happens to offset commits if a consumer crashes before committing?

> Answer:

**Q10.** Explain why committing an offset before processing a message is dangerous.

> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** Design a Kafka topology (topics, partitions, consumer groups) for an order fulfillment system with: Order Service (producer), Inventory Service (consumer), Payment Service (consumer), Notification Service (consumer). Each service must process every order independently.

> Answer:

**Q12.** Write a Python implementation of an idempotent Kafka consumer using a PostgreSQL deduplication table.



> Answer:

**Q13.** Debug: A consumer is processing messages correctly but the same message keeps appearing. What are the possible causes and how would you diagnose each?

> Answer:

**Q14.** Design a dead-letter queue strategy for a payment processing consumer that processes Stripe webhooks.

> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** Design a globally distributed event streaming architecture for a system with producers in 3 regions and consumers that need to process events from all regions in order. Explain the trade-offs you make.

> Answer:

**Q16.** Exactly-once delivery in Kafka is described as "at-least-once delivery + idempotent consumers". Explain why this is the practical implementation approach rather than true transport-level exactly-once, and under what conditions even this approach breaks down.

> Answer:

---

## Bonus

**Bonus 1.** (+5 pts) Kafka Streams and Apache Flink are both used for stream processing. Compare them: what problem does each solve, when would you choose one over the other, and what is the key architectural difference?

> Answer:
