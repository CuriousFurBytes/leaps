# Module 12: Capstone Project

> Build a production-shaped React and TypeScript application that synthesizes the whole topic.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Project Brief](#project-brief)
5. [Milestones](#milestones)
6. [Help and Getting Unstuck](#help-and-getting-unstuck)
7. [Acceptance Criteria](#acceptance-criteria)
8. [Common Pitfalls](#common-pitfalls)
9. [Cross-Links](#cross-links)
10. [Summary](#summary)

## Overview

The capstone asks you to build a realistic product surface rather than another isolated exercise. You will design and implement a TypeScript React application that fetches, edits, filters, persists, tests, and deploys user-facing data. The point is synthesis: language fundamentals, type modeling, component boundaries, state transitions, effects, accessibility, tests, performance, and deployment all matter at the same time.

This module intentionally does not provide a complete copy-paste solution. Professional growth comes from making design decisions, discovering tradeoffs, and debugging your own implementation. The help sections give staged hints and checkpoints so you can move forward without losing ownership of the build.

## Prerequisites

- Modules 01 through 11 in this topic.
- Comfort creating a React + TypeScript project with a modern toolchain.
- Familiarity with testing, accessibility checks, and deployment workflows.

## Objectives

By the end of this module, you will be able to:
- Design a production-shaped React and TypeScript application from requirements.
- Model application data and UI state with clear TypeScript contracts.
- Implement accessible, tested, performant components and workflows.
- Explain architectural tradeoffs in your final project documentation.

## Project Brief

Build a **Learning Sprint Planner**: a web app that lets a learner plan study sprints, track module tasks, capture notes, and review progress. The app should support local sample data and a replaceable API boundary so it can later move to a real backend.

Minimum domain model example:

```typescript
type TaskStatus = "todo" | "doing" | "done";

type SprintTask = {
  id: string;
  title: string;
  module: string;
  estimateMinutes: number;
  status: TaskStatus;
};
```

A minimal component boundary might begin like this:

```tsx
type TaskCardProps = {
  task: SprintTask;
  onStatusChange: (id: string, status: TaskStatus) => void;
};

export function TaskCard({ task, onStatusChange }: TaskCardProps) {
  return (
    <article aria-label={`Task: ${task.title}`}>
      <h2>{task.title}</h2>
      <p>{task.module} · {task.estimateMinutes} minutes</p>
      <button onClick={() => onStatusChange(task.id, "done")}>Mark done</button>
    </article>
  );
}
```

## Milestones

1. Define requirements, user stories, and a small architecture note.
2. Create the React + TypeScript project and commit the initial running app.
3. Model domain types, sample data, and an API adapter boundary.
4. Build task list, filtering, editing, and progress summary features.
5. Add accessible forms, loading states, empty states, and error states.
6. Add unit, component, and integration tests for core workflows.
7. Profile rendering, fix avoidable re-renders, and document performance decisions.
8. Deploy the app and write a final retrospective.

## Help and Getting Unstuck

### Hint 1: Start with Data

Write the domain types before writing UI. If the data model is confused, components will become confused too.

```typescript
type Sprint = {
  id: string;
  name: string;
  startsOn: string;
  endsOn: string;
  tasks: SprintTask[];
};
```

### Hint 2: Keep Boundaries Small

Create an API module even if it initially returns local data. React components should ask for data through a function, not import and mutate a global array directly.

```typescript
export async function listSprintTasks(): Promise<SprintTask[]> {
  return structuredClone(sampleTasks);
}
```

### Hint 3: Test User Behavior

Prefer tests that describe user outcomes. A good test says what the learner can do, not which private helper function was called.

```typescript
// Pseudocode for a component test.
// Render the task list, click "Mark done", and assert the progress summary changes.
```

## Acceptance Criteria

- The app runs locally with documented setup commands.
- Core domain types avoid `any` and model realistic loading, success, and error states.
- React components have clear prop boundaries and accessible labels.
- At least one workflow is covered by an automated test.
- The project includes a short architecture note and final retrospective.
- The deployed or locally built version matches the documented feature set.

## Common Pitfalls

### 1. Building Screens Before Modeling State

Wrong approach:

```tsx
export function App() {
  return <div>Lots of hard-coded task markup</div>;
}
```

Correct approach:

```tsx
const tasks: SprintTask[] = sampleTasks;
export function App() {
  return tasks.map((task) => <TaskCard key={task.id} task={task} onStatusChange={updateStatus} />);
}
```

Modeling first keeps the UI connected to real behavior.

### 2. Hiding Errors

Wrong approach:

```typescript
catch (error) {
  return [];
}
```

Correct approach:

```typescript
catch (error) {
  return { status: "error", message: "Could not load tasks." };
}
```

Users and developers both need visible failure states.

### 3. Skipping Accessibility Until the End

Wrong approach:

```tsx
<div onClick={saveTask}>Save</div>
```

Correct approach:

```tsx
<button type="button" onClick={saveTask}>Save</button>
```

Semantic elements make interaction, keyboard support, and assistive technology easier from the start.

## Cross-Links

- [[javascript-typescript-react]] for the full sequence this project synthesizes.
- [[devops-platform-engineering]] for test design and feedback loops.
- [[css]] for inclusive interface fundamentals.
- [[css]] for state vocabulary.

## Summary

- The capstone is a realistic build, not a lecture module.
- You will synthesize JavaScript, TypeScript, React, testing, accessibility, performance, and deployment.
- Help is staged as hints so you keep ownership of the implementation.
- Acceptance criteria define what finished means without prescribing every line of code.
- A strong final submission includes both working software and clear architectural reasoning.
