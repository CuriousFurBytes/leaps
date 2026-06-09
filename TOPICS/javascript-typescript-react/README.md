# JavaScript, TypeScript and React

> A zero-to-expert path for building reliable, typed, interactive web applications with JavaScript, TypeScript, and React.

## Table of Contents
1. [Why Learn JavaScript, TypeScript and React?](#why-learn-javascript-typescript-and-react)
2. [Prerequisites](#prerequisites)
3. [Module Map](#module-map)
4. [Cross-Links](#cross-links)
5. [Quick Reference](#quick-reference)

## Why Learn JavaScript, TypeScript and React?

JavaScript began as a small browser scripting language and became the universal runtime of the web. It now runs in browsers, servers, desktop apps, mobile shells, build tools, test runners, and edge environments. Learning it deeply means understanding both the historical browser constraints that shaped the language and the modern module, package, and tooling ecosystem that powers production software.

TypeScript adds a static type system on top of JavaScript without replacing JavaScript's runtime. That split is essential: TypeScript improves design feedback, editor tooling, refactoring, and maintainability, but the code still executes as JavaScript. Expert TypeScript developers know how to model domain data, avoid unsound type tricks, and keep types helpful rather than ornamental.

React teaches a component model for user interfaces: UI is described as a function of state, and React reconciles those descriptions with the real screen. That model supports applications from small dashboards to large product surfaces, but it requires discipline around state, effects, rendering performance, accessibility, testing, and architecture.

Together, JavaScript, TypeScript, and React form one of the most practical stacks for modern product engineering. This topic starts from zero, builds the language and type foundations, then moves into production React architecture and ends with a realistic capstone application.

## Prerequisites

- Basic computer literacy: files, folders, command-line navigation, and text editing.
- [[css]] — helpful for HTML, CSS, and HTTP concepts, but this path defines the minimum needed as it goes.
- [[go]] — helpful for variables, functions, and control flow, but Module 01 reviews them from first principles.

## Module Map

| # | Module | Difficulty | Status |
|---|--------|------------|--------|
| 01 | [Web Language Foundations](./modules/01_web_language_foundations/README.md) | Beginner | [ ] |
| 02 | [Modern JavaScript](./modules/02_modern_javascript/README.md) | Beginner | [ ] |
| 03 | [TypeScript Fundamentals](./modules/03_typescript_fundamentals/README.md) | Beginner | [ ] |
| 04 | Browser APIs, DOM, and Events | Intermediate | [ ] |
| 05 | Async JavaScript and Data Fetching | Intermediate | [ ] |
| 06 | React Components, Props, and State | Intermediate | [ ] |
| 07 | React Effects, Forms, and Routing | Intermediate | [ ] |
| 08 | Testing, Debugging, and Tooling | Advanced | [ ] |
| 09 | Advanced TypeScript for Applications | Advanced | [ ] |
| 10 | React Performance and Accessibility | Advanced | [ ] |
| 11 | Production Architecture and Deployment | Expert | [ ] |
| 12 | [Capstone Project](./modules/12_capstone_project/README.md) | Expert | [ ] |

## Cross-Links

- [[css]] for HTML, CSS, accessibility, HTTP, and browser fundamentals.
- [[go]] for language-independent control flow and data modeling.
- [[devops-platform-engineering]] for test strategy, test doubles, and quality feedback loops.
- [[devops-platform-engineering]] for API vocabulary used throughout the stack.
- [[css]] for the meaning of state in interactive systems.

## Quick Reference

| Task | Command or Pattern | Notes |
|---|---|---|
| Check Node.js | `node --version` | Use an actively supported LTS release for projects. |
| Run a script | `node index.js` | Executes JavaScript outside the browser. |
| Create a package | `npm init` | Generates `package.json`. |
| Install TypeScript | `npm install --save-dev typescript` | Project-local compiler is preferred. |
| Type-check | `npx tsc --noEmit` | Checks types without writing build output. |
| Create React app with Vite | `npm create vite@latest` | Choose a React + TypeScript template. |
| Start dev server | `npm run dev` | Runs the app locally during development. |
| Component shape | `function Name(props) { return ... }` | React components are functions that return UI descriptions. |
