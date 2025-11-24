# Repository layout for the FRAMES ecosystem

This keeps one small, authoritative platform repo for the shared database contract, and separate repos for each application that consumes it. No shared UI, users, or runtime engines live together — only the DB contract is shared.

## Repos at a glance
- `platform-db` (platform team owns this)
  - Schema and migrations (Alembic/SQL)
  - DB docs, ERD, onboarding, and runbooks
  - Published contracts: OpenAPI/GraphQL specs and optional generated clients
  - Releases: SemVer tags (e.g., v1.4.2) that apps pin to
- `app-<name>` (one per application)
  - The app’s code, UI/backend, its CI/CD, and app docs
  - Depends on a pinned `platform-db` release; applies platform migrations during deploy
  - No ad‑hoc schema changes here — schema lives in `platform-db`
- `hub` (optional, tiny)
  - README only: links to `platform-db` and all apps, ownership matrix, current platform version in use per app

## How schema changes flow
1) Propose a change in `platform-db` (PR with migration + notes).  
2) Platform CI runs migration lint/dry-run and regenerates contracts/clients.  
3) Merge + tag a release (SemVer). Publish artifacts (e.g., client wheels, OpenAPI bundle).  
4) Each app bumps its pinned platform version, applies migrations, runs contract tests, then deploys.  
5) Track rollout status in the hub README (optional).

## Platform repo checklist (`platform-db`)
- Migrations: Alembic (or SQL) with backward-compat policy documented.
- Contracts: OpenAPI/GraphQL specs checked in; optional generated clients published on release.
- CI: migration dry-run, contract generation, client packaging, release tagging.
- Docs: onboarding (local + cloud DB), how to propose schema changes, upgrade guide for consumers.
- Branching: trunk + short-lived feature branches; releases via tags.

## App repo checklist (`app-<name>`)
- Pin to a specific `platform-db` release (version file or requirements entry).
- Apply platform migrations in deploy pipeline before starting the app.
- Run contract/compat tests against the pinned platform version (and optionally latest).
- App-specific docs: setup, env vars (pointing to DATABASE_URL), run/deploy/runbook.
- CI: unit/integration tests, contract tests, lint/format.

## Hub README (optional)
- Link to `platform-db` and each app repo.
- Show which platform version each app is pinned to and who owns it.
- Quickstart links for onboarding and support.

## Naming suggestion
- `platform-db`
- `app-onboarding-lms`
- `app-research-analytics`
- `app-ai-core`
- `hub` (if you want a single landing README)
