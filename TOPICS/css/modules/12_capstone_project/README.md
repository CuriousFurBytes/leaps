# Module 12: Capstone Project

> Build a production-quality responsive marketing site and component system that synthesizes the full CSS path.

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
The capstone is build-oriented. You will create a realistic responsive site for a small product, service, publication, or nonprofit. The project should demonstrate layout, typography, color, component states, responsive behavior, accessibility, debugging discipline, and maintainable CSS architecture.

Do not copy a full solution. Use the prompts, checkpoints, and hints to make your own decisions and explain your tradeoffs. The value of the capstone is the judgment you practice while converting requirements into a working interface.

## Prerequisites
- Modules 01–11 in this CSS topic.
- Comfort editing HTML and CSS in a browser-based workflow.

## Objectives
By the end of this module, you will be able to:
- Design and implement a responsive multi-section interface.
- Organize CSS around tokens, components, layout utilities, and states.
- Test styles against accessibility, responsiveness, and maintainability criteria.
- Explain architectural tradeoffs in a project README.

## Project Brief
Build a polished landing site with at least a hero, navigation, feature grid, testimonial or proof section, pricing or call-to-action section, and footer. Use semantic HTML and write the CSS yourself. The visual design is up to you, but the final result should look intentional at mobile, tablet, and desktop widths.

```css
/* Suggested starting architecture: customize, do not blindly copy. */
:root {
  --color-bg: #ffffff;
  --color-text: #111827;
  --space-4: 1rem;
}

.site-shell {
  width: min(100% - 2rem, 72rem);
  margin-inline: auto;
}
```

## Milestones
1. Define content, audience, and success criteria.
2. Create semantic HTML for all required sections.
3. Establish tokens for color, spacing, type, and radius.
4. Build mobile-first layout, then add responsive enhancements.
5. Add interactive states for links, buttons, and focus.
6. Test reduced motion, contrast, keyboard navigation, and overflow.
7. Write a short architecture note explaining your CSS decisions.

## Help and Getting Unstuck
- If spacing feels random, create a small spacing scale and reuse it.
- If selectors become long, add meaningful component classes.
- If layout breaks at one width, inspect the element that overflows before adding media queries.
- If the design lacks hierarchy, adjust type scale, contrast, and whitespace before adding decoration.
- If you are stuck, return to [[css#module-map]] and review the module most closely related to the problem.

## Acceptance Criteria
- The project has at least six meaningful page sections.
- CSS uses low-specificity selectors and reusable custom properties.
- Layout works at narrow, medium, and wide viewport sizes.
- Focus states are visible and color contrast is intentional.
- The project includes notes about tradeoffs, limitations, and future improvements.

## Cross-Links
- [[html]]
- [[accessibility]]
- [[design-systems]]

## Summary
- The capstone proves you can synthesize the whole CSS learning path.
- The output is a real interface, not a worksheet.
- The project should demonstrate responsive layout, accessibility, architecture, and debugging judgment.
- Help sections are hints, not a replacement for your own implementation work.
- A strong submission explains why the CSS is organized the way it is.
