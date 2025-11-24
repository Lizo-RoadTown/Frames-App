# FRAMES Monorepo Structure

This repository contains three integrated applications sharing a common database for the FRAMES multi-university research collaboration.

## Repository Structure

```
FRAMES-App/
├── apps/                          # Application code
│   ├── research-analytics/        # Faculty/researcher analytics dashboard (ACTIVE)
│   │   ├── backend/              # Flask API, analytics engine
│   │   ├── frontend/             # React dashboards, templates
│   │   ├── requirements.txt
│   │   └── .env.example
│   │
│   ├── onboarding-lms/           # Student onboarding LMS (IN DEVELOPMENT)
│   │   └── [To be built - AI-powered module system]
│   │
│   └── ai-core/                  # AI prediction engine (PLANNED)
│       └── [Future - NDA framework implementation]
│
├── shared/                        # Shared code across all apps
│   ├── database/                 # Database models, connection, migrations
│   │   ├── db_connection.py     # Centralized DB connection
│   │   ├── db_models.py         # SQLAlchemy models
│   │   ├── database.py          # Flask-SQLAlchemy instance
│   │   ├── models.py            # Dataclass models
│   │   ├── bootstrap_db.py      # Initialize schema
│   │   └── test_db_connection.py # Test connectivity
│   │
│   └── utils/                    # Shared utilities
│       └── [Common helper functions]
│
├── docs/                          # Documentation
│   ├── research-analytics/       # Analytics docs
│   ├── onboarding-lms/          # LMS docs
│   ├── ai-prediction-core/      # AI core docs
│   ├── shared/                  # Shared docs (Azure setup, roadmap)
│   └── archive/                 # Historical documents
│
├── scripts/                       # Utility scripts
├── .env                          # Environment variables (NOT in git)
├── .env.example                  # Environment template
└── README.md                     # Main project README

```

## Three Applications

### 1. Research Analytics (apps/research-analytics/)
**Status:** ✅ Active and functional
**Purpose:** Faculty and researcher dashboard for analyzing team dynamics
**Tech Stack:** Flask, SQLAlchemy, React, PostgreSQL
**Database:** 14 tables (teams, faculty, projects, universities, students, etc.)

**Key Features:**
- University dashboards
- Team collaboration analytics
- Risk factor analysis
- Multi-university network visualization

**Run:**
```bash
cd apps/research-analytics
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env  # Configure database
python backend/app.py
```

### 2. Onboarding LMS (apps/onboarding-lms/)
**Status:** 🚧 In development
**Purpose:** AI-powered student onboarding and learning management
**Priority:** HIGH - Needed before next cohort
**Timeline:** 10 weeks to launch

**Planned Features:**
- AI-generated training modules (10-20 modules)
- Team lead content workflow (no Git/coding required)
- Progressive Web App (PWA) for mobile
- Module analytics tracking
- Embedded AI assistant for post-launch updates

**Documentation:** See `docs/onboarding-lms/`

### 3. AI Core (apps/ai-core/)
**Status:** 📅 Planned
**Purpose:** AI prediction engine for mission success forecasting
**Framework:** Non-Decomposable Architecture (NDA)
**Timeline:** Post-LMS launch

**Planned Features:**
- Mission success prediction
- NDA framework implementation
- Energy modeling
- Factor interaction analysis

**Documentation:** See `docs/ai-prediction-core/`

## Shared Database

All three applications connect to the same **Neon PostgreSQL** database:
- **Connection:** Configured in `.env` file
- **Schema:** 14 tables (see `shared/database/db_models.py`)
- **Provider:** Neon (PostgreSQL 15, free tier)

### Database Tables:
- `teams`, `faculty`, `projects`, `universities`, `students`
- `audit_logs`, `risk_factors`, `factor_values`
- `factor_models`, `model_factors`, `model_validations`
- `outcomes`, `interfaces`, `interface_factor_values`

### Initialize Database:
```bash
python shared/database/bootstrap_db.py
```

### Test Connection:
```bash
python shared/database/test_db_connection.py
```

## Development Workflow

### Working on a Single App
```bash
# Create a feature branch
git checkout -b feature/analytics-new-chart

# Make changes in apps/research-analytics/
# Commit and push
git add apps/research-analytics/
git commit -m "Add new analytics chart"
git push origin feature/analytics-new-chart
```

### Working Across Multiple Apps
```bash
# If you need to update shared database models
git checkout -b feature/add-module-tables

# Update shared/database/db_models.py
# Update affected apps
git add shared/database/ apps/onboarding-lms/ apps/research-analytics/
git commit -m "Add module tables for LMS"
```

### Using GitHub Projects

You can organize work using:
- **Labels:** `app:research-analytics`, `app:onboarding-lms`, `app:ai-core`
- **Milestones:** "LMS v1.0 Launch", "Analytics v2.0", "AI Core Research Phase"
- **Projects:** Create separate project boards for each app or one unified board

## Benefits of Monorepo

✅ **Single Source of Truth:** Database schema in one place (`shared/database/`)
✅ **Easy Updates:** Change schema once, all apps get it
✅ **Simplified Development:** Work on multiple apps simultaneously
✅ **Shared Code:** Utilities and common functions in `shared/`
✅ **Unified History:** One git history for all changes
✅ **Better Visibility:** See how apps interact and depend on each other

## Environment Setup

1. **Clone the repository:**
```bash
git clone https://github.com/Lizo-RoadTown/Frames-App.git
cd Frames-App
```

2. **Set up environment:**
```bash
cp .env.example .env
# Edit .env with your database connection string
```

3. **Initialize database:**
```bash
python shared/database/bootstrap_db.py
```

4. **Run an app:**
```bash
cd apps/research-analytics
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python backend/app.py
```

## Next Steps

- [ ] Build out onboarding-lms initial structure
- [ ] Create GitHub Projects for task management
- [ ] Set up CI/CD for automated testing
- [ ] Document API endpoints for each app
- [ ] Create deployment guides for each application

## Contact

**Principal Investigator & Project Lead:**
Elizabeth Osborn, Ph.D.
Associate Professor, Industrial & Manufacturing Engineering
California State Polytechnic University, Pomona
Email: eosborn@cpp.edu

## License

Academic research project - California State Polytechnic University, Pomona
