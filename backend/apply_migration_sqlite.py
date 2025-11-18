"""
Lightweight migration script that uses only the Python standard library
to create the SQLite schema and insert rows from `frames_data.json`.

This avoids requiring Flask/SQLAlchemy to be installed so the migration
can be executed in minimal environments. It supports `--backup` and
`--force` semantics similar to the main migration CLI.
"""
import argparse
import json
import os
import shutil
import sqlite3
from datetime import datetime


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'frames_data.json')
DB_FILE = os.path.join(BASE_DIR, 'frames.db')


def backup_file(path):
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    dst = f"{path}.bak-{ts}"
    shutil.copy2(path, dst)
    return dst


def ensure_tables(conn):
    cur = conn.cursor()
    # Use TEXT for JSON/meta columns for broad compatibility
    cur.execute('''
    CREATE TABLE IF NOT EXISTS teams (
        id TEXT PRIMARY KEY,
        university_id TEXT,
        discipline TEXT,
        lifecycle TEXT,
        name TEXT,
        size INTEGER,
        experience INTEGER,
        description TEXT,
        created_at TEXT,
        meta TEXT
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS faculty (
        id TEXT PRIMARY KEY,
        university_id TEXT,
        name TEXT,
        role TEXT,
        description TEXT,
        created_at TEXT,
        meta TEXT
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        university_id TEXT,
        name TEXT,
        type TEXT,
        duration INTEGER,
        description TEXT,
        created_at TEXT,
        meta TEXT
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS interfaces (
        id TEXT PRIMARY KEY,
        university_id TEXT,
        from_entity TEXT,
        to_entity TEXT,
        interface_type TEXT,
        bond_type TEXT,
        energy_loss INTEGER,
        created_at TEXT,
        meta TEXT
    )
    ''')

    conn.commit()


def migrate(data, conn, force=False):
    cur = conn.cursor()
    counts = {'teams': 0, 'faculty': 0, 'projects': 0, 'interfaces': 0}

    # Upsert via INSERT OR REPLACE
    for t in data.get('teams', []):
        cur.execute('''INSERT OR REPLACE INTO teams
            (id, university_id, discipline, lifecycle, name, size, experience, description, created_at, meta)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            t.get('id'),
            t.get('university_id'),
            t.get('discipline'),
            t.get('lifecycle'),
            t.get('name'),
            t.get('size'),
            t.get('experience'),
            t.get('description'),
            t.get('created_at'),
            json.dumps(t.get('meta')) if t.get('meta') is not None else None,
        ))
        counts['teams'] += 1

    for f in data.get('faculty', []):
        cur.execute('''INSERT OR REPLACE INTO faculty
            (id, university_id, name, role, description, created_at, meta)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            f.get('id'),
            f.get('university_id'),
            f.get('name'),
            f.get('role'),
            f.get('description'),
            f.get('created_at'),
            json.dumps(f.get('meta')) if f.get('meta') is not None else None,
        ))
        counts['faculty'] += 1

    for p in data.get('projects', []):
        cur.execute('''INSERT OR REPLACE INTO projects
            (id, university_id, name, type, duration, description, created_at, meta)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            p.get('id'),
            p.get('university_id'),
            p.get('name'),
            p.get('type'),
            p.get('duration'),
            p.get('description'),
            p.get('created_at'),
            json.dumps(p.get('meta')) if p.get('meta') is not None else None,
        ))
        counts['projects'] += 1

    for i in data.get('interfaces', []):
        cur.execute('''INSERT OR REPLACE INTO interfaces
            (id, university_id, from_entity, to_entity, interface_type, bond_type, energy_loss, created_at, meta)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            i.get('id'),
            i.get('university_id'),
            i.get('from') or i.get('from_entity'),
            i.get('to') or i.get('to_entity'),
            i.get('interfaceType') or i.get('interface_type'),
            i.get('bondType') or i.get('bond_type'),
            i.get('energyLoss') or i.get('energy_loss'),
            i.get('created_at'),
            json.dumps(i.get('meta')) if i.get('meta') is not None else None,
        ))
        counts['interfaces'] += 1

    conn.commit()
    return counts


def main():
    parser = argparse.ArgumentParser(description='Apply migration into SQLite DB (lightweight, no external deps)')
    parser.add_argument('--backup', action='store_true', help='Backup frames_data.json before migrating')
    parser.add_argument('--force', action='store_true', help='Write to DB (default: dry-run if not provided)')
    args = parser.parse_args()

    if not os.path.exists(DATA_FILE):
        print('Source file not found:', DATA_FILE)
        return 1

    if args.backup:
        dst = backup_file(DATA_FILE)
        print('Backup created at:', dst)

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Ensure DB directory exists
    db_dir = os.path.dirname(DB_FILE)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    try:
        ensure_tables(conn)

        if not args.force:
            # Dry-run: just report counts
            counts = {
                'teams': len(data.get('teams', [])),
                'faculty': len(data.get('faculty', [])),
                'projects': len(data.get('projects', [])),
                'interfaces': len(data.get('interfaces', [])),
            }
            print('Dry-run mode. Counts:', counts)
            return 0

        counts = migrate(data, conn, force=True)
        print('Migration applied. Counts:', counts)
        return 0

    finally:
        conn.close()


if __name__ == '__main__':
    raise SystemExit(main())
