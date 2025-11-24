# Azure PostgreSQL Free Tier - Quick Fix

## Problem

You're trying to deploy with `Standard_D4s_v3` which is **NOT free tier** and will fail deployment or charge you money.

---

## Solution: Use the Azure Portal (Easier than Template)

**The deployment template is complex. Let's use the Azure Portal GUI instead:**

### Step 1: Delete Failed Deployment (if any)

1. Go to [Azure Portal](https://portal.azure.com)
2. Search for "Resource groups"
3. If you see "FRAMES-Resources", delete it (it's from failed deployment)
4. Start fresh

---

### Step 2: Create PostgreSQL Database (Correct Way)

1. **In Azure Portal, click "+ Create a resource"**

2. **Search: "Azure Database for PostgreSQL"**
   - Select "Azure Database for PostgreSQL Flexible Server"
   - Click "Create"

3. **Basics Tab - IMPORTANT SETTINGS:**

   ```
   Subscription: Azure for Students
   Resource Group: Create new → "FRAMES-Resources"
   Server name: frames-db
   Region: West US 2 (or closest to you)
   PostgreSQL version: 15
   Workload type: Development ← IMPORTANT!

   ⚠️ CRITICAL: Click "Configure server"
   ```

4. **In Configure Server Dialog:**

   ```
   Compute tier: Burstable ← NOT General Purpose!
   Compute size: Standard_B1ms ← This is the FREE tier!

   Verify it shows:
   - 1 vCore
   - 2 GiB memory
   - ✓ Free tier eligible

   Storage: 32 GiB ← Maximum for free tier
   Backup retention: 7 days

   Click "Save"
   ```

5. **Authentication:**
   ```
   Authentication method: PostgreSQL authentication only
   Admin username: framesadmin
   Password: [Create strong password - WRITE IT DOWN!]
   Confirm password: [Same password]
   ```

6. **Networking Tab:**
   ```
   Connectivity method: Public access (allowed IP addresses)

   Firewall rules:
   ☑ Allow public access from any Azure service
   ☑ Add current client IP address
   ```

7. **All Other Tabs:**
   - Leave defaults
   - Skip to "Review + Create"

8. **Review + Create:**
   ```
   ⚠️ VERIFY: Should say "Estimated cost: $0.00/month"

   If it shows ANY cost, go back and check:
   - Compute tier = Burstable
   - Compute size = Standard_B1ms
   - Storage = 32 GiB or less
   ```

9. **Click "Create"**
   - Deployment takes 5-10 minutes
   - Wait for "Deployment complete"

---

## Step 3: Get Connection Details

Once deployment completes:

1. Click "Go to resource"

2. Look for **Server name** on Overview page:
   ```
   frames-db.postgres.database.azure.com
   ```

3. Click "Connection strings" (left sidebar under Settings)

4. Copy the connection string format:
   ```
   Host=frames-db.postgres.database.azure.com
   Port=5432
   Database=postgres
   Username=framesadmin
   Password=[your password]
   SSL Mode=Require
   ```

---

## Step 4: Create FRAMES Database

### Option A: Azure Cloud Shell (Easiest)

1. In Azure Portal, click **Cloud Shell** icon (>_) at top right

2. If prompted, select **Bash**

3. Run this command (replace with YOUR server name and password):
   ```bash
   psql "host=frames-db.postgres.database.azure.com port=5432 dbname=postgres user=framesadmin sslmode=require"
   ```

4. Enter your password when prompted

5. Create the database:
   ```sql
   CREATE DATABASE frames;
   ```

6. Verify it was created:
   ```sql
   \l
   ```
   You should see `frames` in the list

7. Exit:
   ```sql
   \q
   ```

---

## Step 5: Update Your .env File

Create or update `c:\Users\LizO5\FRAMES Python\.env`:

```env
# FRAMES Azure Database
DATABASE_URL=postgresql://framesadmin:YOUR_ACTUAL_PASSWORD@frames-db.postgres.database.azure.com:5432/frames?sslmode=require

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Generate a secure secret key
SECRET_KEY=your-secret-key-here

# Azure info (optional)
AZURE_RESOURCE_GROUP=FRAMES-Resources
```

**To generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Step 6: Test Connection

From your computer:

```bash
# Navigate to project
cd "c:\Users\LizO5\FRAMES Python"

# Activate virtual environment
venv\Scripts\activate

# Test connection
python -c "from sqlalchemy import create_engine; import os; from dotenv import load_dotenv; load_dotenv(); engine = create_engine(os.getenv('DATABASE_URL')); conn = engine.connect(); print('✅ Connection successful!'); conn.close()"
```

**Expected output:**
```
✅ Connection successful!
```

---

## Common Errors & Fixes

### Error: "Deployment failed - quota exceeded"
**Cause:** Selected wrong VM size (not B1ms)
**Fix:** Delete resource group, start over with Burstable B1ms

### Error: "Cost will be $XX/month"
**Cause:** Wrong tier or storage size
**Fix:** Must be:
- Compute tier: **Burstable**
- Compute size: **Standard_B1ms**
- Storage: **≤ 32 GiB**

### Error: "Connection refused"
**Cause:** Firewall not configured
**Fix:**
1. Go to your PostgreSQL server in Azure
2. Click "Networking"
3. Add your IP address
4. Check "Allow Azure services"
5. Click "Save"

### Error: "SSL required"
**Cause:** Missing sslmode parameter
**Fix:** Add `?sslmode=require` to end of DATABASE_URL

---

## Verify Free Tier

After deployment, check you're actually using free tier:

1. Go to Azure Portal → **Cost Management + Billing**
2. Click **Cost analysis**
3. Filter by resource group: "FRAMES-Resources"
4. Should show: **$0.00**

If it shows any cost, you selected the wrong tier!

---

## What You Should Have

After successful setup:

✅ PostgreSQL server named `frames-db`
✅ Database named `frames` (not postgres)
✅ Connection string in `.env` file
✅ Firewall allows your IP
✅ Cost shows $0.00
✅ Can connect from your laptop

---

## Next Steps

Once database is working:

1. **Initialize schema:**
   ```bash
   python backend/database.py
   ```

2. **Or migrate existing data:**
   ```bash
   python backend/migrate_to_postgres.py
   ```

3. **Verify tables created:**
   ```bash
   # From Cloud Shell
   psql "host=frames-db.postgres.database.azure.com port=5432 dbname=frames user=framesadmin sslmode=require"

   \dt  # List tables
   ```

---

## Summary: Why Template Failed

The ARM template you showed has:
```json
"vmName": {
    "defaultValue": "Standard_D4s_v3"  // ❌ Wrong!
}
```

**Should be:**
```json
"vmName": {
    "defaultValue": "Standard_B1ms"  // ✅ Correct!
}
```

**But honestly, just use the Azure Portal GUI - it's much easier and you can see what you're selecting!**

---

**Need help?** Let me know what error message you're seeing and I can help troubleshoot.

---

*Last updated: 2025-01-23*
