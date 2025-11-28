# Developer Onboarding Guide

**Date:** 2025-11-28
**Version:** 1.0
**Audience:** New developers and AI agents joining FRAMES
**Time to Complete:** 2-3 hours

---

## Table of Contents

1. [Welcome](#welcome)
2. [Prerequisites](#prerequisites)
3. [Environment Setup](#environment-setup)
4. [Understanding the Codebase](#understanding-the-codebase)
5. [Running Locally](#running-locally)
6. [Common Tasks](#common-tasks)
7. [Troubleshooting](#troubleshooting)
8. [Resources](#resources)

---

## Welcome

Welcome to FRAMES! This guide will help you get up and running quickly.

### What is FRAMES?

FRAMES is an **Onboarding & Training Engine** for large student research projects. We transform team leads' Notion documentation into interactive training modules for new students.

**Key Principle:** We don't replace existing workflows. We extract what's already documented and turn it into self-service onboarding.

### What You'll Build

By the end of this guide, you'll have:
- ✅ Full FRAMES stack running locally
- ✅ Connected to Neon PostgreSQL database
- ✅ Notion API integration working
- ✅ Understanding of project structure
- ✅ Ability to make changes confidently

---

## Prerequisites

### Required Software

1. **Python 3.14+**
   ```bash
   python --version
   # Should show: Python 3.14.x
   ```

2. **Node.js 18+** (for React frontend)
   ```bash
   node --version
   # Should show: v18.x or higher

   npm --version
   # Should show: 9.x or higher
   ```

3. **Git**
   ```bash
   git --version
   # Should show: git version 2.x
   ```

4. **Code Editor** (VSCode recommended)

### Required Accounts

1. **Neon PostgreSQL Account**
   - Sign up: https://neon.tech
   - Free tier is sufficient
   - Create new project: "FRAMES"

2. **Notion Account**
   - Sign up: https://notion.so
   - Create workspace: "FRAMES Development"
   - Get API token (see Environment Setup)

3. **GitHub Access**
   - Repository: https://github.com/Lizo-RoadTown/Frames-App
   - Request access from maintainer

---

## Environment Setup

### Step 1: Clone Repository

```bash
# Clone the repo
git clone https://github.com/Lizo-RoadTown/Frames-App.git
cd Frames-App

# Check you're on main branch
git branch
# Should show: * main

# Pull latest changes
git pull origin main
```

### Step 2: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep Flask
# Should show: Flask 2.x
```

### Step 3: Configure Environment Variables

Create `.env` file in root directory:

```bash
# Copy example file
cp .env.example .env

# Edit .env file
notepad .env  # Windows
nano .env     # Mac/Linux
```

**Required Variables:**

```bash
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/database

# Notion API
NOTION_TOKEN=ntn_xxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_MODULE_DB_ID=eac1ce58-6169-4dc3-a821-29858ae59e76

# Optional: GitHub
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
```

**How to get DATABASE_URL:**
1. Go to Neon dashboard (https://console.neon.tech)
2. Select your "FRAMES" project
3. Click "Connection string"
4. Copy the connection string
5. Paste into .env

**How to get NOTION_TOKEN:**
1. Go to https://www.notion.so/my-integrations
2. Click "New integration"
3. Name: "FRAMES Development"
4. Select your workspace
5. Click "Submit"
6. Copy "Internal Integration Token"
7. Paste into .env as `NOTION_TOKEN`

**How to get NOTION_MODULE_DB_ID:**
1. Open Module Library database in Notion
2. Copy database URL: `https://notion.so/xxxxx?v=yyyyy`
3. Extract database ID (xxxxx part, with dashes)
4. Paste into .env

### Step 4: Setup Database

```bash
# Test database connection
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('DATABASE_URL')[:30])"
# Should show: postgresql://user@host...

# Create tables
python shared/database/migrations/create_tables.py

# Verify tables created
python -c "from backend.database import db; from sqlalchemy import inspect; inspector = inspect(db.engine); print(inspector.get_table_names())"
# Should show: ['teams', 'faculty', 'projects', ...]
```

### Step 5: Install Frontend Dependencies

```bash
cd apps/onboarding-lms/frontend-react

# Install packages
npm install

# Verify installation
npm list react
# Should show: react@18.x

cd ../../..  # Back to root
```

---

## Understanding the Codebase

### Directory Structure

```
Frames-App/
├── README.md                       # Project overview
├── .env                            # Environment variables (SECRET - not in git)
├── requirements.txt                # Python dependencies
│
├── backend/                        # Flask API
│   ├── app.py                      # Main Flask application
│   ├── models.py                   # Data models
│   ├── lms_routes.py               # LMS module endpoints
│   └── database.py                 # SQLAlchemy setup
│
├── shared/                         # Shared code
│   └── database/
│       ├── db_models.py            # Database models (teams, students, etc.)
│       └── migrations/             # Database migration scripts
│
├── apps/                           # Applications
│   └── onboarding-lms/
│       ├── frontend-react/         # React student app
│       │   ├── src/
│       │   │   ├── App.js          # Main React component
│       │   │   └── components/     # React components
│       │   └── package.json
│       └── backend/                # LMS-specific backend (if needed)
│
├── scripts/                        # Automation scripts
│   ├── sync_postgres_to_notion.py  # Sync data to Notion
│   ├── import_cadence_to_postgres.py # Import CADENCE data
│   └── enhance_modules.py          # Module enhancement
│
├── modules/                        # Training modules
│   └── exports/                    # 68 module JSON files
│
├── docs/                           # Documentation
│   ├── COMPLETE_SYSTEM_ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   ├── DATABASE_SCHEMA_REFERENCE.md
│   ├── NOTION_API_INTEGRATION.md
│   └── DEVELOPER_ONBOARDING.md (this file)
│
├── agent_coordination/             # AI agent scripts
│   └── (agent automation files)
│
└── cadence_spec_full/              # CADENCE specifications
    ├── intent/
    ├── agents/
    └── pipelines/
```

### Key Concepts

**1. Three-Layer Architecture**
```
Authoring (Notion) → Transformation (Postgres) → Runtime (React)
```

**2. Data Flow**
```
Team Lead creates in Notion
  → Agent extracts to Postgres
    → Postgres syncs to Notion DBs
      → React app renders for students
```

**3. Agent System**
- **Alpha:** Database architect, module engineer
- **Beta:** Notion sync, documentation (you're reading Beta's work!)
- **Gamma:** Data import, file cleanup

---

## Running Locally

### Start Backend (Flask)

```bash
# From root directory
python backend/app.py

# Should see:
# * Running on http://127.0.0.1:5000
# * Debugger is active!
```

**Test Backend:**
```bash
# In another terminal
curl http://localhost:5000/api/network-data

# Should return JSON with projects, teams, faculty
```

### Start Frontend (React)

```bash
# In another terminal
cd apps/onboarding-lms/frontend-react

npm start

# Should automatically open browser to:
# http://localhost:3000
```

**What You Should See:**
- React app loads
- Module browser shows training modules
- Dark theme applied
- No console errors

### Verify Full Stack

1. **Backend Health:**
   - Visit: http://localhost:5000/
   - Should see: "FRAMES API is running"

2. **API Endpoints:**
   - Visit: http://localhost:5000/api/teams
   - Should see: JSON array of teams

3. **Frontend:**
   - Visit: http://localhost:3000
   - Should see: Module browser interface

4. **Database:**
   ```bash
   python -c "from shared.database.db_models import TeamModel; print(TeamModel.query.count())"
   # Should show number of teams (0 or more)
   ```

---

## Common Tasks

### Task 1: Add a New Module

**Step 1: Create Module JSON**
```bash
cd modules/exports

# Create new file: my-new-module.json
cat > my-new-module.json << 'EOF'
{
  "module_id": "new-module-001",
  "title": "My New Training Module",
  "slug": "my-new-training-module",
  "description": "Learn the basics of...",
  "category": "Software",
  "difficulty": "Beginner",
  "estimated_minutes": 30,
  "target_audience": "Undergraduate",
  "status": "Draft",
  "tags": ["training", "basics"],
  "learning_objectives": [
    "Understand concept X",
    "Apply technique Y"
  ],
  "sections": []
}
EOF
```

**Step 2: Validate Module**
```bash
python scripts/validate_module.py my-new-module.json
```

**Step 3: Test in App**
```bash
# Restart backend
python backend/app.py

# Visit: http://localhost:3000
# Should see new module in catalog
```

---

### Task 2: Update Database Schema

**Step 1: Add Field to Model**
```python
# shared/database/db_models.py
class TeamModel(db.Model):
    # ... existing fields ...

    # Add new field
    team_size = db.Column(db.Integer, default=0)
```

**Step 2: Create Migration**
```bash
# Create migration file
cat > shared/database/migrations/add_team_size.py << 'EOF'
from backend.database import db
from shared.database.db_models import TeamModel

def migrate():
    # Add column
    db.engine.execute(
        "ALTER TABLE teams ADD COLUMN team_size INTEGER DEFAULT 0"
    )
    print("✅ Added team_size column")

if __name__ == "__main__":
    migrate()
EOF

# Run migration
python shared/database/migrations/add_team_size.py
```

**Step 3: Verify**
```python
python -c "from shared.database.db_models import TeamModel; \
           team = TeamModel.query.first(); \
           print(f'Team size: {team.team_size}')"
```

---

### Task 3: Sync Data to Notion

**Step 1: Ensure Notion Token is Set**
```bash
echo $NOTION_TOKEN
# Should show: ntn_xxxxx...
```

**Step 2: Run Sync Script**
```bash
python scripts/sync_postgres_to_notion.py

# Should see:
# [SYNC] Starting Postgres → Notion sync
# [OK] Created 5 records
# [OK] Updated 10 records
```

**Step 3: Verify in Notion**
- Open Notion workspace
- Check Team Members database
- Should see new/updated records

---

### Task 4: Run Tests

```bash
# Run backend tests
python -m pytest backend/tests/

# Run specific test
python -m pytest backend/tests/test_teams.py

# Run with coverage
python -m pytest --cov=backend
```

---

### Task 5: Create Git Branch

```bash
# Create feature branch
git checkout -b feature/my-new-feature

# Make changes
# ... edit files ...

# Stage changes
git add .

# Commit
git commit -m "Add my new feature

- Implemented X
- Fixed Y
- Updated Z"

# Push to GitHub
git push -u origin feature/my-new-feature

# Create pull request on GitHub
```

---

## Troubleshooting

### Issue: "DATABASE_URL is not set"

**Problem:** .env file not loaded or DATABASE_URL missing

**Solution:**
```bash
# Check .env exists
ls -la .env

# Verify DATABASE_URL is set
cat .env | grep DATABASE_URL

# If missing, add it:
echo "DATABASE_URL=postgresql://..." >> .env

# Restart application
```

---

### Issue: "Could not connect to database"

**Problem:** Neon database is hibernated or connection string wrong

**Solution:**
```bash
# Test connection manually
psql $DATABASE_URL

# If fails, check:
# 1. Is Neon database active? (check Neon dashboard)
# 2. Is connection string correct? (copy from Neon)
# 3. Is network accessible? (try ping)

# Wake up hibernated database
curl https://console.neon.tech/app/projects/YOUR_PROJECT_ID
```

---

### Issue: "Notion API: unauthorized"

**Problem:** NOTION_TOKEN is invalid or expired

**Solution:**
```bash
# Verify token format
echo $NOTION_TOKEN | head -c 10
# Should start with: ntn_

# Regenerate token:
# 1. Go to https://www.notion.so/my-integrations
# 2. Click your integration
# 3. Click "Show" under Internal Integration Token
# 4. Copy and update .env
# 5. Restart application
```

---

### Issue: "Module not found: react-notion-x"

**Problem:** Frontend dependencies not installed

**Solution:**
```bash
cd apps/onboarding-lms/frontend-react

# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Verify
npm list react-notion-x
# Should show version
```

---

### Issue: "Port 5000 already in use"

**Problem:** Another process using port 5000

**Solution:**
```bash
# Find process using port 5000
# On Windows:
netstat -ano | findstr :5000

# On Mac/Linux:
lsof -i :5000

# Kill the process
# On Windows:
taskkill /PID <PID> /F

# On Mac/Linux:
kill -9 <PID>

# Or use different port
python backend/app.py --port 5001
```

---

### Issue: "react-scripts: command not found"

**Problem:** Frontend dependencies not in PATH

**Solution:**
```bash
cd apps/onboarding-lms/frontend-react

# Reinstall dependencies
npm install

# Use npx to run
npx react-scripts start

# Or add to PATH
export PATH="$PATH:./node_modules/.bin"
npm start
```

---

## Development Workflow

### Daily Workflow

1. **Pull Latest Changes**
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/my-task
   ```

3. **Make Changes**
   - Edit code
   - Test locally
   - Commit frequently

4. **Test Before Push**
   ```bash
   # Run backend
   python backend/app.py

   # Run frontend
   cd apps/onboarding-lms/frontend-react && npm start

   # Run tests
   python -m pytest
   ```

5. **Push and Create PR**
   ```bash
   git push -u origin feature/my-task
   # Create PR on GitHub
   ```

6. **Code Review**
   - Wait for review
   - Address feedback
   - Merge when approved

---

### Code Style

**Python (PEP 8):**
```python
# Good
def sync_to_notion(database_id, records):
    """Sync records to Notion database."""
    for record in records:
        create_page(database_id, record)

# Bad
def syncToNotion(databaseId,records):
  for r in records:
    create_page(databaseId,r)
```

**JavaScript (ESLint):**
```javascript
// Good
const fetchModules = async () => {
  const response = await fetch('/api/modules');
  return response.json();
};

// Bad
const fetchModules = async () =>
{
const response=await fetch('/api/modules')
return response.json()
}
```

---

### Commit Messages

**Format:**
```
<type>: <short summary>

<detailed description>

<additional context>
```

**Examples:**
```bash
# Good
git commit -m "feat: Add module progress tracking

- Create module_progress table
- Add API endpoint /api/modules/:id/progress
- Update frontend to display progress

Closes #123"

# Bad
git commit -m "updates"
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Add tests
- `chore`: Maintenance

---

## Resources

### Documentation

- [Complete System Architecture](COMPLETE_SYSTEM_ARCHITECTURE.md) - System overview
- [API Reference](API_REFERENCE.md) - API endpoints
- [Database Schema](DATABASE_SCHEMA_REFERENCE.md) - Database tables
- [Notion Integration](NOTION_API_INTEGRATION.md) - Notion API guide
- [CADENCE Spec Compliance](CADENCE_SPEC_COMPLIANCE.md) - Spec requirements

### External Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Notion API Docs](https://developers.notion.com/)
- [Neon Documentation](https://neon.tech/docs)
- [react-notion-x GitHub](https://github.com/NotionX/react-notion-x)

### Getting Help

**Questions?**
1. Check documentation in `docs/`
2. Search existing GitHub issues
3. Ask in team chat
4. Create new GitHub issue

**Found a Bug?**
1. Check if already reported
2. Create GitHub issue with:
   - Description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots/logs

**Want to Contribute?**
1. Fork repository
2. Create feature branch
3. Make changes
4. Submit pull request

---

## Next Steps

Now that you're set up:

1. **Explore the Codebase**
   - Read `COMPLETE_SYSTEM_ARCHITECTURE.md`
   - Browse `backend/app.py`
   - Check out React components

2. **Try Common Tasks**
   - Add a test module
   - Query the database
   - Make a simple API call

3. **Pick Your First Issue**
   - Check GitHub issues labeled "good first issue"
   - Ask maintainer for assignment
   - Create feature branch and start coding

4. **Join Team Communication**
   - Slack/Discord (get invite from maintainer)
   - Weekly standups
   - Code review process

---

## Checklist

Before you're fully onboarded, complete this checklist:

- [ ] Python 3.14+ installed
- [ ] Node.js 18+ installed
- [ ] Repository cloned
- [ ] .env file configured
- [ ] Neon database connected
- [ ] Notion API token working
- [ ] Backend running (Flask on :5000)
- [ ] Frontend running (React on :3000)
- [ ] Can query database
- [ ] Can make API calls
- [ ] Read system architecture docs
- [ ] Created first feature branch
- [ ] Know how to get help

---

**Congratulations!** You're ready to contribute to FRAMES! 🎉

---

**Last Updated:** 2025-11-28
**Maintained By:** Agent Beta
**Questions:** Create GitHub issue or ask in team chat
**Estimated Setup Time:** 2-3 hours
