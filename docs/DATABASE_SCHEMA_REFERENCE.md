# Database Schema Reference

**Date:** 2025-11-28
**Database:** PostgreSQL (Neon hosted)
**ORM:** SQLAlchemy
**Schema Location:** `shared/database/db_models.py`

---

## Table of Contents

1. [Overview](#overview)
2. [Connection](#connection)
3. [Existing Tables](#existing-tables)
4. [CADENCE Tables (Canonical)](#cadence-tables-canonical)
5. [Module & Progress Tables](#module--progress-tables)
6. [Relationships](#relationships)
7. [Indexes](#indexes)
8. [Migrations](#migrations)
9. [Example Queries](#example-queries)

---

## Overview

FRAMES uses **PostgreSQL** (hosted on Neon) as the canonical source of truth for all data.

### Schema Organization

```
Database: frames
│
├── Existing Tables (Research Analytics)
│   ├── teams
│   ├── faculty
│   ├── projects
│   ├── interfaces
│   ├── universities
│   ├── outcomes
│   └── students
│
├── CADENCE Tables (Canonical per spec)
│   ├── people          ← New
│   ├── projects        ← Overlaps with existing (TODO: merge)
│   ├── tasks           ← New
│   ├── meetings        ← New
│   └── documents       ← New
│
└── Module & Progress Tables
    ├── modules         ← New
    ├── module_progress ← New
    └── leaderboard     ← New
```

---

## Connection

### Environment Variable

```bash
DATABASE_URL=postgresql://user:password@host:5432/database
```

Example (Neon):
```bash
DATABASE_URL=postgresql://user:xyz@ep-example-123.us-east-2.aws.neon.tech/frames?sslmode=require
```

### SQLAlchemy Configuration

```python
# backend/app.py
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
```

### Testing Connection

```python
from backend.database import db
from shared.database.db_models import TeamModel

# Test query
teams = TeamModel.query.all()
print(f"Found {len(teams)} teams")
```

---

## Existing Tables

### teams

**Purpose:** Track teams within projects (multi-university collaboration)

```sql
CREATE TABLE teams (
    id VARCHAR PRIMARY KEY,
    university_id VARCHAR INDEX,      -- Which university owns this team
    project_id VARCHAR NOT NULL INDEX, -- Which project (PROVES, CADENCE, etc.)
    discipline VARCHAR,                -- Engineering, CS, Design, etc.
    name VARCHAR NOT NULL,
    description TEXT,
    created_at VARCHAR,                -- ISO timestamp
    meta JSON                          -- Flexible metadata
);
```

**Indexes:**
- `university_id` - Filter teams by university
- `project_id` - Filter teams by project

**Example Data:**
```json
{
  "id": "team-001",
  "university_id": "cal_poly",
  "project_id": "cadence",
  "discipline": "Electrical Engineering",
  "name": "Avionics Team",
  "description": "Team focused on avionics subsystem",
  "created_at": "2025-01-15T10:00:00Z",
  "meta": {}
}
```

---

### faculty

**Purpose:** Faculty advisors and program coordinators

```sql
CREATE TABLE faculty (
    id VARCHAR PRIMARY KEY,
    university_id VARCHAR INDEX,
    name VARCHAR NOT NULL,
    role VARCHAR,                      -- Faculty Advisor, Program Coordinator
    description TEXT,
    created_at VARCHAR,
    meta JSON
);
```

**Example Data:**
```json
{
  "id": "fac-001",
  "university_id": "cal_poly",
  "name": "Dr. Sarah Chen",
  "role": "Faculty Advisor - Engineering",
  "description": "Specializes in aerospace systems",
  "created_at": "2025-01-01T00:00:00Z"
}
```

---

### projects

**Purpose:** Research projects (PROVES, CADENCE, contract projects)

```sql
CREATE TABLE projects (
    id VARCHAR PRIMARY KEY,
    university_id VARCHAR INDEX,       -- NULL for collaborative projects
    name VARCHAR NOT NULL,
    type VARCHAR,                      -- collaborative, contract, proposal
    is_collaborative BOOLEAN DEFAULT FALSE, -- TRUE for PROVES
    duration INTEGER,                  -- Months
    description TEXT,
    created_at VARCHAR,
    meta JSON
);
```

**Example Data:**
```json
{
  "id": "cadence",
  "university_id": null,               // Multi-university
  "name": "CADENCE CubeSat",
  "type": "collaborative",
  "is_collaborative": true,
  "duration": 36,
  "description": "Multi-university CubeSat satellite project",
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

### interfaces

**Purpose:** Relationships between entities (teams, faculty, projects)

```sql
CREATE TABLE interfaces (
    id VARCHAR PRIMARY KEY,
    from_entity VARCHAR NOT NULL,      -- Source ID (team, faculty, project)
    to_entity VARCHAR NOT NULL,        -- Target ID
    interface_type VARCHAR,            -- knowledge_transfer, mentoring, etc.
    bond_type VARCHAR,
    energy_loss INTEGER,               -- 0-100 (health metric, 0=healthy)
    from_university VARCHAR INDEX,
    to_university VARCHAR INDEX,
    is_cross_university BOOLEAN DEFAULT FALSE INDEX,
    created_at VARCHAR,
    meta JSON
);
```

**Indexes:**
- `from_university` - Cross-university analysis
- `to_university`
- `is_cross_university` - Quickly find cross-university bonds

**Example Data:**
```json
{
  "id": "int-001",
  "from_entity": "fac-001",
  "to_entity": "team-001",
  "interface_type": "mentoring",
  "energy_loss": 15,                   // Low loss = healthy relationship
  "from_university": "cal_poly",
  "to_university": "cal_poly",
  "is_cross_university": false
}
```

---

### universities

**Purpose:** University registry

```sql
CREATE TABLE universities (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    is_lead BOOLEAN DEFAULT FALSE,     -- Lead university for program
    active BOOLEAN DEFAULT TRUE,
    meta JSON,
    created_at VARCHAR
);
```

**Example Data:**
```json
{
  "id": "cal_poly",
  "name": "California Polytechnic State University, Pomona",
  "is_lead": true,
  "active": true,
  "created_at": "2025-01-01T00:00:00Z"
}
```

---

### students

**Purpose:** Individual student tracking for term-based rotation

```sql
CREATE TABLE students (
    id VARCHAR PRIMARY KEY,
    university_id VARCHAR NOT NULL INDEX,
    name VARCHAR NOT NULL,
    team_id VARCHAR,                   -- FK to teams
    expertise_area VARCHAR,            -- Electrical, Software, Mechanical
    graduation_term VARCHAR,           -- e.g., "Spring 2026"
    terms_remaining INTEGER NOT NULL DEFAULT 4,
    status VARCHAR,                    -- incoming/established/outgoing (auto-calc)
    is_lead BOOLEAN DEFAULT FALSE,     -- Team lead designation
    active BOOLEAN DEFAULT TRUE,       -- FALSE when graduated
    created_at VARCHAR,
    graduated_at VARCHAR,              -- Set when terms_remaining hits 0
    meta JSON
);
```

**Status Calculation:**
- `incoming`: terms_remaining >= 4
- `established`: 2 <= terms_remaining < 4
- `outgoing`: terms_remaining < 2

**Example Data:**
```json
{
  "id": "student-001",
  "university_id": "cal_poly",
  "name": "Alice Johnson",
  "team_id": "team-001",
  "expertise_area": "Software",
  "graduation_term": "Spring 2026",
  "terms_remaining": 3,
  "status": "established",
  "is_lead": false,
  "active": true,
  "created_at": "2025-01-15T10:00:00Z"
}
```

---

### outcomes

**Purpose:** Track mission and program success metrics

```sql
CREATE TABLE outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    university_id VARCHAR NOT NULL,
    project_id VARCHAR,
    outcome_type VARCHAR NOT NULL,     -- mission_success or program_success
    success BOOLEAN NOT NULL,
    cohort_year INTEGER,
    notes TEXT,
    recorded_at VARCHAR,
    meta JSON
);
```

**Example Data:**
```json
{
  "id": 1,
  "university_id": "cal_poly",
  "project_id": "cadence",
  "outcome_type": "mission_success",
  "success": true,
  "cohort_year": 2025,
  "notes": "Successful satellite deployment",
  "recorded_at": "2025-06-15T00:00:00Z"
}
```

---

## CADENCE Tables (Canonical)

Per CADENCE spec (`cadence_spec_full/intent/data_intent_spec.md`), these 5 tables are **canonical**:

### people

**Purpose:** Team members and contacts (CADENCE-specific)

```sql
CREATE TABLE people (
    person_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    role VARCHAR,                      -- Team Lead, Engineer, Student
    email VARCHAR,
    subsystem VARCHAR                  -- Avionics, Power, Software, etc.
);
```

**Note:** This overlaps with `students` and `faculty` tables. Future work: merge into unified schema.

**Example Data:**
```json
{
  "person_id": "person-001",
  "name": "Dr. Sarah Martinez",
  "role": "Team Lead",
  "email": "sarah@example.com",
  "subsystem": "All"
}
```

---

### tasks

**Purpose:** Project tasks and todos

```sql
CREATE TABLE tasks (
    task_id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    desc TEXT,
    status VARCHAR,                    -- Not Started, In Progress, Complete, Blocked
    due TIMESTAMP,
    assignee VARCHAR,                  -- FK to people.person_id
    project VARCHAR                    -- FK to projects.project_id
);
```

**Indexes:**
- `status` - Filter by status
- `assignee` - Find user's tasks
- `project` - Project task list

**Example Data:**
```json
{
  "task_id": "task-001",
  "title": "Complete PDR slides",
  "desc": "Prepare preliminary design review presentation",
  "status": "In Progress",
  "due": "2025-12-15T17:00:00Z",
  "assignee": "person-002",
  "project": "cadence"
}
```

---

### meetings

**Purpose:** Meeting notes and action items

```sql
CREATE TABLE meetings (
    meeting_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    date TIMESTAMP,
    attendees TEXT[],                  -- Array of person_ids
    project VARCHAR                    -- FK to projects.project_id
);
```

**Example Data:**
```json
{
  "meeting_id": "meeting-001",
  "name": "Weekly Avionics Standup",
  "date": "2025-11-25T15:00:00Z",
  "attendees": ["person-001", "person-002", "person-003"],
  "project": "cadence"
}
```

---

### documents

**Purpose:** Reference documents and files

```sql
CREATE TABLE documents (
    doc_id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    url VARCHAR,                       -- Link to file (Google Drive, GitHub, etc.)
    type VARCHAR,                      -- Datasheet, Procedure, Reference
    category VARCHAR,                  -- structural, technical, workflow, program
    subsystem VARCHAR                  -- Avionics, Power, etc.
);
```

**Indexes:**
- `category` - Filter by document type
- `subsystem` - Subsystem documentation

**Example Data:**
```json
{
  "doc_id": "doc-001",
  "title": "Avionics Hardware Specification",
  "url": "https://drive.google.com/...",
  "type": "Technical Specification",
  "category": "technical",
  "subsystem": "Avionics"
}
```

---

## Module & Progress Tables

_(To be created - schema pending)_

### modules

```sql
CREATE TABLE modules (
    module_id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    slug VARCHAR UNIQUE,
    description TEXT,
    category VARCHAR,
    difficulty VARCHAR,                -- Beginner, Intermediate, Advanced
    estimated_minutes INTEGER,
    target_audience VARCHAR,
    status VARCHAR DEFAULT 'Draft',   -- Draft, Review, Published
    tags TEXT[],
    sections JSONB,                    -- Module content structure
    notion_page_id VARCHAR,
    github_file VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    meta JSONB
);
```

---

### module_progress

```sql
CREATE TABLE module_progress (
    id VARCHAR PRIMARY KEY,
    module_id VARCHAR NOT NULL,        -- FK to modules
    student_id VARCHAR NOT NULL,       -- FK to students
    status VARCHAR,                    -- not_started, in_progress, completed
    completed_sections TEXT[],
    time_spent_minutes INTEGER,
    score INTEGER,                     -- 0-100
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    meta JSONB
);
```

---

## Relationships

### Entity Relationship Diagram

```
universities
    ├── 1:N → teams
    ├── 1:N → faculty
    ├── 1:N → students
    └── 1:N → projects (some NULL for collaborative)

projects
    ├── 1:N → teams
    ├── 1:N → tasks
    └── 1:N → meetings

teams
    └── 1:N → students

people (CADENCE)
    ├── 1:N → tasks (as assignee)
    └── N:M → meetings (as attendees)

modules
    └── 1:N → module_progress

students
    └── 1:N → module_progress
```

### Foreign Key Constraints

**Current:** Implemented as logical relationships (application-level)
**Future:** Add database-level FK constraints for data integrity

---

## Indexes

### Existing Indexes

```sql
-- teams table
CREATE INDEX idx_teams_university ON teams(university_id);
CREATE INDEX idx_teams_project ON teams(project_id);

-- faculty table
CREATE INDEX idx_faculty_university ON faculty(university_id);

-- projects table
CREATE INDEX idx_projects_university ON projects(university_id);

-- interfaces table
CREATE INDEX idx_interfaces_from_university ON interfaces(from_university);
CREATE INDEX idx_interfaces_to_university ON interfaces(to_university);
CREATE INDEX idx_interfaces_cross_university ON interfaces(is_cross_university);

-- students table
CREATE INDEX idx_students_university ON students(university_id);
```

### Recommended Indexes (CADENCE Tables)

```sql
-- tasks table
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_assignee ON tasks(assignee);
CREATE INDEX idx_tasks_project ON tasks(project);
CREATE INDEX idx_tasks_due ON tasks(due);

-- meetings table
CREATE INDEX idx_meetings_date ON meetings(date);
CREATE INDEX idx_meetings_project ON meetings(project);

-- documents table
CREATE INDEX idx_documents_category ON documents(category);
CREATE INDEX idx_documents_subsystem ON documents(subsystem);
CREATE INDEX idx_documents_type ON documents(type);

-- modules table
CREATE INDEX idx_modules_slug ON modules(slug);
CREATE INDEX idx_modules_status ON modules(status);
CREATE INDEX idx_modules_category ON modules(category);

-- module_progress table
CREATE INDEX idx_progress_module ON module_progress(module_id);
CREATE INDEX idx_progress_student ON module_progress(student_id);
CREATE INDEX idx_progress_status ON module_progress(status);
```

---

## Migrations

### Creating Tables

**Location:** `shared/database/migrations/`

**Example Migration:**
```python
# shared/database/migrations/create_cadence_tables.py
from backend.database import db
from shared.database.cadence_models import (
    PeopleModel, TasksModel, MeetingsModel, DocumentsModel
)

def migrate():
    """Create CADENCE canonical tables"""
    db.create_all()  # Creates all defined models
    print("✅ CADENCE tables created")

if __name__ == "__main__":
    migrate()
```

### Running Migrations

```bash
# Create tables
python shared/database/migrations/create_cadence_tables.py

# Verify
python -c "from backend.database import db; \
           from sqlalchemy import inspect; \
           inspector = inspect(db.engine); \
           print(inspector.get_table_names())"
```

---

## Example Queries

### Teams & Students

**Get all teams for a project:**
```python
from shared.database.db_models import TeamModel

teams = TeamModel.query.filter_by(project_id='cadence').all()
for team in teams:
    print(f"{team.name} - {team.discipline}")
```

**Get all students on a team:**
```python
from shared.database.db_models import StudentModel

students = StudentModel.query.filter_by(team_id='team-001').all()
for student in students:
    print(f"{student.name} - {student.status}")
```

**Find outgoing students (graduating soon):**
```python
students = StudentModel.query.filter(
    StudentModel.terms_remaining < 2,
    StudentModel.active == True
).all()
```

---

### CADENCE Queries

**Get all tasks assigned to a person:**
```python
from shared.database.cadence_models import TasksModel

tasks = TasksModel.query.filter_by(
    assignee='person-001',
    status='In Progress'
).all()
```

**Get upcoming meetings:**
```python
from shared.database.cadence_models import MeetingsModel
from datetime import datetime, timedelta

next_week = datetime.now() + timedelta(days=7)
meetings = MeetingsModel.query.filter(
    MeetingsModel.date <= next_week
).order_by(MeetingsModel.date).all()
```

**Get documents by subsystem:**
```python
from shared.database.cadence_models import DocumentsModel

docs = DocumentsModel.query.filter_by(
    subsystem='Avionics',
    category='technical'
).all()
```

---

### Analytics Queries

**Count active students per university:**
```python
from shared.database.db_models import StudentModel
from sqlalchemy import func

counts = db.session.query(
    StudentModel.university_id,
    func.count(StudentModel.id)
).filter_by(active=True).group_by(
    StudentModel.university_id
).all()

for university_id, count in counts:
    print(f"{university_id}: {count} students")
```

**Cross-university interfaces:**
```python
from shared.database.db_models import InterfaceModel

cross_uni = InterfaceModel.query.filter_by(
    is_cross_university=True
).all()

print(f"Found {len(cross_uni)} cross-university collaborations")
```

---

## Database Backup & Restore

### Backup (Neon)

```bash
# Export to SQL dump
pg_dump $DATABASE_URL > frames_backup.sql

# Export specific tables
pg_dump $DATABASE_URL -t teams -t students > frames_teams_backup.sql
```

### Restore

```bash
# Restore from dump
psql $DATABASE_URL < frames_backup.sql
```

---

## Performance Tips

1. **Use Indexes:** Always query on indexed columns (university_id, project_id, status)
2. **Batch Inserts:** Use `bulk_insert_mappings()` for multiple records
3. **Connection Pooling:** Neon handles this automatically
4. **Query Only What You Need:** Use `.with_entities()` to select specific columns

**Example - Efficient Query:**
```python
# Bad - loads all columns
students = StudentModel.query.all()

# Good - only loads name and status
students = StudentModel.query.with_entities(
    StudentModel.name,
    StudentModel.status
).all()
```

---

## Troubleshooting

### Common Issues

**Connection Refused:**
```
Check DATABASE_URL is correct
Verify Neon database is active (not hibernated)
Test connection: psql $DATABASE_URL
```

**Table Doesn't Exist:**
```
Run migrations: python shared/database/migrations/create_cadence_tables.py
Verify: SELECT * FROM pg_tables WHERE schemaname = 'public';
```

**Foreign Key Violations:**
```
Check referenced record exists first
Use try/except to catch IntegrityError
```

---

**Last Updated:** 2025-11-28
**Maintained By:** Agent Beta
**Schema Version:** 2.0 (CADENCE tables added)
**Next Migration:** Merge people/students/faculty into unified schema
