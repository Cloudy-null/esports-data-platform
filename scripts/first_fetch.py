"""Fetch recent pro matches from OpenDota and save them as raw JSON."""

import json
import urllib.request
from pathlib import Path

URL = "https://api.opendota.com/api/proMatches"
OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "pro_matches_sample.json"


def main():
    req = urllib.request.Request(URL, headers={"User-Agent": "esports-data-platform/0.1"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        matches = json.load(resp)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(matches, indent=2), encoding="utf-8")

    print(f"Got {len(matches)} matches -> {OUT_PATH}")
    print("First 5 matches:")
    for m in matches[:5]:
        radiant = m.get("radiant_name") or "Unknown"
        dire = m.get("dire_name") or "Unknown"
        print(f"  {m['match_id']}: {radiant} vs {dire}")


if __name__ == "__main__":
    main()
