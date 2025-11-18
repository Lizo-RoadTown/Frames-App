# Parallel Task Assignments - FRAMES Project

**Created:** 2025-11-18
**Context:** Multi-university collaborative dashboard for space mission knowledge transfer research

---

## ⚠️ CRITICAL CONTEXT - READ THIS FIRST

### What FRAMES Actually Is

**NOT a single university system** - This is a collaborative platform for **8 universities** working together on space missions.

**The Universities:**
1. **Cal Poly Pomona** - Lead research institution
2. **Texas State University**
3. **Columbia University**
4. **5 others** (Uni_D through Uni_H - placeholders for now)

**The PROVES Project:**
A **shared collaborative mission** across all 8 universities. Each university ALSO has their own internal projects (CubeSats, research initiatives), but PROVES is the one big shared project they all work on together.

**The Purpose:**
- Track team structures, faculty, and knowledge transfer interfaces across universities
- **All universities can see all data** (transparency/learning from each other)
- Each university can **only edit their own data**
- Researcher at Cal Poly Pomona uses aggregated data to train AI for predicting mission success

**Success Metrics Being Tracked:**
1. **Mission Success** - Did the payload launch successfully?
2. **Program Success** - Did the next generation (cohort) successfully continue the program?

### Current Project Status

**✓ COMPLETED (Session 1):**
- Multi-university database schema created
- 8 universities seeded
- PROVES shared project created
- Sample data for Cal Poly Pomona, Texas State, Columbia
- Cross-university interfaces working

**🚧 IN PROGRESS (Current Agent - Session 2):**
- Updating API endpoints for multi-university support
- Building comparative dashboard backend
- Adding university filtering to all GET/POST/DELETE operations

**👉 YOUR TASKS (Below):**
Independent work that won't conflict with Session 2 backend development

---

## Task 1: Build Comparative Dashboard Frontend HTML/CSS

### Task ID: `PARALLEL-TASK-1-FRONTEND-DASHBOARD`

### Objective
Create the HTML and CSS for the main comparative dashboard that shows all 8 universities side-by-side so they can compare their team structures, metrics, and learn from each other.

### Why This Matters
This is the **primary interface** for the collaborative learning aspect. Universities need to see each other's data to understand what works and what doesn't for knowledge transfer.

### Detailed Requirements

#### 1. Create the HTML File

**Location:** `frontend/templates/comparative_dashboard.html`

**Structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FRAMES - Comparative Dashboard</title>
    <link rel="stylesheet" href="/static/comparative_dashboard.css">
</head>
<body>
    <header>
        <h1>FRAMES - Multi-University Comparative Dashboard</h1>
        <nav>
            <button id="viewAllBtn" class="active">All Universities</button>
            <button id="viewProvesBtn">PROVES Collaboration</button>
            <button id="viewOutcomesBtn">Outcomes</button>
        </nav>
    </header>

    <main id="dashboardContent">
        <!-- This section will show all 8 universities side-by-side -->
        <section id="allUniversitiesView">
            <h2>All Universities Overview</h2>

            <div class="universities-grid">
                <!-- Repeat this card 8 times, one per university -->
                <!-- University 1: Cal Poly Pomona -->
                <div class="university-card" data-university-id="CalPolyPomona">
                    <div class="university-header lead">
                        <h3>Cal Poly Pomona</h3>
                        <span class="lead-badge">Lead Institution</span>
                    </div>
                    <div class="university-metrics">
                        <div class="metric">
                            <span class="metric-label">Teams</span>
                            <span class="metric-value" id="cpp-teams">4</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Faculty</span>
                            <span class="metric-value" id="cpp-faculty">2</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Projects</span>
                            <span class="metric-value" id="cpp-projects">2</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Interfaces</span>
                            <span class="metric-value" id="cpp-interfaces">7</span>
                        </div>
                    </div>
                    <div class="university-visualization">
                        <!-- Placeholder for molecular visualization -->
                        <div class="viz-placeholder">Molecular Visualization</div>
                    </div>
                    <div class="university-actions">
                        <button class="btn-view-detail">View Details</button>
                    </div>
                </div>

                <!-- University 2: Texas State -->
                <div class="university-card" data-university-id="TexasState">
                    <div class="university-header">
                        <h3>Texas State</h3>
                    </div>
                    <div class="university-metrics">
                        <div class="metric">
                            <span class="metric-label">Teams</span>
                            <span class="metric-value" id="texas-teams">4</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Faculty</span>
                            <span class="metric-value" id="texas-faculty">2</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Projects</span>
                            <span class="metric-value" id="texas-projects">2</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Interfaces</span>
                            <span class="metric-value" id="texas-interfaces">6</span>
                        </div>
                    </div>
                    <div class="university-visualization">
                        <div class="viz-placeholder">Molecular Visualization</div>
                    </div>
                    <div class="university-actions">
                        <button class="btn-view-detail">View Details</button>
                    </div>
                </div>

                <!-- University 3: Columbia -->
                <div class="university-card" data-university-id="Columbia">
                    <div class="university-header">
                        <h3>Columbia</h3>
                    </div>
                    <div class="university-metrics">
                        <div class="metric">
                            <span class="metric-label">Teams</span>
                            <span class="metric-value" id="columbia-teams">4</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Faculty</span>
                            <span class="metric-value" id="columbia-faculty">2</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Projects</span>
                            <span class="metric-value" id="columbia-projects">2</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Interfaces</span>
                            <span class="metric-value" id="columbia-interfaces">6</span>
                        </div>
                    </div>
                    <div class="university-visualization">
                        <div class="viz-placeholder">Molecular Visualization</div>
                    </div>
                    <div class="university-actions">
                        <button class="btn-view-detail">View Details</button>
                    </div>
                </div>

                <!-- Universities 4-8: Uni_D through Uni_H -->
                <!-- Copy the structure above for Uni_D, Uni_E, Uni_F, Uni_G, Uni_H -->
                <!-- Set all metrics to 0 for now since we haven't seeded data for them yet -->

                <div class="university-card" data-university-id="Uni_D">
                    <div class="university-header">
                        <h3>University D</h3>
                        <span class="coming-soon">Data Coming Soon</span>
                    </div>
                    <div class="university-metrics">
                        <div class="metric">
                            <span class="metric-label">Teams</span>
                            <span class="metric-value">0</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Faculty</span>
                            <span class="metric-value">0</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Projects</span>
                            <span class="metric-value">0</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Interfaces</span>
                            <span class="metric-value">0</span>
                        </div>
                    </div>
                    <div class="university-visualization">
                        <div class="viz-placeholder empty">No Data Yet</div>
                    </div>
                </div>

                <!-- Repeat for Uni_E, Uni_F, Uni_G, Uni_H -->

            </div>

            <!-- Cross-University Connections Section -->
            <section class="cross-university-section">
                <h3>PROVES Cross-University Collaboration Network</h3>
                <div class="collaboration-matrix">
                    <p>Showing knowledge transfer interfaces between universities</p>
                    <!-- Placeholder for network visualization -->
                    <div class="network-viz-placeholder">
                        <svg width="800" height="400">
                            <!-- Will be populated by JavaScript later -->
                            <text x="400" y="200" text-anchor="middle" fill="#666">
                                Cross-University Network Graph (JavaScript Integration Pending)
                            </text>
                        </svg>
                    </div>
                </div>

                <div class="collaboration-list">
                    <h4>Active Cross-University Interfaces:</h4>
                    <ul>
                        <li>Cal Poly Pomona ↔ Texas State: 2 strong interfaces</li>
                        <li>Texas State ↔ Columbia: 1 moderate interface</li>
                        <li>Cal Poly Pomona ↔ Columbia: 1 strong interface</li>
                    </ul>
                </div>
            </section>
        </section>

        <!-- PROVES View (hidden by default) -->
        <section id="provesView" class="hidden">
            <h2>PROVES Collaborative Mission</h2>
            <div class="proves-overview">
                <p>8 universities collaborating on multi-university space mission</p>
                <!-- Will be populated via JavaScript -->
            </div>
        </section>

        <!-- Outcomes View (hidden by default) -->
        <section id="outcomesView" class="hidden">
            <h2>Mission & Program Outcomes</h2>
            <table class="outcomes-table">
                <thead>
                    <tr>
                        <th>University</th>
                        <th>Missions Launched</th>
                        <th>Mission Success Rate</th>
                        <th>Program Cohorts</th>
                        <th>Transfer Success Rate</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- Will be populated via JavaScript -->
                </tbody>
            </table>
        </section>
    </main>

    <script src="/static/comparative_dashboard.js"></script>
</body>
</html>
```

#### 2. Create the CSS File

**Location:** `frontend/static/comparative_dashboard.css`

**Requirements:**
- **Responsive grid layout** - 8 cards should fit nicely (2 rows of 4, or 4 rows of 2 on smaller screens)
- **Color coding** - Lead institution (Cal Poly Pomona) should have distinct styling
- **Card hover effects** - Slight elevation/shadow on hover
- **Clear metrics display** - Large readable numbers
- **Mobile responsive** - Stack cards vertically on small screens

**CSS Starter (you can enhance this):**
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #f5f7fa;
    color: #333;
}

header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    color: white;
    padding: 2rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

header h1 {
    font-size: 2rem;
    margin-bottom: 1rem;
}

nav {
    display: flex;
    gap: 1rem;
}

nav button {
    padding: 0.75rem 1.5rem;
    border: 2px solid white;
    background: transparent;
    color: white;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}

nav button:hover {
    background: white;
    color: #1e3c72;
}

nav button.active {
    background: white;
    color: #1e3c72;
}

main {
    padding: 2rem;
    max-width: 1600px;
    margin: 0 auto;
}

.universities-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.university-card {
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    padding: 1.5rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.university-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

.university-header {
    border-bottom: 2px solid #e0e0e0;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
}

.university-header.lead {
    border-bottom: 2px solid #2a5298;
}

.university-header h3 {
    font-size: 1.5rem;
    color: #333;
}

.lead-badge {
    display: inline-block;
    background: #2a5298;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 15px;
    font-size: 0.75rem;
    margin-top: 0.5rem;
}

.coming-soon {
    display: inline-block;
    background: #ffa500;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 15px;
    font-size: 0.75rem;
    margin-top: 0.5rem;
}

.university-metrics {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin: 1rem 0;
}

.metric {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;
}

.metric-label {
    font-size: 0.875rem;
    color: #666;
    margin-bottom: 0.5rem;
}

.metric-value {
    font-size: 2rem;
    font-weight: bold;
    color: #2a5298;
}

.university-visualization {
    margin: 1rem 0;
    min-height: 200px;
}

.viz-placeholder {
    background: #e9ecef;
    border: 2px dashed #ccc;
    border-radius: 8px;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
    font-style: italic;
}

.viz-placeholder.empty {
    background: #f8f9fa;
    color: #999;
}

.university-actions {
    margin-top: 1rem;
}

.btn-view-detail {
    width: 100%;
    padding: 0.75rem;
    background: #2a5298;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    transition: background 0.3s ease;
}

.btn-view-detail:hover {
    background: #1e3c72;
}

.cross-university-section {
    margin-top: 3rem;
    padding: 2rem;
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.network-viz-placeholder {
    margin: 2rem 0;
    background: #f8f9fa;
    border-radius: 8px;
    padding: 2rem;
}

.collaboration-list ul {
    list-style: none;
    padding: 1rem;
}

.collaboration-list li {
    padding: 0.75rem;
    margin: 0.5rem 0;
    background: #f8f9fa;
    border-left: 4px solid #2a5298;
    border-radius: 4px;
}

.hidden {
    display: none;
}

/* Responsive Design */
@media (max-width: 768px) {
    .universities-grid {
        grid-template-columns: 1fr;
    }

    header h1 {
        font-size: 1.5rem;
    }

    nav {
        flex-direction: column;
    }
}
```

#### 3. Create Basic JavaScript for View Switching

**Location:** `frontend/static/comparative_dashboard.js`

**Purpose:** Handle switching between "All Universities", "PROVES", and "Outcomes" views.

```javascript
// View switching functionality
document.addEventListener('DOMContentLoaded', function() {
    const viewAllBtn = document.getElementById('viewAllBtn');
    const viewProvesBtn = document.getElementById('viewProvesBtn');
    const viewOutcomesBtn = document.getElementById('viewOutcomesBtn');

    const allUniversitiesView = document.getElementById('allUniversitiesView');
    const provesView = document.getElementById('provesView');
    const outcomesView = document.getElementById('outcomesView');

    function showView(viewToShow) {
        // Hide all views
        allUniversitiesView.classList.add('hidden');
        provesView.classList.add('hidden');
        outcomesView.classList.add('hidden');

        // Remove active class from all buttons
        viewAllBtn.classList.remove('active');
        viewProvesBtn.classList.remove('active');
        viewOutcomesBtn.classList.remove('active');

        // Show selected view and activate button
        viewToShow.element.classList.remove('hidden');
        viewToShow.button.classList.add('active');
    }

    viewAllBtn.addEventListener('click', () => {
        showView({ element: allUniversitiesView, button: viewAllBtn });
    });

    viewProvesBtn.addEventListener('click', () => {
        showView({ element: provesView, button: viewProvesBtn });
    });

    viewOutcomesBtn.addEventListener('click', () => {
        showView({ element: outcomesView, button: viewOutcomesBtn });
    });

    // TODO: Add API integration later when backend endpoints are ready
    // This is just the UI shell for now
});
```

### Acceptance Criteria

✓ HTML file created at correct location
✓ CSS file created with responsive grid layout
✓ 8 university cards displayed (3 with data, 5 placeholders)
✓ Cal Poly Pomona has "Lead Institution" badge
✓ View switching buttons work (All Universities / PROVES / Outcomes)
✓ Cards have hover effects
✓ Mobile responsive (cards stack on small screens)
✓ Cross-university collaboration section included
✓ No JavaScript errors in browser console

### What NOT to Do

❌ Don't integrate API calls yet (backend endpoints not ready)
❌ Don't build actual molecular visualizations (just placeholder divs)
❌ Don't modify any Python files
❌ Don't touch the database

### Testing Your Work

1. Open the HTML file in a browser directly or via Flask server
2. Resize browser window to test responsiveness
3. Click view switching buttons - should show/hide sections
4. Hover over cards - should see elevation effect
5. Check browser console - no JavaScript errors

---

## Task 2: Create Documentation for API Endpoints

### Task ID: `PARALLEL-TASK-2-API-DOCS`

### Objective
Document the API endpoints that WILL exist after Session 2 is complete, so other developers (and future AI agents) understand how to use the multi-university API.

### Why This Matters
Other universities will be integrating with this system. They need clear documentation on:
- How to query their own data
- How to view other universities' data
- How PROVES collaboration works
- What permissions they have

### Detailed Requirements

#### Create API Documentation File

**Location:** `docs/API_DOCUMENTATION.md`

**Structure:**

```markdown
# FRAMES API Documentation

**Version:** 1.0 (Phase 1)
**Base URL:** `http://localhost:5000/api`
**Authentication:** Header-based (Phase 1) - JWT planned for Phase 2

---

## Authentication

### Current (Phase 1): Header-Based

All requests must include:
```
X-University-ID: CalPolyPomona
```

**Valid University IDs:**
- CalPolyPomona
- TexasState
- Columbia
- Uni_D
- Uni_E
- Uni_F
- Uni_G
- Uni_H

**Permissions:**
- **Read:** All universities can view all data
- **Write:** Universities can only create/update/delete their own data
- **Researcher Mode:** `X-Is-Researcher: true` grants cross-university write access (Cal Poly Pomona only)

---

## Universities

### GET /api/universities

Get list of all participating universities.

**Request:**
```http
GET /api/universities HTTP/1.1
X-University-ID: CalPolyPomona
```

**Response:**
```json
{
  "universities": [
    {
      "id": "CalPolyPomona",
      "name": "Cal Poly Pomona",
      "is_lead": true,
      "active": true,
      "created_at": "2025-11-18T..."
    },
    {
      "id": "TexasState",
      "name": "Texas State University",
      "is_lead": false,
      "active": true,
      "created_at": "2025-11-18T..."
    }
    // ... 6 more universities
  ]
}
```

---

## Teams

### GET /api/teams

Get teams with optional university filtering.

**Query Parameters:**
- `university_id` (optional) - Filter by specific university

**Request - All Teams:**
```http
GET /api/teams HTTP/1.1
X-University-ID: CalPolyPomona
```

**Request - One University's Teams:**
```http
GET /api/teams?university_id=TexasState HTTP/1.1
X-University-ID: CalPolyPomona
```

**Response:**
```json
[
  {
    "id": "CalPolyPomona_team_software",
    "university_id": "CalPolyPomona",
    "discipline": "software",
    "lifecycle": "established",
    "name": "Cal Poly Pomona Software",
    "size": 5,
    "experience": 24,
    "description": "Flight software and data processing team",
    "created_at": "2025-11-18T..."
  }
  // ... more teams
]
```

### POST /api/teams

Create a new team for YOUR university only.

**Request:**
```http
POST /api/teams HTTP/1.1
X-University-ID: CalPolyPomona
Content-Type: application/json

{
  "name": "Cal Poly Pomona New Team",
  "discipline": "mechanical",
  "lifecycle": "incoming",
  "size": 3,
  "experience": 6,
  "description": "New mechanical engineering team"
}
```

**Response:**
```json
{
  "id": "CalPolyPomona_team_mechanical",
  "university_id": "CalPolyPomona",
  "name": "Cal Poly Pomona New Team",
  "discipline": "mechanical",
  "lifecycle": "incoming",
  "size": 3,
  "experience": 6,
  "description": "New mechanical engineering team",
  "created_at": "2025-11-18T..."
}
```

**Note:** The system automatically sets `university_id` to match your `X-University-ID` header. You cannot create teams for other universities unless you have researcher mode.

### PUT /api/teams/{id}

Update an existing team (your university only).

**Request:**
```http
PUT /api/teams/CalPolyPomona_team_software HTTP/1.1
X-University-ID: CalPolyPomona
Content-Type: application/json

{
  "size": 6,
  "experience": 30
}
```

**Response:** Updated team object

**Error:** 403 Forbidden if trying to update another university's team

### DELETE /api/teams/{id}

Delete a team (your university only).

**Request:**
```http
DELETE /api/teams/CalPolyPomona_team_software HTTP/1.1
X-University-ID: CalPolyPomona
```

**Response:**
```json
{
  "success": true
}
```

**Error:** 403 Forbidden if trying to delete another university's team

---

## Faculty

### GET /api/faculty

Get faculty members with optional filtering.

**Query Parameters:**
- `university_id` (optional)

**Request:**
```http
GET /api/faculty?university_id=TexasState HTTP/1.1
X-University-ID: CalPolyPomona
```

**Response:**
```json
[
  {
    "id": "TexasState_faculty_pi",
    "university_id": "TexasState",
    "name": "Dr. Texas State PI",
    "role": "Principal Investigator",
    "description": "Project oversight and coordination",
    "created_at": "2025-11-18T..."
  }
]
```

### POST /api/faculty

Create faculty member (your university only).

### PUT /api/faculty/{id}

Update faculty (your university only).

### DELETE /api/faculty/{id}

Delete faculty (your university only).

---

## Projects

### GET /api/projects

Get projects with optional filtering.

**Query Parameters:**
- `university_id` (optional)
- `collaborative` (optional) - Filter for collaborative projects like PROVES

**Request - All Projects:**
```http
GET /api/projects HTTP/1.1
X-University-ID: CalPolyPomona
```

**Request - PROVES Only:**
```http
GET /api/projects?collaborative=true HTTP/1.1
X-University-ID: CalPolyPomona
```

**Response:**
```json
[
  {
    "id": "PROVES",
    "university_id": null,
    "name": "PROVES - Multi-University Collaborative Mission",
    "type": "proves",
    "is_collaborative": true,
    "duration": 36,
    "description": "Shared collaborative space mission...",
    "created_at": "2025-11-18T..."
  },
  {
    "id": "CalPolyPomona_project_cubesat",
    "university_id": "CalPolyPomona",
    "name": "Cal Poly Pomona CubeSat Mission",
    "type": "jpl-contract",
    "is_collaborative": false,
    "duration": 24,
    "description": "Primary satellite mission...",
    "created_at": "2025-11-18T..."
  }
]
```

**Note:** PROVES project has `university_id: null` because it's shared across all universities.

---

## Interfaces

### GET /api/interfaces

Get knowledge transfer interfaces with optional filtering.

**Query Parameters:**
- `university_id` (optional) - Interfaces involving this university
- `cross_university` (optional) - If "true", only show cross-university interfaces

**Request - Cross-University Only:**
```http
GET /api/interfaces?cross_university=true HTTP/1.1
X-University-ID: CalPolyPomona
```

**Response:**
```json
[
  {
    "id": "cross_cpp_texas_1",
    "from": "CalPolyPomona_team_proves",
    "to": "TexasState_team_proves",
    "interfaceType": "team-to-team",
    "bondType": "codified-strong",
    "energyLoss": 5,
    "from_university": "CalPolyPomona",
    "to_university": "TexasState",
    "is_cross_university": true,
    "created_at": "2025-11-18T..."
  }
]
```

---

## Comparative Dashboard

### GET /api/dashboard/comparative

Get aggregated data for all universities (side-by-side comparison).

**Request:**
```http
GET /api/dashboard/comparative HTTP/1.1
X-University-ID: CalPolyPomona
```

**Response:**
```json
{
  "universities": {
    "CalPolyPomona": {
      "name": "Cal Poly Pomona",
      "is_lead": true,
      "teams": [...],
      "faculty": [...],
      "projects": [...],
      "metrics": {
        "team_count": 4,
        "faculty_count": 2,
        "project_count": 2,
        "interface_count": 7
      }
    },
    "TexasState": {
      "name": "Texas State University",
      "is_lead": false,
      "teams": [...],
      "faculty": [...],
      "projects": [...],
      "metrics": {
        "team_count": 4,
        "faculty_count": 2,
        "project_count": 2,
        "interface_count": 6
      }
    }
    // ... all 8 universities
  },
  "cross_university_interfaces": [
    {
      "id": "cross_cpp_texas_1",
      "from": "CalPolyPomona_team_proves",
      "to": "TexasState_team_proves",
      "bondType": "codified-strong"
    }
  ],
  "aggregate_metrics": {
    "total_teams": 12,
    "total_faculty": 6,
    "total_projects": 7,
    "total_interfaces": 13,
    "cross_university_count": 4
  }
}
```

**Use Case:** This endpoint powers the comparative dashboard frontend where all 8 universities are displayed side-by-side.

---

## Outcomes

### GET /api/outcomes

Get mission/program success outcomes.

**Query Parameters:**
- `university_id` (optional)
- `outcome_type` (optional) - "mission_success" or "program_success"

**Request:**
```http
GET /api/outcomes?university_id=CalPolyPomona HTTP/1.1
X-University-ID: CalPolyPomona
```

**Response:**
```json
[
  {
    "id": 1,
    "university_id": "CalPolyPomona",
    "project_id": "CalPolyPomona_project_cubesat",
    "outcome_type": "mission_success",
    "success": true,
    "cohort_year": 2024,
    "notes": "Successful payload launch in partnership with JPL",
    "recorded_at": "2024-12-01T..."
  }
]
```

### POST /api/outcomes

Record a new outcome (your university only, or researcher mode for all).

**Request:**
```http
POST /api/outcomes HTTP/1.1
X-University-ID: CalPolyPomona
Content-Type: application/json

{
  "project_id": "CalPolyPomona_project_cubesat",
  "outcome_type": "mission_success",
  "success": true,
  "cohort_year": 2024,
  "notes": "Payload successfully deployed to orbit"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Missing required field: name"
}
```

### 403 Forbidden
```json
{
  "error": "Can only modify your own university's data"
}
```

### 404 Not Found
```json
{
  "error": "Team not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Database error",
  "trace": "..."
}
```

---

## Example Workflows

### Workflow 1: View My University's Data

```javascript
// 1. Get my teams
const teams = await fetch('/api/teams?university_id=CalPolyPomona', {
  headers: { 'X-University-ID': 'CalPolyPomona' }
}).then(r => r.json());

// 2. Get my faculty
const faculty = await fetch('/api/faculty?university_id=CalPolyPomona', {
  headers: { 'X-University-ID': 'CalPolyPomona' }
}).then(r => r.json());
```

### Workflow 2: Compare All Universities

```javascript
const comparison = await fetch('/api/dashboard/comparative', {
  headers: { 'X-University-ID': 'CalPolyPomona' }
}).then(r => r.json());

// Now you have data for all 8 universities
comparison.universities.CalPolyPomona.metrics.team_count; // 4
comparison.universities.TexasState.metrics.team_count; // 4
```

### Workflow 3: Record Mission Success

```javascript
await fetch('/api/outcomes', {
  method: 'POST',
  headers: {
    'X-University-ID': 'CalPolyPomona',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    project_id: 'CalPolyPomona_project_cubesat',
    outcome_type: 'mission_success',
    success: true,
    cohort_year: 2024,
    notes: 'Successful launch!'
  })
});
```

---

## Notes for Future Phases

**Phase 2 (Planned):**
- JWT authentication replaces headers
- Real-time WebSocket updates
- Postgres database
- Advanced RBAC (roles: admin, editor, viewer)

**Current Limitations (Phase 1):**
- Header-based auth is NOT secure (trust-based)
- No rate limiting
- SQLite database (not for production scale)
- No real-time updates (must refresh)

---

**End of API Documentation**
```

### Acceptance Criteria

✓ Documentation file created at `docs/API_DOCUMENTATION.md`
✓ All endpoint categories documented (Universities, Teams, Faculty, Projects, Interfaces, Outcomes, Dashboard)
✓ Request/response examples for each endpoint
✓ Query parameters documented
✓ Authentication explained clearly
✓ Permission model documented
✓ Error responses documented
✓ Example workflows provided
✓ Notes about PROVES shared project
✓ Cross-university interface explanation

---

## What I'm Working On (Parallel Work)

### Session 2: Backend API Implementation

**My Tasks (No Conflicts with Yours):**

1. **Update existing endpoints in `backend/app.py`:**
   - Add university_id filtering to GET /api/teams
   - Add university_id filtering to GET /api/faculty
   - Add university_id filtering to GET /api/projects
   - Add university_id filtering to GET /api/interfaces
   - Add permission checks to POST/PUT/DELETE

2. **Create new endpoints:**
   - GET /api/universities (list all 8 universities)
   - GET /api/dashboard/comparative (aggregated data)
   - GET /api/outcomes (outcomes data)
   - POST /api/outcomes (record outcomes)

3. **Add authentication helpers:**
   - Header-based university identification
   - Permission checking middleware
   - Researcher mode flag

**Files I'm Modifying:**
- `backend/app.py` (adding/updating routes)
- No HTML/CSS files (that's your domain)

**We Won't Conflict Because:**
- You're working on frontend HTML/CSS/JavaScript
- I'm working on backend Python API
- You're working on documentation
- Different files entirely

---

## Timeline

**Your Tasks:** Can be completed independently, no dependencies
**My Tasks:** Building API endpoints that will eventually power your frontend
**Integration Point:** After both are done, we connect your frontend to my backend API

---

## Questions?

If anything is unclear, document your questions and we can address them. The key things to remember:

1. **8 universities**, not 1
2. **PROVES is shared**, other projects are university-specific
3. **All can see all, each can edit their own**
4. **Cal Poly Pomona is lead** (special badge in UI)
5. **No backend integration yet** - just build the UI shell

---

**End of Parallel Task Assignments**
