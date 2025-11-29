**FRAMES Architecture Design (Phase‑1 → Phase‑2)**

**Overview:**
- **Purpose:** Provide a clear incremental migration path from the existing single-file HTML + file-backed state (`backend/frames_data.json`) to a robust Flask + JS application backed by a production-ready database (Postgres+JSONB). The design focuses on a safe Phase‑1 (dev-ready, minimal disruption) and a Phase‑2 (production readiness) that adds real-time collaboration, auth/RBAC, backup and audit maturity, and CI/CD.

**Goals & Acceptance Criteria:**
- **Safe migration:** dry-run migration tool with backups and rollback. Acceptance: `backend/migrate_frames.py --dry-run` produces a `migration_map.json` and `--force --backup` creates timestamped backups and `backend/frames.db` (or Postgres writes) without data loss.
- **Observable changes:** all writes are auditable and restorable. Acceptance: `audit_logs` table contains actor/action/entity/timestamps for any write executed during testing.
- **Minimal UI disruption:** support Play/Sandbox mode while switching reads/writes to DB incrementally. Acceptance: sandbox flows continue to work unchanged; one read endpoint converted to DB-backed with parity tests.
- **Progressive enhancement:** Phase‑1 uses SQLite dev DB, Phase‑2 migrates to Postgres with JSONB columns for flexible entity payloads.

**High-level Components:**
- **Backend:** Flask app (`backend/app.py`) with REST API; SQLAlchemy ORM models in `backend/db_models.py`; migration CLI `backend/migrate_frames.py`; lightweight `backend/apply_migration_sqlite.py` for constrained environments.
- **Frontend:** Single-page JS client (`frontend/static/api.js`) that uses REST; later adds WebSocket handlers for real-time events.
- **Persistence:** Dev: SQLite (`backend/frames.db`). Prod: Postgres with JSONB for flexible payloads and indexed query fields.
- **Audit & Backups:** `AuditLog` model (actor, action, entity_type, entity_id, payload_before, payload_after, meta, timestamp). Backup CLI `backend/backup_db.py` for timestamped compressed backups.
- **CI / Deployment:** Dockerfiles, GitHub Actions for lint/test/build, and optional Heroku/GCP/Render deployment steps.

**Database Design (recommended for Phase‑2 / Prod)**
- Choice: **Postgres + JSONB**. Rationale: flexible schema via JSONB for entity payloads, strong transactional semantics, easy replication, and mature toolchain.

- Core tables (conceptual):
  - **teams**
    - id: text (PK)
    - payload: jsonb (full Team object)
    - discipline: text (indexed via expression `payload->>'discipline'`)
    - lifecycle: text (indexed)
    - created_at, updated_at: timestamptz
  - **faculty**
    - id: text (PK)
    - payload: jsonb
    - role: text (indexed)
    - created_at, updated_at
  - **projects**
    - id: text (PK)
    - payload: jsonb
    - type: text (indexed)
    - created_at, updated_at
  - **interfaces**
    - id: text (PK)
    - payload: jsonb
    - from_id: text (indexed)
    - to_id: text (indexed)
    - interface_type: text (indexed)
  - **sandboxes** (dev/Play mode)
    - id, university_id, payload(jsonb), created_at, updated_at
  - **audit_logs**
    - id: serial (PK)
    - actor: text
    - action: text
    - entity_type: text
    - entity_id: text
    - payload_before: jsonb nullable
    - payload_after: jsonb nullable
    - meta: jsonb nullable
    - created_at: timestamptz default now()

- Indexing & queries:
  - Add GIN index on JSONB columns where we will run content queries.
  - Add functional indexes for commonly queried keys (e.g., payload->>'discipline').

**SQLite (Phase‑1) mapping:**
- Use SQLAlchemy models with typed columns for PKs, timestamps and a `db.Text` column storing JSON strings for payloads. Keep the same logical table/column names so migration to Postgres requires minimal model changes.

**API Versioning Strategy:**
- Prefix routes with `/api/v1/...` for the current Phase‑1 public API. When incompatible changes are needed, create `/api/v2/...` and deprecate `/api/v1` over a release cycle.
- Backwards-compatible changes: add fields to `payload` JSONB; keep endpoints stable.
- Breaking changes: create new version with migration path and compatibility shims.

**Real-time / Event Model (Phase‑2):**
- Pattern: Server publishes events for create/update/delete actions. Clients subscribe to receive events and apply them to local state.
- Choice: **Socket.IO (Flask-SocketIO)** for simple rooms + reconnection handling. Alternative: WebSocket-driven custom protocol.
- Event payloads:
  - `{ type: 'entity:created', entity: 'team', id: 'team_123', payload: {...}, meta: {actor, ts} }`
  - `{ type: 'entity:updated', ... }`
  - Events should include `op_id` (server-assigned operation id) and `causal_ts` to support ordering and client-side reconciliation.
- Rooms: per-university room for sandboxes and a global default for shared views.
- Conflict model: last-writer-wins for non-critical fields, with optional operation-based CRDTs for collaborative edits if needed later.

**Auth & RBAC (phase plan):**
- Phase‑1 (MVP): lightweight header-based actor identification for auditing (e.g., `X-Actor`) and an admin token environment variable to protect management endpoints.
- Phase‑2 (recommended): JWT-based auth with user accounts and roles (admin/editor/viewer). Integration steps:
  - Add `users` table with hashed passwords (bcrypt) and roles.
  - Use `/auth/login` to return JWT; secure endpoints check `Authorization: Bearer <token>`.
  - RBAC middleware: annotate endpoints with required roles.

**Migration Strategy (from `frames_data.json`):**
- Tools in repo:
  - `backend/migrate_frames.py` (canonical, SQLAlchemy-based). Supports `--dry-run` (writes `migration_map.json`) and `--force --backup` (creates timestamped backups and writes data to DB).
  - `backend/apply_migration_sqlite.py` (lightweight sqlite-only helper) for constrained environments.

- Steps (safe, repeatable):
  1. Backup `frames_data.json` and current DB. (CLI flag `--backup` creates `frames_data.json.bak-<ts>` and `backups/frames.db.bak-<ts>.gz`.)
  2. Dry-run: `python backend/migrate_frames.py --dry-run` → inspect `backend/migration_map.json`.
  3. Confirm consistency and run `python backend/migrate_frames.py --force --backup` to write DB tables.
  4. Run `scripts/verify_migration.py` to validate row counts and sample rows.
  5. If rollback needed, restore backed up `frames.db` or restore Postgres via `pg_restore` from compressed dump.

**Auditing & Backups (MVP) — Lightweight approach:**
- Application-level audit helper `_log_audit(actor, action, entity, id, before, after, meta)` that writes to `audit_logs`. Keep writes best-effort and non-blocking (catch exceptions) during initial rollout.
- Backup CLI `backend/backup_db.py` that:
  - Creates compressed backup of SQLite DB or `pg_dump` for Postgres.
  - Writes manifest including checksum and timestamp into `backups/manifest.json`.
  - Optionally rotates old backups by retention policy.
- Retention policy (Phase‑1): keep last 7 daily backups and weekly monthly snapshots. Implement rotation as a later task.

**Transactions & Concurrency:**
- Use DB transactions for multi-step operations (update entity + audit log) to ensure consistency when possible. For SQLite, be aware of its write-locking model; batch or short transactions recommended.
- For high-concurrency Phase‑2, Postgres ensures row-level locking and better concurrency semantics.

**Observability & Monitoring:**
- Add structured logs for API calls and key migration operations. Include correlation IDs where possible.
- Expose a `/health` endpoint returning DB connectivity and backup status.

**CI/CD & Deployment:**
- Dockerize the app (single Dockerfile for Flask app). Provide `docker-compose.yml` for local dev with Postgres, Redis (if websockets scale needed), and the app.
- GitHub Actions pipelines:
  - `lint` (flake8/black), `test` (unit/integration), `build` (docker build), `deploy` (manual trigger for staging/production).
- Deploy options: container registry → Kubernetes or managed service (Elastic Beanstalk, App Engine, Render). For early stages, deploy to a single small instance with backups and scheduled tasks for DB dumps.

**Security Considerations:**
- Protect management endpoints and migration CLI behind auth and/or require local execution only.
- Sanitize and limit file uploads and snapshots; avoid storing secrets in plain text in backups.
- Use TLS in production for all endpoints and tokens.

**Risks & Mitigations:**
- Risk: data loss during migration. Mitigation: mandatory backups, dry-run mode, and verification scripts.
- Risk: audit writes fail and we miss history. Mitigation: initial best-effort writes logged to STDOUT and metrics; later move to synchronous transactions when stable.
- Risk: SQLite concurrency limits. Mitigation: keep SQLite for dev only; Postgres for production.

**Acceptance Tests / Validation:**
- Dry-run vs canonical migration parity: counts in `migration_map.json` should match `scripts/verify_migration.py` results after canonical run.
- Audit recording: perform create/update/delete calls with `X-Actor`, verify `audit_logs` entries.
- Sandbox parity: `copy-live-to-sandbox` flow preserves system state snapshot and can be restored to live state via `POST /api/state`.

**Next actionable steps (short timeline):**
1. Finalize this architecture doc (you approve or request changes).
2. Implement the backup CLI `backend/backup_db.py` and add a small smoke test that creates a sandbox and verifies an audit log entry (MVP work you offered).
3. Instrument remaining write endpoints (ensure all create/update/delete paths call `_log_audit`).
4. Add `docker-compose.yml` + simple `Dockerfile` for local dev and CI pipeline skeleton in `.github/workflows/ci.yml`.

**Files added / changed in Phase‑1:**
- `backend/db_models.py` — SQLAlchemy models
- `backend/migrate_frames.py` — migration CLI
- `backend/apply_migration_sqlite.py` — sqlite-only migration
- `backend/backup_db.py` — (next task) backup CLI
- `docs/PHASE1_MIGRATION.md` — migration instructions
- `docs/ARCHITECTURE_DESIGN.md` — this design file

**Contact points / decision areas where I need your input:**
- Confirm: use Postgres+JSONB for production? (Recommended)
- Confirm: prefer Socket.IO for real-time or a plain WebSocket solution?
- Do you want immediate implementation of the backup CLI + audit instrumentation now? (I can implement both and run smoke tests in the WSL venv.)

---

If you say "Go", I will: create `backend/backup_db.py`, instrument any remaining write endpoints for `_log_audit` (if any are missing), run a smoke test to create a sandbox and verify the audit row, and add a short usage section to `docs/PHASE1_MIGRATION.md` showing backup/restore commands.