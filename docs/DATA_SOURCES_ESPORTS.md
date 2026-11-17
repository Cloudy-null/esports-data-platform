# Saudi Esports Radar: Data Source Test

Test date: 2026-10-26 to 2026-10-27. Nothing was built. Samples are in `samples/` (listed in `.gitignore`).

## Read this first: how far the test got

This machine is on a King Abdulaziz University network that intercepts HTTPS for most esports sites. Their certificates are re-signed by `CN=KAU-CA-INTERNAL`, which this machine does not trust, so every HTTPS request to them fails. Turning certificate checks off was blocked as a security risk, and I did not try to work around that.

| Host | Reachable from this network |
|---|---|
| api.opendota.com | Yes, normal TLS |
| api.twitch.tv | Yes, but id.twitch.tv (where tokens come from) is intercepted |
| liquipedia.net, api.pandascore.co, api.start.gg, developer.riotgames.com, battlefy.com, escharts.com, esportsworldcup.com, hltv.org, vlr.gg | No, intercepted |
| web.archive.org | Yes, until it rate limited me (HTTP 429) |

What this means:
- **OpenDota is the only source with live samples.**
- For the other sources, I read the terms and docs from recent Wayback Machine copies (dates are given below) and got results from web search.
- Repeat the live tests on a home connection or mobile hotspot, or ask KAU IT how to install their root certificate properly.

## 1. Source by source

### Liquipedia (MediaWiki API and LiquipediaDB API)
- **Access:**
  - The MediaWiki API (`/<wiki>/api.php`) is free and needs no key.
  - The LiquipediaDB (LPDB) API is the structured one for matches, teams and placements. It needs a key, granted on request.
- **Auth:** none for MediaWiki. A key for LPDB.
- **Free tier and limits:** quotes are from the API terms (Wayback copy 2026-10-05):
  - MediaWiki: "Rate limit all HTTP requests to no more than 1 request per 2 seconds. API "action=parse" requests should not exceed 1 request per 30 seconds"
  - LPDB: "Rate limit all requests to no more than 60 requests per 1 hour."
  - Both: a custom User-Agent with contact details is required, and gzip must be supported.
- **Paid LPDB plans** (from liquipedia.net/api, copy 2026-06-18): Basic is $49 per month per data type, with 1000 requests per hour. Premium is $199 per month per data type, with 5000 requests per hour.
- **Free plan eligibility:**
  - Free access covers "Educational Purposes", "Non-Commercial Public Websites" (projects that "do not monetize and do not duplicate existing Liquipedia features") and "Community Feature Development".
  - Code must be open source: "we require that your project's code be open-sourced. In most instances, free access is provided on a limited-time basis."
  - Never granted to betting projects or "Liquipedia Replicas".
- **Automated access:** "Automated access to non-API endpoints (ie, generated HTML pages) is not permitted." Scraping the HTML pages is out.
- **Attribution and republishing:** "Liquipedia content is licensed under CC-BY-SA 3.0, which requires that you attribute Liquipedia as the source of your data." You can republish on a public site with attribution, and the same license must pass on to derived data.
- **robots.txt** (copy 2026-05-01):
  - Blocks AI and SEO crawlers completely, including ClaudeBot and GPTBot.
  - Lists `/<wiki>/api.php` as Disallow for generic crawlers. That rule is aimed at crawlers. The API terms are what govern an API client.
- **Live test:** not possible here (intercepted).
- **Verdict: ALLOWED** through the API only, with attribution. LPDB needs an approved key. Free LPDB access fits this project if it stays non-commercial and open source, but it may be time limited. If you ever add ads or a paid tier, budget $49 per month or more per data type per game.

### PandaScore
- **Access:** REST API. Sign up for a token.
- **Free tier** (from pandascore.co/pricing, copy 2026-05-20):
  - "All accounts start out on the free plan which comes with a 1000 API requests per hour limitation. No credit card is required to sign up."
  - The free "Fixtures" plan covers "Calendar: Future and past match schedule" and "Pre-match Data: Information on tournaments, team and players".
  - "Post-match Data: Results and detailed per-game data" and computed statistics start at "From 400€ per videogame per month".
- **The catch:** the free tier gives schedules and teams. Per-game results and stats are paid. The docs page also says "The Fixtures Only plan is available to all users for free." Whether final series scores come with fixtures is not confirmed (see section 3).
- **Betting:** "These stats plans are only available to customers with non betting-related usage." Not an issue here, but it means an ML predictions page must never look like odds.
- **Terms on automated access, attribution and republishing:** **not obtained.** The terms page was unreachable live and has no Wayback copy. Web search turned up nothing either.
- **Live test:** not possible here.
- **Verdict: UNCLEAR.** The API is clearly intended for automated use, but I could not read the republishing and attribution terms. Read them at signup before using it on a public site.

### Twitch Helix API
- **Access:** REST. `GET /helix/streams?language=ar` gives live streams with `viewer_count` and `game_name`.
- **Auth:** a Client ID plus an app access token from id.twitch.tv (client credentials flow).
- **Live test:** without a token, the server answered `401 {"message":"OAuth token is missing"}` (saved in `samples/twitch/`). No live Arabic stream data was collected: I have no credentials, and the token endpoint is intercepted on this network.
- **Rate limit:** about 800 points per minute for app tokens, from my memory of Twitch docs. Not verified this session.
- **Terms** (Developer Agreement, copy 2025-03-10):
  - Storage: "Do not store copies of Twitch Content or Program Materials, unless you: (a) obtain prior written authorization from Twitch ...; (b) control the rights associated with such content; or (c) cache such information for only a twenty-four hour time period without further sharing it with third parties."
  - Research use needs approval: "Twitch will consider authorizing you to use the Twitch APIs to engage in the following activities only after entering into a separate agreement and running through an approval process: ... Research - educational and non-commercial projects that examine trends over specific time periods."
  - Commercial use: "Twitch Data ... or insights derived from that data, may not be sold, licensed, monetized, distributed for commercial purposes ... without Twitch's prior written permission."
  - Attribution: "You must ensure that there is a clear path to the source from displays of Program Materials in Your Services."
- **Verdict:**
  - **ALLOWED** for a live "who is streaming in Arabic right now" widget that links back to Twitch.
  - **NOT ALLOWED without Twitch approval** for the planned "viewership snapshots" archive. Keeping viewer counts past 24 hours and showing trends over time is the exact "Research" case that needs a separate agreement.
  - Apply for that approval early, or limit the feature to live data plus a 24 hour window.

### OpenDota
- **Access:** REST at api.opendota.com. It also has a SQL "explorer" endpoint over its pro match database.
- **Auth:** none needed. A key raises the limits.
- **Free tier, measured from response headers:** `X-Rate-Limit-Remaining-Minute: 59`, `X-Rate-Limit-Remaining-Day: 2999`, so 60 per minute and 3000 per day.
- **Terms:** the API intro says only "You can use the API without a key, but registering for a key allows increased rate limits and usage." I found no written terms on republishing or attribution. The project is open source and the underlying data comes from Valve's public match data.
- **Live test:** worked. About 12 requests, spaced out.
- **Verdict: ALLOWED** for reading and showing match data, with a credit to OpenDota as good practice. It covers only one game (Dota 2).

### Start.gg
- **Access:** GraphQL API at api.start.gg.
- **Auth:** a personal token from Developer Settings. Tokens "expire after 1 year".
- **Limits** (copy 2026-05-12): "You may not average more than 80 requests per 60 seconds." and "maximum of 1000 objects per request".
- **Terms on automated access, republishing and commercial use:** **not obtained** (no archived copy, nothing found by search).
- **Relevance:** Start.gg mostly hosts grassroots and fighting game brackets. Saudi fighting game and Saudi eLeague community events sometimes run on it. Top tier Saudi club matches are not there.
- **Live test:** not possible here.
- **Verdict: UNCLEAR** on terms, and **low value** for the core project.

### Official EWC website (esportsworldcup.com)
- **Access:** HTML pages only. No public API is documented.
- **robots.txt** (copy 2025-12-17): `User-agent: * / Disallow:`, which allows all crawling.
- **Terms** (copy 2026-09-23): you agree not to use the site "To engage in any data mining, harvesting, scraping, or other unauthorized collection of data or personal data." Also: "data compilations, are the property of the Esports World Cup website ... and are protected by Saudi Arabia and international copyright laws."
- **Verdict: NOT ALLOWED** for automated collection. The robots.txt is permissive, but the terms forbid scraping. Use the site as a human reference, and get EWC results from Liquipedia instead.

### Riot Games API
- **Access:** REST with a developer key. A production key requires a registered and approved product.
- **Terms** (General Policies, updated 2025-03-11):
  - "All products must be registered in, and audited by Riot Games through the Developer Portal".
  - You must show the line "[Your product] isn't endorsed by Riot Games ...".
  - "Your product cannot feature betting or gambling functionality."
  - Monetization is allowed once approved.
- **Relevance:** the Riot API serves ranked and player data, not professional esports match results. Pro LoL and Valorant results come from Liquipedia or PandaScore. The "LoL Esports" endpoints people use are unofficial and undocumented.
- **Verdict: ALLOWED in principle** after registration, but **not useful** for Saudi pro team results.

### Battlefy
- **Access:** no public, documented API found. The site's web app calls internal endpoints.
- **Terms:** not obtained (intercepted, no archive copy found).
- **Verdict: UNCLEAR, treat as NOT ALLOWED.** With no documented API, only undocumented endpoints would be left. It also mostly hosts amateur events.

### Esports Charts (escharts.com)
- **Access:** website, plus paid data services.
- **Terms** (copy 2023-12-04, the newest available):
  - "you may not: (a) use any data mining, robots or similar data gathering or extraction methods".
  - The license is "for your personal or internal business use only".
  - "The publication of the received data with the obligatory indication of the source of such data is possible only after establishing a written agreement".
- **Verdict: NOT ALLOWED** without a paid written agreement.

### Others noted, not tested
- **HLTV and VLR.gg:** intercepted, so their current terms were not checked. Both are known to forbid scraping and have no public API. Do not plan on them.
- **TwitchTracker:** a third-party site with an Arabic language channel ranking. It is a scraper of Twitch itself, and its terms were not checked. Use it only to sanity check numbers by hand, not as a data feed.
- **Steam Web API (Dota match history):** intercepted. OpenDota already covers this data.

## 2. Samples fetched

### Saudi and MENA teams (OpenDota, Dota 2, live)
Files are in `samples/opendota/`.

| OpenDota team_id | Name in OpenDota | Pro maps on record | Last map |
|---|---|---|---|
| 9247354 | Team Falcons | 889 | 2026-08-21 (TI 2026, lost 0-3 to Team Liquid) |
| 10074801 | FALCONS PRIME | 3 | 2026-03 |
| 9368468 | Twisted Minds | 125 | 2024-07 |
| 9445138 | Twisted Minds | 7 | 2024-06 |
| 9080826 | Twisted Minds | 6 | 2023-06 |
| 10136357 | Nigma Galaxy (with a trailing space in the name) | 77 | 2026-08 (TI 2026) |
| 7554697 / 10000118 | Nigma Galaxy (older IDs) | 1207 / 16 | 2026-05 / 2025-12 |
| 10182732 | Team Saudi Arabia | 9 | 2026-07 |
| 9130799 | Saudi Arabia | 3 | 2023-07 |
| 9367616 | GAMAX SAUDI | 6 | 2024-03 |

- **Roster check:** `/teams/9247354/players` flags only two current members of Team Falcons (Cr1t- and Malr1ne). A Dota roster has five, so the "current member" flag is unreliable.

### EWC Club Championship (web search, official press release and news)
File: `samples/ewc/club_championship_top5.json`.

| Year | Winner | Runner-up | Note |
|---|---|---|---|
| 2024 | Team Falcons (5665 pts per Hotspawn) | Team Liquid (2545) | Point totals differ between outlets |
| 2025 | Team Falcons (5200) | Team Liquid (4200) | Twisted Minds was around 3200 before the final week. Final total not confirmed. |
| 2026 (Jul 6 to Aug 23) | AG.AL International (5300) | Team Falcons (4600) | Winner confirmed by the official EWC press release. Decided by Trackmania on the last day. |

- **Per-game results were not collected.** Liquipedia is the right source for those (one page per game per year), and it was unreachable. Outlets also disagree on 2024 point totals, a good reminder to take numbers from one structured source.

### Twitch Arabic streams
- **No live sample** (no token, and the token host is intercepted).
- **Indirect signal from search:** TwitchTracker's Arabic channel ranking for October 2026 runs to at least 41 pages, with channels near rank 1000 to 2000 averaging about 10 to 14 viewers. The top Arabic personality channels (for example YZNSA, m5aoi, RakanooLive) average in the low thousands.
- These numbers are rough. They come from search snippets, not measurement.

## 3. Tests ("test, do not trust")

### Are names and IDs consistent across sources?
- **Within OpenDota alone: no.**
  - Twisted Minds has three team IDs, and Nigma Galaxy has four.
  - Names carry stray spaces ("Nigma Galaxy ", "ANBU DIVISION ").
  - Similar names collide: "Falcons Prime", "FalconBlade" and "Falcon eSports" are different teams.
  - A national "Team Saudi Arabia" has two IDs.
- **Across sources:** not testable live today. Every source uses its own IDs: OpenDota uses Valve team_ids, Liquipedia uses page names per game wiki, and PandaScore uses its own numeric IDs.
- **Org vs. roster:** Team Falcons is a single club, but it exists as separate team entities per game in every source.
- **Plan for an ID mapping table** you maintain by hand: org, then game, then the ID in each source, with date ranges. Liquipedia page names are the most stable anchor.

### Which games have enough match history to train a prediction model for Saudi teams?
- **Dota 2 (Team Falcons): yes.**
  - 889 pro maps on record. From April 2024 to August 2026, about 710 maps in 29 months, roughly 25 maps per month.
  - OpenDota gives every map with both team IDs and the winner, plus rich per-map stats.
  - This is the strongest case, and it is free.
- **CS2 (Team Falcons): likely yes, needs Liquipedia or PandaScore.**
  - Falcons is a top tier CS2 team with constant events. Search found ESL Pro League S24 on Oct 3, the Thunderpick World Championship mid-October, and IEM Cologne Major 2026 champions in June.
  - Match count not measured.
- **Rainbow Six Siege and Overwatch (Twisted Minds): probably enough for a simple Elo-style model, not for anything fancy.**
  - Twisted Minds plays the R6 Europe and MENA League and reached a BLAST R6 Major. They won OWCS World Finals 2025. Regular league play exists.
  - Not measured.
- **Rocket League (Twisted Minds, Falcons):** both qualified for the 2026 Boston Major. Plausible, not measured.
- **Dota 2 (Twisted Minds):** no. Its last map was in July 2024.
- **Game-hopping titles** (Fortnite, Apex, EA FC, fighting games, chess): these are individual or battle-royale formats. A match-winner model does not fit them.

### How many Saudi-team matches happen per week outside EWC season?
- **Measured for Dota 2 only:**
  - Team Falcons averages about 5 to 6 maps per week across the year, roughly 2 series.
  - Its schedule has real gaps. No maps in June 2024, June 2025, September 2026 or October 2026 (to the 26th). June is the lead-up to EWC. Sept and Oct 2026 come after TI.
  - Every Saudi and MENA Dota ID I checked has zero maps since TI 2026 ended in late August, while the global pro scene played 43 to 345 maps per week in the same weeks.
- **Across all games (estimate, not measured):**
  - Falcons fields many rosters and CS2 alone runs most weeks of the year, so the org likely plays several series per week across games.
  - Dota 2 alone, the one free and fully legal source, can go silent for two months.

### How many Arabic Twitch streams are live at a typical time, and how big are they?
- **Not measured.** It needs a Twitch app token from a network that does not intercept id.twitch.tv.
- To measure it, page through `GET /helix/streams?language=ar&first=100` until the cursor ends. Do this at a few times of day, and count streams and the sum of `viewer_count`.
- Any count you keep past 24 hours falls under the storage limit above.

## 4. Ranking and verdict

| Rank | Source | Verdict | Why |
|---|---|---|---|
| 1 | Liquipedia API (LPDB key) | ALLOWED with attribution | The only legal source covering every game, EWC history and MENA teams. CC-BY-SA. Free access needs an approved application, a non-commercial site and open-source code, and may be time limited. |
| 2 | OpenDota | ALLOWED | Free, keyless, generous limits, deep history. Dota 2 only. |
| 3 | PandaScore | UNCLEAR | Good API with a free schedule tier, but results are paid (from 400 EUR per game per month) and the terms were not read. |
| 4 | Twitch Helix | ALLOWED for live display, NOT ALLOWED for a stored history without approval | 24 hour cache rule plus the "Research" approval clause. |
| 5 | Riot API | ALLOWED after registration | Does not cover pro results. |
| 6 | Start.gg | UNCLEAR | Terms not read. Grassroots events only. |
| 7 | Battlefy | UNCLEAR, treat as NOT ALLOWED | No public API. |
| 8 | EWC website | NOT ALLOWED (automated) | The terms forbid scraping. |
| 9 | Esports Charts | NOT ALLOWED | Robots and data mining banned, publication needs a written deal. |

**Is there enough steady, legal data for a year-round project? Partly.**

- **Team and match tracking:** this can run year round, but only if Liquipedia grants an LPDB key (or you pay PandaScore). Falcons and Twisted Minds play in CS2, R6, Overwatch, Rocket League and other titles outside EWC, so there is regular content most weeks. Without Liquipedia, the only free legal feed is OpenDota, and Saudi Dota activity goes completely quiet for weeks at a time (zero maps in Sept and Oct 2026).
- **EWC history:** small and static (three editions). Liquipedia covers it well, and so does a hand-maintained table.
- **ML predictions:** realistic for Falcons in Dota 2 now, and likely for Falcons CS2 once LPDB access exists. Sample sizes for other Saudi rosters are probably thin. Keep predictions clearly non-betting: both Liquipedia and PandaScore refuse betting projects.
- **Arabic Twitch viewership history:** the weakest part. A live "now streaming" view is fine. A stored, year-round snapshot archive needs written approval from Twitch first.

**Before building, do these on a network without TLS interception:**
1. Apply for a Liquipedia LPDB key, describing the project as non-commercial and open source.
2. Create a free PandaScore account. Read its terms, and test whether the free tier includes final series scores.
3. Register a Twitch app, measure Arabic live streams at three times of day, and ask Twitch about research approval.
4. Re-run the OpenDota counts monthly to see whether the Sept and Oct 2026 Dota gap is an off-season or a roster change.

## Sources used
- Liquipedia API terms, API page and robots.txt (Wayback copies dated above)
- PandaScore pricing and docs intro (Wayback)
- Twitch Developer Agreement (Wayback, 2025-03-10)
- Start.gg rate limit and authentication docs (Wayback)
- Riot General Policies (Wayback, 2026-07-14)
- EWC terms and robots.txt (Wayback)
- Esports Charts terms (Wayback, 2023-12-04)
- OpenDota live API
- [AG.AL Crowned EWC 26 Club Champion (EWC)](https://esportsworldcup.com/en/press-releases/agal-crowned-ewc26-club-champion)
- [Dot Esports EWC 2026 standings](https://dotesports.com/news/news/ewc-standings-ag-al-win)
- [Hotspawn EWC 2025](https://www.hotspawn.com/?p=94619)
- [Hotspawn EWC 2024](https://www.hotspawn.com/?p=71313)
- [SiegeGG on Twisted Minds](https://siege.gg/news/twisted-minds-qualify-for-blast-r6-major-salt-lake-city)
- [Strafe Falcons vs TyLoo](https://www.strafe.com/match/team-falcons-vs-tyloo-swiss-2026-esl-pro-league-season-24-755b13/)
- [TwitchTracker Arabic ranking](https://twitchtracker.com/channels/viewership/arabic?page=40)
