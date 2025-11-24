# Codebase Audit Report (2025-11-18)

## Duplicate Model Definitions
- `backend/db_models.py` contains:
  - Flask-SQLAlchemy models: TeamModel, FacultyModel, ProjectModel, InterfaceModel, AuditLog
  - Plain SQLAlchemy models (with `Base`): University, Team, Faculty, Project, Interface
- `backend/app.py` defines the `Sandbox` model inline (Flask-SQLAlchemy). `db_models.py` intentionally does not duplicate it (see comments at lines 129–131).

## Duplicate Migration Scripts
- `backend/migrate_frames.py` contains two migration scripts:
  - First script: top of file through line ~171 (uses Flask app context, SQLAlchemy models)
  - Second script: starts after a comment at line 173 (re-imports, redefines migration logic)

## Architectural Inconsistencies
- Models are split between Flask-SQLAlchemy and plain SQLAlchemy in `db_models.py`.
- Migration script structure is confusing due to duplication.
- Sandbox model is only defined in `app.py` (not duplicated in `db_models.py`).

## Recommendations
- Remove duplicate migration script from `migrate_frames.py` (keep only the canonical one).
- Consolidate models in `db_models.py` to use only Flask-SQLAlchemy; remove plain SQLAlchemy section.
- Ensure Sandbox model is defined only once (preferably in `db_models.py` for consistency, or document why it must remain in `app.py`).
- Proceed with Alembic for schema management and repository pattern for data access.

---

_This file documents the current state of the codebase and should be updated as issues are resolved._
