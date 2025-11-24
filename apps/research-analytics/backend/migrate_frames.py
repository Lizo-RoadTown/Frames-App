"""
Migration script to move `frames_data.json` into the SQLAlchemy DB.

Usage:
  - Dry run (default): `python migrate_frames.py`
  - Force write: `python migrate_frames.py --force`
  - Backup original file: `python migrate_frames.py --backup`

The script runs inside the Flask app context so SQLAlchemy config is used
from `app.py`. It writes a `migration_map.json` describing counts and id
mapping and prints a short verification summary.
"""
import argparse
import json
import os
import shutil
from datetime import datetime

from app import app, db, DATA_FILE
import db_models


def load_source(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def backup_file(path):
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    dst = f"{path}.bak-{ts}"
    shutil.copy2(path, dst)
    return dst


def migrate(data, dry_run=True):
    teams = data.get('teams', [])
    faculty = data.get('faculty', [])
    projects = data.get('projects', [])
    interfaces = data.get('interfaces', [])

    summary = {
        'teams': len(teams),
        'faculty': len(faculty),
        'projects': len(projects),
        'interfaces': len(interfaces),
    }

    print('Migration plan:')
    for k, v in summary.items():
        print(f'  - {k}: {v}')

    if dry_run:
        print('\nDry run mode - no DB writes will be performed.')
        return summary

    # Perform DB writes inside Flask app context
    with app.app_context():
        try:
            # Insert teams
            for t in teams:
                obj = db_models.TeamModel(
                    id=t.get('id'),
                    discipline=t.get('discipline'),
                    lifecycle=t.get('lifecycle'),
                    name=t.get('name'),
                    size=t.get('size'),
                    experience=t.get('experience'),
                    description=t.get('description'),
                    created_at=t.get('created_at')
                )
                db.session.merge(obj)

            # Insert faculty
            for f in faculty:
                obj = db_models.FacultyModel(
                    id=f.get('id'),
                    name=f.get('name'),
                    role=f.get('role'),
                    description=f.get('description'),
                    created_at=f.get('created_at')
                )
                db.session.merge(obj)

            # Insert projects
            for p in projects:
                obj = db_models.ProjectModel(
                    id=p.get('id'),
                    name=p.get('name'),
                    type=p.get('type'),
                    duration=p.get('duration'),
                    description=p.get('description'),
                    created_at=p.get('created_at')
                )
                db.session.merge(obj)

            # Insert interfaces
            for i in interfaces:
                obj = db_models.InterfaceModel(
                    id=i.get('id'),
                    from_entity=i.get('from') or i.get('from_entity'),
                    to_entity=i.get('to') or i.get('to_entity'),
                    interface_type=i.get('interfaceType') or i.get('interface_type'),
                    bond_type=i.get('bondType') or i.get('bond_type'),
                    energy_loss=i.get('energyLoss') or i.get('energy_loss'),
                    created_at=i.get('created_at')
                )
                db.session.merge(obj)

            db.session.commit()
            print('\nMigration committed to database.')

            # Basic verification counts
            counts = {
                'teams': db.session.query(db_models.TeamModel).count(),
                'faculty': db.session.query(db_models.FacultyModel).count(),
                'projects': db.session.query(db_models.ProjectModel).count(),
                'interfaces': db.session.query(db_models.InterfaceModel).count(),
            }

            print('\nVerification counts after migration:')
            for k, v in counts.items():
                print(f'  - {k}: {v}')

            return counts

        except Exception as e:
            db.session.rollback()
            print('Error during migration:', e)
            raise


def main():
    parser = argparse.ArgumentParser(description='Migrate frames_data.json into SQL DB')
    parser.add_argument('--force', action='store_true', help='Actually write to the DB (default is dry-run)')
    parser.add_argument('--backup', action='store_true', help='Make a timestamped backup of the source file before migrating')
    parser.add_argument('--file', default=DATA_FILE, help='Path to frames_data.json (default from app)')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print('Source file not found:', args.file)
        return 1

    if args.backup:
        dst = backup_file(args.file)
        print('Backup created at:', dst)

    data = load_source(args.file)

    if args.force:
        print('Running migration with DB writes (force)')
        result = migrate(data, dry_run=False)
    else:
        print('Running dry-run migration (no DB writes). Use --force to apply.')
        result = migrate(data, dry_run=True)

    # Write a small migration summary file
    out = {
        'source_file': args.file,
        'timestamp': datetime.now().isoformat(),
        'mode': 'force' if args.force else 'dry-run',
        'summary': result,
    }
    with open('migration_map.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)

    print('\nWrote migration summary to migration_map.json')
    return 0


