#!/usr/bin/env python3
"""Verify FRAMES migration: print table counts and sample rows.

Usage:
  python scripts/verify_migration.py [--db PATH] [--limit N] [--json]

Defaults:
  --db  ../backend/frames.db  (relative to this script file)
  --limit 5
"""
import argparse
import json
import os
import sqlite3
from pathlib import Path


def detect_default_db():
    base = Path(__file__).resolve().parent.parent
    return str((base / 'backend' / 'frames.db').resolve())


def table_exists(conn, name):
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,))
    return cur.fetchone() is not None


def get_tables(conn):
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    return [r[0] for r in cur.fetchall()]


def sample_rows(conn, table, limit=5):
    cur = conn.execute(f"SELECT * FROM {table} LIMIT ?", (limit,))
    cols = [d[0] for d in cur.description] if cur.description else []
    rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    return rows


def count_table(conn, table):
    cur = conn.execute(f"SELECT COUNT(*) FROM {table}")
    return cur.fetchone()[0]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--db', default=detect_default_db(), help='Path to SQLite DB')
    p.add_argument('--limit', type=int, default=5, help='Sample rows per table')
    p.add_argument('--json', action='store_true', help='Output machine-friendly JSON')
    args = p.parse_args()

    if not os.path.exists(args.db):
        print('DB not found:', args.db)
        raise SystemExit(1)

    conn = sqlite3.connect(args.db)
    try:
        conn.row_factory = sqlite3.Row
        tables = get_tables(conn)

        # Prefer known FRAMES tables ordering
        known = ['teams', 'faculty', 'projects', 'interfaces', 'sandboxes']
        ordered = [t for t in known if t in tables] + [t for t in tables if t not in known]

        out = {'db': args.db, 'tables': {}}

        for t in ordered:
            try:
                cnt = count_table(conn, t)
                samples = sample_rows(conn, t, limit=args.limit)
            except Exception as e:
                cnt = None
                samples = []
            out['tables'][t] = {'count': cnt, 'samples': samples}

        if args.json:
            print(json.dumps(out, indent=2, ensure_ascii=False))
        else:
            print(f"DB: {args.db}")
            for t, info in out['tables'].items():
                print(f"\nTable: {t}")
                print(f"  Count: {info['count']}")
                print(f"  Samples (up to {args.limit}):")
                if not info['samples']:
                    print('    (no rows)')
                else:
                    for r in info['samples']:
                        # compact json per row
                        print('   -', json.dumps(r, ensure_ascii=False))

    finally:
        conn.close()


if __name__ == '__main__':
    main()
