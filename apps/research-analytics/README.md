# FRAMES Research Analytics Dashboard

Faculty and researcher analytics dashboard for analyzing team dynamics and collaboration patterns across 8 universities in the FRAMES research collaboration.

## Status: ✅ Active and Functional

This application is currently deployed and being used for multi-university research analytics.

## Features

- **University Dashboards:** Track participation and engagement per university
- **Team Analytics:** Monitor team dynamics and collaboration patterns
- **Risk Factor Analysis:** Identify and analyze risk factors in team performance
- **Multi-University Network:** Visualize collaboration across institutions
- **Faculty Tools:** Research-specific analytics and insights

## Tech Stack

- **Backend:** Flask, SQLAlchemy, PostgreSQL
- **Frontend:** React, vanilla JavaScript
- **Database:** Neon PostgreSQL (shared with other FRAMES apps)
- **Deployment:** Development server (production deployment planned)

## Database Schema

This app uses 14 shared tables:
- `teams`, `faculty`, `projects`, `universities`, `students`
- `audit_logs`, `risk_factors`, `factor_values`
- `factor_models`, `model_factors`, `model_validations`
- `outcomes`, `interfaces`, `interface_factor_values`

## Setup

1. **Install dependencies:**
```bash
cd apps/research-analytics
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your database connection string
```

3. **Initialize database (if not already done):**
```bash
cd ../../
python shared/database/bootstrap_db.py
```

4. **Run the application:**
```bash
cd apps/research-analytics
python backend/app.py
```

5. **Access the dashboard:**
Open http://localhost:5000 in your browser

## API Endpoints

### Universities
- `GET /api/universities` - List all universities
- `GET /api/university/<id>` - Get university details

### Teams
- `GET /api/teams` - List all teams
- `GET /api/team/<id>` - Get team details

### Students
- `GET /api/students` - List all students
- `POST /api/students` - Add new student

### Analytics
- `GET /api/analytics/<team_id>` - Get team analytics
- `GET /api/risk-factors` - List risk factors

## Project Structure

```
research-analytics/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── analytics.py        # Analytics engine
│   ├── models.py           # Dataclass models
│   ├── db_models.py        # SQLAlchemy models (symlink to shared/)
│   ├── db_connection.py    # Database connection (symlink to shared/)
│   └── ...
├── frontend/
│   ├── static/             # JS, CSS files
│   │   ├── api.js
│   │   ├── dashboard-standalone.js
│   │   └── multi-university-network.js
│   └── templates/          # HTML templates
│       └── index.html
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

## Development

### Adding New Features
```bash
# Create feature branch
git checkout -b feature/analytics-new-chart

# Make changes
# Test locally
python backend/app.py

# Commit
git add .
git commit -m "Add new analytics chart"
git push origin feature/analytics-new-chart
```

### Updating Database Schema
Database models are in `../../shared/database/`. If you update them:
1. Update `shared/database/db_models.py`
2. Create migration script if needed
3. Test with other apps to ensure compatibility

## Testing

Run endpoint tests:
```bash
python backend/test_endpoints.py
```

## Documentation

Full documentation available in:
- `../../docs/research-analytics/ARCHITECTURE.md`
- `../../docs/research-analytics/API_REFERENCE.md`

## Contributing

This is part of the FRAMES monorepo. See `../../MONOREPO_STRUCTURE.md` for development workflow.

## Contact

Elizabeth Osborn, Ph.D. - eosborn@cpp.edu
California State Polytechnic University, Pomona
