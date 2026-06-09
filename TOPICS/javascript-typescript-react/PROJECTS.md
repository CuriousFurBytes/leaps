# Projects: JavaScript, TypeScript and React

> Project ideas for this topic, ranging from beginner to expert.
> Projects are optional but highly recommended — building things is the fastest path to real understanding.
> After completing a project, log it in the topic README.md Projects table.

---

## Beginner Projects

### Project 1: Todo List Application

**Difficulty:** Beginner
**Relevant Modules:** 01–03
**Estimated Time:** 4–8 hours

**Description:**
Build a classic todo list using vanilla JavaScript (no frameworks). The app should let users add new todos, mark them as complete, delete them, and filter by status (all / active / completed). Persist the todos to `localStorage` so they survive page refreshes.

**Requirements:**
- At least 3 separate JavaScript functions (add todo, toggle complete, delete todo)
- DOM manipulation using `querySelector`, `addEventListener`, and `createElement`
- Data persisted to `localStorage` using `JSON.stringify` and `JSON.parse`
- No external libraries — only HTML, CSS, and JavaScript

**Stretch goals:**
- Add drag-and-drop reordering
- Add due dates with overdue highlighting
- Add a "clear completed" bulk action

---

### Project 2: Weather Widget

**Difficulty:** Beginner
**Relevant Modules:** 04–05
**Estimated Time:** 4–6 hours

**Description:**
Build a weather widget using the Open-Meteo API (free, no API key required) that shows the current weather for a location the user searches. Practice `fetch`, async/await, DOM manipulation, and handling loading and error states.

**Requirements:**
- Accept a city name as user input and use a geocoding API to convert it to coordinates
- Fetch current weather from the Open-Meteo API using the coordinates
- Display temperature, weather description, and wind speed
- Handle loading state (show a spinner or "Loading..." message)
- Handle errors gracefully (invalid city name, network failure)

**API reference:**
- Geocoding: `https://geocoding-api.open-meteo.com/v1/search?name={city}`
- Weather: `https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true`

**Stretch goals:**
- Show a 7-day forecast
- Cache the last-searched city in localStorage
- Add geolocation support (`navigator.geolocation`)

---

## Intermediate Projects

### Project 3: Single-Page Application with Public API

**Difficulty:** Intermediate
**Relevant Modules:** 06–09
**Estimated Time:** 12–20 hours

**Description:**
Build a multi-page SPA using React and TypeScript that fetches data from a public API and presents it in a browsable UI. Good API choices: the GitHub API (repositories and users), the Open Library API (books), or the Rick and Morty API (characters).

**Requirements:**
- Built with React 18 and TypeScript (strict mode)
- Multiple "pages" using React Router v6
- API data fetching using `fetch` with `async`/`await` and typed response interfaces
- At least one search/filter feature
- Loading and error states handled in the UI
- At least 3 component tests using React Testing Library

**Stretch goals:**
- Add infinite scroll or pagination
- Add a favourites feature persisted to localStorage
- Add URL-synced filters (filter state reflected in the browser URL)

---

### Project 4: Analytics Dashboard

**Difficulty:** Intermediate
**Relevant Modules:** 07–10
**Estimated Time:** 15–25 hours

**Description:**
Build a data dashboard that displays charts and metrics from a data source of your choice. The goal is to practice complex state management, derived data computation, and rendering performance.

**Requirements:**
- React + TypeScript + Vite
- At least three different chart/visualization types (use a library like Recharts or Chart.js)
- Global filter controls that affect multiple charts simultaneously (use React Context or useReducer)
- Date range selection
- Data fetching with React Query or SWR (or simulate with static JSON data)
- The dashboard must be responsive (readable on both desktop and mobile)

**Stretch goals:**
- Add CSV export for the displayed data
- Add dark mode toggle
- Write tests for the data transformation utilities

---

## Advanced Projects

### Project 5: Full-Stack Next.js Application

**Difficulty:** Advanced
**Relevant Modules:** 08–12
**Estimated Time:** 30–50 hours

**Description:**
Build a full-stack Next.js application using the App Router. The application should include user authentication, at least two API routes, and a database. A good scope: a note-taking app, a bookmarks manager, or a simple project tracker.

**Requirements:**
- Next.js 14+ with the App Router and TypeScript
- Authentication using NextAuth.js (or similar)
- At least two server-side API routes
- Database integration (SQLite with Prisma, or PostgreSQL)
- Both server-side rendered pages and client components
- Deployed to Vercel (free tier is sufficient)
- A README explaining the architecture

**Stretch goals:**
- Add real-time features using WebSockets or Server-Sent Events
- Add image upload with file storage
- Achieve ≥ 80% test coverage on API routes

---

## Expert Projects

### Project 6: Build a Custom React Feature

**Difficulty:** Expert
**Relevant Modules:** 09–12
**Estimated Time:** 20–40 hours

**Description:**
Deepen your understanding of React internals by building something that extends or augments React itself. Choose one of the following:

**Option A — Build a state management library:**
Build a minimal, type-safe state management library in the spirit of Zustand or Jotai. It should use React's `useSyncExternalStore` hook, support multiple stores, and be usable as a drop-in replacement for simple `useState` cases.

**Option B — Build a form validation library:**
Build a React hooks-based form validation library in the spirit of React Hook Form. It should support custom validators, async validation, nested field groups, and provide typed field registration.

**Option C — Build a data grid component:**
Build a headless, virtualized data grid component using `react-window` or your own virtual scroll implementation. It must handle 100,000+ rows without performance issues, support column sorting and filtering, and be fully keyboard-accessible.

**Requirements (all options):**
- Written in TypeScript with full type safety
- Published as an npm package (or structured to be)
- At least 80% test coverage
- A documentation site or detailed README with usage examples

> [!IMPORTANT]
> This project is intentionally open-ended. The goal is not to build a production library
> (though you could!) but to deeply understand the React primitives by building on top of them.
> Favour learning over completeness — a partial, deeply-understood implementation beats a
> copy-pasted complete one.
