# FRAMES Repository Structure

This repository contains three integrated applications sharing a common database.

## Structure

```
FRAMES-App/
├── apps/
│   ├── research-analytics/    # Faculty/researcher analytics (ACTIVE)
│   ├── onboarding-lms/        # Student onboarding LMS (IN DEVELOPMENT)
│   └── ai-core/               # AI prediction engine (PLANNED)
│
├── shared/
│   └── database/              # Shared database models & utilities
│
├── docs/                      # Documentation by application
├── .env                       # Environment variables (not in git)
└── README.md
```

## Quick Start

### Research Analytics (Active App)

```bash
cd apps/research-analytics
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Add your DATABASE_URL
python backend/app.py
```

### Database Setup
```bash
# Test connection
python shared/database/test_db_connection.py

# Initialize tables
python shared/database/bootstrap_db.py
```

## Database

All apps connect to the same **Neon PostgreSQL** database.

**Tables:** teams, faculty, projects, universities, students, audit_logs, risk_factors, factor_values, factor_models, model_factors, model_validations, outcomes, interfaces, interface_factor_values

**Connection:** Set `DATABASE_URL` in `.env` file

## Development

### Working on One App
```bash
git checkout -b feature/analytics-chart
# Make changes in apps/research-analytics/
git commit -m "Add chart"
```

### Updating Shared Database
```bash
git checkout -b feature/add-tables
# Edit shared/database/db_models.py
# Update affected apps
git commit -m "Add new tables"
```

### Project Management
Use GitHub:
- **Labels:** `app:research-analytics`, `app:onboarding-lms`, `app:ai-core`
- **Milestones:** "LMS v1.0", "Analytics v2.0"
- **Projects:** Create boards per app or unified

## Contact

Elizabeth Osborn, Ph.D. - eosborn@cpp.edu
California State Polytechnic University, Pomona
