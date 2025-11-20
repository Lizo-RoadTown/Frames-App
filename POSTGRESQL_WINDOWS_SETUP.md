# PostgreSQL Setup for Windows - Step by Step

## Step 1: Download PostgreSQL

1. **Go to the official download page:**
   - Visit: https://www.postgresql.org/download/windows/
   - Click "Download the installer"

2. **Choose the installer:**
   - Click on "Windows x86-64" for 64-bit Windows
   - Latest version (PostgreSQL 16 or 15)
   - Download from EnterpriseDB

## Step 2: Install PostgreSQL

1. **Run the installer** (postgresql-16.x-windows-x64.exe)

2. **Installation wizard:**
   - Click "Next" on welcome screen
   - Installation directory: `C:\Program Files\PostgreSQL\16` (default is fine)
   - Select components: ✅ All selected (PostgreSQL Server, pgAdmin 4, Command Line Tools)
   - Data directory: `C:\Program Files\PostgreSQL\16\data` (default is fine)

3. **Set password (IMPORTANT!):**
   - You'll be asked to set a password for the "postgres" superuser
   - **Choose a simple password** like: `postgres123` or `admin`
   - **WRITE IT DOWN!** You'll need this later
   - Example: I'll use `postgres` as the password in this guide

4. **Port:**
   - Default: `5432`
   - Keep this unless you have a conflict

5. **Locale:**
   - Default locale is fine
   - Click "Next"

6. **Summary:**
   - Review settings
   - Click "Next" to install

7. **Wait for installation:**
   - Takes 2-3 minutes
   - Click "Finish" when done

## Step 3: Verify PostgreSQL is Running

1. **Check Windows Services:**
   - Press `Win + R`
   - Type: `services.msc`
   - Press Enter
   - Look for "postgresql-x64-16" service
   - Status should be "Running"

2. **If not running:**
   - Right-click → "Start"

## Step 4: Create the FRAMES Database

### Option A: Using pgAdmin (GUI - Easiest)

1. **Open pgAdmin 4:**
   - Start Menu → PostgreSQL 16 → pgAdmin 4
   - Wait for browser to open

2. **Connect to server:**
   - Expand "Servers" in left panel
   - Click "PostgreSQL 16"
   - Enter your password when prompted

3. **Create database:**
   - Right-click "Databases"
   - Select "Create" → "Database..."
   - Database name: `frames`
   - Owner: `postgres` (default)
   - Click "Save"

4. **Verify:**
   - You should see "frames" under Databases

### Option B: Using Command Line (psql)

1. **Open Command Prompt:**
   - Press `Win + R`
   - Type: `cmd`
   - Press Enter

2. **Navigate to PostgreSQL bin:**
   ```cmd
   cd "C:\Program Files\PostgreSQL\16\bin"
   ```

3. **Connect to PostgreSQL:**
   ```cmd
   psql -U postgres
   ```

4. **Enter your password** when prompted

5. **Create database:**
   ```sql
   CREATE DATABASE frames;
   ```

6. **Verify:**
   ```sql
   \l
   ```
   You should see "frames" in the list

7. **Exit:**
   ```sql
   \q
   ```

## Step 5: Install Python Dependencies

1. **Open Command Prompt:**
   ```cmd
   cd "c:\Users\LizO5\FRAMES Python"
   ```

2. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

   This installs:
   - ✅ `psycopg2-binary` (PostgreSQL adapter)
   - ✅ `python-dotenv` (environment variables)

3. **Verify installation:**
   ```cmd
   pip list | findstr psycopg2
   pip list | findstr dotenv
   ```

## Step 6: Update .env File

1. **Open .env file** in your text editor:
   - Location: `c:\Users\LizO5\FRAMES Python\.env`

2. **Update DATABASE_URL:**

   Change from:
   ```
   DATABASE_URL=sqlite:///instance/frames.db
   ```

   To (replace `YOUR_PASSWORD` with your actual password):
   ```
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/frames
   ```

   **Examples:**

   If your password is `postgres`:
   ```
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/frames
   ```

   If your password is `admin123`:
   ```
   DATABASE_URL=postgresql://postgres:admin123@localhost:5432/frames
   ```

3. **Save the file**

## Step 7: Run the Migration

1. **Open Command Prompt:**
   ```cmd
   cd "c:\Users\LizO5\FRAMES Python\backend"
   ```

2. **Run migration script:**
   ```cmd
   python migrate_to_postgres.py
   ```

3. **Expected output:**
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
   ✅ Migrated X records from projects

   📦 Migrating teams...
   ✅ Migrated X records from teams

   📦 Migrating faculty...
   ✅ Migrated X records from faculty

   📦 Migrating interfaces...
   ✅ Migrated X records from interfaces

   ==================================================
   ✅ Migration Complete! Migrated X total records
   ==================================================
   ```

## Step 8: Test Your Application

1. **Start Flask server:**
   ```cmd
   cd "c:\Users\LizO5\FRAMES Python\backend"
   python app.py
   ```

2. **Expected output:**
   ```
    * Running on http://127.0.0.1:5000
   ```

3. **Open browser:**
   - Go to: http://localhost:5000
   - Test all pages
   - Verify data appears correctly

## Step 9: Verify Data in PostgreSQL

### Using pgAdmin:

1. Open pgAdmin 4
2. Navigate to: Servers → PostgreSQL 16 → Databases → frames → Schemas → public → Tables
3. Right-click any table (e.g., "teams") → View/Edit Data → All Rows
4. Verify your data appears

### Using psql:

```cmd
cd "C:\Program Files\PostgreSQL\16\bin"
psql -U postgres -d frames
```

```sql
-- See all tables
\dt

-- Count records in each table
SELECT COUNT(*) FROM teams;
SELECT COUNT(*) FROM faculty;
SELECT COUNT(*) FROM projects;
SELECT COUNT(*) FROM interfaces;

-- View some data
SELECT * FROM teams LIMIT 5;
```

## Troubleshooting

### Error: "Connection refused"

**Solution:**
1. Check PostgreSQL service is running (services.msc)
2. Verify port 5432 is not blocked by firewall
3. Try restarting PostgreSQL service

### Error: "Password authentication failed"

**Solution:**
1. Double-check your password in .env file
2. Make sure no extra spaces in DATABASE_URL
3. Try resetting postgres password:
   ```cmd
   cd "C:\Program Files\PostgreSQL\16\bin"
   psql -U postgres
   ALTER USER postgres PASSWORD 'newpassword';
   ```

### Error: "database 'frames' does not exist"

**Solution:**
1. Create the database in pgAdmin or psql
2. Make sure you spelled it correctly (lowercase "frames")

### Error: "psycopg2 module not found"

**Solution:**
```cmd
pip install psycopg2-binary
```

### Error: "No module named 'dotenv'"

**Solution:**
```cmd
pip install python-dotenv
```

### Port 5432 already in use

**Solution:**
- Another PostgreSQL instance is running
- OR use a different port (5433) and update .env:
  ```
  DATABASE_URL=postgresql://postgres:password@localhost:5433/frames
  ```

## After Migration

### Keep SQLite as Backup

Your original SQLite database is still at:
- `backend/instance/frames.db`

Don't delete it until you're confident PostgreSQL is working perfectly!

### Add pgAdmin to Path (Optional)

If you want to run `psql` from any folder:

1. Right-click "This PC" → Properties
2. Advanced System Settings → Environment Variables
3. Under System Variables, find "Path"
4. Click "Edit" → "New"
5. Add: `C:\Program Files\PostgreSQL\16\bin`
6. Click OK on all dialogs
7. Restart Command Prompt

### Enable Extensions (Optional)

For advanced features, connect with psql and run:

```sql
-- Vector search for AI
CREATE EXTENSION IF NOT EXISTS vector;

-- Full-text search
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

Note: `vector` extension needs to be installed separately (pgvector)

## Next Steps

✅ PostgreSQL installed and running
✅ Database created
✅ Migration complete
✅ Application tested

**What's next?**

According to [docs/IMPLEMENTATION_ROADMAP.md](docs/IMPLEMENTATION_ROADMAP.md):

**Phase 2: Discord Integration** - Capture real-time team communication
- Set up Discord bot
- Capture messages and interactions
- Derive knowledge transfer interfaces

See the roadmap for details!

## Useful PostgreSQL Commands

### View running PostgreSQL version:
```sql
SELECT version();
```

### List all databases:
```sql
\l
```

### Connect to frames database:
```sql
\c frames
```

### List all tables:
```sql
\dt
```

### Describe table structure:
```sql
\d teams
```

### Back up database:
```cmd
cd "C:\Program Files\PostgreSQL\16\bin"
pg_dump -U postgres frames > C:\backup\frames_backup.sql
```

### Restore database:
```cmd
psql -U postgres frames < C:\backup\frames_backup.sql
```

## Resources

- PostgreSQL Windows Documentation: https://www.postgresql.org/docs/current/tutorial-install.html
- pgAdmin Documentation: https://www.pgadmin.org/docs/
- psql Commands: https://www.postgresql.org/docs/current/app-psql.html

---

**Need help?** Refer back to [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) for general troubleshooting or [MIGRATION_QUICKSTART.md](MIGRATION_QUICKSTART.md) for quick reference.
