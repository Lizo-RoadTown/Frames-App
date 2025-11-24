# Getting Started Checklist - FRAMES 2025 Pivot

## Overview
This checklist guides you through setting up the new student onboarding module system for FRAMES.

**Estimated Time:** 2-3 hours for initial setup
**Prerequisites:** Microsoft Azure for Students account, GitHub account

---

## Week 1: Foundation Setup

### Day 1-2: Database Migration to Azure

#### ☐ Step 1: Create Azure PostgreSQL Database
Follow: [AZURE_DATABASE_SETUP.md](AZURE_DATABASE_SETUP.md)

- [ ] Log into [Azure Portal](https://portal.azure.com)
- [ ] Create new "Azure Database for PostgreSQL - Flexible Server"
  - Server name: `frames-db` (or your choice)
  - Region: Closest to you
  - Compute: **Burstable B1MS** (free tier)
  - Storage: **32 GB** (free tier limit)
  - Admin username: `framesadmin`
  - Password: **Save this securely!**
- [ ] Configure networking
  - Allow Azure services: ✓
  - Add your current IP address: ✓
- [ ] Verify cost is $0.00/month
- [ ] Create resource (wait 5-10 min)

**Expected Result:** Email confirmation that resource is created

---

#### ☐ Step 2: Create FRAMES Database

Using Azure Cloud Shell (easiest):

```bash
# Connect to PostgreSQL
psql "host=frames-db.postgres.database.azure.com port=5432 dbname=postgres user=framesadmin sslmode=require"

# Enter your password when prompted

# Create database
CREATE DATABASE frames;

# Verify
\l

# Exit
\q
```

**Expected Result:** Database `frames` appears in list

---

#### ☐ Step 3: Update Local Configuration

1. Open `.env` file (create from `.env.example` if needed)

2. Update `DATABASE_URL`:
   ```env
   DATABASE_URL=postgresql://framesadmin:YOUR_PASSWORD@frames-db.postgres.database.azure.com:5432/frames?sslmode=require
   ```
   Replace:
   - `YOUR_PASSWORD` with your actual password
   - `frames-db` with your server name if different

3. Generate new `SECRET_KEY`:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copy output and update in `.env`

4. Set production mode:
   ```env
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

**Expected Result:** `.env` file configured with Azure connection

---

#### ☐ Step 4: Test Connection

```bash
# From FRAMES Python directory
cd "c:\Users\LizO5\FRAMES Python"

# Activate virtual environment
venv\Scripts\activate

# Test connection
python -c "from sqlalchemy import create_engine; import os; from dotenv import load_dotenv; load_dotenv(); engine = create_engine(os.getenv('DATABASE_URL')); conn = engine.connect(); print('✓ Connection successful!'); conn.close()"
```

**Expected Result:** `✓ Connection successful!`

**If it fails:**
- Check password is correct
- Check server name is correct
- Check your IP is in Azure firewall rules
- Check `?sslmode=require` is at end of URL

---

#### ☐ Step 5: Migrate Existing Data

```bash
# Initialize database with existing schema
python backend/database.py

# OR migrate from SQLite if you have data:
# python backend/migrate_to_postgres.py
```

**Expected Result:** Tables created in Azure database

**Verify in Azure Cloud Shell:**
```bash
psql "host=frames-db.postgres.database.azure.com port=5432 dbname=frames user=framesadmin sslmode=require"

\dt  # List all tables

# Should see: universities, teams, students, faculty, etc.

SELECT * FROM universities;  # Check sample data

\q
```

---

### Day 2-3: GitHub Collaboration Setup

#### ☐ Step 1: Identify Team Leads

Create a list:

| Name | GitHub Username | Email | Role |
|------|----------------|-------|------|
| Example Lead | @exampleuser | lead@email.com | Lab Safety SME |
|  |  |  |  |
|  |  |  |  |

**Action:** Get this information from your team leads

---

#### ☐ Step 2: Add Collaborators to GitHub

1. Go to [github.com/Lizo-RoadTown/Frames-App](https://github.com/Lizo-RoadTown/Frames-App)
2. Click **Settings** → **Collaborators** → **Add people**
3. Add each team lead by username or email
4. They'll receive invitation email

**Expected Result:** Team leads accept invitations and have access

---

#### ☐ Step 3: Set Up Branch Protection

1. In repo, go to **Settings** → **Branches**
2. Click **Add branch protection rule**
3. Branch name pattern: `main`
4. Enable:
   - ✓ Require a pull request before merging
   - ✓ Require approvals: 1
5. Save changes

**Expected Result:** No one can push directly to `main`

---

#### ☐ Step 4: Team Lead Onboarding

Send to each team lead:

```
Hi [Name],

You've been added as a collaborator to the FRAMES project!

Please complete these steps:
1. Accept GitHub invitation (check your email)
2. Clone repository: https://github.com/Lizo-RoadTown/Frames-App
3. Read: GITHUB_COLLABORATION_GUIDE.md
4. Complete practice workflow:
   - Create test branch
   - Make small change
   - Create pull request
   - I'll review and merge

Let me know when done!
```

**Expected Result:** All team leads complete practice workflow

---

### Day 3-4: Plan First Modules

#### ☐ Step 1: Identify Priority Modules

Fill in this table:

| Priority | Module Topic | SME (Who?) | Est. Time | Target Date |
|----------|-------------|-----------|-----------|-------------|
| 1 | Lab Safety Fundamentals | | 20 min | |
| 2 | | | | |
| 3 | | | | |

**Recommended first modules:**
- Lab Safety (always priority 1)
- Equipment Introduction
- Software Setup
- Team Communication Protocols

---

#### ☐ Step 2: Gather Existing Content

For each priority module, collect:
- [ ] Existing presentations (PowerPoint, PDF)
- [ ] Training videos
- [ ] Photos of equipment
- [ ] Checklists or procedures
- [ ] FAQ documents

**Storage:** Create a shared folder (OneDrive, Google Drive, etc.)

---

#### ☐ Step 3: Create Module Outlines

For top priority module, outline sections:

**Example: Lab Safety Fundamentals**
1. Introduction (2 min) - Why safety matters
2. PPE Requirements (5 min) - Required protective equipment
3. Emergency Procedures (5 min) - What to do in emergencies
4. Equipment Safety (5 min) - Safe operation guidelines
5. Knowledge Check (3 min) - Self-assessment questions

**Your outline:**
1.
2.
3.
4.
5.

---

## Week 2: Development Begins

### Day 5-7: Database Schema for Modules

#### ☐ Step 1: Create Migration Script

You or developer:
1. Create file: `backend/migrations/add_module_system.sql`
2. Copy schema from [STUDENT_ONBOARDING_SYSTEM_DESIGN.md](STUDENT_ONBOARDING_SYSTEM_DESIGN.md)
3. Review tables to be created

#### ☐ Step 2: Run Migration

```bash
# Connect to Azure database
psql "host=frames-db.postgres.database.azure.com port=5432 dbname=frames user=framesadmin sslmode=require"

# Run migration
\i backend/migrations/add_module_system.sql

# Verify tables created
\dt

# Should see new tables:
# - modules
# - module_sections
# - module_assignments
# - module_progress
# - module_analytics_events

\q
```

#### ☐ Step 3: Create SQLAlchemy Models

Developer work - no action needed from you yet

---

### Day 8-10: Start Content Creation

#### ☐ Team Leads: Create First Module (JSON Version)

Until UI is built, team leads create modules as JSON files:

1. Copy template from [GITHUB_COLLABORATION_GUIDE.md](GITHUB_COLLABORATION_GUIDE.md)
2. Fill in your module content
3. Save as `backend/modules/your-module-name.json`
4. Create pull request

**You'll review and provide feedback**

---

## Quick Reference

### Important Documents

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [AZURE_DATABASE_SETUP.md](AZURE_DATABASE_SETUP.md) | Azure database setup | Setting up database |
| [GITHUB_COLLABORATION_GUIDE.md](GITHUB_COLLABORATION_GUIDE.md) | Team lead Git workflow | Onboarding team leads |
| [STUDENT_ONBOARDING_SYSTEM_DESIGN.md](STUDENT_ONBOARDING_SYSTEM_DESIGN.md) | Technical architecture | Development reference |
| [PROJECT_ROADMAP_2025.md](PROJECT_ROADMAP_2025.md) | Full project plan | Big picture planning |

---

### Key Credentials (Store Securely!)

**Azure Database:**
- Server: `__________.postgres.database.azure.com`
- Username: `framesadmin`
- Password: `__________` ← **Write this down!**
- Database: `frames`

**Flask:**
- SECRET_KEY: `__________` ← **Generate with Python command**

**GitHub:**
- Repo: https://github.com/Lizo-RoadTown/Frames-App

---

### Helpful Commands

**Activate Python virtual environment:**
```bash
cd "c:\Users\LizO5\FRAMES Python"
venv\Scripts\activate
```

**Connect to Azure database:**
```bash
psql "host=YOUR_SERVER.postgres.database.azure.com port=5432 dbname=frames user=framesadmin sslmode=require"
```

**Check Git status:**
```bash
git status
git log --oneline -5
```

**Run Flask app:**
```bash
python backend/app.py
```

---

## Troubleshooting

### "Can't connect to database"
1. Check `.env` has correct connection string
2. Verify password is correct
3. Check your IP is in Azure firewall rules
4. Ensure `?sslmode=require` is at end of URL

### "Permission denied on GitHub"
1. Verify you accepted invitation
2. Check you're pushing to your feature branch, not `main`
3. Contact admin if still issues

### "Module not loading"
1. Check JSON syntax is valid (use JSONLint.com)
2. Verify file is in correct location
3. Check file permissions

---

## Success Criteria

After Week 1, you should have:
- ✅ Azure database running and accessible
- ✅ Team leads have GitHub access
- ✅ First 3 modules planned with outlines
- ✅ Existing content gathered and organized

After Week 2, you should have:
- ✅ Module system tables in database
- ✅ API endpoints working (developer work)
- ✅ First module content created (JSON format)
- ✅ Team leads comfortable with workflow

---

## Questions or Issues?

**Database Issues:**
- Review: [AZURE_DATABASE_SETUP.md](AZURE_DATABASE_SETUP.md)
- Check: Azure Portal → Your server → Networking
- Verify: Connection string in `.env`

**GitHub Issues:**
- Review: [GITHUB_COLLABORATION_GUIDE.md](GITHUB_COLLABORATION_GUIDE.md)
- Check: Repository → Settings → Collaborators
- Create: GitHub Issue for help

**Content Questions:**
- Review: Module template in collaboration guide
- Ask: Subject matter expert for your module
- Reference: Existing training materials

---

## Next Steps After Checklist Complete

1. **Development Sprint 1:** Backend API (Week 3-4)
2. **Development Sprint 2:** React frontend (Week 5-6)
3. **Content Creation:** Team leads build modules (Week 6-8)
4. **Testing:** Pilot with students (Week 8)
5. **Launch:** Full deployment (Week 9-10)

See [PROJECT_ROADMAP_2025.md](PROJECT_ROADMAP_2025.md) for detailed timeline.

---

**Ready to start?** Begin with "Day 1-2: Database Migration to Azure"

Good luck! 🚀

---

*Last updated: 2025-01-23*
