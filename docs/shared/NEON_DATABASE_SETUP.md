# Neon Database Setup Guide

A quick reference for provisioning the FRAMES PostgreSQL database on [Neon](https://neon.tech) and wiring it into your local `.env`.

## 1. Create (or reuse) a Neon project
1. Sign in at [console.neon.tech](https://console.neon.tech/).
2. Click **Create project** → choose `PostgreSQL 15`, keep the free tier.
3. Give the project a descriptive name such as `frames-prod`.
4. Neon creates a default branch/database pair (e.g. `main` / `neondb`). You can keep those defaults.

## 2. Grab the connection string
1. In the project dashboard open **Connection Details**.
2. Click **Copy connection string** (the URI that looks like `postgresql://user:password@...neon.tech/neondb?sslmode=require`).
3. Store the string securely; never commit it. Place it in `secrets/notion_token.txt`? (No.)

## 3. Update `.env`
```
# Database
DATABASE_URL=postgresql://user:password@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```
Keep the URI exactly as Neon provides (it already enforces SSL).

## 4. Test the connection
```bash
python - <<'PY'
import os, psycopg2
conn = psycopg2.connect(os.environ["DATABASE_URL"])
with conn.cursor() as cur:
    cur.execute("select version();")
    print(cur.fetchone()[0])
conn.close()
PY
```
or use `psql "$env:DATABASE_URL"` if you have the CLI.

## 5. Recommended practices
- Use Neon branches for feature environments.
- Enable automatic daily backups (Neon keeps point-in-time restore for 7 days on the free tier).
- When sharing credentials with agents, use `.env` or secret files—never commit real URIs.
