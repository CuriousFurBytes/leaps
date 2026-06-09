# Module 12: Capstone API Platform

> Build a production-style API platform that exposes both REST and GraphQL interfaces over the same domain.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Project Brief](#project-brief)
5. [Milestones](#milestones)
6. [Help and Getting Unstuck](#help-and-getting-unstuck)
7. [Acceptance Criteria](#acceptance-criteria)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

## Overview

The capstone is build-oriented. You will design an API platform for a realistic content marketplace with users, articles, comments, purchases, and moderation workflows. The platform must expose a REST API for integration partners and a GraphQL API for a rich client application.

Do not hand yourself a copy-paste solution. The point is to make architectural decisions, record tradeoffs, test behavior, and discover where REST and GraphQL complement or complicate each other.

## Prerequisites

- Modules 01 through 11 in this topic.
- Practical comfort with HTTP, REST resources, GraphQL schemas, authorization, pagination, caching, and observability.
- Familiarity with [[databases]], [[security]], and [[software-architecture]].

## Objectives

By the end of this module, you will be able to:

- Design REST resources and GraphQL types for the same domain model.
- Implement consistent authentication, authorization, validation, and error semantics.
- Compare caching, pagination, and observability strategies across both API styles.
- Write contract tests and operational runbooks for an API platform.
- Defend architectural tradeoffs in a concise design review.

## Project Brief

Build an API platform for a content marketplace. Authors publish articles, readers purchase premium access, moderators review flagged comments, and partner systems need stable REST integrations. The frontend product team needs GraphQL for flexible article pages and dashboards.

```text
Required domain objects:
- User
- Article
- Comment
- Purchase
- ModerationCase
```

```yaml
required_interfaces:
  rest:
    - GET /articles
    - GET /articles/{id}
    - POST /articles
    - PATCH /articles/{id}
    - POST /articles/{id}/comments
  graphql:
    - Query.article
    - Query.articles
    - Mutation.createArticle
    - Mutation.addComment
    - Mutation.openModerationCase
```

```graphql
type Article {
  id: ID!
  title: String!
  body: String!
  author: User!
  comments(first: Int!, after: String): CommentConnection!
}
```

## Milestones

1. Model the domain and write a one-page API decision record.
2. Design REST endpoints with representations, status codes, error bodies, and pagination.
3. Design the GraphQL schema with queries, mutations, connection pagination, and typed errors where appropriate.
4. Implement or pseudocode handlers and resolvers for the core flows.
5. Add authentication and authorization rules for authors, readers, moderators, and partners.
6. Add contract tests for REST and schema/operation tests for GraphQL.
7. Add observability: structured logs, request IDs, metrics, and example dashboard questions.
8. Present a final tradeoff review explaining what each interface is best for.

## Help and Getting Unstuck

### Hint 1: Start with Invariants

Write rules before endpoints. For example: only authors can edit their own drafts, only moderators can close moderation cases, and premium body text requires a purchase.

### Hint 2: Separate Resource Identity from View Shape

A REST article URL should remain stable even if clients need different views. GraphQL field selection can vary per screen, but resolvers still need authorization and cost controls.

### Hint 3: Test the Contract, Not Just the Code

```bash
# Example smoke checks to adapt to your stack.
curl -i http://localhost:3000/articles
curl -i -X POST http://localhost:3000/articles -H "Content-Type: application/json" -d '{"title":"Draft"}'
```

### Hint 4: Watch for N+1 and Overfetching

```graphql
query Dashboard {
  articles(first: 20) {
    edges {
      node {
        title
        author { name }
        comments(first: 5) { edges { node { body } } }
      }
    }
  }
}
```

If this query causes one database query per article or per comment, introduce batching, preloading, or query planning.

## Acceptance Criteria

- REST and GraphQL interfaces cover the required use cases.
- Every operation documents authorization, validation, success responses, and error responses.
- Pagination is stable and explained.
- At least one caching strategy is implemented or justified for each API style.
- Tests demonstrate happy paths, validation failures, authorization failures, and compatibility expectations.
- A final design review compares the two styles without declaring a universal winner.

## Cross-Links

- [[graphql-rest#module-map]]
- [[databases]]
- [[security]]
- [[software-architecture]]

## Summary

- The capstone turns theory into a realistic, reviewable API platform.
- REST is used where stable partner integrations and HTTP semantics are valuable.
- GraphQL is used where client-selected graph traversal improves product iteration.
- Security, performance, testing, and observability are first-class requirements.
- Your final artifact should show judgment, not just feature coverage.
