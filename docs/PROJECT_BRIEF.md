UPDATE FROM A SECOND REVIEW (use this to adjust the project plan)

GOAL
CV for Data Engineer / ML Engineer roles in Jeddah or Riyadh. Graduating Jan 2027. Nothing is built yet (today is Nov 2, 2026).

DECISION
Build Project 1 (esports data pipeline) only. Park Project 2 (HR Call Notes) until after job applications. It is closer to a full-stack/AI-app role than a data role, and it depends on a real recruiter, Arabic speech-to-text quality and PDPL handling.

NEW SCOPE: ALL TEAMS, MANY GAMES (not Saudi-only)
- Saudi/MENA becomes a featured filter, not the project's identity.
- Falcons is one ORGANIZATION with different TEAMS per game, and each source names them differently. Proposed schema: organization, team (org + game), team_source_map (source + source team ID -> team), match (game, source, date, teams, winner).
- ID mapping at scale: exact ID match first, then fuzzy-match candidates, then a manual review queue. Never auto-merge on name similarity ("Falcons Prime" vs "FalconBlade").
- Limit to top-tier and regional-major events to keep cleanup manageable.

EXISTING COMPETITION (checked)
- Per-game stats sites (EsportsEarnings, ggscore, Esports Charts, etc.) and hand-edited EWC standings articles exist.
- Dota 2 draft-based prediction projects are very common on GitHub (~0.63 AUC typical). The model is NOT my differentiator.
- My differentiator: clean cross-game entity resolution + data quality tests + a prediction model with a time-based split, a baseline, and public accuracy tracking.
- Don't claim "nothing like this exists."

FACT CORRECTION
Esports World Cup 2026 was held in Paris, the first one outside Saudi Arabia. Don't write "EWC in Riyadh" in the pitch. Say "Saudi-owned clubs at the Esports World Cup."

DATA SOURCES AND RULES
1. OpenDota: Dota 2 pro matches. Phase 1, plus the model.
2. PandaScore: free plan has schedules, results and context data, 1000 requests/hour, no credit card. Covers CS, Valorant, LoL, Dota 2, Rocket League and others. One adapter serves many games (game = parameter). Detailed stats endpoints are paid. I have NOT read their terms yet. Read them before building, especially public display rules.
3. Liquipedia: LPDB API needs approved access, limited to 60 requests/hour. Free access is for educational projects and non-commercial public sites, but requires the code to be open source, is often time-limited, never allows betting-related projects, and refuses sites that replicate Liquipedia's features. Paid plans start at $49/month per data type per game. Must credit Liquipedia (CC BY-SA 3.0), cache results, and send a custom User-Agent with contact info. Fallback with no key: the MediaWiki API (1 request per 2 s, parse requests 1 per 30 s, no HTML scraping). Use it for EWC history only, loaded once and kept in the database. Access is not guaranteed.
4. Rocket League: rocketleague.com/competitive/schedule is only an event-level list (no match data, no documented API), so it is NOT a pipeline source. Use PandaScore, or the Octane.gg API (unverified whether it is still maintained, test first).
5. Still rejected: official EWC site, Esports Charts, storing Twitch history.

PLAN
- Public GitHub repo from Day 1.
- Prediction for one game only (Dota 2). Other games: results and tracking only.
- Orchestrator: skip Airflow/Dagster, use scheduled GitHub Actions. Keep dbt (DuckDB + dbt is light).
- n8n alerts only if time is left.
- No betting or odds anywhere. State "learning only" on the site.
- Site: analytics, not Liquipedia-style browse-everything pages.
- Weeks: (1) Dota ingestion, schema, ID mapping; (2) dbt models, quality checks, PandaScore adapter for CS2/Valorant/Rocket League; (3) model + baseline + accuracy tracking; (4) public site, README, daily run, EWC history if time allows.
- Week 1: Day 1 repo + raw OpenDota sample; Day 2 schema + adapter; Day 3 load a month of pro matches and count messy IDs; Day 4 review-queue mapping logic; Day 5 data quality tests; Day 6 PandaScore sample + terms check; Day 7 CI action + README.

CV NOTES
- Projects go right after education. 3-4 bullets per project: what I built, how, a real number.
- Only list shipped work, never invent numbers. One finished project beats two half-finished ones.
- Frame the title around engineering, e.g. "Esports Data Platform", not "esports".
- Header: "Jeddah, open to Riyadh". Bilingual Arabic/English, Saudi certificates (Tuwaiq, SDAIA, Misk) count, one-page plain layout.
- Apply early: many big Saudi employers recruit graduates months before graduation.