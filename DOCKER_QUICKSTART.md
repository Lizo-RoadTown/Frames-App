# Docker PostgreSQL - Super Quick Start! 🚀

You have Docker, so this is THE EASIEST method. 2 minutes total!

## Option 1: Docker Compose (Recommended - One Command!)

A `docker-compose.yml` file is already in your project. Just run:

```bash
cd "c:\Users\LizO5\FRAMES Python"
docker-compose up -d
```

✅ **Done!** PostgreSQL is running with database `frames` already created!

---

## Option 2: Docker Command (If you prefer manual control)

```bash
docker run --name frames-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=frames \
  -p 5432:5432 \
  -v frames-data:/var/lib/postgresql/data \
  -d postgres:15
```

✅ **Done!** PostgreSQL is running with database `frames` already created!

---

## Next Steps

### 1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 2. Update .env file:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/frames
```

### 3. Run migration:
```bash
cd backend
python migrate_to_postgres.py
```

### 4. Test app:
```bash
python app.py
```

---

## VS Code PostgreSQL Extension (Optional but Nice)

1. Install "PostgreSQL" by Microsoft in VS Code
2. Connect to: `localhost:5432`, user: `postgres`, password: `postgres`, database: `frames`
3. Browse your data directly in VS Code!

---

## Useful Commands

```bash
# Using Docker Compose:
docker-compose up -d          # Start
docker-compose down           # Stop
docker-compose logs -f        # View logs
docker-compose restart        # Restart

# Using Docker directly:
docker start frames-postgres  # Start
docker stop frames-postgres   # Stop
docker logs frames-postgres   # View logs
docker restart frames-postgres # Restart

# Connect to database:
docker exec -it frames-postgres psql -U postgres -d frames

# Backup:
docker exec frames-postgres pg_dump -U postgres frames > backup.sql
```

---

## Complete Setup Checklist

- [ ] Run `docker-compose up -d` (or docker run command)
- [ ] Run `pip install -r requirements.txt`
- [ ] Update `.env` with PostgreSQL connection string
- [ ] Run `python backend/migrate_to_postgres.py`
- [ ] Run `python backend/app.py`
- [ ] Test at http://localhost:5000

**That's it!** 🎉

See [POSTGRESQL_DOCKER_SETUP.md](POSTGRESQL_DOCKER_SETUP.md) for detailed documentation.
