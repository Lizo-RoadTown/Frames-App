# PostgreSQL Migration Checklist

Use this checklist to track your progress through the local PostgreSQL setup.

## Phase 1: Install PostgreSQL

- [ ] Download PostgreSQL installer from https://www.postgresql.org/download/windows/
- [ ] Run installer and complete installation wizard
- [ ] Set postgres password (write it down!)
- [ ] Verify PostgreSQL service is running in Windows Services

## Phase 2: Create Database

Choose one method:

### Option A: pgAdmin (Recommended)
- [ ] Open pgAdmin 4 from Start Menu
- [ ] Connect to PostgreSQL 16 server
- [ ] Right-click Databases → Create → Database
- [ ] Name it "frames"
- [ ] Verify database appears in list

### Option B: Command Line
- [ ] Open Command Prompt
- [ ] Navigate to: `C:\Program Files\PostgreSQL\16\bin`
- [ ] Run: `psql -U postgres`
- [ ] Execute: `CREATE DATABASE frames;`
- [ ] Verify with: `\l`

## Phase 3: Install Python Dependencies

- [ ] Open Command Prompt in project directory
- [ ] Run: `pip install -r requirements.txt`
- [ ] Verify psycopg2-binary installed
- [ ] Verify python-dotenv installed

## Phase 4: Configure Connection

- [ ] Open `.env` file in text editor
- [ ] Update `DATABASE_URL` line with your PostgreSQL connection string
  - Example: `DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/frames`
- [ ] Replace `YOUR_PASSWORD` with your actual postgres password
- [ ] Save the file

## Phase 5: Run Migration

- [ ] Open Command Prompt
- [ ] Navigate to: `cd "c:\Users\LizO5\FRAMES Python\backend"`
- [ ] Run: `python migrate_to_postgres.py`
- [ ] Verify you see "✅ Migration Complete!" message
- [ ] Note how many records were migrated

## Phase 6: Test Application

- [ ] In backend directory, run: `python app.py`
- [ ] Open browser to: http://localhost:5000
- [ ] Test main landing page
- [ ] Click "Program Management Portal"
- [ ] Select a university
- [ ] Verify data displays correctly
- [ ] Test faculty page
- [ ] Test student teams page
- [ ] Test research dashboard

## Phase 7: Verify Data (Optional)

Using pgAdmin:
- [ ] Open pgAdmin 4
- [ ] Navigate to frames → Schemas → public → Tables
- [ ] Right-click "teams" → View/Edit Data → All Rows
- [ ] Verify your team data appears
- [ ] Check other tables (faculty, projects, interfaces)

## Phase 8: Backup (Recommended)

- [ ] Keep your SQLite database as backup: `backend/instance/frames.db`
- [ ] Don't delete it until PostgreSQL is fully tested and deployed

## Troubleshooting Checklist

If you encounter errors, check these:

- [ ] PostgreSQL service is running (services.msc)
- [ ] Password in .env matches your postgres password
- [ ] Database "frames" exists (check in pgAdmin)
- [ ] Port 5432 is not blocked by firewall
- [ ] No typos in DATABASE_URL connection string
- [ ] psycopg2-binary is installed (`pip list | findstr psycopg2`)

## Success Criteria

You're done when:

✅ PostgreSQL is installed and running
✅ Database "frames" exists
✅ Migration script completes successfully
✅ Flask app starts without errors
✅ Website displays data correctly
✅ All university/faculty/team pages work

## What's Next?

After completing this checklist:

1. **Commit your work** (don't commit .env!)
2. **Update PythonAnywhere** environment variables
3. **Move to Phase 2:** Discord Integration
   - See: [docs/IMPLEMENTATION_ROADMAP.md](docs/IMPLEMENTATION_ROADMAP.md)

---

## Quick Reference

**PostgreSQL Download:** https://www.postgresql.org/download/windows/

**Detailed Guide:** [POSTGRESQL_WINDOWS_SETUP.md](POSTGRESQL_WINDOWS_SETUP.md)

**Quick Start:** [MIGRATION_QUICKSTART.md](MIGRATION_QUICKSTART.md)

**Connection String Format:**
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/frames
```

**Common Commands:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run migration
cd backend
python migrate_to_postgres.py

# Start Flask
python app.py
```

---

**Print this checklist** and check off items as you complete them!
