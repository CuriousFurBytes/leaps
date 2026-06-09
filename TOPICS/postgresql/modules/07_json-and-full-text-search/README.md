# Module 07: JSON and Full-Text Search

[← Module 06](../06_advanced-sql/) | [Topic Home](../../README.md) | [Next → Module 08](../08_stored-procedures-and-triggers/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-red)
![Time](https://img.shields.io/badge/time-8--10h-orange)

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

PostgreSQL's JSONB type and full-text search capabilities make it a serious contender for use cases traditionally delegated to specialized databases. This module covers JSONB storage (binary JSON with indexing support), the complete set of JSONB operators and functions, GIN indexes for JSONB containment and path queries, and PostgreSQL's full-text search system: tsvectors, tsqueries, and the lexeme-based matching engine.

Understanding JSONB is increasingly important as APIs return JSON and applications need to query it at the database level — without extracting it to application code first.

> [!NOTE]
> This module stub will be expanded into a full module in a future update.

---

## Prerequisites

- [[modules/04_indexes-and-performance]] — you need to understand: GIN index type (introduced here, used heavily with JSONB and FTS)
- [[modules/02_data-types-and-schema]] — you need to understand: PostgreSQL's type system and how types affect storage

---

## Objectives

By the end of this module, you will be able to:

1. Store and query JSON data using the JSONB type and its operators (`->`, `->>`, `@>`, `?`, `#>`, `#>>`)
2. Create GIN indexes on JSONB columns and understand the difference between `jsonb_ops` and `jsonb_path_ops`
3. Update JSONB values using the `||` concatenation and `-` removal operators
4. Build a full-text search system using tsvectors, tsqueries, and ts_rank
5. Create a generated tsvector column with a GIN index for efficient full-text search
6. Combine FTS with additional filters (date ranges, categories) efficiently

---

## Theory

> [!NOTE]
> Full theory section coming in a future update. Topics will include:
>
> **JSON vs JSONB**
> - JSON: stores text as-is; no indexing; exact whitespace/order preservation
> - JSONB: binary format; faster operations; GIN-indexable; reorders keys; strips whitespace
> - When to use JSON (exact preservation needed) vs JSONB (almost always)
>
> **JSONB Operators**
> - `->` key/index access (returns JSON)
> - `->>` key/index access (returns TEXT)
> - `#>` path access (array of keys)
> - `#>>` path access as TEXT
> - `@>` containment: does the left JSONB contain the right?
> - `<@` reverse containment
> - `?` key existence
> - `?|` any key exists
> - `?&` all keys exist
>
> **JSONB Modification**
> - `||` concatenation (merge/override)
> - `-` key removal
> - `#-` path removal
> - jsonb_set() for targeted updates
> - jsonb_insert() for inserting into arrays
>
> **GIN Indexes for JSONB**
> - jsonb_ops (default): indexes every key and value; supports all operators
> - jsonb_path_ops: indexes only containment (@>); smaller; faster for @> queries
>
> **Full-Text Search**
> - tsvector: a normalized list of lexemes (word stems) with position information
> - tsquery: a search expression with AND (&), OR (|), NOT (!), phrase (@>)
> - to_tsvector(language, text): convert text to tsvector
> - to_tsquery(language, query): convert query string to tsquery
> - The @@ match operator
> - ts_rank and ts_rank_cd: relevance scoring
> - Dictionary configurations (english, simple, pg_catalog.english)
>
> **Generated Columns for FTS**
> - GENERATED ALWAYS AS ... STORED for auto-updating tsvector columns
> - GIN index on tsvector column
> - Performance: pre-computed tsvectors vs on-the-fly

---

## Key Concepts

**JSONB:** Binary JSON stored in a decomposed format that supports efficient indexing and querying. Unlike `JSON`, JSONB normalizes whitespace and key ordering, making it slightly larger on write but much faster on query.

**GIN (Generalized Inverted Index):** An index type that maps values to lists of rows containing them — like a book's index. Ideal for JSONB containment queries and full-text search where a single value (a key, a word stem) appears in many rows.

**tsvector:** A sorted list of lexemes (normalized word forms) derived from a document, with optional position and weight information. The output of `to_tsvector('english', 'Jumping foxes jump')` might be `'fox':2 'jump':1,3`.

**tsquery:** A search expression in the form of lexemes connected by AND (`&`), OR (`|`), NOT (`!`), and phrase operators. The output of `to_tsquery('english', 'jump & fox')` matches documents containing both stems.

**Lexeme:** A canonical word form used in full-text search. PostgreSQL normalizes words to lexemes (removing suffixes, lowercasing) so that "running," "runs," and "ran" all match a search for "run."

---

## Examples

> Full worked examples coming in a future update.
>
> Planned examples:
> - Example 1: Storing product attributes as JSONB and querying by attribute
> - Example 2: GIN index on JSONB and comparing @> vs ->> query performance
> - Example 3: Full-text search on a blog posts table with tsvector column and ranking
> - Example 4: Combining FTS with JSONB filters in a single query

---

## Common Pitfalls

> Full pitfalls section coming in a future update.
>
> Planned pitfalls:
> - Using `->>` (returns TEXT) when you need `->` (returns JSON) for further nesting
> - GIN index not used when querying with `->>` instead of `@>`
> - FTS not matching because of dictionary mismatch (index built with 'english', query uses 'simple')
> - Storing large JSONB documents when relational modeling would be cleaner

---

## Cross-Links

- [[modules/04_indexes-and-performance]] — GIN indexes are introduced here; understanding B-tree vs GIN trade-offs is essential
- [[modules/10_partitioning-and-extensions]] — pg_trgm is a related extension for fuzzy string matching
- [[modules/08_stored-procedures-and-triggers]] — triggers can auto-update tsvector columns (alternative to generated columns)
- [[django-fastapi-flask]] — Django's SearchVector and searchable JSONB fields use the mechanisms covered here

---

## Summary

> Full summary coming in a future update. Key topics covered will be:
>
> - JSON vs JSONB: storage differences and when to use each
> - JSONB operators: ->, ->>, @>, ?, || and the full set
> - GIN indexes: jsonb_ops vs jsonb_path_ops
> - Full-text search: tsvector, tsquery, @@, ts_rank
> - Generated tsvector columns with GIN indexes
> - Combining FTS with other filters
