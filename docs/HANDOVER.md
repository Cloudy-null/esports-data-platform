# HANDOVER

Last updated: 2026-11-17

This file is the single source of truth for a new engineer or a new chat. Sections 1 to 6 are rewritten every session. Section 7 only grows.

## 1. Current status

Day 1 of Week 1 is done. Nothing else exists yet.

What works:
- `scripts/first_fetch.py` calls the OpenDota `proMatches` endpoint, saves the raw JSON to `data/raw/pro_matches_sample.json`, and prints the first 5 matches. It uses a custom User-Agent and a 30 second timeout.
- Planning docs are written: `docs/PROJECT_BRIEF.md` (agreed scope) and `docs/DATA_SOURCES_ESPORTS.md` (source test results).
- Two subagents exist in `.claude/agents/`: `data-quality-reviewer.md` and `handover-writer.md`.

What does not exist yet:
- No database schema, no adapter, no entity resolution, no data quality tests, no model.
- No tests of any kind, no linter or formatter setup, no CI (GitHub Actions), no README, no `.env.example`, no dependency file. The script uses only the Python standard library.
- No UI, so no `docs/DESIGN.md` yet.

## 2. Architecture overview and folder map

The target design is in `docs/PROJECT_BRIEF.md`. In short: ingest from sources, resolve team identities, test data quality, build a Dota 2 prediction model with a time-based split and a baseline, and track accuracy in public. Saudi and MENA teams are a featured filter. Planned schema: organization, team (organization + game), team_source_map (source + source team ID to team), match (game, source, date, teams, winner).

Planned layers (from CLAUDE.md): config, domain/core, adapters/io, entrypoints. None of these exist yet.

Folder map as it is today:

```
CLAUDE.md                          project rules
.gitignore                         ignores data/ and __pycache__/
.claude/agents/
    data-quality-reviewer.md       subagent
    handover-writer.md             subagent
docs/
    PROJECT_BRIEF.md               agreed scope and 4 week plan
    DATA_SOURCES_ESPORTS.md        source test results and verdicts
    HANDOVER.md                    this file
    SESSION_LOG.md                 one entry per session
scripts/
    first_fetch.py                 one-off OpenDota fetch (not layered)
```

`first_fetch.py` is a throwaway first step. It mixes config, network calls, file writing, and printing in one file. The real code should be split into the layers above.

## 3. How to run, test, and deploy

Run the only script that exists (Python 3, no extra packages):

```
python scripts/first_fetch.py
```

It needs a network that does not intercept HTTPS for api.opendota.com. OpenDota worked on the KAU network in the earlier source test. Other hosts (Liquipedia, PandaScore and more) were intercepted there. Never turn off certificate checks to get around this. Use a home connection or hotspot instead.

Test: there are no tests yet. Lint and format: not set up yet. CI: not set up yet. Deploy: nothing to deploy yet.

## 4. Data sources and known data issues

Full details and quotes are in `docs/DATA_SOURCES_ESPORTS.md`. Short version:

- OpenDota (Dota 2): allowed, no key needed, 60 requests per minute and 3000 per day. Only source with live samples so far. This is the Phase 1 source and the model source.
- PandaScore: free plan gives schedules and team info, 1000 requests per hour. Results are paid. Terms not read yet. One adapter can serve many games (game is a parameter).
- Liquipedia: LPDB key needs approval, 60 requests per hour, open source code required, credit required (CC BY-SA 3.0), custom User-Agent with contact info required. No HTML scraping. MediaWiki API fallback, EWC history only.
- Rocket League: the official schedule page is not a data source. Use PandaScore or Octane.gg (check that it is still maintained first).
- Rejected: official EWC site, Esports Charts, storing Twitch history, Battlefy.

Known data issues (measured in OpenDota):
- One club can have many team IDs. Twisted Minds has 3 IDs, Nigma Galaxy has 4, and Team Saudi Arabia has 2.
- Names have stray spaces ("Nigma Galaxy ", "ANBU DIVISION ").
- Similar names are different teams ("Falcons Prime", "FalconBlade", "Falcon eSports"). Never merge on name similarity.
- The "current member" flag in the team players endpoint is unreliable (Team Falcons showed only 2 of 5).
- Saudi and MENA Dota teams had zero maps in September and October 2026, so the data can go quiet.
- In `proMatches`, `radiant_name` and `dire_name` can be missing or empty. Treat team name as optional and team ID as the key.

## 5. Open CHECK items and known bugs

CHECK items:
- CHECK: CLAUDE.md says UI work must use the "frontend-design" and "Impeccable" skills. Neither is installed. Install them, or decide what to use instead, before any UI work.
- CHECK: the interview-coach agent works in Claude Code, but `.claude/agents/interview-coach.md` is not in the repo. It is probably defined at user level, outside the repo. Decide whether to copy it into `.claude/agents/` so the repo is complete.
- CHECK: CLAUDE.md also refers to a design-lead agent, which is not in `.claude/agents/` either. Same question.
- CHECK: `docs/DATA_SOURCES_ESPORTS.md` says `samples/` is listed in `.gitignore`. It is not. `.gitignore` only has `data/` and `__pycache__/`. Add `samples/` before any sample file is created, so raw data is never committed.
- CHECK: PandaScore terms on republishing and attribution were not read. Read them before building the adapter.
- CHECK: does the PandaScore free plan include final series scores? Not confirmed.
- CHECK: is Octane.gg still maintained? Test it before relying on it for Rocket League.
- CHECK: Liquipedia LPDB key application not sent yet.

Known bugs in `scripts/first_fetch.py` (recorded, not fixed):
- No validation of the response. If OpenDota returns an error object like `{"error": ...}` instead of a list, it is saved as if it were real data, and then `matches[:5]` crashes.
- No HTTP status check and no type check on the response or on each match.
- Uses `print` instead of logging. CLAUDE.md requires logging.
- `m['match_id']` is a required field and fails with a raw KeyError if missing. In a pipeline this should log and skip the bad record.
- Everything is in one script. It is not split into config, adapter, and entrypoint layers.
- No tests.
- No README, no CI yet.

`data/` is in `.gitignore`, so the raw sample file will not be committed. `samples/` is not (see CHECK above).

## 6. Next 3 tasks

These follow the Week 1 plan in `docs/PROJECT_BRIEF.md`.

1. Day 2, part A: schema. Write the schema as SQL for DuckDB in `sql/schema.sql` with four tables: organization, team, team_source_map, match. Add a unit test that creates the tables in an in-memory DuckDB. Explain why first before adding the DuckDB dependency, then pin it. Show the design and wait for the OK before writing code.
2. Day 2, part B: OpenDota adapter. Create a module in an adapters folder with one function that fetches `proMatches`, checks the HTTP status, checks the response is a list, and validates each match (required: `match_id`, team IDs, winner; optional: team names, with a default). Bad records are logged and skipped. Use `logging`, not `print`. Add tests with saved fake responses, including an error object and a record with no `match_id`.
3. Day 3: load a month of pro matches into the database and count how many team IDs are messy (same name with different IDs, names with stray spaces). Save the counts, because they become a real number for the CV. Re-quiz the owner first (see the session log): required vs optional fields, and one row per source ID in team_source_map.

Day 4 (not yet a task) is the review-queue mapping logic: exact ID, then fuzzy candidates, then manual review. Never auto-merge.

## 7. Project history

Dated timeline. Never delete entries. Add new ones at the bottom.

- 2026-10-26 to 2026-10-27: Data source test (no code). OpenDota was the only source reachable with live samples because the network re-signs HTTPS for the others. Results are in `docs/DATA_SOURCES_ESPORTS.md`.
- 2026-11-02: Second review of the plan. Scope changed from Saudi-only to all teams and many games, with Saudi and MENA as a featured filter. Decided to build only the esports pipeline and park the HR Call Notes project. Written in `docs/PROJECT_BRIEF.md`.
- 2026-11-16: First code. Commit "feat: first OpenDota fetch" added `scripts/first_fetch.py`, which saves a raw sample of pro matches.
- 2026-11-17: Docs commits added `docs/PROJECT_BRIEF.md`, `docs/DATA_SOURCES_ESPORTS.md`, `CLAUDE.md`, and the subagents in `.claude/agents/`. This set the project rules and scope.
- 2026-11-17: Handover and session log created. Review of the repo found that CLAUDE.md names skills and agents that are not installed, and that `samples/` is not in `.gitignore`. Recorded as CHECK items in section 5. No code changed.
