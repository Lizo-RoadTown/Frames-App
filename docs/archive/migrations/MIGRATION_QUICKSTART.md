# PostgreSQL Migration Quick Start

## Ready to migrate? Follow these steps:

### 1. Install Dependencies

```bash
cd "c:\Users\LizO5\FRAMES Python"
pip install -r requirements.txt
```

This will install:
- `psycopg2-binary` - PostgreSQL adapter for Python
- `python-dotenv` - Load environment variables from .env file

### 2. Choose Your PostgreSQL Option

#### Option A: Railway (Easiest - $5/month)
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Create New Project → Provision PostgreSQL
4. Copy the DATABASE_URL from Variables tab

#### Option B: Local PostgreSQL (Free)
1. Download from [postgresql.org](https://www.postgresql.org/download/)
2. Install and remember your password
3. Create database named `frames`
4. Use: `postgresql://postgres:YOUR_PASSWORD@localhost:5432/frames`

#### Option C: Heroku ($7/month)
1. Install Heroku CLI
2. `heroku create frames-app`
3. `heroku addons:create heroku-postgresql:mini`
4. `heroku config:get DATABASE_URL`

### 3. Update .env File

Edit `.env` in the root directory:

```bash
# Change this line:
DATABASE_URL=sqlite:///instance/frames.db

# To your PostgreSQL connection string:
DATABASE_URL=postgresql://username:password@host:port/database
```

Example for Railway:
```bash
DATABASE_URL=postgresql://postgres:abc123@containers-us-west-45.railway.app:5432/railway
```

Example for local:
```bash
DATABASE_URL=postgresql://postgres:mypassword@localhost:5432/frames
```

### 4. Run Migration

```bash
cd backend
python migrate_to_postgres.py
```

You should see:
```
✅ Migration Complete! Migrated X total records
```

### 5. Test Application

```bash
python app.py
```

Visit http://localhost:5000 and verify everything works!

### 6. Deploy to PythonAnywhere

Update your PythonAnywhere environment variable:
1. Go to PythonAnywhere Web tab
2. Click "Environment variables"
3. Add: `DATABASE_URL` = `your-postgresql-url`
4. Reload web app

---

## What if I get errors?

See [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) for detailed troubleshooting.

Common issues:
- **"psycopg2 not installed"** → Run `pip install psycopg2-binary`
- **"Connection refused"** → Check PostgreSQL is running
- **"Database does not exist"** → Create the database first
- **"Still using SQLite"** → Make sure you updated .env correctly

---

## Files Created

✅ `.env.example` - Template configuration
✅ `.env` - Your local configuration (gitignored)
✅ `backend/migrate_to_postgres.py` - Migration script
✅ `POSTGRESQL_SETUP.md` - Detailed setup guide
✅ `MIGRATION_QUICKSTART.md` - This file
✅ `requirements.txt` - Updated with PostgreSQL dependencies

---

## Next: Discord Integration

Once PostgreSQL is working, move to Phase 2:
- See [docs/IMPLEMENTATION_ROADMAP.md](docs/IMPLEMENTATION_ROADMAP.md)
- Discord bot setup is next!

---

**Need help? Check the detailed guide:** [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md)
