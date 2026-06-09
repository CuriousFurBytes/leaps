# Exercises — Module 01: Introduction to PostgreSQL

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Actually type the SQL and run it — don't just read it mentally.
3. **Check your answer** against the acceptance criteria.
4. **Score yourself honestly** in the [Scoring Log](#scoring-log) at the bottom.
5. If you're stuck after a genuine effort, use the hints one at a time — not all at once.

---

## Difficulty Legend

| Symbol | Difficulty | Expected Time | Points |
|--------|-----------|--------------|--------|
| 🟢 Easy | Recall and basic application | 5–10 min | 1 pt |
| 🟡 Medium | Requires combining 2+ concepts | 15–25 min | 2 pts |
| 🔴 Hard | Multi-step, requires real problem-solving | 30–60 min | 3 pts |
| ⭐ Challenge | Open-ended; more than one good answer | 60+ min | 5 pts |

---

## Exercise 1: Create a Movies Table [🟢 Easy] [1 pt]

### Context
You are building a movie database. This exercise focuses on creating a table with appropriate data types and constraints.

### Task
Create a table called `movies` with the following columns:
- `id` — auto-incrementing primary key
- `title` — required, no length limit
- `director` — required, no length limit
- `release_year` — optional integer
- `rating` — decimal rating from 0.0 to 10.0 (optional, but must be in that range if provided)
- `in_theaters` — boolean, defaults to false
- `added_at` — timestamp with timezone, defaults to current time

### Requirements
- [ ] Table is named exactly `movies`
- [ ] `id` auto-increments and is the primary key
- [ ] `title` and `director` cannot be NULL
- [ ] `rating` has a CHECK constraint enforcing 0.0–10.0 range
- [ ] `in_theaters` defaults to false
- [ ] `added_at` defaults to now()

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

Use `SERIAL` or `BIGSERIAL` for the auto-incrementing primary key. Use `NUMERIC(4,1)` for the rating — it stores up to 9999.9, but a CHECK constraint will restrict it to 0.0–10.0.

</details>

<details>
<summary>Hint 2 (only if Hint 1 wasn't enough)</summary>

```sql
rating NUMERIC(4,1) CHECK (rating >= 0.0 AND rating <= 10.0)
```

</details>

### Expected Output / Acceptance Criteria
After creating the table, `\d movies` should show all 7 columns with their types and constraints.

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```sql
CREATE TABLE movies (
    id           BIGSERIAL    PRIMARY KEY,
    title        TEXT         NOT NULL,
    director     TEXT         NOT NULL,
    release_year INTEGER,
    rating       NUMERIC(4,1) CHECK (rating >= 0.0 AND rating <= 10.0),
    in_theaters  BOOLEAN      NOT NULL DEFAULT false,
    added_at     TIMESTAMPTZ  NOT NULL DEFAULT now()
);
```

**Explanation:**
`BIGSERIAL` is used instead of `SERIAL` because it uses a 64-bit integer — a good habit for production tables. `NUMERIC(4,1)` means "up to 4 digits total, 1 after the decimal point." The CHECK constraint is applied inline. `in_theaters` is `NOT NULL DEFAULT false` — it has a meaningful default but is always required to have some value.

**Common wrong answers and why they fail:**
- Using `FLOAT` for rating — FLOAT is approximate and can produce unexpected values like 7.99999; use NUMERIC for ratings
- Using `TIMESTAMP` instead of `TIMESTAMPTZ` — loses timezone context, causes bugs in multi-timezone environments

</details>

---

## Exercise 2: Insert and Query Movies [🟢 Easy] [1 pt]

### Context
Building on Exercise 1's `movies` table.

### Task
Insert at least 4 movies into the table, then write two SELECT queries:
1. All movies released before 2000
2. All movies with a rating above 8.0, sorted by rating descending

### Requirements
- [ ] At least 4 rows inserted, with varied years and ratings
- [ ] Query 1 uses a WHERE clause filtering on `release_year`
- [ ] Query 2 uses WHERE and ORDER BY
- [ ] At least one movie has no rating (NULL)

### Hints
<details>
<summary>Hint 1</summary>

For a movie with no rating, simply omit the `rating` column from your INSERT, or include it with the explicit value `NULL`.

</details>

### Expected Output / Acceptance Criteria
Query 2 should return only movies with rating > 8.0, sorted highest first.

### Solution
<details>
<summary>Show Solution</summary>

```sql
INSERT INTO movies (title, director, release_year, rating, in_theaters) VALUES
    ('Blade Runner', 'Ridley Scott', 1982, 8.1, false),
    ('Inception', 'Christopher Nolan', 2010, 8.8, false),
    ('The Shawshank Redemption', 'Frank Darabont', 1994, 9.3, false),
    ('Parasite', 'Bong Joon-ho', 2019, 8.5, true),
    ('Nosferatu', 'F.W. Murnau', 1922, NULL, false);  -- no rating for this one

-- Query 1: Movies before 2000
SELECT title, director, release_year
  FROM movies
 WHERE release_year < 2000
 ORDER BY release_year;

-- Query 2: Highly rated movies
SELECT title, rating
  FROM movies
 WHERE rating > 8.0
 ORDER BY rating DESC;
```

**Explanation:**
NULL is inserted for Nosferatu's rating by simply not including it (or writing `NULL` explicitly). The WHERE clause `rating > 8.0` automatically excludes NULL rows — comparisons with NULL return NULL, which is falsy in a WHERE condition.

</details>

---

## Exercise 3: Finding NULL Values and Updating Data [🟡 Medium] [2 pts]

### Context
You have a movies table with some rows missing ratings. This exercise requires combining NULL detection, filtering, and targeted updates.

### Task
1. Write a query that finds all movies with a NULL rating.
2. Update `Nosferatu`'s rating to 7.9 and verify the change.
3. Write a query that finds all movies where `release_year` is NULL OR rating is NULL (using OR in the WHERE clause).

### Requirements
- [ ] Query 1 uses `IS NULL` (not `= NULL`)
- [ ] UPDATE targets only the correct row (use `title = 'Nosferatu'` in WHERE)
- [ ] Query 3 uses OR to combine two NULL checks
- [ ] All three parts produce correct results

### Hints
<details>
<summary>Hint 1</summary>

Remember: `WHERE rating = NULL` will never match any rows. You must use `WHERE rating IS NULL`.

</details>

<details>
<summary>Hint 2</summary>

For the combined query in part 3: `WHERE condition1 OR condition2` — each condition can be a separate IS NULL check.

</details>

### Expected Output / Acceptance Criteria
After the UPDATE, a SELECT on Nosferatu should show rating = 7.9. Query 3 should return any movies missing either field.

```
Expected for Query 1 (before update):
 title
-----------
 Nosferatu
```

### Solution
<details>
<summary>Show Solution</summary>

```sql
-- Part 1: Find movies with no rating
SELECT title, release_year, rating
  FROM movies
 WHERE rating IS NULL;

-- Part 2: Update Nosferatu's rating
UPDATE movies
   SET rating = 7.9
 WHERE title = 'Nosferatu'
RETURNING title, rating;  -- verify what was changed

-- Part 3: Movies missing year OR rating
SELECT title, release_year, rating
  FROM movies
 WHERE release_year IS NULL
    OR rating IS NULL;
```

**Explanation:**
`IS NULL` is the only correct way to test for NULL. The `RETURNING` clause after the UPDATE confirms what was changed without needing a separate SELECT. The OR condition in part 3 returns rows matching either (or both) conditions.

**Alternative approaches:**
`COALESCE(rating, 0)` would treat NULL as 0 in expressions, but `IS NULL` is the right tool for testing the absence of a value.

</details>

---

## Exercise 4: Aggregating Data [🟡 Medium] [2 pts]

### Context
Aggregation queries (COUNT, AVG, MIN, MAX, GROUP BY) are essential for answering "how many" and "what's the average" questions. This exercise practices combining aggregation with filtering.

### Task
Using the `movies` table, write the following queries:
1. Count the total number of movies in the table.
2. Find the average rating across all movies that **have** a rating (exclude NULLs).
3. Find the movie with the highest rating — return its title and rating.
4. Count movies by decade (1920s, 1980s, 1990s, 2000s, 2010s) — group by `(release_year / 10) * 10`.

### Requirements
- [ ] Query 2 uses WHERE to exclude NULL ratings before averaging
- [ ] Query 3 uses ORDER BY and LIMIT (not a subquery — that's Module 03)
- [ ] Query 4 uses GROUP BY with an arithmetic expression
- [ ] All queries return correct results

### Hints
<details>
<summary>Hint 1</summary>

For query 4, the expression `(release_year / 10) * 10` uses integer division in PostgreSQL: `1994 / 10 = 199`, then `199 * 10 = 1990`. This groups 1990–1999 together as 1990.

</details>

### Expected Output / Acceptance Criteria
```
-- Query 4 expected output (approximately):
 decade | count
--------+-------
   1920 |     1
   1980 |     1
   1990 |     1
   2010 |     2
```

### Solution
<details>
<summary>Show Solution</summary>

```sql
-- Query 1: Total count
SELECT COUNT(*) AS total_movies FROM movies;

-- Query 2: Average rating (exclude NULLs using WHERE)
SELECT AVG(rating)::NUMERIC(4,2) AS avg_rating
  FROM movies
 WHERE rating IS NOT NULL;
-- Note: AVG() also ignores NULLs automatically, but explicit WHERE is clearer

-- Query 3: Highest-rated movie
SELECT title, rating
  FROM movies
 WHERE rating IS NOT NULL
 ORDER BY rating DESC
 LIMIT 1;

-- Query 4: Count by decade
SELECT (release_year / 10) * 10 AS decade,
       COUNT(*) AS movie_count
  FROM movies
 WHERE release_year IS NOT NULL
 GROUP BY decade
 ORDER BY decade;
```

**Explanation:**
`COUNT(*)` counts all rows including NULLs. `COUNT(column)` counts only non-NULL values. `AVG()` ignores NULL by definition. The integer arithmetic in query 4 is a useful technique for bucketing continuous values into ranges.

</details>

---

## Exercise 5: Schema Design — A Recipe Database [🔴 Hard] [3 pts]

### Context
This is a multi-step problem that requires designing a schema and then populating and querying it. You may need to design your solution before writing it — that design process is part of the exercise.

### Task
Design and create a schema for a recipe database with these entities:
- **recipes**: name, description, prep_time (minutes), cook_time (minutes), servings, difficulty (easy/medium/hard), created_at
- **ingredients**: name, unit (e.g., 'cup', 'gram', 'piece')
- **recipe_ingredients**: links recipes to ingredients with a quantity (use NUMERIC)

Then:
1. Insert at least 2 recipes and 5 ingredients, with each recipe using at least 3 ingredients.
2. Write a query that returns all ingredients for a specific recipe, including their quantities and units.
3. Write a query that finds all recipes that use a specific ingredient (by ingredient name).

### Requirements
- [ ] Three tables with appropriate primary keys
- [ ] `recipe_ingredients` has foreign keys to both `recipes` and `ingredients`
- [ ] `difficulty` is constrained to only 'easy', 'medium', or 'hard' (use CHECK)
- [ ] Query 2 uses a JOIN between recipe_ingredients and ingredients
- [ ] Query 3 uses a JOIN and WHERE on the ingredient name
- [ ] All tables and queries work correctly

### Hints
<details>
<summary>Hint 1 (structural hint)</summary>

The `recipe_ingredients` table is a **junction table** (also called a join table or bridge table) for a many-to-many relationship: one recipe uses many ingredients, and one ingredient can be used in many recipes. It needs foreign keys to both `recipes.id` and `ingredients.id`, plus a `quantity` column.

</details>

<details>
<summary>Hint 2 (SQL hint)</summary>

For query 2, you need to JOIN `recipe_ingredients` with `ingredients`:
```sql
SELECT i.name, ri.quantity, i.unit
  FROM recipe_ingredients ri
  JOIN ingredients i ON ri.ingredient_id = i.id
 WHERE ri.recipe_id = ?;
```

</details>

<details>
<summary>Hint 3 (near-solution hint)</summary>

For query 3 (recipes that use a specific ingredient), you need to go through the junction table:
```sql
SELECT r.name
  FROM recipes r
  JOIN recipe_ingredients ri ON ri.recipe_id = r.id
  JOIN ingredients i ON i.id = ri.ingredient_id
 WHERE i.name = 'flour';
```

</details>

### Expected Output / Acceptance Criteria
- `\d recipe_ingredients` shows two foreign key constraints
- Query 2 returns ingredient rows for one recipe (at least 3 rows)
- Query 3 returns recipe names that use the queried ingredient

### Solution
<details>
<summary>Show Solution</summary>

```sql
-- Step 1: Create tables
CREATE TABLE recipes (
    id          BIGSERIAL PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    description TEXT,
    prep_time   INTEGER CHECK (prep_time >= 0),   -- minutes
    cook_time   INTEGER CHECK (cook_time >= 0),   -- minutes
    servings    INTEGER CHECK (servings > 0),
    difficulty  TEXT NOT NULL DEFAULT 'medium'
                CHECK (difficulty IN ('easy', 'medium', 'hard')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE ingredients (
    id   BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    unit TEXT NOT NULL  -- e.g., 'cup', 'gram', 'whole', 'tbsp'
);

CREATE TABLE recipe_ingredients (
    recipe_id     BIGINT  NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    ingredient_id BIGINT  NOT NULL REFERENCES ingredients(id),
    quantity      NUMERIC(8, 2) NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (recipe_id, ingredient_id)  -- composite PK prevents duplicates
);

-- Step 2: Insert data
INSERT INTO recipes (name, description, prep_time, cook_time, servings, difficulty)
VALUES
    ('Simple Pancakes', 'Fluffy weekend pancakes', 10, 20, 4, 'easy'),
    ('Chocolate Chip Cookies', 'Classic chewy cookies', 15, 12, 24, 'easy');

INSERT INTO ingredients (name, unit) VALUES
    ('flour', 'cup'),
    ('sugar', 'cup'),
    ('butter', 'cup'),
    ('egg', 'whole'),
    ('milk', 'cup'),
    ('baking powder', 'tsp'),
    ('chocolate chips', 'cup');

-- Step 3: Link recipes to ingredients
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
    (1, 1, 1.5),  -- pancakes: 1.5 cups flour
    (1, 4, 2),    -- pancakes: 2 eggs
    (1, 5, 1.25), -- pancakes: 1.25 cups milk
    (1, 6, 2),    -- pancakes: 2 tsp baking powder
    (2, 1, 2.25), -- cookies: 2.25 cups flour
    (2, 2, 0.75), -- cookies: 0.75 cups sugar
    (2, 3, 1),    -- cookies: 1 cup butter
    (2, 4, 2),    -- cookies: 2 eggs
    (2, 7, 2);    -- cookies: 2 cups chocolate chips

-- Query 2: Ingredients for pancakes (recipe_id = 1)
SELECT i.name AS ingredient, ri.quantity, i.unit
  FROM recipe_ingredients ri
  JOIN ingredients i ON ri.ingredient_id = i.id
 WHERE ri.recipe_id = 1
 ORDER BY i.name;

-- Query 3: Recipes that use flour
SELECT r.name AS recipe
  FROM recipes r
  JOIN recipe_ingredients ri ON ri.recipe_id = r.id
  JOIN ingredients i ON i.id = ri.ingredient_id
 WHERE i.name = 'flour';
```

**Step-by-step explanation:**
1. Three tables: recipes (entity), ingredients (entity), recipe_ingredients (junction)
2. The junction table's PRIMARY KEY is composite `(recipe_id, ingredient_id)` — this prevents inserting the same ingredient twice for the same recipe
3. `ON DELETE CASCADE` on recipe_id means deleting a recipe automatically removes its ingredient links
4. Query 2 joins through the junction table to get ingredient details for one recipe
5. Query 3 joins through both junction and ingredients to find recipes by ingredient name

**Why a junction table:** Without it, you'd need to store ingredients as a comma-separated list in a TEXT column — then you couldn't efficiently search by ingredient, enforce quantity constraints, or link to a normalized ingredient record.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 | — | —/1 | — | — |
| Exercise 2 | — | —/1 | — | — |
| Exercise 3 | — | —/2 | — | — |
| Exercise 4 | — | —/2 | — | — |
| Exercise 5 | — | —/3 | — | — |
| **Total** | | **—/9** | | |

**Passing threshold:** 6/9 (67%). Aim for 8/9 (89%) before taking the test.
