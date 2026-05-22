# Obsidian Dataview Queries for leaps

A collection of ready-to-use [Dataview](https://github.com/blacksmithgu/obsidian-dataview) queries for building dashboards, tracking progress, and navigating the leaps knowledge base.

**Prerequisites:**
- Obsidian with the Dataview community plugin installed and enabled.
- Open the leaps root directory as your Obsidian vault.
- Frontmatter fields described in each query must exist in your notes (they are populated by the TEMPLATES/).

---

## How to Use These Queries

Copy any `dataview` or `dataviewjs` code block into any Obsidian note. Dataview evaluates the query live against all files in your vault. Paste dashboards into a dedicated note (e.g., `SHARED/dashboard.md`) for a persistent progress overview.

---

## Query 1 — All Topics with Completion Status

Lists every topic in the TOPICS directory with its current status and progress percentage.

**Frontmatter fields used:** `status`, `progress`, `difficulty`

```dataview
TABLE
  status AS "Status",
  progress AS "Progress %",
  difficulty AS "Difficulty"
FROM "TOPICS"
WHERE file.name = "README"
SORT difficulty ASC
```

**Expected output:** A table showing one row per topic, with columns for status (e.g., `in-progress`, `complete`), a numeric progress percentage, and difficulty level. Use this as your main topic overview.

---

## Query 2 — All Unanswered Questions Across Every Topic

Surfaces every question that has been logged but not yet answered, across the entire knowledge base.

**Frontmatter fields used:** `answered` (inline field inside question blocks, or a dedicated questions file per module)

```dataview
TABLE
  file.folder AS "Topic",
  file.mtime AS "Last Modified"
FROM "TOPICS"
WHERE contains(file.name, "questions") AND answered != true
SORT file.folder ASC
```

**Alternative — using inline fields inside question files:**

```dataviewjs
const pages = dv.pages('"TOPICS"').where(p => p.file.name.includes("questions"));
for (const page of pages) {
  const content = await dv.io.load(page.file.path);
  const unanswered = content
    .split("\n")
    .filter(l => l.startsWith("- [ ]") || l.match(/^Q\d+.*answered:: false/));
  if (unanswered.length > 0) {
    dv.header(4, page.file.folder + " / " + page.file.name);
    dv.list(unanswered.map(l => l.replace(/^- \[ \] /, "")));
  }
}
```

**Expected output:** A grouped list of unanswered questions, organized by topic folder. Use this for review sessions — pick a topic and answer its open questions.

---

## Query 3 — Modules Completed This Week

Shows every module whose `completed_date` falls within the current week.

**Frontmatter fields used:** `completed_date` (ISO date string, e.g., `2025-06-10`), `status`

```dataview
TABLE
  file.folder AS "Topic",
  completed_date AS "Completed",
  status AS "Status"
FROM "TOPICS"
WHERE status = "complete" AND completed_date >= date(today) - dur(7 days)
SORT completed_date DESC
```

**Expected output:** A table of recently completed modules — useful for weekly review. If nothing shows, either no modules were completed this week, or `completed_date` fields need to be populated.

---

## Query 4 — All Files That Link to a Specific Topic

Finds every note in the vault that links to a specific topic (replace `python` with any topic name).

**No special frontmatter required — uses Obsidian's link graph.**

```dataview
LIST
FROM [[python]]
SORT file.folder ASC
```

**Expected output:** A flat list of all notes that contain `[[python]]` anywhere in their body. Use this to see where a topic is referenced as a dependency or related concept across the knowledge base.

**Variant — show backlinks across SHARED concepts:**

```dataview
TABLE file.folder AS "Location", file.mtime AS "Last Modified"
FROM [[memory-management]]
SORT file.mtime DESC
```

---

## Query 5 — Test Scores Across All Modules

Aggregates grade records from every topic's `grades.md` or from frontmatter `score` fields.

**Frontmatter fields used:** `score` (number 0–100), `test_date`, `module`

```dataview
TABLE
  module AS "Module",
  score AS "Score",
  test_date AS "Date"
FROM "TOPICS"
WHERE score != null
SORT test_date DESC
```

**DataviewJS variant — compute average score per topic:**

```dataviewjs
const pages = dv.pages('"TOPICS"').where(p => p.score != null);
const byTopic = {};
for (const p of pages) {
  const topic = p.file.folder.split("/")[1] || p.file.folder;
  if (!byTopic[topic]) byTopic[topic] = [];
  byTopic[topic].push(p.score);
}
const rows = Object.entries(byTopic).map(([topic, scores]) => {
  const avg = (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1);
  return [topic, scores.length, avg + "%"];
});
dv.table(["Topic", "Tests Taken", "Average Score"], rows.sort((a, b) => b[2] - a[2]));
```

**Expected output:** A table of all recorded test scores, newest first. The DataviewJS variant groups by topic and shows averages — useful for identifying which topics need more review.

---

## Query 6 — Modules with No Exercises

Identifies modules that are missing an exercises file or have an empty exercises section — a signal that content needs to be added.

**No special frontmatter required.**

```dataviewjs
const topicFolders = dv.pages('"TOPICS"')
  .where(p => p.file.name === "README")
  .map(p => p.file.folder);

const allFiles = dv.pages('"TOPICS"').map(p => p.file.path);

const missing = [];
for (const folder of topicFolders) {
  const hasExercises = allFiles.some(path =>
    path.startsWith(folder) && path.includes("exercises")
  );
  if (!hasExercises) missing.push(folder);
}

if (missing.length === 0) {
  dv.paragraph("All modules have exercises files.");
} else {
  dv.header(4, `${missing.length} module(s) missing exercises:`);
  dv.list(missing);
}
```

**Expected output:** A list of topic/module folder paths that have no `exercises` file. Use this to prioritize content creation — modules without exercises are not fully structured.

---

## Query 7 — Recently Modified Files

Shows the 20 most recently modified files across the entire vault — a quick way to see where activity is happening.

```dataview
TABLE
  file.folder AS "Location",
  file.mtime AS "Modified"
FROM ""
WHERE file.name != ".DS_Store"
SORT file.mtime DESC
LIMIT 20
```

**Variant — recently modified within TOPICS only:**

```dataview
TABLE file.mtime AS "Modified", status AS "Status"
FROM "TOPICS"
SORT file.mtime DESC
LIMIT 15
```

**Expected output:** A table of the 20 most recently touched files. Use this at the start of a study session to pick up where you left off.

---

## Query 8 — Topics by Difficulty

Groups all topic READMEs by their declared difficulty level, giving a curriculum view ordered from beginner to advanced.

**Frontmatter fields used:** `difficulty` (values: `beginner`, `intermediate`, `advanced`, or a number 1–5)

```dataview
TABLE
  rows.file.link AS "Topics"
FROM "TOPICS"
WHERE file.name = "README" AND difficulty != null
GROUP BY difficulty
SORT difficulty ASC
```

**Variant — numeric difficulty with progress:**

```dataview
TABLE
  difficulty AS "Level",
  progress AS "Progress %",
  status AS "Status"
FROM "TOPICS"
WHERE file.name = "README"
SORT difficulty ASC, status ASC
```

**Expected output:** Topics clustered by difficulty. Use this to plan a learning path — start with `beginner` topics and work up, or jump to `advanced` to challenge yourself.

---

## Query 9 — Spaced Repetition Due Items

Surfaces notes that are due for review based on a `next_review` date field. Supports a simple manual spaced repetition system without a dedicated plugin.

**Frontmatter fields used:** `next_review` (ISO date), `review_interval` (days), `ease` (optional float, default 2.5)

```dataview
TABLE
  next_review AS "Due Date",
  review_interval AS "Interval (days)",
  file.folder AS "Topic"
FROM "TOPICS" OR "SHARED"
WHERE next_review != null AND next_review <= date(today)
SORT next_review ASC
```

**DataviewJS variant — calculate next review dates automatically:**

```dataviewjs
const due = dv.pages('"TOPICS" OR "SHARED"')
  .where(p => p.next_review != null && p.next_review <= dv.date("today"))
  .sort(p => p.next_review, "asc");

if (due.length === 0) {
  dv.paragraph("Nothing due for review today.");
} else {
  dv.header(4, `${due.length} item(s) due for review:`);
  dv.table(
    ["Note", "Topic", "Due", "Interval"],
    due.map(p => [
      p.file.link,
      p.file.folder,
      p.next_review,
      (p.review_interval ?? "?") + " days"
    ])
  );
}
```

**Expected output:** Notes whose `next_review` date is today or in the past. After reviewing, manually update `next_review` to `today + interval` and increase `review_interval` if recall was easy. This implements a simple Leitner-style system in plain frontmatter.

---

## Query 10 — Global Statistics Dashboard

A summary table showing vault-wide learning statistics. Paste this into a dedicated `SHARED/dashboard.md` note.

```dataviewjs
// ── Counts ───────────────────────────────────────────────────────────────────
const allTopicReadmes = dv.pages('"TOPICS"').where(p => p.file.name === "README");
const totalTopics = allTopicReadmes.length;
const complete = allTopicReadmes.filter(p => p.status === "complete").length;
const inProgress = allTopicReadmes.filter(p => p.status === "in-progress").length;
const notStarted = allTopicReadmes.filter(p => !p.status || p.status === "not-started").length;

// ── Scores ───────────────────────────────────────────────────────────────────
const scored = dv.pages('"TOPICS"').where(p => p.score != null);
const avgScore = scored.length > 0
  ? (scored.map(p => p.score).array().reduce((a, b) => a + b, 0) / scored.length).toFixed(1)
  : "N/A";

// ── Notes ────────────────────────────────────────────────────────────────────
const totalNotes = dv.pages('"TOPICS" OR "SHARED"').length;
const sharedConcepts = dv.pages('"SHARED/concepts"').length;

// ── Output ───────────────────────────────────────────────────────────────────
dv.header(3, "leaps — Knowledge Base Statistics");
dv.table(
  ["Metric", "Value"],
  [
    ["Total Topics", totalTopics],
    ["Complete", complete + " (" + ((complete / totalTopics) * 100 || 0).toFixed(0) + "%)"],
    ["In Progress", inProgress],
    ["Not Started", notStarted],
    ["Total Notes", totalNotes],
    ["Shared Concepts", sharedConcepts],
    ["Test Scores Recorded", scored.length],
    ["Average Test Score", avgScore + (avgScore !== "N/A" ? "%" : "")],
  ]
);

// ── Recently Active Topics ────────────────────────────────────────────────────
dv.header(4, "Recently Active Topics");
const recent = dv.pages('"TOPICS"')
  .sort(p => p.file.mtime, "desc")
  .limit(5);
dv.list(recent.map(p => p.file.link + " — " + p.file.mtime.toFormat("yyyy-MM-dd")));
```

**Expected output:** A summary statistics block showing total topics, completion breakdown, total notes, shared concept count, test score count and average, plus a list of the 5 most recently modified topics. Use this as your vault homepage.

---

## Tips for Customizing Queries

- **Change the source folder:** Replace `"TOPICS"` with `"SHARED"` or `""` (all files) as needed.
- **Filter by tag:** Add `WHERE contains(file.tags, "#review")` to any query.
- **Combine sources:** Use `FROM "TOPICS" OR "SHARED/concepts"`.
- **Export to CSV:** Dataview does not export natively, but DataviewJS can build Markdown tables you can copy.
- **Performance:** On large vaults, prefer `TABLE` queries over `dataviewjs` for simple reads — they are faster.

---

## Related Files

- [`TEMPLATES/`](../TEMPLATES/) — Note templates with the frontmatter fields these queries depend on.
- [`SHARED/`](../SHARED/) — Shared concepts referenced in Query 4 and Query 10.
- [`tools/vscode-settings.json`](./vscode-settings.json) — VS Code settings (if not using Obsidian).
