# FRAMES Backend API

Flask-based REST API server for the FRAMES platform.

---

## 📖 Overview

The FRAMES backend provides REST API endpoints for:

- **Teams Management** - Create, read, update, delete teams
- **Students Management** - Student records and progress tracking
- **Faculty Management** - Faculty advisors and roles
- **Projects Management** - Research projects across universities
- **LMS Modules** - Training module content and metadata
- **Analytics** - Program health metrics and visualizations
- **Network Data** - 3D molecular visualization data

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL database (Neon recommended)
- Notion API token (for LMS modules)

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL and Notion token

# Run development server
python app.py
```

Server runs on [http://localhost:5000](http://localhost:5000)

---

## 📂 Project Structure

```
backend/
├── app.py                      # Main Flask application
├── lms_routes.py              # LMS module endpoints
├── test_lms_endpoints.py      # API tests
├── test_lms_quick.py          # Quick API tests
├── requirements.txt           # Python dependencies
└── venv/                      # Virtual environment (excluded from git)
```

---

## 🔌 API Endpoints

### Core Endpoints

**Dashboard:**

- `GET /dashboard` - Program Health Dashboard (3D visualization)
- `GET /api/network-data` - Network data for visualization

**Teams:**

- `GET /api/teams` - List all teams
- `POST /api/teams` - Create new team
- `GET /api/teams/:team_id` - Get team details
- `PUT /api/teams/:team_id` - Update team
- `DELETE /api/teams/:team_id` - Delete team

**Students:**

- `GET /api/students` - List all students
- `POST /api/students` - Create new student
- `GET /api/students/:student_id` - Get student details
- `PUT /api/students/:student_id` - Update student
- `DELETE /api/students/:student_id` - Delete student

**LMS Modules:**

- `GET /api/lms/modules` - List all training modules
- `GET /api/lms/modules/:module_id` - Get module details
- `POST /api/lms/modules/:module_id/progress` - Track student progress

**Analytics:**

- `GET /analytics` - Analytics dashboard
- `GET /api/analytics/summary` - Summary metrics

### Complete API Documentation

See **[docs/API_REFERENCE.md](../docs/API_REFERENCE.md)** for full API documentation with request/response examples.

---

## 🗄️ Database

### Connection

The backend connects to PostgreSQL (Neon) using environment variables:

```bash
DATABASE_URL=postgresql://user:password@host:5432/database
```

### Schema

See **[docs/DATABASE_SCHEMA_REFERENCE.md](../docs/DATABASE_SCHEMA_REFERENCE.md)** for complete schema documentation.

**Key Tables:**

- `teams` - Student teams across universities
- `students` - Student records
- `faculty` - Faculty advisors
- `projects` - Research projects
- `universities` - University information
- `interfaces` - Team/faculty/project interfaces
- `people` - CADENCE team members (canonical)
- `tasks` - CADENCE tasks (canonical)
- `meetings` - CADENCE meetings (canonical)
- `documents` - CADENCE documents (canonical)

---

## 🧪 Testing

### Run All Tests

```bash
python test_lms_endpoints.py
```

### Quick Smoke Tests

```bash
python test_lms_quick.py
```

### Manual Testing with cURL

```bash
# List all teams
curl http://localhost:5000/api/teams

# Create team
curl -X POST http://localhost:5000/api/teams \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Team", "project_id": "test"}'

# Get module details
curl http://localhost:5000/api/lms/modules/mod-001
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Database
DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/frames?sslmode=require

# Notion API
NOTION_TOKEN=ntn_xxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_MODULE_DB_ID=eac1ce58-6169-4dc3-a821-29858ae59e76

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
```

### CORS Configuration

CORS is enabled for all origins in development mode. Update `app.py` for production:

```python
CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})
```

---

## 📊 Key Features

### Multi-University Support

All endpoints support filtering by `university_id`:

```bash
GET /api/teams?university_id=cal_poly
GET /api/students?university_id=texas_state
```

### Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error description",
  "message": "Human-readable error message"
}
```

### Response Format

All successful responses follow this format:

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Disable `FLASK_DEBUG`
- [ ] Configure CORS for specific origins
- [ ] Use production database URL
- [ ] Set up HTTPS
- [ ] Configure rate limiting
- [ ] Enable authentication (JWT)
- [ ] Set up monitoring and logging

### Recommended: Gunicorn

```bash
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📝 Development

### Adding New Endpoints

1. Define route in `app.py` or create new route file
2. Follow existing error handling patterns
3. Update API documentation in `docs/API_REFERENCE.md`
4. Add tests in `test_lms_endpoints.py`

### Code Style

- Follow PEP 8 style guidelines
- Use type hints where possible
- Write descriptive docstrings
- Handle errors gracefully

---

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error:**

```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution:** Check `DATABASE_URL` in `.env` file

**CORS Error:**

```
Access to fetch at 'http://localhost:5000' has been blocked by CORS policy
```

**Solution:** Ensure CORS is enabled in `app.py`

**Module Import Error:**

```
ModuleNotFoundError: No module named 'flask'
```

**Solution:** Activate virtual environment and install dependencies:

```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## 📚 Additional Documentation

- **[Complete System Architecture](../docs/COMPLETE_SYSTEM_ARCHITECTURE.md)** - How FRAMES works
- **[API Reference](../docs/API_REFERENCE.md)** - Complete API documentation
- **[Database Schema](../docs/DATABASE_SCHEMA_REFERENCE.md)** - Database structure
- **[Developer Onboarding](../docs/DEVELOPER_ONBOARDING.md)** - Setup guide

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/Lizo-RoadTown/Frames-App/issues)
- **Documentation:** [docs/](../docs/)
- **Contact:** eosborn@cpp.edu

---

**Last Updated:** 2025-11-28
**Maintained By:** Agent Beta
