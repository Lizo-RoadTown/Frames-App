# PostgreSQL Setup with Docker - Quick & Easy! 🐳

Since you have Docker Desktop, this is the FASTEST way to get PostgreSQL running.

## Benefits of Docker Approach:

✅ No installer needed
✅ Clean and isolated
✅ Easy to reset/restart
✅ Same setup works everywhere
✅ Takes 2 minutes instead of 20

---

## Step 1: Install VS Code PostgreSQL Extension

1. **Open VS Code**
2. **Go to Extensions** (Ctrl+Shift+X)
3. **Search for:** `PostgreSQL`
4. **Install:** "PostgreSQL" by Microsoft (Chris Kolkman's is also good)

---

## Step 2: Start PostgreSQL in Docker

### Option A: Using Command Line (Recommended)

Open Command Prompt or PowerShell and run:

```bash
docker run --name frames-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -v frames-data:/var/lib/postgresql/data \
  -d postgres:15
```

**What this does:**
- Creates container named `frames-postgres`
- Sets postgres password to `postgres`
- Exposes port 5432
- Creates persistent volume `frames-data` (data survives container restart)
- Uses PostgreSQL 15

**Expected output:**
```
Unable to find image 'postgres:15' locally
15: Pulling from library/postgres
...
Status: Downloaded newer image for postgres:15
abc123def456... (long container ID)
```

### Option B: Using Docker Desktop GUI

1. Open Docker Desktop
2. Search for `postgres` in Images
3. Pull `postgres:15`
4. Click "Run"
5. Expand "Optional settings"
   - Container name: `frames-postgres`
   - Port: `5432`
   - Environment variable: `POSTGRES_PASSWORD=postgres`
6. Click "Run"

---

## Step 3: Verify Container is Running

```bash
docker ps
```

You should see:
```
CONTAINER ID   IMAGE         COMMAND                  STATUS          PORTS                    NAMES
abc123def456   postgres:15   "docker-entrypoint.s…"   Up 30 seconds   0.0.0.0:5432->5432/tcp   frames-postgres
```

**OR** check Docker Desktop → Containers tab → `frames-postgres` should be running (green)

---

## Step 4: Create 'frames' Database

### Option A: Using Command Line

```bash
docker exec -it frames-postgres psql -U postgres -c "CREATE DATABASE frames;"
```

**Expected output:**
```
CREATE DATABASE
```

**Verify it was created:**
```bash
docker exec -it frames-postgres psql -U postgres -c "\l"
```

You should see `frames` in the list.

### Option B: Using VS Code PostgreSQL Extension

1. **Open Command Palette** (Ctrl+Shift+P)
2. **Type:** `PostgreSQL: Add Connection`
3. **Enter details:**
   - Hostname: `localhost`
   - User: `postgres`
   - Password: `postgres`
   - Port: `5432`
   - Use SSL: `Standard Connection`
   - Database: `postgres` (connect to default first)
4. **Save connection**
5. **In PostgreSQL explorer**, right-click your connection
6. **Select "New Query"**
7. **Type:** `CREATE DATABASE frames;`
8. **Run query** (Ctrl+Shift+E or click play button)

### Option C: Using Docker Desktop + psql

1. Open Docker Desktop
2. Click on `frames-postgres` container
3. Click "Terminal" tab (opens shell inside container)
4. Run:
   ```bash
   psql -U postgres
   ```
5. In psql prompt:
   ```sql
   CREATE DATABASE frames;
   \l
   \q
   ```

---

## Step 5: Install Python Dependencies

Open Command Prompt in your project directory:

```bash
cd "c:\Users\LizO5\FRAMES Python"
pip install -r requirements.txt
```

This installs:
- ✅ `psycopg2-binary`
- ✅ `python-dotenv`

---

## Step 6: Update .env File

Open `.env` file and update:

```bash
# Change from:
DATABASE_URL=sqlite:///instance/frames.db

# To:
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/frames
```

**Save the file.**

---

## Step 7: Run Migration

```bash
cd backend
python migrate_to_postgres.py
```

**Expected output:**
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

---

## Step 8: Test Application

```bash
cd backend
python app.py
```

Open browser: http://localhost:5000

Test all pages to verify data appears correctly!

---

## Step 9: View Data in VS Code (Optional)

1. **Open PostgreSQL extension** in VS Code (database icon in sidebar)
2. **Connect to your database** (should auto-detect localhost:5432)
3. **Expand:** frames → Schemas → public → Tables
4. **Right-click any table** → "Select Top 1000"
5. **View your data** directly in VS Code!

---

## Docker Management Commands

### Check if container is running:
```bash
docker ps
```

### Stop PostgreSQL:
```bash
docker stop frames-postgres
```

### Start PostgreSQL again:
```bash
docker start frames-postgres
```

### View logs:
```bash
docker logs frames-postgres
```

### Connect to PostgreSQL shell:
```bash
docker exec -it frames-postgres psql -U postgres -d frames
```

### Remove container (if you need to start fresh):
```bash
docker stop frames-postgres
docker rm frames-postgres
# Then run the 'docker run' command again from Step 2
```

### Remove container AND data (complete reset):
```bash
docker stop frames-postgres
docker rm frames-postgres
docker volume rm frames-data
# Then run the 'docker run' command again from Step 2
```

---

## Troubleshooting

### Error: "Port 5432 already in use"

Another PostgreSQL is running. Either:

**Option 1:** Stop other PostgreSQL
```bash
# Check what's using port 5432
netstat -ano | findstr :5432

# Stop PostgreSQL Windows service (if installed)
# services.msc → postgresql → Stop
```

**Option 2:** Use different port
```bash
# Use port 5433 instead
docker run --name frames-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5433:5432 \
  -v frames-data:/var/lib/postgresql/data \
  -d postgres:15

# Update .env:
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/frames
```

### Error: "Cannot connect to Docker daemon"

- Make sure Docker Desktop is running
- Check system tray for Docker icon
- Restart Docker Desktop

### Error: "psycopg2 not installed"

```bash
pip install psycopg2-binary
```

### Error: "database 'frames' does not exist"

Run the create database command again:
```bash
docker exec -it frames-postgres psql -U postgres -c "CREATE DATABASE frames;"
```

### Error: "password authentication failed"

Make sure .env has the correct password:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/frames
                                    ^^^^^^^^ this must match POSTGRES_PASSWORD from docker run
```

---

## Auto-Start PostgreSQL on Boot (Optional)

If you want PostgreSQL to start automatically when you boot your computer:

```bash
docker update --restart unless-stopped frames-postgres
```

Now PostgreSQL will start whenever Docker Desktop starts!

---

## Backup and Restore

### Backup database:
```bash
docker exec frames-postgres pg_dump -U postgres frames > backup.sql
```

### Restore database:
```bash
docker exec -i frames-postgres psql -U postgres frames < backup.sql
```

---

## Advantages of Docker Setup

✅ **Isolated:** Doesn't affect your system
✅ **Portable:** Same setup on any OS
✅ **Easy reset:** Just delete and recreate container
✅ **Version control:** Easy to switch PostgreSQL versions
✅ **Clean uninstall:** Remove container, done!

---

## Next Steps

Once PostgreSQL migration is complete:

1. ✅ PostgreSQL running in Docker
2. ✅ Database created
3. ✅ Data migrated
4. ✅ Application tested
5. 🔜 **Phase 2: Discord Integration**

See [docs/IMPLEMENTATION_ROADMAP.md](docs/IMPLEMENTATION_ROADMAP.md) for next steps!

---

## Quick Reference Card

```bash
# Start container (first time)
docker run --name frames-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v frames-data:/var/lib/postgresql/data -d postgres:15

# Create database
docker exec -it frames-postgres psql -U postgres -c "CREATE DATABASE frames;"

# Connection string for .env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/frames

# Start/stop
docker start frames-postgres
docker stop frames-postgres

# View logs
docker logs frames-postgres

# Connect to database
docker exec -it frames-postgres psql -U postgres -d frames

# Backup
docker exec frames-postgres pg_dump -U postgres frames > backup.sql
```

---

**That's it!** Docker makes this SO much easier than installing PostgreSQL traditionally. 🎉
