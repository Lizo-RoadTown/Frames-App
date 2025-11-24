# Azure Database for PostgreSQL Setup Guide

## Overview
This guide will help you set up a FREE Azure Database for PostgreSQL for the FRAMES project using your Azure for Students account.

**Cost:** $0/month (750 hours free = 24/7 uptime)
**Storage:** 32 GB (more than enough)
**Backup:** 32 GB included

---

## Step 1: Access Azure Portal

1. Go to [portal.azure.com](https://portal.azure.com)
2. Sign in with your Microsoft/university account
3. Verify you see "Azure for Students" in your subscriptions

---

## Step 2: Create PostgreSQL Database

### Using Azure Portal (Recommended for First Time)

1. **Click "Create a resource"** (top left)

2. **Search for "Azure Database for PostgreSQL"**
   - Select "Azure Database for PostgreSQL Flexible Server"
   - Click **Create**

3. **Basics Tab:**
   ```
   Subscription: Azure for Students
   Resource Group: Create new → "FRAMES-Resources"
   Server name: frames-db (or frames-postgres)
   Region: Choose closest (e.g., West US 2)
   PostgreSQL version: 15 (latest stable)
   Workload type: Development

   Compute + Storage: Click "Configure server"
   └─ Compute tier: Burstable
   └─ Compute size: B1ms (1 vCore, 2 GiB RAM) ✓ Free tier eligible
   └─ Storage: 32 GiB (maximum free tier)
   └─ Backup retention: 7 days

   Authentication:
   └─ Authentication method: PostgreSQL authentication
   └─ Admin username: framesadmin
   └─ Password: [Create strong password - SAVE THIS!]
   ```

4. **Networking Tab:**
   ```
   Connectivity method: Public access (allowed IP addresses)

   Firewall rules:
   ☑ Allow public access from any Azure service within Azure
   ☑ Add current client IP address (your laptop)

   Note: You can add more IPs later
   ```

5. **Security Tab:**
   ```
   (Use defaults - all optional for free tier)
   ```

6. **Tags Tab:**
   ```
   Name: Project    Value: FRAMES
   Name: Environment    Value: Production
   (Optional but helpful for organization)
   ```

7. **Review + Create:**
   - Verify "Estimated cost: $0.00/month" appears
   - Click **Create**
   - Deployment takes 5-10 minutes

---

## Step 3: Get Connection String

Once deployment completes:

1. **Go to your PostgreSQL server** (frames-db)

2. **Click "Connection strings"** (left sidebar under Settings)

3. **Copy the connection string:**
   ```
   Host=frames-db.postgres.database.azure.com
   Port=5432
   Database={your_database}
   Username=framesadmin
   Password={your_password}
   SSL Mode=Require
   ```

4. **Format for Python (.env file):**
   ```
   postgresql://framesadmin:{password}@frames-db.postgres.database.azure.com:5432/postgres?sslmode=require
   ```

   **Important:**
   - Replace `{password}` with your actual password
   - Default database is `postgres` - we'll create `frames` database next

---

## Step 4: Create FRAMES Database

### Option A: Using Azure Cloud Shell (Easy)

1. In Azure Portal, click **Cloud Shell** icon (>_) at top
2. Select **Bash**
3. Run:
   ```bash
   psql "host=frames-db.postgres.database.azure.com port=5432 dbname=postgres user=framesadmin sslmode=require"
   # Enter password when prompted

   # Create database
   CREATE DATABASE frames;

   # Verify
   \l

   # Exit
   \q
   ```

### Option B: Using pgAdmin (If you have it installed locally)

1. Open pgAdmin
2. Right-click Servers → Create → Server
3. Enter:
   - Name: FRAMES Azure
   - Host: frames-db.postgres.database.azure.com
   - Port: 5432
   - Username: framesadmin
   - Password: [your password]
   - SSL: Require
4. Right-click Databases → Create → Database
5. Name: frames

---

## Step 5: Update Your .env File

Update `c:\Users\LizO5\FRAMES Python\.env`:

```env
# FRAMES Azure Production Database
DATABASE_URL=postgresql://framesadmin:YOUR_PASSWORD@frames-db.postgres.database.azure.com:5432/frames?sslmode=require

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=YOUR_NEW_SECRET_KEY_HERE_GENERATE_ONE

# Azure Configuration (optional - for future use)
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=FRAMES-Resources
```

**Security Note:**
- Never commit `.env` to Git (already in .gitignore ✓)
- Generate new SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`

---

## Step 6: Update Firewall Rules (As Needed)

### Add Team Member IP Addresses

1. Go to your PostgreSQL server in Azure Portal
2. Click **Networking** (left sidebar)
3. Under **Firewall rules**, click **+ Add IP address**
4. Enter:
   - Rule name: "TeamLead-John" (descriptive name)
   - Start IP: [their IP]
   - End IP: [same IP for single address]
5. Click **Save**

### Allow All Azure Services (Already done)
- ☑ "Allow public access from any Azure service" should be checked
- This lets your Flask app (when deployed to Azure) access the database

---

## Step 7: Test Connection

From your local machine:

```bash
# Activate venv
cd "c:\Users\LizO5\FRAMES Python"
venv\Scripts\activate

# Install Azure-specific psycopg2 if needed
pip install psycopg2-binary

# Test connection
python -c "from sqlalchemy import create_engine; import os; from dotenv import load_dotenv; load_dotenv(); engine = create_engine(os.getenv('DATABASE_URL')); conn = engine.connect(); print('✓ Connection successful!'); conn.close()"
```

If successful, you'll see: `✓ Connection successful!`

---

## Step 8: Run Database Migration

Now migrate your existing data (if any) or initialize fresh database:

### Option A: Fresh Database (No existing data)

```bash
python backend/database.py
```

This creates all tables from scratch.

### Option B: Migrate from SQLite (If you have data)

```bash
python backend/migrate_to_postgres.py
```

This copies all data from `backend/instance/frames.db` to Azure PostgreSQL.

---

## Step 9: Verify Tables Created

### Using Azure Cloud Shell:

```bash
psql "host=frames-db.postgres.database.azure.com port=5432 dbname=frames user=framesadmin sslmode=require"

# List all tables
\dt

# Should see:
# universities, teams, students, faculty, projects, interfaces, etc.

# Check sample data
SELECT * FROM universities;

\q
```

---

## Common Issues & Solutions

### Issue: "Could not connect to server"
**Solution:**
- Check firewall rules include your IP
- Verify password is correct
- Confirm SSL mode is required: `?sslmode=require`

### Issue: "Database does not exist"
**Solution:**
- Make sure you created `frames` database (Step 4)
- Check DATABASE_URL points to `frames` not `postgres`

### Issue: "SSL connection required"
**Solution:**
- Add `?sslmode=require` to end of DATABASE_URL

### Issue: "Cost showing as non-zero"
**Solution:**
- Verify Compute tier is "Burstable B1ms"
- Check Storage is ≤ 32 GB
- Confirm "Azure for Students" subscription is selected

---

## Monitoring Your Free Tier Usage

1. Go to **Azure Portal** → **Cost Management + Billing**
2. Click **Cost analysis**
3. Filter by "FRAMES-Resources" resource group
4. Should show $0.00 as long as you stay within:
   - 750 hours/month compute
   - 32 GB storage
   - 32 GB backup

**Tip:** Set up a budget alert:
- Cost Management → Budgets → Create
- Set budget to $1.00
- Get email if you somehow exceed free tier

---

## Next Steps

Once database is set up and running:

1. ✅ Update `.env` with Azure connection string
2. ✅ Test connection
3. ✅ Run migration or initialize database
4. ✅ Update documentation to reflect Azure setup
5. ✅ Share connection instructions with team (minus password!)
6. 🔄 Deploy Flask app to Azure App Service (optional, future)
7. 🔄 Set up automated backups (already included in free tier!)

---

## Security Best Practices

### Passwords
- Store database password in `.env` (gitignored)
- Use different passwords for dev/prod
- Rotate passwords periodically

### Connection Strings
- Never commit to Git
- Share with team via secure channel (Azure Key Vault, 1Password, etc.)
- Each team member can have their own database user (optional)

### Firewall
- Only add IPs that need access
- Remove old team members' IPs when they leave
- Consider VPN if available

### Backups
- Azure automatically backs up (7-day retention included)
- Test restore process periodically
- Export critical data separately

---

## Azure Resources Used

- **PostgreSQL Flexible Server**: frames-db
- **Resource Group**: FRAMES-Resources
- **Region**: [Your selected region]
- **Free Tier**: 750 hours compute + 32GB storage (monthly)
- **Cost**: $0.00/month ✓

---

## Support

### Azure Documentation
- [Azure Database for PostgreSQL](https://learn.microsoft.com/azure/postgresql/)
- [Azure for Students](https://azure.microsoft.com/free/students/)

### FRAMES Project
- See main README.md for project-specific help
- Contact: [Your contact info]

---

**Setup completed?** Mark this checklist:

- [ ] Azure PostgreSQL server created
- [ ] Database `frames` created
- [ ] Firewall rules configured
- [ ] .env file updated with connection string
- [ ] Connection tested successfully
- [ ] Database initialized/migrated
- [ ] Tables verified in Azure
- [ ] Team members added to firewall (if applicable)
- [ ] Budget alert configured (optional)
- [ ] Backup strategy documented

**Estimated setup time:** 20-30 minutes for first time

---

*Last updated: 2025-01-23*
