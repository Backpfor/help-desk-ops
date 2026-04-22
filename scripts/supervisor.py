#!/usr/bin/env python3
"""
Supervision Agent – Help Desk Ops

Workflow enforced before a task can move to Done:
  Buchung ✅  →  Mail ✅  →  Reminder ✅ (if no response after 3 days)

Checks:
  1. Tasks missing Buchung or Mail in in-progress
  2. Tasks in Done that bypassed the workflow (missing Buchung or Mail)
  3. Reminders due (in-progress since >= 3 days, mail sent, no reminder yet)
  4. Priority countries stuck in backlog (DE, PL, ES)
  5. Booking format compliance

Mail style standard (enforced at generation, reminded here):
  - Short, simple, non-technical
  - 2-3 sentences: general cause + action taken + result
  - Always end with confirmation request to client
  - Language: DE → Deutsch | FR → Français | all others → English
"""

import re
import sys
from datetime import date, datetime
from pathlib import Path

BASE_DIR        = Path(__file__).parent.parent
TASKS_DIR       = BASE_DIR / "tasks"
BOOKINGS_DIR    = BASE_DIR / "bookings"

PRIORITY_COUNTRIES  = {"DE", "PL", "ES"}
REMINDER_DELAY_DAYS = 3

BUCHUNG_RE = re.compile(
    r'^[A-Z]{2}\|'
    r'(\d+|FILLER|WH [^|]+)\|'
    r'(Phone|Email|Onsite)\|'
    r'[^|]+\|'
    r'[^|]+\|'
    r'[^|]+\|'
    r'[^|]+\|'
    r'.+'
)


# ── helpers ──────────────────────────────────────────────────────────────────

def parse_table(fp: Path) -> list[dict]:
    headers, rows = [], []
    for line in fp.read_text(encoding="utf-8").splitlines():
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

def flag(val: str) -> bool:
    return val.strip().lower() in {"✅", "oui", "yes", "x", "ok", "done"}


# ── checks ───────────────────────────────────────────────────────────────────

def check_workflow_in_progress() -> list[dict]:
    """Tasks in In Progress missing Buchung or Mail."""
    fp = TASKS_DIR / "in-progress.md"
    if not fp.exists():
        return []
    issues = []
    for row in parse_table(fp):
        if not row.get("Titel", "").strip():
            continue
        missing = []
        if not flag(row.get("Buchung", "")):
            missing.append("Buchung")
        if not flag(row.get("Mail", "")):
            missing.append("Mail")
        if missing:
            issues.append({
                "id":      row.get("ID", "?"),
                "title":   row.get("Titel", "?"),
                "country": row.get("Land", "?"),
                "missing": missing,
            })
    return issues


def check_workflow_done() -> list[dict]:
    """Tasks in Done that skipped Buchung or Mail."""
    fp = TASKS_DIR / "done.md"
    if not fp.exists():
        return []
    issues = []
    for row in parse_table(fp):
        if not row.get("Titel", "").strip():
            continue
        missing = []
        if not flag(row.get("Buchung", "")):
            missing.append("Buchung")
        if not flag(row.get("Mail", "")):
            missing.append("Mail")
        if missing:
            issues.append({
                "id":      row.get("ID", "?"),
                "title":   row.get("Titel", "?"),
                "country": row.get("Land", "?"),
                "missing": missing,
            })
    return issues


def check_reminders_due() -> list[dict]:
    """In-progress tasks: mail sent, no reminder yet, open >= 3 days."""
    fp = TASKS_DIR / "in-progress.md"
    if not fp.exists():
        return []
    today = date.today()
    due = []
    for row in parse_table(fp):
        if not row.get("Titel", "").strip():
            continue
        if not flag(row.get("Mail", "")):
            continue
        if flag(row.get("Reminder", "")):
            continue
        seit = row.get("Seit", "").strip()
        try:
            opened = datetime.strptime(seit, "%Y-%m-%d").date()
            days = (today - opened).days
            if days >= REMINDER_DELAY_DAYS:
                due.append({
                    "id":      row.get("ID", "?"),
                    "title":   row.get("Titel", "?"),
                    "country": row.get("Land", "?"),
                    "store":   row.get("Filiale", "?"),
                    "days":    days,
                })
        except ValueError:
            pass
    return due


def check_priority_backlog() -> list[dict]:
    """Priority country tasks sitting in Backlog."""
    fp = TASKS_DIR / "backlog.md"
    if not fp.exists():
        return []
    return [
        row for row in parse_table(fp)
        if row.get("Land", "").strip().upper() in PRIORITY_COUNTRIES
        and row.get("Titel", "").strip()
    ]


def check_booking_format() -> list[dict]:
    """Buchungen in bookings/ that don't match the expected format."""
    issues = []
    for fp in BOOKINGS_DIR.rglob("*.md"):
        for i, raw in enumerate(fp.read_text(encoding="utf-8").splitlines(), 1):
            line = raw.strip()
            if re.match(r'^[A-Z]{2}\|', line) and not BUCHUNG_RE.match(line):
                issues.append({"file": fp.name, "line": i, "preview": line[:80]})
    return issues


# ── report ───────────────────────────────────────────────────────────────────

def run():
    today = date.today().isoformat()
    sep = "=" * 64
    print(f"\n{sep}")
    print(f"  SUPERVISION REPORT – {today}")
    print(f"{sep}\n")

    errors = 0

    # 1. Workflow violations – In Progress
    wf_ip = check_workflow_in_progress()
    print(f"🔴  WORKFLOW INCOMPLETE – IN PROGRESS  ({len(wf_ip)})")
    if wf_ip:
        for w in wf_ip:
            print(f"    [{w['country']}] {w['id']} – {w['title']}"
                  f"  →  missing: {', '.join(w['missing'])}")
        errors += len(wf_ip)
    else:
        print("    ✅  All in-progress tasks have Buchung + Mail.")

    # 2. Workflow violations – Done
    wf_done = check_workflow_done()
    print(f"\n🔴  WORKFLOW INCOMPLETE – DONE  ({len(wf_done)})")
    if wf_done:
        for w in wf_done:
            print(f"    [{w['country']}] {w['id']} – {w['title']}"
                  f"  →  missing: {', '.join(w['missing'])}")
        errors += len(wf_done)
    else:
        print("    ✅  All done tasks correctly completed.")

    # 3. Reminders due
    due = check_reminders_due()
    print(f"\n⏰  REMINDERS DUE  ({len(due)})")
    if due:
        for r in due:
            print(f"    [{r['country']}] Store {r['store']} | {r['id']} – {r['title']}"
                  f"  →  open {r['days']} day(s)")
        errors += len(due)
    else:
        print("    ✅  No reminders due.")

    # 4. Priority backlog
    prio = check_priority_backlog()
    print(f"\n🚨  PRIORITY TASKS IN BACKLOG  ({len(prio)})")
    if prio:
        for p in prio:
            print(f"    [{p.get('Land','?')}] {p.get('ID','?')} – {p.get('Titel','?')}"
                  f"  (priority: {p.get('Priorität','?')})")
        errors += len(prio)
    else:
        print("    ✅  No priority tasks waiting.")

    # 5. Booking format
    bad = check_booking_format()
    print(f"\n📋  BOOKING FORMAT ISSUES  ({len(bad)})")
    if bad:
        for b in bad:
            print(f"    {b['file']} line {b['line']}: {b['preview']}")
        errors += len(bad)
    else:
        print("    ✅  All bookings correctly formatted.")

    # 6. Mail style reminder
    print(f"\n📧  MAIL STYLE REMINDER")
    print( "    Every response mail must be:")
    print( "    • Short and non-technical (no error codes, no service names)")
    print( "    • Structure: general cause → action taken → result")
    print( "    • End with confirmation request to client")
    print( "    • Language: DE→Deutsch | FR→Français | all others→English")

    print(f"\n{sep}")
    print(f"  {'⚠️  ' + str(errors) + ' issue(s) require attention.' if errors else '🎉  All checks passed.'}")
    print(f"{sep}\n")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    run()
