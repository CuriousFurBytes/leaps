# Module 11: Event-Driven APIs

[← Module 10: API Gateway and Platforms](../10_api-gateway-and-platforms/README.md) | [Topic Home](../../README.md) | [Next → Module 12: Capstone Project](../12_capstone-project/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-expert-red)
![Time](https://img.shields.io/badge/time-5h-orange)

> Webhooks (delivery guarantees, retry logic, signature verification), Server-Sent Events (SSE), WebSockets vs. SSE vs. polling trade-offs, and real-time API design patterns.

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

REST and GraphQL request-response patterns work well for reading and writing data. But some
use cases require the *server* to push data to clients when events occur, without the client
polling. This module covers the three main patterns for event-driven APIs: webhooks (server calls
the client's registered URL when something happens), Server-Sent Events (server streams events
to the client over HTTP), and WebSockets (full-duplex bidirectional communication). You will
understand the delivery guarantees, failure modes, and appropriate use cases for each.

> [!NOTE]
> This module is a stub. Full theory, examples, exercises, and test are pending.

---

## Prerequisites

- Module 02: REST Fundamentals — HTTP fundamentals (SSE is HTTP-based)
- Module 07: GraphQL Advanced — GraphQL subscriptions use WebSockets; this module provides the transport layer depth

---

## Objectives

By the end of this module, you will be able to:

1. Implement a webhook endpoint with HMAC signature verification and at-least-once delivery handling
2. Implement a Server-Sent Events (SSE) endpoint and client
3. Explain the trade-offs between polling, SSE, WebSockets, and webhooks for a given real-time use case
4. Design a webhook delivery system with retry logic and exponential backoff
5. Describe at-most-once vs. at-least-once vs. exactly-once delivery semantics

---

## Theory

> [!NOTE]
> Full theory content pending. Will cover:
> - Polling: simple but wasteful; short polling vs. long polling; when acceptable (low frequency updates)
> - Webhooks: event-to-URL delivery; HMAC-SHA256 signature verification (the `X-Hub-Signature-256` pattern); delivery guarantees (at-least-once); idempotency keys for deduplication; retry with exponential backoff; dead letter queue pattern; GitHub, Stripe, Shopify webhook examples
> - Server-Sent Events (SSE): HTTP streaming; `Content-Type: text/event-stream`; the `EventSource` API in browsers; one-directional (server → client); automatic reconnection with `Last-Event-ID`; when SSE beats WebSockets
> - WebSockets: full-duplex bidirectional; the upgrade handshake; `ws://` vs `wss://`; connection management and heartbeats; use cases (collaborative editing, live gaming, chat)
> - Comparison Matrix: polling vs. SSE vs. WebSockets vs. webhooks — directionality, overhead, browser support, infrastructure complexity

---

## Key Concepts

- **Webhook**: A callback over HTTP. When an event occurs (e.g., a payment succeeds), the server makes an HTTP POST to a URL registered by the client.
- **At-least-once delivery**: A guarantee that every event will be delivered at least once, but possibly more than once. Clients must be idempotent.
- **HMAC signature**: A cryptographic signature (using HMAC-SHA256) included with webhook payloads so the receiving server can verify the payload came from the expected sender.
- **SSE (Server-Sent Events)**: An HTTP-based unidirectional streaming protocol where the server pushes events to clients over a long-lived HTTP connection.
- **WebSocket**: A full-duplex communication protocol over a single TCP connection, upgraded from HTTP. Enables bidirectional real-time communication.
- **Long polling**: A pattern where the client makes an HTTP request and the server holds the response open until an event occurs or a timeout expires, then the client immediately makes another request.

---

## Examples

> [!NOTE]
> Full worked examples pending. Will include: webhook endpoint with HMAC verification (Python/FastAPI), SSE endpoint and client, WebSocket echo server, polling vs SSE comparison.

---

## Common Pitfalls

> [!NOTE]
> Full pitfalls section pending. Will cover: not verifying webhook signatures (allows spoofing), not handling idempotency for webhooks (duplicate processing), using WebSockets when SSE suffices (unnecessary complexity), not implementing reconnection for SSE clients.

---

## Cross-Links

- [[graphql-rest/modules/07_graphql-advanced]] — GraphQL subscriptions use the WebSocket transport covered here
- [[graphql-rest/modules/08_api-security]] — Webhook signature verification; WebSocket authentication
- [[systems-architecture]] — Event-driven architecture patterns; message queues vs. webhooks; pub/sub
- [[networks]] — TCP connections and the WebSocket upgrade handshake

---

## Summary

> [!NOTE]
> Full summary pending.
