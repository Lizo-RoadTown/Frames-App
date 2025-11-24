# Shared Database

Centralized database models, connection utilities, and migration scripts used across all FRAMES applications.

## Overview

All three FRAMES applications (research-analytics, onboarding-lms, ai-core) connect to the same Neon PostgreSQL database using these shared components.

## Files

### Core Components

- **`db_connection.py`** - Centralized database connection utility
  - Creates SQLAlchemy engine from environment variables
  - Handles connection pooling
  - Used by all apps

- **`db_models.py`** - SQLAlchemy ORM models
  - Defines 14 database tables
  - Used for migrations and ORM queries
  - Mirrors the dataclass models in `models.py`

- **`database.py`** - Flask-SQLAlchemy instance
  - Integrates SQLAlchemy with Flask apps
  - Used by Flask applications

- **`models.py`** - Lightweight dataclass models
  - Python dataclasses for type safety
  - Used in application logic
  - More lightweight than ORM models

### Utilities

- **`bootstrap_db.py`** - Initialize database schema
  - Creates all 14 tables from scratch
  - Safe to run multiple times (won't drop existing data)
  - Run once when setting up new database

- **`test_db_connection.py`** - Test database connectivity
  - Verifies connection string is correct
  - Runs simple SELECT 1 query
  - Use for debugging connection issues

## Database Schema

### Current Tables (14 total)

#### Core Entities
- `universities` - 8 collaborating universities
- `students` - Student participants
- `faculty` - Faculty and researchers
- `teams` - Student teams
- `projects` - Research projects

#### Analytics & Risk Assessment
- `risk_factors` - Identified risk factors
- `factor_values` - Risk factor measurements
- `outcomes` - Mission outcomes
- `interfaces` - Team interfaces
- `interface_factor_values` - Interface-specific factor values

#### AI/ML Components
- `factor_models` - Trained prediction models
- `model_factors` - Factors used in models
- `model_validations` - Model performance metrics

#### Auditing
- `audit_logs` - System activity logs

### Planned Tables

For onboarding-lms:
- `modules` - Training modules
- `module_sections` - Module content sections
- `module_assignments` - Student assignments
- `module_progress` - Progress tracking
- `module_analytics_events` - Detailed analytics
- `module_feedback` - Student feedback

## Setup

### 1. Configure Environment

Create `.env` file in your app directory:
```bash
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key-here
```

### 2. Initialize Database

From the repository root:
```bash
python shared/database/bootstrap_db.py
```

### 3. Test Connection

```bash
python shared/database/test_db_connection.py
```

Expected output:
```
Connection test succeeded (SELECT 1 -> 1)
```

## Usage in Applications

### Using in Flask App

```python
import sys
sys.path.append('../../shared/database')

from db_connection import get_engine
from db_models import TeamModel, StudentModel

engine = get_engine()
# Use engine for queries
```

### Using Bootstrap Script

```python
from shared.database.bootstrap_db import bootstrap_database

# Initialize all tables
bootstrap_database()
```

### Testing Connection

```python
from shared.database.db_connection import get_engine

engine = get_engine()
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(f"Connected: {result.scalar()}")
```

## Database Provider: Neon PostgreSQL

**Provider:** Neon (https://neon.tech)
**Plan:** Free tier
**Features:**
- PostgreSQL 15
- Generous free tier limits
- Auto-suspend when inactive (saves resources)
- Easy connection string management
- No credit card required for free tier

**Connection String Format:**
```
postgresql://username:password@host.region.postgres.neon.tech:5432/dbname?sslmode=require
```

## Migrations

### Current Migration Strategy

1. Update `db_models.py` with new tables/columns
2. Run `bootstrap_db.py` to create new tables
3. Manually migrate existing data if needed

### Future: Alembic Migrations (Planned)

For production, we'll add Alembic for proper database migrations:
- Track schema changes over time
- Rollback capability
- Automatic migration generation
- Better team collaboration

## Adding New Tables

When adding tables for new features:

1. **Update `db_models.py`:**
```python
class NewTableModel(db.Model):
    __tablename__ = 'new_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    # ... more columns
```

2. **Run bootstrap:**
```bash
python shared/database/bootstrap_db.py
```

3. **Test in all apps** to ensure compatibility

4. **Document changes** in this README and commit

## Best Practices

✅ **DO:**
- Use `db_connection.get_engine()` for database access
- Test connection before making schema changes
- Document new tables in this README
- Use transactions for multi-step operations
- Add indexes for frequently queried columns

❌ **DON'T:**
- Hardcode connection strings in apps
- Create separate database instances per app
- Modify shared models without testing all apps
- Drop tables manually (use migrations)
- Store sensitive data unencrypted

## Troubleshooting

### Connection Failed
```bash
# Check .env file has correct DATABASE_URL
# Test connection
python shared/database/test_db_connection.py
```

### Tables Not Found
```bash
# Initialize database schema
python shared/database/bootstrap_db.py
```

### Import Errors
```python
# Add shared database to Python path
import sys
sys.path.append('../../shared/database')
```

## Contact

Questions about database schema or shared components:
Elizabeth Osborn, Ph.D. - eosborn@cpp.edu
