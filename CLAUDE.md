# CLAUDE.md

## Project
- Name: Esports Data Platform
- One line: Pipeline that collects pro esports match data, resolves team identities across sources, tests data quality, and tracks prediction accuracy. Saudi and MENA teams are a featured filter.
- Owner: Abdulrahman Aljahdali (GitHub: cloudy-null). I must be able to explain every part of this repo in an interview.
- Agreed scope: docs/PROJECT_BRIEF.md. Data source findings: docs/DATA_SOURCES_ESPORTS.md. Read both before planning any feature.

## How to work with me
- Use the Superpowers workflow for any new feature: brainstorm, then write a plan, then build with tests, then review. Show me the design and the plan and wait for my OK before writing code.
- For tiny fixes (a typo, one line), skip the full workflow.
- Small steps. One feature or fix per session. Do not start extra work I did not ask for.
- If you are unsure about something, write CHECK: <question> in the handover doc and keep going with the safest choice. Do not guess silently.
- Test data, do not trust it. Every input from outside (files, APIs, scraped pages) gets validated.
- Never disable TLS or certificate checks to get around a network problem. Stop and tell me.

## Code structure (software engineering style)
- Separate layers. Keep these apart and never mix them in one file:
  - config: settings and env vars only, loaded in one place
  - domain/core: business logic, pure functions where possible, no I/O
  - adapters/io: anything that talks to the outside (APIs, DB, files, scraping). One adapter per data source.
  - entrypoints: CLI, API routes, jobs, UI. Thin. They call core, they do not hold logic.
- One responsibility per module. If a file passes about 300 lines, propose a split.
- Clear names over clever code. No abbreviations I would not understand.
- Type hints in Python.
- No secrets in code. Use .env and keep .env.example updated.
- Dependencies pinned. Explain why before adding any new library.
- Logging, not print. Errors are handled where they can be handled and logged with context.

## Tests and quality
- Every core function gets unit tests. Every pipeline stage gets at least one data test.
- Run the linter, formatter, and tests before saying a task is done. Report the results.
- CI (GitHub Actions) runs lint and tests on every push.

## Git
- Small commits with clear messages: <type>: <what changed> (feat, fix, refactor, test, docs, chore).
- Never add Co-Authored-By, "Generated with Claude Code", or session links to commit messages or PR descriptions. Commits are authored by me only.
- Never commit raw data, samples, secrets, or large binaries.

## Documentation (keep these updated, always)
- README.md: what it is, why it exists, screenshot or demo link, how to run it in under 5 commands, architecture diagram.
- docs/HANDOVER.md: the single source of truth for a new engineer (or a new chat) picking this up. Sections:
  1. Current status (what works, what does not)
  2. Architecture overview and folder map
  3. How to run, test, and deploy
  4. Data sources and known data issues
  5. Open CHECK items and known bugs
  6. Next 3 tasks
  7. Project history: a dated timeline of milestones, big changes, and why they happened. Never delete history entries. Add new ones at the bottom.
  Sections 1 to 6 are rewritten to stay current. Section 7 only grows.
  Update it at the end of EVERY session.
- docs/SESSION_LOG.md: append a dated entry each session: what was done, what broke, decisions made, what is next. Never edit old entries.
- docs/decisions/NNN-title.md: one short file per important technical decision (context, options, choice, trade-off). If a decision is replaced later, keep the old file and mark it "Superseded by NNN".

## Writing style for all docs
- Plain simple English, student level. No corporate language.
- No emojis. No em dashes.

## Frontend and design (for any UI work)
- Use the design-lead agent, the frontend-design skill for building, and the Impeccable skill for critique and polish.
- Never use the default AI look: no Inter-only typography, no purple gradients, no generic hero with three feature cards.
- Before building UI, write docs/DESIGN.md: aesthetic direction, the reference sites I chose, font pair, color tokens, spacing scale. Wait for my OK.
- Colors and fonts as CSS variables in one place. Reuse components, do not restyle each page.
- After building, take screenshots (desktop and mobile) with Playwright, compare against the references, and fix what looks off before saying it is done.
