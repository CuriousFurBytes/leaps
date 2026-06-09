# Module 10: Accessibility Testing

[← Performance Testing](../09_performance-testing/) | [Topic Home](../../README.md) | [Next → QA Strategy and Metrics](../11_qa-strategy-and-metrics/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-red)
![Time](https://img.shields.io/badge/time-6--7h-orange)

---

> WCAG 2.1 levels (A/AA/AAA); automated tools (axe-core, Lighthouse); screen reader testing with NVDA and VoiceOver; keyboard navigation testing.

## Overview

This module is a stub. Content will be added in a future iteration.

**Topics covered in this module:**

- WCAG 2.1 — the four principles (Perceivable, Operable, Understandable, Robust); A/AA/AAA conformance levels
- axe-core — the industry-standard accessibility rule engine; `@axe-core/playwright` for automated scanning
- Lighthouse — running Lighthouse accessibility audits in CI
- Keyboard navigation testing — tab order, focus management, keyboard traps, skip links
- Screen reader testing — NVDA (Windows), VoiceOver (macOS/iOS), TalkBack (Android); how to test with each
- ARIA attributes — roles, states, properties; when ARIA helps and when it creates more confusion
- Color contrast testing — WCAG contrast ratios, automated detection, manual verification
- Common accessibility bugs — missing alt text, unlabeled form fields, poor focus indicators, inaccessible modals
- Legal context — ADA, Section 508, European Accessibility Act; why accessibility has legal implications

## Prerequisites

- Module 05: End-to-End Testing in this topic — Playwright-based accessibility testing builds on E2E foundations
- Basic HTML knowledge — semantic HTML elements, form elements, ARIA attributes

## Objectives

By the end of this module, you will be able to:

1. Run axe-core accessibility audits via Playwright and interpret the results
2. Identify WCAG 2.1 AA violations and know how to fix the most common ones
3. Test keyboard navigation for a web application
4. Use NVDA or VoiceOver to verify screen reader compatibility for a basic flow
5. Integrate automated accessibility testing into a CI/CD pipeline

## Cross-Links

- [[qa-testing/modules/05_e2e-testing]] — Playwright is the primary tool for automated accessibility testing in this module
- [[javascript-typescript-react]] — React component accessibility with React Testing Library's accessibility queries
- [[qa-testing/modules/11_qa-strategy-and-metrics]] — Accessibility requirements belong in the QA strategy
