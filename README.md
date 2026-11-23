# Clearance and Access Roster Auditor

A small Python tool for CYB333 Security Automation that audits a personnel
security roster and flags the compliance problems a Program Security
Representative (PSR) would otherwise have to catch by reading a spreadsheet
line by line.

The goal is simple and practical. Instead of a person scanning every row for
dates that have slipped, the script reads the roster, applies a fixed set of
rules, and prints a short list of who needs attention.

## What it checks

The finished tool will run three checks against each person on the roster:

1. Clearances that are expired or expiring inside a warning window. **(working)**
2. Annual training that is overdue. *(in progress)*
3. Access still marked Active on a clearance that has already expired. *(in progress)*

Right now the clearance expiration check is built and tested. The other two
checks and the grouped report are the remaining work.

## Roster format

The tool reads a comma-separated values (CSV) file named `sample_roster.csv`
with one person per row and these columns:

| Column | Meaning |
| --- | --- |
| `name` | Person's name |
| `clearance_level` | Confidential, Secret, TS, or TS/SCI |
| `access_status` | Active or Suspended |
| `sap_indoctrination_date` | Date read into the program |
| `clearance_expiration_date` | Date the clearance lapses |
| `last_training_date` | Date of the last annual training |

All dates use the `YYYY-MM-DD` format, for example `2026-11-19`.

## Running it

```
python roster_auditor.py
```

The warning window is set near the top of `roster_auditor.py` with the
`WARNING_WINDOW_DAYS` value, which controls how many days ahead the tool warns
about a clearance that is about to expire. Making that a command-line option is
on the list for the final week.

## A note on the data

The roster in this repository is made up. The names, dates, and clearance
levels are all invented for testing, and none of it represents a real person or
a real program. The tool is meant to run only against test data or a roster you
are authorized to review. No real personnel information, passwords, or keys
belong in this repository, since the repo itself is part of the security
perimeter.

## Development setup

- Python 3.12 in an isolated Anaconda environment (`cyb333`)
- Visual Studio Code with the Python, Pylance, and Jupyter extensions
- Standard library only (`csv` and `datetime`), so there are no third-party
  dependencies to manage

## Status

This is a work in progress for the Week 3 and Week 4 project in CYB333. The
expiration check works end to end. The overdue-training check, the access
check, and an output report that groups people by the kind of problem are
still to come.
