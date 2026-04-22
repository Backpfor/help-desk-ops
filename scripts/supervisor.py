#!/usr/bin/env python3
"""
Supervision Agent – Help Desk Ops
Checks: reminders due, priority backlog, booking format compliance.
"""

import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
TASKS_DIR = BASE_DIR / "tasks"
BOOKINGS_DIR = BASE_DIR / "bookings"

PRIORITY_COUNTRIES = {"DE", "PL", "ES"}
REMINDER_DELAY_DAYS = 3
BUCHUNG_RE = re.compile(
    r'^[A-Z]{2}\|'
    r'(\d+|FILLER|WH [^|]+)\|'
    r'(Phone|Email|Onsite)\|'
    r'[^|]+\|'   # customer
    r'[^|]+\|'   # hw/sw
    r'[^|]+\|'   # problem
    r'[^|]+\|'   # solution
    r'.+'        # fazit
)


def parse_table(filepath: Path) -> list[dict]:
    headers, rows = [], []
    for line in filepath.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not headers:
            headers = cells
        elif re.match(r'^[-| ]+$', line):
            continue
        elif any(c for c in cells):
            rows.append(dict(zip(headers, cells)))
    return rows


def reminders_due() -> list[dict]:
    fp = TASKS_DIR / "in-progress.md"
    if not fp.exists():
        return []
    alerts = []
    today = date.today()
    for row in parse_table(fp):
        seit = row.get("Seit", "").strip()
        if not seit:
            continue
        try:
            opened = datetime.strptime(seit, "%Y-%m-%d").date()
            days = (today - opened).days
            if days >= REMINDER_DELAY_DAYS:
                alerts.append({
                    "id":      row.get("ID", "?"),
                    "title":   row.get("Titel", "?"),
                    "country": row.get("Land", "?"),
                    "store":   row.get("Filiale", "?"),
                    "days":    days,
                })
        except ValueError:
            pass
    return alerts


def priority_backlog() -> list[dict]:
    fp = TASKS_DIR / "backlog.md"
    if not fp.exists():
        return []
    return [
        row for row in parse_table(fp)
        if row.get("Land", "").strip().upper() in PRIORITY_COUNTRIES
        and row.get("Titel", "").strip()
    ]


def format_issues() -> list[dict]:
    issues = []
    for fp in BOOKINGS_DIR.rglob("*.md"):
        for i, raw in enumerate(fp.read_text(encoding="utf-8").splitlines(), 1):
            line = raw.strip()
            if re.match(r'^[A-Z]{2}\|', line) and not BUCHUNG_RE.match(line):
                issues.append({"file": fp.name, "line": i, "preview": line[:80]})
    return issues


def run():
    today = date.today().isoformat()
    sep = "=" * 62
    print(f"\n{sep}")
    print(f"  SUPERVISION REPORT – {today}")
    print(f"{sep}\n")

    # ── 1. Reminders due ────────────────────────────────────────
    due = reminders_due()
    print(f"⏰  REMINDERS DUE  ({len(due)})")
    if due:
        for r in due:
            print(f"    [{r['country']}] Store {r['store']} | {r['id']} – {r['title']}"
                  f"  →  open {r['days']} day(s)")
    else:
        print("    ✅  No reminders due.")

    # ── 2. Priority backlog ──────────────────────────────────────
    prio = priority_backlog()
    print(f"\n🚨  PRIORITY TASKS IN BACKLOG  ({len(prio)})")
    if prio:
        for p in prio:
            print(f"    [{p.get('Land','?')}] {p.get('ID','?')} – {p.get('Titel','?')}"
                  f"  (priority: {p.get('Priorität','?')})")
    else:
        print("    ✅  No priority tasks waiting.")

    # ── 3. Booking format ────────────────────────────────────────
    bad = format_issues()
    print(f"\n📋  BOOKING FORMAT ISSUES  ({len(bad)})")
    if bad:
        for b in bad:
            print(f"    {b['file']} line {b['line']}: {b['preview']}")
    else:
        print("    ✅  All bookings correctly formatted.")

    print(f"\n{sep}\n")

    # Exit 1 if anything requires attention (useful for CI)
    if due or prio or bad:
        sys.exit(1)


if __name__ == "__main__":
    run()
