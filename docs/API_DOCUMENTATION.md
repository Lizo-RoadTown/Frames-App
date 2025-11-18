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
  "proves_project": {
    "id": "PROVES",
    "name": "PROVES - Multi-University Collaborative Mission",
    "is_collaborative": true
  },
  "aggregate_metrics": {
    "university_count": 8,
    "total_teams": 12,
    "total_faculty": 6,
    "total_projects": 7,
    "total_interfaces": 17,
    "cross_university_interfaces": 4
  }
}
```

### GET /api/dashboard/proves

Get PROVES collaborative project details.

**Request:**
```http
GET /api/dashboard/proves HTTP/1.1
X-University-ID: CalPolyPomona
```

**Response:**
```json
{
  "project": {
    "id": "PROVES",
    "name": "PROVES - Multi-University Collaborative Mission",
    "description": "Shared collaborative space mission...",
    "is_collaborative": true,
    "duration": 36
  },
  "participating_teams": [
    {
      "id": "CalPolyPomona_team_proves",
      "university_id": "CalPolyPomona",
      "name": "Cal Poly Pomona PROVES Team",
      "size": 6,
      "experience": 12
    }
    // ... more teams
  ],
  "collaboration_interfaces": [
    {
      "id": "cross_cpp_texas_1",
      "from": "CalPolyPomona_team_proves",
      "to": "TexasState_team_proves",
      "bondType": "codified-strong",
      "is_cross_university": true
    }
  ],
  "metrics": {
    "university_count": 3,
    "team_count": 12,
    "interface_count": 4
  }
}
```

---

## Outcomes

### GET /api/outcomes

Get mission/program success outcomes.

**Query Parameters:**
- `university_id` (optional) - Filter by specific university

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
    "notes": "Successful payload launch",
    "recorded_at": "2025-11-18T..."
  },
  {
    "id": 2,
    "university_id": "CalPolyPomona",
    "outcome_type": "program_success",
    "success": true,
    "cohort_year": 2024,
    "notes": "Knowledge successfully transferred to incoming cohort",
    "recorded_at": "2025-11-18T..."
  }
]
```

### POST /api/outcomes

Record a new outcome.

**Request:**
```http
POST /api/outcomes HTTP/1.1
X-University-ID: CalPolyPomona
Content-Type: application/json

{
  "university_id": "CalPolyPomona",
  "project_id": "CalPolyPomona_project_cubesat",
  "outcome_type": "mission_success",
  "success": true,
  "cohort_year": 2024,
  "notes": "Successful payload launch to LEO"
}
```

**Response:** Created outcome object (201 Created)

**Permissions:** Can only create outcomes for your own university (unless researcher mode)

---

**End of API Documentation**
