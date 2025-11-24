# FRAMES Phase 1: Multi-University Collaborative Dashboard - FINAL PLAN

**Date:** 2025-11-18
**Lead Institution:** Cal Poly Pomona
**Participating Universities:** 8 total (placeholders until confirmed)

---

## Project Context

### The PROVES Collaboration

**Structure:**
- **8 universities** working together on space mission research
- **PROVES mission** - One shared collaborative project across all institutions
- **Individual missions** - Each university has their own projects/payloads
- **Cal Poly Pomona** - Leading institution, researcher conducting AI analysis

### Success Metrics Being Tracked

**Level 1: Mission Success**
- Did the payload launch successfully?
- Was the proposal accepted?
- Was the contract fulfilled?

**Level 2: Program Success (Generational)**
- Did the outgoing cohort successfully transfer knowledge to incoming?
- Did the next generation achieve another payload launch?
- Did the program persist beyond the founding generation?

### Dashboard Purpose

1. **Data Collection** - Capture team structures, interfaces, knowledge flow
2. **Open Source Sharing** - All universities see all data (transparency)
3. **Iterative Learning** - Compare outcomes, identify patterns, improve
4. **Research Platform** - Feed AI model for mission success prediction

---

## Phase 1 Core Requirements

### Must Have for Launch

1. ✅ **Multi-university data model**
   - 8 placeholder universities
   - Cal Poly Pomona + 7 others (Uni_A, Uni_B, etc.)
   - Each university owns their data

2. ✅ **PROVES project visibility**
   - One shared "PROVES" project
   - Cross-university teams contributing
   - Interfaces between universities tracked

3. ✅ **Individual university projects**
   - Each university has 2-3 internal projects
   - Internal team structures
   - Internal knowledge transfer tracking

4. ✅ **Comparative dashboard**
   - Side-by-side view of all 8 universities
   - Metrics comparison
   - Cross-university collaboration visibility

5. ✅ **Outcomes tracking**
   - Record mission success/failure
   - Record generational transfer outcomes
   - Link outcomes to interface characteristics

6. ✅ **Open data access**
   - All universities can view all data
   - Each university can only edit their own
   - Researcher (Cal Poly) has admin access

---

## Database Schema (Final)

### Core Tables

```sql
-- Universities (8 placeholders)
CREATE TABLE universities (
    id TEXT PRIMARY KEY,              -- CalPolyPomona, Uni_A, Uni_B, etc.
    name TEXT NOT NULL,               -- "Cal Poly Pomona", "University A"
    is_lead BOOLEAN DEFAULT FALSE,    -- TRUE for Cal Poly Pomona
    active BOOLEAN DEFAULT TRUE,
    meta JSON,
    created_at TEXT
);

-- Teams (scoped to university)
CREATE TABLE teams (
    id TEXT PRIMARY KEY,              -- CalPolyPomona_team_1
    university_id TEXT NOT NULL,
    discipline TEXT,                  -- software, electrical, mechanical, etc.
    lifecycle TEXT,                   -- incoming, established, outgoing
    name TEXT NOT NULL,
    size INTEGER,
    experience INTEGER,               -- months
    description TEXT,
    created_at TEXT,
    meta JSON,
    FOREIGN KEY (university_id) REFERENCES universities(id)
);

-- Faculty (scoped to university)
CREATE TABLE faculty (
    id TEXT PRIMARY KEY,
    university_id TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT,
    description TEXT,
    created_at TEXT,
    meta JSON,
    FOREIGN KEY (university_id) REFERENCES universities(id)
);

-- Projects (university-owned, but PROVES is special)
CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    university_id TEXT,               -- NULL for shared PROVES project
    name TEXT NOT NULL,
    type TEXT,                        -- 'proves' | 'jpl-contract' | 'internal'
    is_collaborative BOOLEAN,         -- TRUE for PROVES
    duration INTEGER,
    description TEXT,
    created_at TEXT,
    meta JSON,
    FOREIGN KEY (university_id) REFERENCES universities(id)
);

-- Interfaces (can cross university boundaries)
CREATE TABLE interfaces (
    id TEXT PRIMARY KEY,
    from_entity TEXT NOT NULL,        -- e.g., "CalPolyPomona.team_1"
    to_entity TEXT NOT NULL,          -- e.g., "Uni_A.team_2" (cross-university)
    interface_type TEXT,              -- team-to-team, team-to-faculty, etc.
    bond_type TEXT,                   -- codified-strong, institutional-weak, etc.
    energy_loss INTEGER,
    created_at TEXT,
    meta JSON,
    -- Denormalized for querying
    from_university TEXT,
    to_university TEXT,
    is_cross_university BOOLEAN       -- TRUE if from_university != to_university
);

-- Outcomes (mission/program success tracking)
CREATE TABLE outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    university_id TEXT NOT NULL,
    project_id TEXT,                  -- Which project/mission
    outcome_type TEXT NOT NULL,       -- 'mission_success' | 'program_success'
    success BOOLEAN NOT NULL,         -- Did it succeed?
    cohort_year INTEGER,              -- Academic year
    notes TEXT,
    recorded_at TEXT,
    meta JSON,
    FOREIGN KEY (university_id) REFERENCES universities(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Audit logs (research tracking)
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    actor TEXT NOT NULL,              -- user@CalPolyPomona
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT,
    university_id TEXT,
    payload_before TEXT,
    payload_after TEXT,
    meta JSON,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);
```

---

## Initial Data Seed

### 8 Universities (Placeholders)

```python
universities = [
    {'id': 'CalPolyPomona', 'name': 'Cal Poly Pomona', 'is_lead': True},
    {'id': 'TexasState', 'name': 'Texas State University', 'is_lead': False},
    {'id': 'Columbia', 'name': 'Columbia University', 'is_lead': False},
    {'id': 'Uni_D', 'name': 'University D', 'is_lead': False},
    {'id': 'Uni_E', 'name': 'University E', 'is_lead': False},
    {'id': 'Uni_F', 'name': 'University F', 'is_lead': False},
    {'id': 'Uni_G', 'name': 'University G', 'is_lead': False},
    {'id': 'Uni_H', 'name': 'University H', 'is_lead': False},
]
```

### PROVES Shared Project

```python
proves_project = {
    'id': 'PROVES',
    'university_id': None,  # Shared across all
    'name': 'PROVES - Multi-University Collaborative Mission',
    'type': 'proves',
    'is_collaborative': True,
    'duration': 36,  # 3 years
    'description': 'Shared collaborative space mission across 8 universities'
}
```

### Sample Data per University

Each university gets:
- 2-3 internal projects (university-owned)
- 3-5 teams (Software, Electrical, MissionOps, etc.)
- 1-2 faculty advisors
- Internal interfaces (team-to-team, team-to-faculty)
- PROVES interfaces (connecting to other universities)

---

## API Endpoints (Phase 1)

### Universities

```
GET    /api/universities              # List all 8 universities
GET    /api/universities/{id}         # Get specific university
POST   /api/universities              # Create university (admin only)
```

### Teams (University-Scoped)

```
GET    /api/teams?university_id={id}  # Get teams for one university
GET    /api/teams                     # Get all teams (all universities)
POST   /api/teams                     # Create team (in your university)
PUT    /api/teams/{id}                # Update team (own university only)
DELETE /api/teams/{id}                # Delete team (own university only)
```

### Projects

```
GET    /api/projects?university_id={id}  # University's projects
GET    /api/projects                     # All projects
GET    /api/projects/proves              # PROVES collaborative project
POST   /api/projects                     # Create project
```

### Interfaces (Cross-University)

```
GET    /api/interfaces?university_id={id}      # Interfaces involving this university
GET    /api/interfaces?cross_university=true   # Only cross-university interfaces
POST   /api/interfaces                         # Create interface
```

### Outcomes (Research Data)

```
GET    /api/outcomes?university_id={id}   # Outcomes for one university
GET    /api/outcomes                      # All outcomes (research view)
POST   /api/outcomes                      # Record outcome
```

### Comparative Dashboard

```
GET    /api/dashboard/comparative         # All universities side-by-side
GET    /api/dashboard/proves              # PROVES collaboration status
GET    /api/dashboard/outcomes            # Aggregated outcomes data
```

---

## UI Views

### 1. University Operations Dashboard

**Route:** `/#/university/{id}`

```
+------------------------------------------------------------+
| Cal Poly Pomona Dashboard                                  |
+------------------------------------------------------------+
| My Projects (3)  | My Teams (5)  | My Faculty (2)         |
+------------------------------------------------------------+
| Internal Projects:                                         |
| - JPL CubeSat Mission (jpl-contract) - Active             |
| - Propulsion Research (internal) - Active                  |
|                                                            |
| Collaborative:                                             |
| - PROVES (multi-university) - Active                       |
|   Connected to: Uni_D, TexasState, Columbia               |
+------------------------------------------------------------+
|              Molecular Visualization                       |
|         (Cal Poly Pomona teams & interfaces)              |
+------------------------------------------------------------+
| Cross-University Connections:                              |
| CalPolyPomona.Software <-> TexasState.Software            |
| CalPolyPomona.PROVES_Lead <-> Uni_D.PROVES_Lead           |
+------------------------------------------------------------+
```

### 2. Comparative Dashboard (Main View)

**Route:** `/#/comparative`

```
+------------------------------------------------------------------------------+
| All Universities - PROVES Collaboration                                      |
+------------------------------------------------------------------------------+
| Select View: [All Data] [PROVES Only] [Outcomes] [Analytics]               |
+------------------------------------------------------------------------------+
| Cal Poly | Texas    | Columbia | Uni_D | Uni_E | Uni_F | Uni_G | Uni_H     |
| Pomona   | State    |          |       |       |       |       |            |
+------------------------------------------------------------------------------+
| Teams: 5 | Teams: 4 | Teams: 6 | T: 3  | T: 4  | T: 5  | T: 3  | T: 4      |
| Fac: 2   | Fac: 2   | Fac: 3   | F: 1  | F: 2  | F: 2  | F: 1  | F: 2      |
| Proj: 3  | Proj: 2  | Proj: 4  | P: 2  | P: 3  | P: 2  | P: 3  | P: 2      |
+------------------------------------------------------------------------------+
|                    Side-by-Side Visualizations                              |
|  [CPP vis] [Texas vis] [Columbia vis] [Uni_D] [Uni_E] [Uni_F] [Uni_G] [H] |
+------------------------------------------------------------------------------+
| PROVES Cross-University Network:                                            |
| • CPP ↔ Texas: 3 interfaces (2 strong, 1 moderate)                         |
| • Texas ↔ Columbia: 2 interfaces (1 strong, 1 weak)                        |
| • Columbia ↔ Uni_D: 4 interfaces (3 strong, 1 moderate)                    |
| [View full network diagram]                                                 |
+------------------------------------------------------------------------------+
```

### 3. Outcomes Tracking Dashboard

**Route:** `/#/outcomes`

```
+------------------------------------------------------------+
| Mission & Program Outcomes                                 |
+------------------------------------------------------------+
| University      | Missions | Success | Program | Success  |
|                 | Launched | Rate    | Cohorts | Rate     |
+------------------------------------------------------------+
| Cal Poly Pomona |    3     |  100%   |    2    |   100%   |
| Texas State     |    2     |  100%   |    1    |   100%   |
| Columbia        |    1     |  100%   |    1    |   100%   |
| Uni_D           |    0     |   N/A   |    0    |    N/A   |
| ...             |  ...     |  ...    |  ...    |   ...    |
+------------------------------------------------------------+
| [Record New Outcome] [Export for AI Analysis]             |
+------------------------------------------------------------+
| Recent Outcomes:                                           |
| • Cal Poly Pomona - CubeSat Launch Success (2024)         |
| • Texas State - Cohort 2→3 Transfer Success (2024)        |
| • Columbia - Payload Launch Success (2023)                |
+------------------------------------------------------------+
```

---

## Phase 1 Implementation Plan

### Step 1: Clean Foundation (2 hours)

**Tasks:**
- Remove duplicate models from `db_models.py`
- Remove duplicate migration from `migrate_frames.py`
- Keep only Flask-SQLAlchemy models
- Document what remains

**Deliverable:** Clean, single-path codebase

### Step 2: Multi-University Schema (3 hours)

**Tasks:**
- Create `University` model
- Add `university_id` to all models (TeamModel, FacultyModel, ProjectModel)
- Create `Outcomes` model
- Update interfaces to track cross-university connections
- Write migration script

**Deliverable:** Database schema supports 8 universities

### Step 3: Seed Initial Data (2 hours)

**Tasks:**
- Seed 8 universities (Cal Poly Pomona + 7 placeholders)
- Create PROVES shared project
- Seed sample data for 3 universities (Cal Poly, Texas State, Columbia)
  - Each gets 3-5 teams
  - Each gets 1-2 faculty
  - Each gets 2-3 projects
  - Add cross-university PROVES interfaces

**Deliverable:** Database populated with realistic sample data

### Step 4: Update API Endpoints (4 hours)

**Tasks:**
- Add university filtering to GET endpoints
- Enforce university ownership on POST/PUT/DELETE
- Create comparative dashboard endpoint
- Create outcomes endpoints
- Update all endpoints to use database (not SystemState)

**Deliverable:** API fully database-backed and multi-university aware

### Step 5: Simple Authentication (2 hours)

**Tasks:**
- Header-based university identification (`X-University-ID`)
- Permission checks (can only edit own university)
- Researcher mode flag (`X-Is-Researcher: true`)
- Log actor in audit logs

**Deliverable:** Basic access control working

### Step 6: Frontend Updates (4 hours)

**Tasks:**
- Add university selector dropdown
- Create comparative dashboard view
- Update visualization to show cross-university interfaces
- Add outcomes recording form
- Test all CRUD operations

**Deliverable:** UI supports multi-university operations

### Step 7: Testing & Documentation (2 hours)

**Tasks:**
- Write acceptance tests
- Test cross-university scenarios
- Document API for other universities
- Create user guide

**Deliverable:** Phase 1 complete and documented

---

## Phase 1 Acceptance Criteria

**Core Functionality:**
- [ ] 8 universities in database
- [ ] Each university can manage their own teams/faculty/projects
- [ ] PROVES shared project visible to all
- [ ] Cross-university interfaces tracked and displayed
- [ ] Comparative dashboard shows all 8 universities
- [ ] Outcomes can be recorded and viewed
- [ ] Data persists across server restarts
- [ ] All universities can view all data (read-only for others)

**Technical Quality:**
- [ ] No duplicate code (models, migrations)
- [ ] Database is source of truth (no JSON file)
- [ ] Audit logs track all changes
- [ ] Basic authentication working
- [ ] API documented

**Research Readiness:**
- [ ] Outcomes data structure supports AI training
- [ ] Export functionality for research analysis
- [ ] Pattern comparison possible across universities

---

## Total Effort Estimate

**Phase 1: ~19 hours**
1. Clean foundation: 2h
2. Multi-university schema: 3h
3. Seed data: 2h
4. Update endpoints: 4h
5. Authentication: 2h
6. Frontend: 4h
7. Testing & docs: 2h

**Realistic timeline:** 2-3 focused work sessions over 1 week

---

## Questions Resolved

✅ **University count:** 8 total
✅ **Lead institution:** Cal Poly Pomona
✅ **Shared project:** PROVES
✅ **Individual projects:** Each university has their own
✅ **Dashboard purpose:** Data collection + open sharing
✅ **Success metrics:** Mission launch + generational transfer

---

## Next Actions

**Ready to execute Phase 1:**

**Session 1 (6-7 hours):**
1. Clean up duplicates
2. Add multi-university schema
3. Seed initial data
4. Update core endpoints

**Session 2 (6-7 hours):**
5. Add authentication
6. Build frontend views
7. Create comparative dashboard

**Session 3 (4-5 hours):**
8. Test everything
9. Document
10. Deploy for testing

**Would you like me to start with Session 1 now?**

I can begin by:
1. Cleaning up the duplicate code
2. Creating the Universities model
3. Adding university_id to existing models
4. Seeding the 8 universities + PROVES project

Let me know and I'll execute!

---

**End of Phase 1 Final Plan**
