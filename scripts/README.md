# FRAMES Automation Scripts

Collection of Python scripts for CADENCE data import, Notion sync, and system setup.

---

## 📖 Overview

This directory contains automation scripts for:

- **CADENCE Data Import** - Extract and normalize CADENCE project data
- **Notion Integration** - Sync data between Postgres and Notion
- **Database Setup** - Create and populate Module Library
- **GitHub Integration** - Sync issues and PRs with Notion

---

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r ../requirements.txt
```

### Environment Setup

Ensure `.env` file exists in project root with:

```bash
DATABASE_URL=postgresql://user:password@host/database
NOTION_TOKEN=ntn_xxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_MODULE_DB_ID=eac1ce58-6169-4dc3-a821-29858ae59e76
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxx  # Optional
```

---

## 📂 Available Scripts

### Notion Integration

#### `create_notion_workspace_beautiful.py`

Creates beautifully formatted Notion workspace with CADENCE Hub dashboard.

**Usage:**

```bash
python scripts/create_notion_workspace_beautiful.py
```

**What it does:**

- Creates CADENCE Hub page with three-column layout
- Creates 5 Notion databases (Team Members, Projects, Tasks, Meetings, Documents)
- Links databases to dashboard as linked views
- Applies dark theme styling

**Output:** Notion page URL and database IDs

---

#### `sync_notion.py`

Syncs data from Postgres to Notion databases (7-step workflow per spec).

**Usage:**

```bash
python scripts/sync_notion.py
```

**What it does:**

1. Schema Discovery - Query Postgres canonical tables
2. Data Extraction - Extract records from 5 CADENCE tables
3. Notion DB Resolution - Verify database IDs
4. Upsert Logic - Match by external_id, update or create
5. Document Sync - Sync file metadata
6. Validation - Ensure no structural changes
7. Summary Report - Return created/updated counts

**Compliance:** Follows [CADENCE_SPEC_COMPLIANCE.md](../docs/CADENCE_SPEC_COMPLIANCE.md)

---

#### `import_to_notion.py`

Direct import of training modules to Notion Module Library.

**Usage:**

```bash
set NOTION_DATABASE_ID=eac1ce58-6169-4dc3-a821-29858ae59e76
python scripts/import_to_notion.py
```

**What it does:**

- Reads module JSONs from `modules/exports/`
- Creates Notion database pages for each module
- Maps fields per spec (title, category, difficulty, etc.)
- Logs import results

**Output:** `import_log.txt` with success/error details

---

### CADENCE Data Import

#### `extract_cadence_project.py`

Extracts metadata from 1,417 CADENCE Notion export files.

**Usage:**

```bash
python scripts/extract_cadence_project.py
```

**What it does:**

- Scans `temp_cadence_extract/` directory
- Classifies files (Structural, Technical, Workflow, Program, Misc)
- Extracts: title, category, subsystem, relationships
- Exports to `cadence_data.json`

**Categories per spec:**

- Structural Docs (120 files): CAD, ICDs, mass budgets
- Technical Docs (200 files): Datasheets, fabrication
- Workflow Docs (350 files): SOPs, plans, meetings
- Program Docs (600 files): Mission materials
- Miscellaneous (147 files): Excluded from import

---

#### `ingest_cadence_export.py`

Imports CADENCE data from JSON to Postgres canonical schema.

**Usage:**

```bash
python scripts/ingest_cadence_export.py
```

**What it does:**

- Reads `cadence_data.json`
- Normalizes to 5 canonical tables (people, projects, tasks, meetings, documents)
- Validates schema per [CADENCE_SPEC_COMPLIANCE.md](../docs/CADENCE_SPEC_COMPLIANCE.md)
- Upserts to Postgres

**Output:** Postgres populated with CADENCE data

---

### Module Library Setup

#### `deploy_modules_to_db.py`

Deploys training modules to Notion Module Library database.

**Usage:**

```bash
python scripts/deploy_modules_to_db.py
```

**What it does:**

- Reads `modules/exports/*.json`
- Validates module schema
- Creates Notion pages in Module Library
- Links to CADENCE Hub dashboard

---

#### `update_module_library_from_json.py`

Updates existing modules in Notion from JSON exports.

**Usage:**

```bash
python scripts/update_module_library_from_json.py
```

**What it does:**

- Matches modules by slug or title
- Updates properties (category, difficulty, status)
- Preserves existing Notion page IDs

---

### GitHub Integration

#### `notion_github_sync.py`

Syncs GitHub issues and PRs with Notion database.

**Usage:**

```bash
python scripts/notion_github_sync.py
```

**Requirements:**

```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_REPO=Lizo-RoadTown/Frames-App
NOTION_GITHUB_DB_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**What it does:**

- Fetches open issues and PRs from GitHub
- Creates/updates Notion database pages
- Syncs: title, status, assignee, labels, due date
- Bidirectional sync (planned)

---

#### `setup_github_notion.py`

One-time setup for GitHub-Notion integration.

**Usage:**

```bash
python scripts/setup_github_notion.py
```

**What it does:**

- Creates "GitHub Tasks" Notion database
- Configures properties (Status, Assignee, Labels, URL)
- Sets up webhooks (if configured)

---

### Utility Scripts

#### `test_notion_access.py`

Verifies Notion API access and database permissions.

**Usage:**

```bash
python scripts/test_notion_access.py
```

**Output:**

```
✓ Notion API connected
✓ Module Library accessible
✓ Database ID: eac1ce58-6169-4dc3-a821-29858ae59e76
✓ Schema validated
```

---

#### `get_notion_db_ids.py`

Retrieves all Notion database IDs in workspace.

**Usage:**

```bash
python scripts/get_notion_db_ids.py
```

**Output:** `notion_database_ids.json` with all database IDs

---

#### `list_notion_pages.py`

Lists all pages in a Notion database.

**Usage:**

```bash
python scripts/list_notion_pages.py --database-id <db-id>
```

---

### Legacy/Deprecated

The following scripts are kept for reference but not actively maintained:

- `install_notion_deps.py` - Install Notion SDK (use `pip install` instead)
- `rebuild_pdf_modules.py` - PDF-based module generation (deprecated)
- `setup_and_import.py` - Combined setup script (use individual scripts)

---

## 🔄 Common Workflows

### Initial Setup: CADENCE Hub + Modules

```bash
# 1. Create Notion workspace
python scripts/create_notion_workspace_beautiful.py

# 2. Extract CADENCE data
python scripts/extract_cadence_project.py

# 3. Import to Postgres
python scripts/ingest_cadence_export.py

# 4. Sync to Notion
python scripts/sync_notion.py

# 5. Deploy modules
python scripts/deploy_modules_to_db.py
```

---

### Update Existing Modules

```bash
# 1. Update module JSONs in modules/exports/
# 2. Run update script
python scripts/update_module_library_from_json.py
```

---

### Daily Sync: GitHub → Notion

```bash
# Run manually or via cron
python scripts/notion_github_sync.py
```

---

## 📋 Script Dependencies

### Core Libraries

- `notion-client` - Notion API SDK
- `psycopg2` - PostgreSQL adapter
- `sqlalchemy` - ORM
- `python-dotenv` - Environment variables
- `requests` - HTTP requests

### Optional

- `PyGithub` - GitHub API (for GitHub sync)
- `pandas` - Data processing (for analytics)

---

## 🐛 Troubleshooting

### Common Issues

**"Notion API token invalid"**

```
notion_client.errors.APIResponseError: Unauthorized
```

**Solution:** Verify `NOTION_TOKEN` in `.env` file

**"Database not found"**

```
notion_client.errors.APIResponseError: Could not find database
```

**Solution:**

1. Check `NOTION_MODULE_DB_ID` is correct
2. Ensure integration has access to database
3. Run `python scripts/get_notion_db_ids.py` to verify

**"Import failed - schema mismatch"**

```
KeyError: 'title'
```

**Solution:** Validate module JSON schema matches expected format

**"Postgres connection failed"**

```
sqlalchemy.exc.OperationalError: could not connect
```

**Solution:** Check `DATABASE_URL` in `.env`

---

## 📝 Development

### Adding New Scripts

1. Create script in `scripts/` directory
2. Add docstring with description and usage
3. Update this README
4. Test with sample data
5. Document in [DEVELOPER_ONBOARDING.md](../docs/DEVELOPER_ONBOARDING.md)

### Code Style

- Follow PEP 8
- Use type hints
- Add error handling
- Log important operations
- Write clear docstrings

---

## 📚 Additional Documentation

- **[Complete System Architecture](../docs/COMPLETE_SYSTEM_ARCHITECTURE.md)** - System overview
- **[Notion API Integration](../docs/NOTION_API_INTEGRATION.md)** - Notion integration guide
- **[CADENCE Spec Compliance](../docs/CADENCE_SPEC_COMPLIANCE.md)** - Agent behavior contracts
- **[Database Schema Reference](../docs/DATABASE_SCHEMA_REFERENCE.md)** - Database structure

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/Lizo-RoadTown/Frames-App/issues)
- **Documentation:** [docs/](../docs/)
- **Contact:** eosborn@cpp.edu

---

**Last Updated:** 2025-11-28
**Maintained By:** Agent Beta
