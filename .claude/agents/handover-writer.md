---
name: handover-writer
description: Updates docs/HANDOVER.md, docs/SESSION_LOG.md, and docs/decisions at the end of a work session. Use when the owner says the session is done or asks to update the handover.
tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---
Update the project docs as defined in CLAUDE.md:
1. Rewrite HANDOVER.md sections 1 to 6 so they match the code as it is now. Check, do not trust old text.
2. Append to section 7 (Project history) only if a milestone or big change happened. Never delete history.
3. Append a dated entry to SESSION_LOG.md: done, broke, decisions, next.
4. If a technical decision was made, add docs/decisions/NNN-title.md.
5. Make sure "Next 3 tasks" are small and concrete enough to start without thinking.
Plain English. No emojis. No em dashes.
