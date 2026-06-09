# Answers: Module 01 — Introduction to Distributed Systems

## Answer Key

### Easy Questions

**Q1:** Any four of: (1) The network is reliable, (2) Latency is zero, (3) Bandwidth is infinite, (4) The network is secure, (5) Topology doesn't change, (6) There is one administrator, (7) Transport cost is zero, (8) The network is homogeneous.

**Q2:** Consistency — every read returns the most recent write or an error; Availability — every request receives a non-error response; Partition Tolerance — the system continues operating when network messages between nodes are lost or delayed.

**Q3:** A network partition is a failure state in which a subset of nodes in a distributed system cannot communicate with other nodes due to a network failure, effectively splitting the network into isolated groups.

**Q4:** Synchronous communication requires the caller to wait (block) for the callee's response before continuing; asynchronous communication allows the caller to continue immediately after sending a message without waiting for a response.

**Q5:** False. A single-node PostgreSQL is not partition-tolerant because partition tolerance requires multiple nodes — a single-node system cannot be partitioned. It is technically a CA system but this is somewhat academic since "CA" means the system simply doesn't distribute, not that it achieves both C and A in a partition scenario.

### Medium Questions

**Q6:** In a real distributed system, you cannot sacrifice P (Partition Tolerance) because networks *will* partition — cables fail, switches reboot, network links drop. A system that is not partition-tolerant would have to stop operating entirely when any network issue occurs, which is unacceptable for production systems. Therefore, P is a non-negotiable baseline, and the real design decision is: when a partition occurs, do you favor C (refuse requests to stay consistent) or A (serve requests with potentially stale data)?

**Q7:** At 4 engineers and 3 months, the team does not yet have stable domain boundaries (requirements are still changing), no operational expertise with service mesh or distributed tracing, no deployment automation mature enough for 12 services, and no organizational structure aligned with service ownership. Decomposing at this stage will create the wrong boundaries and a distributed monolith. Recommendation: build a well-structured modular monolith with clear module interfaces. Extract services later, one at a time, when specific scaling or compliance reasons emerge.

**Q8:** A distributed monolith is a system that has been split into multiple network-separated processes but maintains tight coupling between them — typically through a shared database, synchronous call chains, or coordinated deployment schedules. It is worse than a proper monolith because it adds network overhead, distributed failure modes, and operational complexity while providing none of the benefits of microservices (independent deployability, independent scaling, team autonomy). It is worse than proper microservices because the coupling prevents the services from being changed, scaled, or deployed independently.

**Q9:** For independent services with p99=50ms each, the approximate p99 for a sequential chain of 5 is near 250ms (5 × 50ms) because for the combined request to be at p99, each service needs to be near its own p99. More precisely, the probability that all 5 are fast is: (0.99)^5 = 0.951, meaning ~5% of requests will see at least one service hit p99, giving an effective combined p99 significantly higher than a single service's p99. This is the "tail latency amplification" problem.

**Q10:** No — a timeout does not definitively mean the payment was not processed. Possible scenarios: (a) the payment succeeded but the response was lost in transit, (b) the payment service received the request, began processing, and the connection dropped before completion, (c) the payment service never received the request. The correct handling is to use an idempotency key with the original request, and on timeout, retry with the same idempotency key. The payment service, if it processed the original, returns the original result. If it didn't, it processes now.

### Hard Questions

**Q11:** Problems: (1) No timeout — `requests.get` will wait indefinitely if the server hangs, blocking the caller thread forever (violates Fallacy 1: network is reliable); (2) No error handling — `resp.json()` will raise an exception if the response is not JSON (e.g., 502 Bad Gateway returns HTML), crashing the caller; (3) No HTTP status check — `resp.json()` is called even if `resp.status_code` is 500 or 404, which may return an error body that doesn't contain `recommendations`; (4) KeyError on `data["recommendations"]` — if the response body doesn't have this key (e.g., error response), this crashes with an unhelpful KeyError. Additional: no retry logic for transient failures, no logging.

**Q12:** (1) Reserve inventory — sync: the checkout cannot proceed without knowing inventory is reserved; a user who attempts to buy an out-of-stock item must know immediately. (2) Process payment — sync: cannot confirm the order without knowing the payment succeeded; failure must be surfaced to the user immediately. (3) Confirm order — sync: need to return order confirmation number to the user in the same response. (4) Send confirmation email — async: the user does not need to wait for email delivery; the email can be sent in the background; failure to send email should not block or roll back the checkout; emails can be retried independently.

**Q13:** Full credit for an implementation that demonstrates at least 4 of: `timeout=` parameter on the request, exponential backoff with jitter on retry, idempotency key in request headers, distinguishing 4xx (permanent, don't retry) from 5xx (transient, retry), and structured log output with at least 3 fields (url, status_code, attempt_number). See README Examples section for a reference implementation.

**Q14:** PA/EL for DynamoDB means: During a **P**artition, DynamoDB favors **A**vailability (it accepts reads and writes even if some replicas are unreachable, returning stale data rather than refusing). During normal (**E**lse) operation, DynamoDB favors low **L**atency over strong Consistency — by default, reads are served from any replica (eventual consistency) rather than always hitting the primary. Observable example: a developer writes `item.counter = 100` then immediately reads it back — with the default eventually consistent read, they may get the old value (e.g., 99) for a brief window. With a strongly consistent read (`ConsistentRead=True`), they always get 100 but with higher latency.

### Expert Questions

**Q15:** Full credit requires: (a) Player's own score: CP component — use a per-player replica or shard that is strongly consistent for that player; the player can only see their own data so there's no cross-player consistency issue; (b) Global leaderboard: AP component — use Cassandra or a Redis sorted set with eventual consistency; 30-second staleness is acceptable, so AP is fine; (c) During partition: AP for the leaderboard, CP for the score tracking within the partitioned region (players can still score but the global leaderboard won't be updated until the partition heals). Architecture must explicitly name the CAP classification of each component and acknowledge that the system is not globally CP or globally AP but a mix.

**Q16:** Full credit for a coherent synthesis that includes: (1) The 8 Fallacies as the foundation — distribution adds failure modes that don't exist locally, so the default assumption must be "distribution is expensive"; (2) CAP theorem as a design constraint — consistency vs. availability is not a choice you make once but a per-component decision based on business requirements; (3) Monolith by default, microservices by justification — starting distributed before problems demand it creates distributed monoliths and premature complexity; (4) The recommendation: start with the simplest architecture that works (often a modular monolith), and introduce distribution only when specific scaling, compliance, or team autonomy requirements emerge.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
