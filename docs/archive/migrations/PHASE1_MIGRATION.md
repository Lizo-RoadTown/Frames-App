**Phase 1 — Migration Guide**

Purpose
- Provide exact, safe steps to migrate FRAMES from file-backed `frames_data.json` to a durable SQLite DB (`backend/frames.db`).
- Include dry-run, apply, verification, and rollback instructions so you can run the migration safely on Windows (PowerShell) or WSL.

Prerequisites
- A working checkout of the repo. The backend is in `backend/`.
- Python 3.10+ installed on the environment you will run commands in (PowerShell or WSL). If using Flask/SQLAlchemy migration, install `requirements.txt` in a venv.
- The repo already contains two migration helpers:
  - `backend/migrate_frames.py` — canonical migration (uses Flask/SQLAlchemy when available).
  - `backend/apply_migration_sqlite.py` — lightweight sqlite3-only migration (no external deps).

High-level workflow
1. Backup the source JSON and DB (if present).
2. Run a dry-run to compute counts and generate `migration_map.json`.
3. Inspect results and sample rows manually (optional).
4. Apply migration with `--backup --force`.
5. Verify DB contents.
6. Roll back if needed using backups.

Commands — PowerShell (Windows)

- Back up `frames_data.json` (manual):
  ```powershell
  Copy-Item .\backend\frames_data.json .\backend\frames_data.json.bak
  ```

- Dry-run (sqlite helper — no external deps):
  ```powershell
  python .\backend\apply_migration_sqlite.py
  ```

- Dry-run (canonical script — requires Flask/SQLAlchemy):
  ```powershell
  # create venv and install deps (one-time)
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt

  # dry-run
  python .\backend\migrate_frames.py
  ```

- Apply migration (backup + force) using sqlite helper (no deps):
  ```powershell
  python .\backend\apply_migration_sqlite.py --backup --force
  ```

- Apply migration using canonical script (with deps installed in venv):
  ```powershell
  # from repo root with venv activated
  python .\backend\migrate_frames.py --backup --force
  ```

Commands — WSL / Linux

- Back up JSON and DB:
  ```bash
  cp "backend/frames_data.json" "backend/frames_data.json.bak"
  cp "backend/frames.db" "backend/frames.db.bak" || true
  ```

- Dry-run (sqlite helper):
  ```bash
  python3 backend/apply_migration_sqlite.py
  ```

- Dry-run (canonical):
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  python3 backend/migrate_frames.py
  ```

- Apply (backup + force) with sqlite helper:
  ```bash
  python3 backend/apply_migration_sqlite.py --backup --force
  ```

- Apply (backup + force) canonical:
  ```bash
  # with venv activated
  python3 backend/migrate_frames.py --backup --force
  ```

Verification
- After applying, inspect `backend/migration_map.json` for the summary produced by the canonical migration (if used).
- Query counts directly with sqlite3 (WSL or Windows):
  ```bash
  sqlite3 backend/frames.db ".tables"
  sqlite3 backend/frames.db "SELECT COUNT(*) FROM teams;"
  sqlite3 backend/frames.db "SELECT COUNT(*) FROM faculty;"
  sqlite3 backend/frames.db "SELECT COUNT(*) FROM projects;"
  sqlite3 backend/frames.db "SELECT COUNT(*) FROM interfaces;"
  ```

- Or use a quick Python verifier (paste into `python` interactive):
  ```python
  import sqlite3
  conn = sqlite3.connect('backend/frames.db')
  for t in ('teams','faculty','projects','interfaces'):
      cur = conn.execute(f"SELECT COUNT(*) FROM {t}")
      print(t, cur.fetchone()[0])
  conn.close()
  ```

Rollback / Recovery
- If something goes wrong, you can revert easily because we take backups:
  - Restore `frames_data.json` from the backup.
    - PowerShell: `Copy-Item .\backend\frames_data.json.bak .\backend\frames_data.json -Force`
    - WSL: `cp backend/frames_data.json.bak backend/frames_data.json`
  - If you also backed up the DB (`frames.db.bak`), restore it:
    - PowerShell: `Copy-Item .\backend\frames.db.bak .\backend\frames.db -Force`
    - WSL: `cp backend/frames.db.bak backend/frames.db`

- If only tables were created (no rows), you can safely remove `backend/frames.db` and re-run migration after fixing source data.

Notes & Recommendations
- Use `apply_migration_sqlite.py` when your environment doesn't have Flask/SQLAlchemy installed — it is safe and dependency-free.
- Prefer running migration in WSL with the repo copied into WSL home if you previously had `/mnt/c` I/O issues.
- The canonical script (`migrate_frames.py`) will import `app.py` and the Flask app; use it when you have installed `requirements.txt` in a venv.
- Keep `migration_map.json` produced by dry-run for auditing and review before applying.
- Do not re-declare the `Sandbox` model in multiple places: currently a `Sandbox` SQLAlchemy model exists in `app.py`; avoid duplicating it in `db_models.py` to prevent duplicate-table errors.

Acceptance / Post-migration
- Switch read endpoints to DB-backed handlers incrementally and run integration tests against the DB.
- Keep the file-backed `SystemState` code around until all critical endpoints are migrated and validated. Only remove file-backed persistence after a successful soak and backups.

If you want, I can now:
- Add a small `scripts/verify_migration.py` helper that prints sample rows and counts, or
- Walk through switching one `GET` endpoint (e.g., `GET /api/teams`) to read from the DB and add a smoke test.

-- End of Phase 1 Migration Guide
