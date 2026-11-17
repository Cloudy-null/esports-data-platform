# SESSION LOG

One entry per session. Never edit old entries. Newest at the bottom.

## 2026-11-17

Done:
- Checked which skills are available. CLAUDE.md says UI work should use "frontend-design" and "Impeccable". Neither is installed.
- Ran a quiz on the existing repo (5 questions and 3 follow-up checks).
- Reviewed `scripts/first_fetch.py` and recorded its known bugs in HANDOVER.md section 5.
- Created `docs/HANDOVER.md` and this file. No code was changed.

Quiz results:
- Timeout in `urlopen`: partly understood. Knew it stops waiting forever. Did not know why a custom User-Agent matters. It tells the server who is calling, and Liquipedia terms require it.
- `m['match_id']` vs `m.get(...)`: not understood at first, then explained. Missing optional data gets a default. Missing required data gets an error. In a pipeline, log the error and skip the bad record.
- Entity resolution: right instinct that similar names are not the same team. Needed the reasoning: exact ID first, then fuzzy candidates, then a manual review queue. Never auto-merge.
- Schema (organization, team, team_source_map): did not know. Explained.
- Time-based split vs random split, and baselines: did not know. Explained. The follow-up check was answered correctly.
- Follow-up check: Twisted Minds has 3 OpenDota IDs, so it needs 3 rows in team_source_map (one row per source ID). Answered 1, which is wrong.

What broke or was found:
- Skills "frontend-design" and "Impeccable" are not installed.
- `.claude/agents/` has only `data-quality-reviewer.md` and `handover-writer.md`. The interview-coach agent works but is defined outside the repo. The design-lead agent, which CLAUDE.md names, is also not in the repo.
- `data/` is in `.gitignore`, but `samples/` is not, even though `docs/DATA_SOURCES_ESPORTS.md` says it is.
- `first_fetch.py` has no response validation, no status checks, uses print instead of logging, is not layered, and has no tests. No README or CI yet.

Decisions:
- No technical decision was made, so no file was added to `docs/decisions/`.
- Bugs in `first_fetch.py` are recorded, not fixed. The fix belongs in the Day 2 adapter.

Next:
- Start of next session: re-quiz on required vs optional fields, and on one row per source ID in team_source_map.
- Then Day 2 of the Week 1 plan. Schema first, then the OpenDota adapter with validation and tests. See HANDOVER.md section 6.
- Settle the CHECK items on skills, missing agents, and `samples/` in `.gitignore` (the last one is a one-line fix).
