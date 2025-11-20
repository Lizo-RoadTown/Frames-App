# PostgreSQL Setup Guide for FRAMES

This guide will walk you through migrating from SQLite to PostgreSQL.

## Why PostgreSQL?

- ✅ FREE and open source
- ✅ Better for multi-university data
- ✅ Native JSON support (JSONB)
- ✅ Better for AI/ML integration
- ✅ Time-series support (TimescaleDB extension)
- ✅ Works with Railway, Heroku, AWS, Google Cloud

---

## Option 1: Railway (Easiest - Recommended)

**Cost:** $5/month for PostgreSQL

### Steps:

1. **Sign up for Railway**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Create a new project**
   - Click "New Project"
   - Select "Provision PostgreSQL"

3. **Get connection string**
   - Click on your PostgreSQL service
   - Go to "Variables" tab
   - Copy the `DATABASE_URL` value
   - Example: `postgresql://postgres:password@containers-us-west-123.railway.app:5432/railway`

4. **Update your .env file**
   ```bash
   DATABASE_URL=postgresql://postgres:password@containers-us-west-123.railway.app:5432/railway
   ```

5. **Run migration** (see below)

---

## Option 2: Heroku (Classic)

**Cost:** $7/month for Mini PostgreSQL

### Steps:

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku app**
   ```bash
   heroku login
   heroku create frames-app
   ```

3. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Get connection string**
   ```bash
   heroku config:get DATABASE_URL
   ```

5. **Update your .env file**
   ```bash
   DATABASE_URL=<paste-url-here>
   ```

6. **Run migration** (see below)

---

## Option 3: Local PostgreSQL (Free - For Development)

### Windows:

1. **Download PostgreSQL**
   - Go to [postgresql.org/download/windows](https://www.postgresql.org/download/windows/)
   - Download PostgreSQL 15 or 16
   - Run installer, remember your password

2. **Create database**
   - Open pgAdmin (installed with PostgreSQL)
   - Right-click "Databases" → "Create" → "Database"
   - Name: `frames`

3. **Get connection string**
   ```
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/frames
   ```

4. **Update your .env file** with the connection string

5. **Run migration** (see below)

### Mac:

```bash
# Install PostgreSQL with Homebrew
brew install postgresql@15

# Start PostgreSQL
brew services start postgresql@15

# Create database
createdb frames

# Connection string:
DATABASE_URL=postgresql://YOUR_USERNAME@localhost:5432/frames
```

### Linux:

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Start service
sudo systemctl start postgresql

# Create database
sudo -u postgres createdb frames

# Connection string:
DATABASE_URL=postgresql://postgres@localhost:5432/frames
```

---

## Running the Migration

Once you have PostgreSQL set up:

### 1. Install Python dependencies

```bash
cd "c:\Users\LizO5\FRAMES Python"
pip install -r requirements.txt
```

This installs:
- `psycopg2-binary` (PostgreSQL adapter)
- `python-dotenv` (environment variable loading)

### 2. Update .env file

Edit `.env` and set your `DATABASE_URL`:

```bash
# Example for Railway:
DATABASE_URL=postgresql://postgres:password@containers-us-west-123.railway.app:5432/railway

# Example for local:
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/frames
```

### 3. Run migration script

```bash
cd backend
python migrate_to_postgres.py
```

You should see:

```
🔄 FRAMES PostgreSQL Migration Tool

✅ Found SQLite database: backend\instance\frames.db
✅ PostgreSQL URL configured: postgresql://postgres@***

==================================================
🚀 Starting FRAMES PostgreSQL Migration
==================================================

🔍 Testing database connections...
✅ SQLite connected. Tables: 8
✅ PostgreSQL connected. Tables: 0

📋 Creating PostgreSQL schema...
✅ PostgreSQL schema created successfully

📦 Migrating projects...
✅ Migrated 3 records from projects

📦 Migrating teams...
✅ Migrated 15 records from teams

... etc ...

==================================================
✅ Migration Complete! Migrated 45 total records
==================================================
```

### 4. Test your application

```bash
cd backend
python app.py
```

Visit `http://localhost:5000` and verify everything works!

---

## Troubleshooting

### Error: "psycopg2 not installed"

```bash
pip install psycopg2-binary
```

### Error: "Connection refused"

- Check PostgreSQL is running
- Verify connection string is correct
- Check firewall settings

### Error: "Database does not exist"

Create the database first:

```sql
CREATE DATABASE frames;
```

### Error: "Role does not exist"

Create the PostgreSQL user:

```sql
CREATE USER frames_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE frames TO frames_user;
```

---

## What Gets Migrated?

The migration script copies all data from these tables:

- ✅ `projects` - All your projects
- ✅ `teams` - Student teams
- ✅ `faculty` - Faculty and mentors
- ✅ `interfaces` - Knowledge transfer interfaces
- ✅ `students` - Student roster
- ✅ `risk_factors` - Research factor definitions
- ✅ `factor_values` - Factor measurements
- ✅ `model_definitions` - ML model configurations

---

## After Migration

### Keep SQLite as backup

Your SQLite database is preserved at `backend/instance/frames.db`. Don't delete it until you're confident PostgreSQL is working.

### Update deployment

If using PythonAnywhere, Railway, or Heroku for deployment, update the DATABASE_URL environment variable there as well.

### Enable PostgreSQL extensions (optional)

For advanced features, enable these extensions:

```sql
-- Vector search for AI embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Time-series data
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Full-text search
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

---

## Cost Summary

| Option | Monthly Cost | Best For |
|--------|-------------|----------|
| Railway | $5 | Quick setup, solo developer |
| Heroku | $7 | Classic PaaS, easy deployment |
| Local | $0 | Development only |
| AWS RDS | $15-50 | Production, scalability |
| Google Cloud SQL | $10-40 | Production, ML integration |

---

## Next Steps

After PostgreSQL is working:

1. ✅ PostgreSQL migration complete
2. 🔄 Phase 2: Discord integration
3. 🔄 Phase 3: GitHub integration
4. 🔄 Phase 4: PM tool integration

See [IMPLEMENTATION_ROADMAP.md](docs/IMPLEMENTATION_ROADMAP.md) for details.

---

## Need Help?

- PostgreSQL docs: [postgresql.org/docs](https://www.postgresql.org/docs/)
- Railway docs: [docs.railway.app](https://docs.railway.app/)
- Heroku Postgres: [devcenter.heroku.com/articles/heroku-postgresql](https://devcenter.heroku.com/articles/heroku-postgresql)
