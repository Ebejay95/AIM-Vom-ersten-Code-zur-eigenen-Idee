#!/usr/bin/env python3
"""
update_scores.py
Nutzung:
  python utils/update_scores.py <aufgabe_name> <status>

<status> = "passed" | "failed"

Wirkung:
- Erhöht attempts für die Aufgabe um 1
- Setzt solved=True bei passed, sonst False
- Legt .scores.json an, falls nicht vorhanden
"""

import json
import os
import sys
from datetime import datetime

SCORES_FILE = ".scores.json"

def load_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r", encoding="utf-8") as f:
                return json.load(f) or {}
        except Exception:
            return {}
    return {}

def save_scores(scores):
    tmp = SCORES_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2, sort_keys=True)
    os.replace(tmp, SCORES_FILE)

def main():
    if len(sys.argv) != 3:
        print("Usage: python utils/update_scores.py <aufgabe_name> <passed|failed>")
        sys.exit(2)

    name = sys.argv[1].strip()
    status = sys.argv[2].strip().lower()
    passed = status == "passed"

    scores = load_scores()
    entry = scores.get(name, {"attempts": 0, "solved": False})
    entry["attempts"] = int(entry.get("attempts", 0)) + 1
    entry["solved"] = bool(passed)
    entry["updated_at"] = datetime.utcnow().isoformat() + "Z"
    scores[name] = entry
    save_scores(scores)

    print(f"[scores] {name}: attempts={entry['attempts']} solved={entry['solved']}")

if __name__ == "__main__":
    main()
