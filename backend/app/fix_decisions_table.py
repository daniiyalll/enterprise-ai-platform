"""
Fixes a schema mismatch where the `decisions` table in the database is
missing columns that the current code expects (e.g. `username`).

This DROPS the existing `decisions` table and recreates it from the
current model — safe for a dev/test database. If you have decision
history you care about keeping, back it up first (this will delete it).

Run from the backend folder:
    python fix_decisions_table.py
"""

from app.database.connection import engine
from app.database.base import Base
from app.models.decision import Decision

print("Dropping old 'decisions' table (if it exists)...")
Decision.__table__.drop(bind=engine, checkfirst=True)

print("Recreating 'decisions' table from the current model...")
Base.metadata.create_all(bind=engine, tables=[Decision.__table__])

print("Done. The 'decisions' table now matches the current code.")
