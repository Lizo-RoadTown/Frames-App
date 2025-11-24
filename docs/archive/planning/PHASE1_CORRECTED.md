# FRAMES Phase 1: Multi-University Collaborative Dashboard

**Date:** 2025-11-18
**Purpose:** Corrected Phase 1 plan accounting for 8-university collaborative architecture

---

## Project Scope (Corrected Understanding)

### The Real System

**FRAMES is a collaborative research instrument for 8 universities:**
- University of Texas State
- Columbia University
- 6 other universities (TBD)

**Working together on:**
- Space missions (CubeSats, JPL contracts, etc.)
- Knowledge transfer research
- AI-based mission success prediction

### Two User Modes

**1. Operations Mode (Per-University)**
- Each university manages their own:
  - Teams (Software, CommsRF, MissionOps, etc.)
  - Faculty advisors
  - Projects
  - Internal interfaces
- Full CRUD control over their own data
- Read-only view of other universities

**2. Research/Comparison Mode (Cross-University)**
- **Main Dashboard** - All 8 universities displayed side-by-side
- Comparative metrics and analytics
- Cross-university interface visualization
- Pattern detection across institutions
- AI training data aggregation

### Key Requirements

1. ✅ **Data isolation** - Each university owns their data
2. ✅ **Shared visibility** - All can see all (read-only for others' data)
3. ✅ **Collaboration tracking** - Cross-university interfaces visible
4. ✅ **Comparative learning** - "Launch conscious" - learn from each other
5. ✅ **Research analytics** - Aggregate data for AI training

---

## Phase 1 Architecture (Corrected)

### Database Schema

**Multi-tenant with university_id everywhere:**

```sql
-- Core entity tables
CREATE TABLE teams (
    id TEXT PRIMARY KEY,
    university_id TEXT NOT NULL,  -- TexasState, Columbia, etc.
    discipline TEXT,
    lifecycle TEXT,
    name TEXT NOT NULL,
    size INTEGER,
    experience INTEGER,
    description TEXT,
    created_at TEXT,
    meta JSON
);

CREATE TABLE faculty (
    id TEXT PRIMARY KEY,
    university_id TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT,
    description TEXT,
    created_at TEXT,
    meta JSON
);

CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    university_id TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT,  -- jpl-contract, multiversity, internal
    duration INTEGER,
    description TEXT,
    created_at TEXT,
    meta JSON
);

CREATE TABLE interfaces (
    id TEXT PRIMARY KEY,
    from_entity TEXT NOT NULL,      -- Can be cross-university
    to_entity TEXT NOT NULL,        -- Can be cross-university
    interface_type TEXT,
    bond_type TEXT,
    energy_loss INTEGER,
    created_at TEXT,
    meta JSON,
    -- For cross-university tracking:
    from_university TEXT,           -- Extracted from from_entity
    to_university TEXT              -- Extracted from to_entity
);

CREATE TABLE universities (
    id TEXT PRIMARY KEY,            -- TexasState, Columbia, etc.
    name TEXT NOT NULL,             -- "University of Texas State"
    active BOOLEAN DEFAULT TRUE,
    meta JSON,
    created_at TEXT
);

-- Audit logging (essential for research)
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    actor TEXT NOT NULL,            -- user@TexasState, researcher@Columbia
    action TEXT NOT NULL,           -- create, update, delete
    entity_type TEXT NOT NULL,
    entity_id TEXT,
    university_id TEXT,             -- Which university's data was affected
    payload_before TEXT,
    payload_after TEXT,
    meta JSON,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### Access Control Pattern

**Authorization logic:**
```python
def can_write(user, entity):
    """Users can only write to their own university's data"""
    return user.university_id == entity.university_id

def can_read(user, entity):
    """Users can read all universities' data"""
    return True

def can_delete(user, entity):
    """Users can only delete their own university's data"""
    return user.university_id == entity.university_id
```

### UI Architecture

**Three main views:**

**1. University Dashboard (Operations Mode)**
```
+--------------------------------------------------+
| University of Texas State                       |
+--------------------------------------------------+
| My Teams (8) | My Faculty (3) | My Projects (3) |
+--------------------------------------------------+
| [Create Team] [Create Faculty] [Create Project] |
+--------------------------------------------------+
|                                                  |
| Molecular Visualization (Texas State only)      |
|                                                  |
+--------------------------------------------------+
| Cross-University Collaborations:                |
| - Columbia.PROVES <-> TexasState.PROVES         |
+--------------------------------------------------+
```

**2. Comparative Dashboard (Research Mode)**
```
+------------------------------------------------------------------------------+
| All Universities - Comparative View                                         |
+------------------------------------------------------------------------------+
| TexasState | Columbia | Berkeley | Stanford | MIT | Caltech | USC | AFRL   |
+------------------------------------------------------------------------------+
| Teams: 8   | Teams: 6 | Teams: 7 | Teams: 5   | ... | ...    | ... | ...    |
| Faculty: 3 | Faculty:2| Faculty:4| Faculty: 3 | ... | ...    | ... | ...    |
+------------------------------------------------------------------------------+
|                    Side-by-Side Molecular Visualizations                    |
| [TexasState vis] [Columbia vis] [Berkeley vis] [Stanford vis] ...          |
+------------------------------------------------------------------------------+
| Aggregate Analytics:                                                        |
| - Cross-university interface health                                         |
| - Knowledge transfer patterns                                               |
| - Mission success correlation                                               |
+------------------------------------------------------------------------------+
```

**3. Admin Panel (Researcher Mode)**
```
+--------------------------------------------------+
| Research Administration                          |
+--------------------------------------------------+
| Manage Universities | Export Data | Run Analysis|
+--------------------------------------------------+
| AI Training Dashboard:                           |
| - Outcomes data entry                            |
| - Pattern visualization                          |
| - Prediction model performance                   |
+--------------------------------------------------+
```

---

## Phase 1 Objectives (Corrected)

### Primary Goals

1. **Multi-university data model** ✅ (partially done)
   - Add `universities` table
   - Ensure all entities have `university_id`
   - Support cross-university interfaces

2. **Database migration** ❌ (incomplete)
   - Migrate from `frames_data.json` to SQLite
   - Populate initial data for 2-3 universities (start small)
   - All endpoints read/write from database

3. **University-scoped operations** ❌
   - Filter queries by `university_id`
   - CRUD endpoints respect university ownership
   - Cross-university read access

4. **Comparative dashboard** ❌
   - New endpoint: `GET /api/dashboard/comparative`
   - Returns aggregated data for all universities
   - Side-by-side visualization support

5. **Basic auth** ❌
   - User identification (which university)
   - Simple token-based auth
   - Enforce write permissions

---

## What's Already Done (Re-evaluated)

✅ **Database schema foundation**
- SQLite database exists
- Core tables created (teams, faculty, projects, interfaces)
- Sample data loads correctly

✅ **Sandbox model** (actually the university container!)
- `Sandbox` table with `university_id`
- This is actually the **university isolation mechanism**
- Just needs to be renamed/repurposed

✅ **API structure**
- REST endpoints exist
- CRUD operations defined
- Analytics endpoints present

✅ **Audit logging infrastructure**
- `audit_logs` table exists
- Audit helper function exists
- Needs completion for all endpoints

---

## What Needs to Be Done (Corrected Priorities)

### 1. Add Universities Table & Model (2 hours)

**Create proper multi-university foundation:**

```python
# backend/db_models.py
class University(db.Model):
    __tablename__ = 'universities'
    id = db.Column(db.String, primary_key=True)  # TexasState, Columbia
    name = db.Column(db.String, nullable=False)   # "University of Texas State"
    active = db.Column(db.Boolean, default=True)
    meta = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
```

**Seed initial universities:**
```python
universities = [
    {'id': 'TexasState', 'name': 'University of Texas State'},
    {'id': 'Columbia', 'name': 'Columbia University'},
    {'id': 'Berkeley', 'name': 'UC Berkeley'},
    # Add remaining 5 universities
]
```

### 2. Add university_id to All Models (1 hour)

**Update existing models:**
```python
class TeamModel(db.Model):
    # ... existing fields ...
    university_id = db.Column(db.String, nullable=False, index=True)

class FacultyModel(db.Model):
    # ... existing fields ...
    university_id = db.Column(db.String, nullable=False, index=True)
```

**Migration strategy:**
- Add columns with default value
- Update existing records
- Make nullable=False after population

### 3. Complete Database Migration (2 hours)

**Tasks:**
- Clean up duplicate migration scripts (keep one)
- Clean up duplicate models (keep Flask-SQLAlchemy only)
- Run migration to import `frames_data.json` if exists
- Seed sample data for 2-3 universities

### 4. Update Endpoints for Multi-University (3 hours)

**Pattern for university-scoped queries:**

```python
@app.route('/api/teams', methods=['GET'])
def get_teams():
    """Get teams - filter by university if specified"""
    university_id = request.args.get('university_id')

    if university_id:
        teams = TeamModel.query.filter_by(university_id=university_id).all()
    else:
        teams = TeamModel.query.all()  # All universities (for comparison)

    return jsonify([t.to_dict() for t in teams])

@app.route('/api/teams', methods=['POST'])
def create_team():
    """Create team - must include university_id"""
    data = request.json

    # Get actor's university from auth (for now, from header)
    actor_university = request.headers.get('X-University-ID', 'TexasState')

    # Ensure team belongs to actor's university
    data['university_id'] = actor_university

    team = TeamModel(**data)
    db.session.add(team)
    db.session.commit()

    _log_audit(actor_university, 'create', 'team', team.id, None, team.to_dict())

    return jsonify(team.to_dict()), 201
```

### 5. Create Comparative Dashboard Endpoint (2 hours)

**New endpoint for side-by-side view:**

```python
@app.route('/api/dashboard/comparative', methods=['GET'])
def get_comparative_dashboard():
    """Return aggregated data for all universities"""
    universities = University.query.filter_by(active=True).all()

    result = {
        'universities': {},
        'cross_university_interfaces': [],
        'aggregate_metrics': {}
    }

    for uni in universities:
        uni_id = uni.id

        # Get counts and data for each university
        teams = TeamModel.query.filter_by(university_id=uni_id).all()
        faculty = FacultyModel.query.filter_by(university_id=uni_id).all()
        projects = ProjectModel.query.filter_by(university_id=uni_id).all()

        result['universities'][uni_id] = {
            'name': uni.name,
            'teams': [t.to_dict() for t in teams],
            'faculty': [f.to_dict() for f in faculty],
            'projects': [p.to_dict() for p in projects],
            'metrics': {
                'team_count': len(teams),
                'faculty_count': len(faculty),
                'project_count': len(projects)
            }
        }

    # Find cross-university interfaces
    all_interfaces = InterfaceModel.query.all()
    for interface in all_interfaces:
        from_uni = interface.from_entity.split('.')[0]  # Parse university from entity ID
        to_uni = interface.to_entity.split('.')[0]

        if from_uni != to_uni:
            result['cross_university_interfaces'].append(interface.to_dict())

    return jsonify(result)
```

### 6. Basic Authentication (2 hours)

**Simple university identification:**

```python
# backend/auth.py
def get_current_university():
    """Get university ID from request headers"""
    # For Phase 1: simple header-based
    # For Phase 2: JWT token with university claim
    return request.headers.get('X-University-ID', 'TexasState')

def require_university_ownership(entity):
    """Ensure user can only modify their own university's data"""
    user_university = get_current_university()

    if entity.university_id != user_university:
        abort(403, description="Can only modify your own university's data")
```

### 7. Frontend Updates (4 hours)

**Add university selector:**
```javascript
// frontend/static/app.js

// Global state
let currentUniversity = 'TexasState';
let viewMode = 'operations'; // or 'comparative'

// Set university context for all API calls
FramesAPI.setUniversity = function(universityId) {
    currentUniversity = universityId;
    // Reload data for new university
    loadUniversityData();
};

// Toggle between operations and comparative view
function toggleViewMode(mode) {
    viewMode = mode;
    if (mode === 'operations') {
        showUniversityDashboard(currentUniversity);
    } else if (mode === 'comparative') {
        showComparativeDashboard();
    }
}

async function showComparativeDashboard() {
    const data = await FramesAPI.getComparativeDashboard();

    // Render side-by-side visualizations
    for (const [uniId, uniData] of Object.entries(data.universities)) {
        renderUniversityPanel(uniId, uniData);
    }

    // Highlight cross-university interfaces
    renderCrossUniversityConnections(data.cross_university_interfaces);
}
```

---

## Phase 1 Acceptance Criteria (Corrected)

### Must Have

✅ **Multi-university data model**
- [ ] Universities table created with 8 universities
- [ ] All entities have `university_id` column
- [ ] Cross-university interfaces trackable

✅ **University-scoped operations**
- [ ] GET endpoints filter by `university_id`
- [ ] POST endpoints enforce university ownership
- [ ] DELETE limited to own university's data

✅ **Comparative dashboard**
- [ ] `/api/dashboard/comparative` endpoint
- [ ] Returns all universities' data aggregated
- [ ] Cross-university interfaces identified

✅ **Data persistence**
- [ ] Database is source of truth (not JSON file)
- [ ] All CRUD operations use database
- [ ] Data survives server restart

✅ **Basic authentication**
- [ ] User identified by university
- [ ] Write permissions enforced
- [ ] Audit logs track actor university

### Should Have

- [ ] Clean codebase (no duplicates)
- [ ] Comprehensive audit logging
- [ ] Verification tests pass
- [ ] Sample data for 3+ universities

### Nice to Have (Defer to Phase 2)

- JWT-based authentication
- Real-time collaboration (WebSockets)
- Advanced cross-university analytics
- Postgres migration

---

## Revised Estimation

### Phase 1 Total: ~16 hours

1. Add Universities table & seed (2h)
2. Add university_id to models (1h)
3. Clean up duplicates (1h)
4. Complete database migration (2h)
5. Update endpoints for multi-university (3h)
6. Create comparative dashboard endpoint (2h)
7. Basic authentication (2h)
8. Frontend updates (4h)
9. Testing & verification (2h)

**Realistic timeline:** 2-3 focused work sessions

---

## Critical Design Decisions

### Question 1: Entity ID Format

**Option A: University-prefixed IDs**
```
team_id = "TexasState.team_1"
faculty_id = "Columbia.faculty_2"
```
**Pros:** Self-documenting, clear ownership
**Cons:** Parsing needed for cross-references

**Option B: Separate university_id column**
```
team_id = "team_1"
university_id = "TexasState"
```
**Pros:** Clean schema, easier queries
**Cons:** Need JOIN or lookup for university

**Recommendation:** Option B (already implemented)

### Question 2: Cross-University Interface Storage

**Current pattern:**
```json
{
  "id": "interface_1",
  "from_entity": "team_1",
  "to_entity": "team_3",
  "interface_type": "team-to-team"
}
```

**For cross-university:**
```json
{
  "id": "interface_cross_1",
  "from_entity": "TexasState.team_1",  // Prefix with university
  "to_entity": "Columbia.team_2",
  "interface_type": "team-to-team",
  "from_university": "TexasState",      // Explicit for querying
  "to_university": "Columbia"
}
```

### Question 3: Sandbox vs University Naming

**Current:** `Sandbox` table with `university_id`

**Options:**
- Rename to `University` (clearer)
- Keep `Sandbox` for "play mode" vs "production mode"
- Have both: `University` for org, `Sandbox` for temporary scenarios

**Recommendation:** Ask user - is "sandbox" meant for testing scenarios, or is it the university container?

---

## Next Steps

**If you approve this corrected plan, I can:**

1. ✅ **Clean up duplicates** (1h)
   - Remove duplicate models from `db_models.py`
   - Remove duplicate migration from `migrate_frames.py`

2. ✅ **Add multi-university foundation** (2h)
   - Create Universities table
   - Add university_id to all models
   - Seed 3 universities (Texas State, Columbia, Berkeley)

3. ✅ **Complete database migration** (2h)
   - Switch endpoints to use database
   - Load sample data for each university
   - Deprecate JSON file

4. ✅ **Build comparative dashboard** (2h)
   - Create `/api/dashboard/comparative` endpoint
   - Return aggregated data
   - Identify cross-university interfaces

**Total first session:** ~7 hours of focused work

**Deliverable:** Working multi-university system with comparative dashboard

---

## Questions for You

1. **University list:** What are the 8 universities?
   - Texas State ✓
   - Columbia ✓
   - 6 others?

2. **Sandbox purpose:** Is "Sandbox" for:
   - Testing/play mode scenarios? OR
   - The actual university data container?

3. **Auth priority:** Should Phase 1 have:
   - Simple header-based university ID (quick)
   - JWT tokens with proper login (more work)
   - Defer auth to Phase 2 (trust mode)

4. **Priority order:** Which matters most first?
   - a) Clean up duplicates and complete migration
   - b) Add multi-university support
   - c) Build comparative dashboard
   - d) All three in parallel

Let me know your answers and I'll execute the corrected Phase 1 plan!

---

**End of Corrected Phase 1 Plan**
