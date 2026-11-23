"""
Clearance and Access Roster Auditor
CYB333 Security Automation

Reads a personnel security roster from a CSV file and flags compliance
problems that a Program Security Representative would otherwise catch by
reading the spreadsheet line by line.

This early version implements the clearance expiration check. The
overdue-training check and the access-removal check are still in progress
and are marked with TODO notes below.

Test data only. Do not run this against a roster that contains real
personnel information, and never commit real data, passwords, or keys to
the repository.
"""

import csv
from datetime import datetime

# Date format used in the roster file (for example 2026-11-19).
DATE_FORMAT = "%Y-%m-%d"

# How far ahead, in days, to warn about a clearance that is about to expire.
WARNING_WINDOW_DAYS = 30


def load_roster(path):
    """Read the roster CSV and return a list of record dictionaries."""
    records = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
    except FileNotFoundError:
        print(f"Could not find the roster file: {path}")
    return records


def parse_date(value):
    """Turn a date string into a date, or return None if it is blank or invalid."""
    value = (value or "").strip()
    if not value:
        return None
    try:
        return datetime.strptime(value, DATE_FORMAT).date()
    except ValueError:
        print(f"Skipping a record with an unreadable date: {value}")
        return None


def check_clearance_expiration(records, today, window_days):
    """Flag anyone whose clearance is expired or expiring within the window."""
    flagged = []
    for person in records:
        expires = parse_date(person.get("clearance_expiration_date"))
        if expires is None:
            continue
        days_left = (expires - today).days
        if days_left < 0:
            flagged.append((person["name"], "EXPIRED", expires))
        elif days_left <= window_days:
            flagged.append((person["name"], f"expiring in {days_left} days", expires))
    return flagged


def main():
    today = datetime.now().date()
    records = load_roster("sample_roster.csv")
    print(f"Loaded {len(records)} records. Audit date {today}.\n")

    print(f"Clearance expiration check (warning window {WARNING_WINDOW_DAYS} days)")
    results = check_clearance_expiration(records, today, WARNING_WINDOW_DAYS)
    if not results:
        print("  No clearances are expired or expiring inside the window.")
    for name, status, expires in results:
        print(f"  {name:<18} {status:<22} (expires {expires})")

    # TODO (final week): add a check for overdue annual training.
    # TODO (final week): add a check for Active access on an expired clearance.
    # TODO (final week): group the results by issue type and write them to an output file.


if __name__ == "__main__":
    main()
