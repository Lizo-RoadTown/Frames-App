# Repository Reorganization Plan

## Current State Analysis

Your repository currently has **mixed concerns** - all three applications are intermingled in the same directories.

**Current structure:**
```
FRAMES Python/
├── backend/           # Mix of all three apps
├── frontend/          # Legacy HTML/JS (research analytics?)
├── docs/              # Various docs
└── (many root-level docs)
```

**Problem:** Hard to tell which code belongs to which application.

---

## Target Structure: Organized Monorepo

### **Goal:** Clear separation of three applications with shared foundation

```
FRAMES/
│
├── apps/
│   ├── onboarding-lms/           # APPLICATION 1
│   │   ├── frontend/             # React student viewer
│   │   ├── admin-ui/             # React team lead dashboard
│   │   ├── api/                  # Flask API for modules
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   ├── research-analytics/       # APPLICATION 2
│   │   ├── frontend/             # React analytics dashboard
│   │   ├── api/                  # Flask API for research
│   │   ├── analytics/            # NDA engine, calculations
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   └── ai-prediction-core/       # APPLICATION 3
│       ├── models/               # ML model definitions
│       ├── training/             # Training pipelines
│       ├── inference/            # Prediction service
│       ├── api/                  # Flask prediction API
│       ├── requirements.txt
│       └── README.md
│
├── shared/
│   ├── database/
│   │   ├── models/               # SQLAlchemy models (all apps)
│   │   │   ├── university.py
│   │   │   ├── team.py
│   │   │   ├── student.py
│   │   │   ├── module.py        # Onboarding LMS
│   │   │   ├── interface.py     # Research analytics
│   │   │   └── prediction.py    # AI core
│   │   │
│   │   ├── migrations/           # Alembic migrations
│   │   │   ├── versions/
│   │   │   └── env.py
│   │   │
│   │   └── seeds/                # Test data
│   │       ├── universities.sql
│   │       └── sample_data.sql
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── permissions.py        # Role-based access
│   │   └── decorators.py         # @require_auth, etc.
│   │
│   ├── utils/
│   │   ├── validators.py
│   │   └── helpers.py
│   │
│   └── config/
│       ├── base.py               # Shared config
│       └── database.py           # DB connection logic
│
├── docs/
│   ├── README.md                 # Docs overview
│   │
│   ├── onboarding-lms/
│   │   ├── README.md
│   │   ├── ARCHITECTURE.md
│   │   ├── API_DOCUMENTATION.md
│   │   ├── AI_ASSISTANT.md
│   │   └── TEAM_LEAD_GUIDE.md
│   │
│   ├── research-analytics/
│   │   ├── README.md
│   │   ├── ARCHITECTURE.md
│   │   ├── NDA_DIAGNOSTICS.md
│   │   └── RESEARCHER_GUIDE.md
│   │
│   ├── ai-prediction-core/
│   │   ├── README.md
│   │   ├── ML_MODELS.md
│   │   └── TRAINING_GUIDE.md
│   │
│   └── shared/
│       ├── DATABASE_SCHEMA.md
│       ├── AZURE_SETUP.md
│       ├── AUTHENTICATION.md
│       └── CONTRIBUTING.md
│
├── scripts/
│   ├── setup_dev_environment.sh
│   ├── migrate_database.py
│   └── seed_database.py
│
├── .github/
│   └── workflows/
│       ├── onboarding-lms-ci.yml
│       ├── research-analytics-ci.yml
│       └── ai-core-ci.yml
│
├── .env.example
├── .gitignore
├── docker-compose.yml            # All three apps for local dev
├── README.md                     # Master README
└── requirements-dev.txt          # Dev dependencies
```

---

## Step-by-Step Migration

### **Phase 1: Create New Structure (No Code Movement Yet)**

**Step 1:** Create documentation branch
```bash
git checkout -b reorganize/documentation
```

**Step 2:** Create new folder structure
```bash
# Create apps directories
mkdir -p apps/onboarding-lms/{frontend,admin-ui,api}
mkdir -p apps/research-analytics/{frontend,api,analytics}
mkdir -p apps/ai-prediction-core/{models,training,inference,api}

# Create shared directories
mkdir -p shared/{database/{models,migrations,seeds},auth,utils,config}

# Create docs structure
mkdir -p docs/{onboarding-lms,research-analytics,ai-prediction-core,shared}

# Create scripts directory
mkdir scripts
```

**Step 3:** Move documentation files
```bash
# Move app-specific docs
mv AZURE_DATABASE_SETUP.md docs/shared/
mv AI_POWERED_MODULE_SYSTEM.md docs/onboarding-lms/
mv STUDENT_ONBOARDING_SYSTEM_DESIGN.md docs/onboarding-lms/ARCHITECTURE.md
mv TEAM_LEAD_CONTENT_WORKFLOW.md docs/onboarding-lms/TEAM_LEAD_GUIDE.md

# Move planning docs to docs/shared
mv PROJECT_ROADMAP_2025.md docs/shared/
mv IMMEDIATE_ACTION_PLAN.md docs/shared/

# Keep or archive
mv UI_INTEGRATION_PLAN.md docs/archive/
mv REACT_LEARNING_ROADMAP.md docs/archive/
```

**Step 4:** Create new master README
```bash
# We'll create this together
```

**Step 5:** Commit documentation reorganization
```bash
git add .
git commit -m "Reorganize documentation for three-app architecture

- Separate docs for onboarding-lms, research-analytics, ai-prediction-core
- Move shared docs to docs/shared
- Archive old planning docs
- Prepare for code reorganization"

git push origin reorganize/documentation
```

---

### **Phase 2: Move Code (Carefully!)**

**Step 1:** Create code reorganization branch
```bash
git checkout -b reorganize/code-structure
```

**Step 2:** Move existing backend code

Currently your `backend/` has:
- `app.py` - Main Flask app (ALL routes mixed together)
- `db_models.py` - Database models (ALL tables)
- `analytics.py` - NDA diagnostics (Research analytics)
- `energy_engine.py` - Energy calculations (Research analytics)
- Migration scripts (Shared)

**Plan:**
```bash
# Shared database models
mv backend/db_models.py shared/database/models/__init__.py
# Then split into individual files (we'll do this together)

# Research analytics
mv backend/analytics.py apps/research-analytics/analytics/nda_diagnostics.py
mv backend/energy_engine.py apps/research-analytics/analytics/energy_engine.py

# Migration scripts
mv backend/migrate_to_postgres.py shared/database/migrations/
mv backend/run_migration.py shared/database/migrations/

# We'll split app.py routes across three API folders
# (This is most complex - do together with Claude Code)
```

**Step 3:** Move frontend code

Currently your `frontend/` has:
- `templates/` - 16 HTML files (Research analytics dashboard)
- `static/` - CSS, JS

**Plan:**
```bash
# These are research analytics templates
mv frontend/templates apps/research-analytics/frontend/templates/
mv frontend/static apps/research-analytics/frontend/static/

# Create new frontend directories
mkdir apps/onboarding-lms/frontend/src
mkdir apps/research-analytics/frontend/src  # For React version
```

**Step 4:** Test everything still works
```bash
# Update imports in Python files
# Test Flask app runs
# Commit incremental changes
```

---

### **Phase 3: Create App-Specific Entry Points**

**Onboarding LMS API:**
```python
# apps/onboarding-lms/api/app.py

from flask import Flask
from shared.database.models import db
from shared.auth import require_auth

app = Flask(__name__)
app.config.from_object('shared.config.base')

# Only module-related routes
from .routes import modules, progress, analytics

app.register_blueprint(modules.bp)
app.register_blueprint(progress.bp)
app.register_blueprint(analytics.bp)

if __name__ == '__main__':
    app.run(port=5001)  # Different port per app
```

**Research Analytics API:**
```python
# apps/research-analytics/api/app.py

from flask import Flask
from shared.database.models import db

app = Flask(__name__)
app.config.from_object('shared.config.base')

# Only research/analytics routes
from .routes import teams, interfaces, analytics, nda

app.register_blueprint(teams.bp)
app.register_blueprint(interfaces.bp)
app.register_blueprint(analytics.bp)
app.register_blueprint(nda.bp)

if __name__ == '__main__':
    app.run(port=5002)
```

**AI Prediction Core API:**
```python
# apps/ai-prediction-core/api/app.py

from flask import Flask
from shared.database.models import db

app = Flask(__name__)
app.config.from_object('shared.config.base')

# Only prediction routes
from .routes import predictions, models, training

app.register_blueprint(predictions.bp)
app.register_blueprint(models.bp)
app.register_blueprint(training.bp)

if __name__ == '__main__':
    app.run(port=5003)
```

---

### **Phase 4: Update Configuration**

**Shared database connection:**
```python
# shared/config/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

**App-specific configs:**
```python
# apps/onboarding-lms/api/config.py

from shared.config.base import BaseConfig

class OnboardingConfig(BaseConfig):
    # LMS-specific settings
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    MAX_MODULE_SIZE_MB = 50
```

---

### **Phase 5: Docker Compose for Local Dev**

```yaml
# docker-compose.yml

version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: frames
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # Application 1: Onboarding LMS
  onboarding-api:
    build:
      context: .
      dockerfile: apps/onboarding-lms/api/Dockerfile
    ports:
      - "5001:5001"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/frames
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    depends_on:
      - postgres

  onboarding-frontend:
    build:
      context: .
      dockerfile: apps/onboarding-lms/frontend/Dockerfile
    ports:
      - "3001:3000"
    environment:
      REACT_APP_API_URL: http://localhost:5001

  # Application 2: Research Analytics
  research-api:
    build:
      context: .
      dockerfile: apps/research-analytics/api/Dockerfile
    ports:
      - "5002:5002"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/frames
    depends_on:
      - postgres

  research-frontend:
    build:
      context: .
      dockerfile: apps/research-analytics/frontend/Dockerfile
    ports:
      - "3002:3000"
    environment:
      REACT_APP_API_URL: http://localhost:5002

  # Application 3: AI Prediction Core
  ai-core-api:
    build:
      context: .
      dockerfile: apps/ai-prediction-core/api/Dockerfile
    ports:
      - "5003:5003"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/frames
      MLFLOW_TRACKING_URI: http://mlflow:5000
    depends_on:
      - postgres

  mlflow:
    image: ghcr.io/mlflow/mlflow:latest
    ports:
      - "5000:5000"
    command: mlflow server --host 0.0.0.0 --port 5000

volumes:
  postgres_data:
```

**Local development:**
```bash
# Start all three apps
docker-compose up

# Or start just one
docker-compose up onboarding-api onboarding-frontend postgres
```

---

## Git Branching Strategy

### **Branch Naming Convention:**

```
main                                      # Stable production code
├── develop                               # Integration branch
│
├── app/onboarding-lms/*                 # LMS features
│   ├── feature/ai-assistant
│   ├── feature/module-viewer
│   └── hotfix/progress-tracking-bug
│
├── app/research-analytics/*             # Research features
│   ├── feature/nda-dashboard
│   ├── feature/comparative-view
│   └── hotfix/chart-rendering
│
├── app/ai-prediction-core/*             # AI features
│   ├── feature/xgboost-model
│   ├── feature/mlflow-integration
│   └── hotfix/training-failure
│
├── shared/database/*                    # Shared DB changes
│   ├── migration/add-module-tables
│   ├── migration/add-prediction-tables
│   └── hotfix/index-performance
│
└── docs/*                               # Documentation updates
    └── update/reorganization-guide
```

### **Workflow:**

**Feature development:**
```bash
# Start new LMS feature
git checkout develop
git checkout -b app/onboarding-lms/feature/ai-assistant

# Work, commit, push
git push origin app/onboarding-lms/feature/ai-assistant

# Create PR to develop
# After review, merge
```

**Database migrations (affects all apps):**
```bash
# Start new migration
git checkout develop
git checkout -b shared/database/migration/add-module-tables

# Create migration
# Test with ALL apps
# Create PR with special tag [MIGRATION]
```

**Hotfixes:**
```bash
# Critical bug in production
git checkout main
git checkout -b app/onboarding-lms/hotfix/broken-module-view

# Fix, test
git push origin app/onboarding-lms/hotfix/broken-module-view

# PR to main (bypasses develop)
# After deploy, merge back to develop
```

---

## Deployment Strategy

### **Independent Deployments**

Each app can deploy separately:

**Azure App Services:**
- `frames-onboarding-api.azurewebsites.net` (Port 5001)
- `frames-research-api.azurewebsites.net` (Port 5002)
- `frames-ai-core.azurewebsites.net` (Port 5003)

**Azure Static Web Apps:**
- `frames-onboarding.azurestaticapps.net` (Student LMS)
- `frames-research.azurestaticapps.net` (Research dashboard)

**Shared:**
- `frames-db.postgres.database.azure.com` (One database, all apps)

---

## Timeline

### **Week 1: Documentation Reorganization**
- [ ] Create folder structure
- [ ] Move docs to new locations
- [ ] Create new master README
- [ ] Create app-specific READMEs
- [ ] Commit and merge to main

### **Week 2: Code Structure (Prep)**
- [ ] Create apps/ folder structure
- [ ] Create shared/ folder structure
- [ ] Don't move code yet, just setup

### **Week 3: Gradual Migration**
- [ ] Move database models to shared/
- [ ] Split into individual model files
- [ ] Test imports work

### **Week 4: Split Flask APIs**
- [ ] Create three separate app.py files
- [ ] Move routes to appropriate apps
- [ ] Test each app runs independently

### **Week 5: Frontend Separation**
- [ ] Move legacy HTML to research-analytics
- [ ] Setup React projects for each app
- [ ] Initial component structure

### **Week 6: Testing & Integration**
- [ ] All three apps run locally
- [ ] Docker Compose setup working
- [ ] Database migrations coordinated
- [ ] CI/CD pipelines configured

---

## Benefits of This Structure

### **For You:**
- ✅ Clear mental model (three distinct projects)
- ✅ Work on one app without affecting others
- ✅ Deploy apps independently
- ✅ Easier to onboard contributors ("you own the LMS")

### **For Development:**
- ✅ Faster CI/CD (only test changed app)
- ✅ Smaller deployment packages
- ✅ Clearer git history
- ✅ Better code organization

### **For Users:**
- ✅ If one app breaks, others still work
- ✅ Can update LMS without touching research tools
- ✅ Different release schedules per app

---

## Questions Before Starting?

1. **Onboarding LMS priority:** Should we finish this FIRST before reorganizing?
   - Pros: Get working system ASAP
   - Cons: More work to reorganize later

2. **Gradual vs Big Bang:**
   - Gradual: Move files over several weeks
   - Big Bang: Reorganize everything in one branch

3. **Testing strategy:** How to ensure nothing breaks during move?

---

## Next Steps

**Option 1: Finish LMS First (RECOMMENDED)**
- Build onboarding LMS in current structure
- Get it working and deployed
- Then reorganize once stable

**Option 2: Reorganize Now**
- Do documentation reorganization this week
- Code reorganization next week
- Build LMS in new structure

**What do you think makes more sense?**

---

*Last updated: 2025-01-23*
