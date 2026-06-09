# Module 02: Messaging and Queues

[← Module 01: Introduction](../01_introduction/README.md) | [Topic Home](../../README.md) | [Next → Module 03: Async Patterns](../03_async-patterns/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-blue)
![Time](https://img.shields.io/badge/time-8h-orange)

> Message brokers, publish/subscribe patterns, delivery semantics, and the operational realities of Kafka and RabbitMQ in production systems.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

---

## Overview

Asynchronous communication, introduced in Module 01 as a concept, requires infrastructure to implement: message brokers. A message broker is a middleware component that accepts messages from producers, stores them reliably, and delivers them to consumers. This decoupling is the architectural foundation for event-driven systems, reliable background processing, and systems that must handle bursty load without falling over.

This module covers the two most common message broker families: Apache Kafka (a distributed log optimized for high-throughput event streaming) and RabbitMQ (a traditional message broker optimized for flexible routing and workload distribution). Understanding when to use each, and understanding the fundamental concepts they share (delivery semantics, consumer groups, dead-letter queues), is essential for any engineer building distributed systems.

The most important concept in this module is **delivery semantics**: the contract between the broker and the consumer regarding how many times a message will be delivered. Getting this wrong causes either lost messages (at-most-once, bad for financial events) or duplicate processing (at-least-once without idempotent consumers, bad for charge operations). Understanding the three delivery semantic tiers — and how to achieve each in practice — is a foundational distributed systems skill.

---

## Prerequisites

- Module 01: Introduction to Distributed Systems — specifically: synchronous vs. asynchronous communication, the concept of temporal decoupling
- Basic understanding of HTTP and network calls — see [[networks]]
- Basic Python programming

---

## Objectives

By the end of this module, you will be able to:

1. Explain the difference between point-to-point (queue) and publish/subscribe (topic) messaging patterns
2. Describe the three delivery semantics (at-most-once, at-least-once, exactly-once) and implement each in Python using a message broker
3. Design a Kafka topic topology for a given event-driven system, including partitioning strategy and consumer group design
4. Configure a dead-letter queue and explain its role in resilient message processing
5. Compare Kafka and RabbitMQ, selecting the appropriate one for a given use case
6. Implement an idempotent consumer that handles at-least-once delivery safely

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be written in a subsequent pass.
> The Objectives above define the scope. The Key Concepts below provide a vocabulary reference.

### Core Concepts to Cover

**What is a Message Broker?**
A message broker is a component that mediates communication between producers and consumers. Unlike direct HTTP calls, a broker decouples the producer and consumer in time (the consumer doesn't need to be running when the producer sends), in space (producer doesn't need to know consumer's address), and in synchrony (producer doesn't wait for consumer to process).

**Point-to-Point vs. Publish/Subscribe:**
- Point-to-point (queue): one message is consumed by exactly one consumer. Used for workload distribution (multiple workers competing for jobs).
- Publish/subscribe (topic): one message is delivered to all subscribers. Used for event notification (multiple services reacting to the same event).

**The Three Delivery Semantics:**
- At-most-once: messages may be lost but are never delivered twice. Fast but lossy. Acceptable for metrics and non-critical logs.
- At-least-once: messages are never lost but may be delivered more than once. Requires idempotent consumers. Default for most production event systems.
- Exactly-once: messages are delivered exactly once. Hardest to achieve; often implemented as at-least-once + idempotent consumers, not true transport-level exactly-once.

**Kafka Architecture:**
Kafka is a distributed commit log. Topics are divided into partitions. Messages within a partition are ordered; messages across partitions are not. Consumer groups allow horizontal scaling — Kafka guarantees each partition is consumed by exactly one consumer within a group at a time. Offsets track consumer position.

```yaml
# Kafka topic configuration example
# 3 partitions, replication factor 3 (production minimum)
kafka-topic-config:
  name: order-events
  partitions: 3
  replication-factor: 3
  retention.ms: 604800000  # 7 days
  cleanup.policy: delete
```

**RabbitMQ Architecture:**
RabbitMQ uses an exchange-queue-binding model. Producers publish to exchanges; exchanges route messages to queues based on routing rules (direct, topic, fanout, headers). Consumers subscribe to queues. More flexible routing than Kafka but less suited to high-throughput event replay.

**Dead-Letter Queues (DLQ):**
When a message cannot be processed successfully (and all retries are exhausted), it is moved to a dead-letter queue for manual inspection or automated alerting. DLQs prevent bad messages from blocking the main queue indefinitely.

**Consumer Groups:**
In Kafka, a consumer group is a logical grouping of consumers that cooperatively consume a topic. Each partition is assigned to exactly one consumer in the group. Adding consumers to a group scales consumption horizontally. Multiple groups reading the same topic receive independent copies of every message.

---

## Key Concepts

**Message broker:** Middleware that accepts, stores, and delivers messages between producers and consumers. Provides temporal decoupling. Examples: Kafka, RabbitMQ, AWS SQS, Google Pub/Sub.

**Topic/Queue:** The logical channel through which messages flow. Kafka uses "topics"; RabbitMQ uses "queues" (with exchanges routing to queues).

**Partition:** In Kafka, a topic is divided into ordered, append-only partitions. Partitioning enables horizontal scaling and preserves ordering within a partition. Partition key (usually a hash of a business ID) determines which partition a message goes to.

**Consumer group:** A named group of consumers sharing the work of consuming a topic. Kafka assigns each partition to one consumer per group. Adding consumers to a group scales throughput.

**Offset:** An integer representing a consumer's position in a partition log. Consumers commit their offset after processing a message. On restart, consumption resumes from the last committed offset.

**Dead-letter queue (DLQ):** A separate queue to which unprocessable messages are moved after exhausting retry attempts. Prevents poison messages from blocking processing indefinitely.

**Idempotent consumer:** A consumer that produces the same outcome regardless of how many times it processes the same message. Required when using at-least-once delivery. Typically implemented using an idempotency key stored in a database.

**Backpressure:** When consumers cannot keep up with producers, a mechanism (queue filling, producer throttling, or rejection) that signals the system is overloaded. Proper backpressure handling prevents memory overflow and cascade failures.

---

## Examples

> Full worked examples to be written. Planned examples:
> 1. Kafka producer/consumer in Python (confluent-kafka library)
> 2. RabbitMQ fanout exchange for event fan-out
> 3. Idempotent consumer implementation with PostgreSQL deduplication table
> 4. Dead-letter queue configuration and handling

```python
# Preview: Kafka producer with at-least-once delivery
from confluent_kafka import Producer

producer = Producer({
    'bootstrap.servers': 'localhost:9092',
    'acks': 'all',           # wait for all in-sync replicas to acknowledge
    'retries': 5,            # retry on transient failure
    'enable.idempotence': True  # prevent duplicate messages from producer
})

def delivery_report(err, msg):
    """Callback called for every message produced."""
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}')

producer.produce(
    topic='order-events',
    key=str(order_id).encode(),    # partition key: same order always goes to same partition
    value=order_event_json.encode(),
    callback=delivery_report
)
producer.flush()  # wait for all messages to be delivered
```

---

## Common Pitfalls

**Pitfall 1: Committing offsets before processing.**
Committing the Kafka offset before the message is fully processed means that if the consumer crashes mid-processing, the message is considered "done" and is never retried. This causes silent data loss.

**Wrong:** Commit offset, then process message.
**Right:** Process message successfully, then commit offset.

**Pitfall 2: Non-idempotent consumers with at-least-once delivery.**
Using at-least-once delivery (the default) with a consumer that charges a credit card on every message will charge the card multiple times if the message is redelivered. Every consumer receiving financial or state-changing messages must be idempotent.

**Pitfall 3: Ignoring consumer lag.**
Consumer lag (the difference between the latest offset and the committed offset) is the primary health signal for a Kafka consumer. A growing lag means consumers are falling behind producers. If not monitored, this leads to unbounded queue growth and eventually OOM or data loss when retention expires.

---

## Cross-Links

- [[systems-architecture/modules/01_introduction]] — Synchronous vs. asynchronous communication; the motivation for message brokers
- [[systems-architecture/modules/03_async-patterns]] — The Saga and Outbox patterns that use message brokers as infrastructure
- [[systems-architecture/modules/06_data-consistency]] — The dual-write problem that the Outbox Pattern solves using a message broker
- [[devops-platform-engineering]] — Kafka cluster deployment, consumer lag monitoring, and broker operations

---

## Summary

- Message brokers provide temporal, spatial, and synchronous decoupling between producers and consumers.
- Point-to-point queues distribute work; publish/subscribe topics fan out events.
- Kafka is a distributed log optimized for high-throughput, ordered event streaming with replay capability.
- RabbitMQ is a traditional broker optimized for flexible routing, acknowledgment-based delivery, and per-message TTL.
- At-most-once: lossy, fast. At-least-once: reliable, requires idempotent consumers. Exactly-once: hardest, often achieved as at-least-once + idempotent consumer.
- Consumer groups enable horizontal scaling in Kafka; each partition is consumed by one consumer per group.
- Idempotent consumers and dead-letter queues are required for production-grade message processing.
