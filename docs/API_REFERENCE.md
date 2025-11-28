# FRAMES API Reference

**Date:** 2025-11-28
**Version:** 1.0
**Base URL:** `http://localhost:5000` (development)
**Framework:** Flask with CORS enabled

---

## Table of Contents

1. [Authentication](#authentication)
2. [Response Format](#response-format)
3. [Error Handling](#error-handling)
4. [Endpoints](#endpoints)
   - [Dashboard & Visualization](#dashboard--visualization)
   - [Teams Management](#teams-management)
   - [Students Management](#students-management)
   - [Faculty Management](#faculty-management)
   - [Projects](#projects)
   - [Analytics](#analytics)
   - [LMS Modules](#lms-modules)
5. [Rate Limiting](#rate-limiting)
6. [Examples](#examples)

---

## Authentication

**Current Status:** No authentication required (development)

**Future:** JWT-based authentication planned
```http
Authorization: Bearer <token>
```

---

## Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error description",
  "message": "Human-readable error message"
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET request |
| 201 | Created | Successful POST request |
| 400 | Bad Request | Invalid input data |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Server-side error |

### Common Errors

**Missing Required Fields:**
```json
{
  "success": false,
  "error": "Missing required field: name",
  "message": "Please provide all required fields"
}
```

**Resource Not Found:**
```json
{
  "success": false,
  "error": "Team not found",
  "message": "No team with ID: team-123"
}
```

---

## Endpoints

### Dashboard & Visualization

#### GET /dashboard
Serve the Program Health Dashboard (3D molecular visualization)

**Parameters:**
- `university` (query, optional): Filter by university

**Response:** HTML page

**Example:**
```http
GET /dashboard?university=cal_poly
```

---

#### GET /api/network-data
Get network data for 3D visualization (projects, teams, faculty, interfaces)

**Response:**
```json
{
  "projects": [
    {
      "id": "proves",
      "name": "PROVES",
      "type": "collaborative",
      "is_nucleus": true,
      "team_size": 6
    }
  ],
  "teams": [
    {
      "id": "proves_team1",
      "name": "PROVES Core Team",
      "project_id": "proves",
      "discipline": "Multidisciplinary",
      "size": 6
    }
  ],
  "faculty": [
    {
      "id": "fac1",
      "name": "Dr. Sarah Chen",
      "role": "Faculty Advisor - Engineering"
    }
  ],
  "interfaces": [
    {
      "from": "proves",
      "to": "contract",
      "energy_loss": 0.1,
      "type": "knowledge_transfer"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/network-data
```

---

### Teams Management

#### GET /api/teams
List all teams

**Parameters:**
- `university_id` (query, optional): Filter by university
- `project_id` (query, optional): Filter by project

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "team-001",
      "name": "PROVES Core Team",
      "university_id": "cal_poly",
      "project_id": "proves",
      "discipline": "Multidisciplinary",
      "description": "Core team working on PROVES satellite",
      "created_at": "2025-01-15T10:00:00Z"
    }
  ]
}
```

**Example:**
```bash
curl "http://localhost:5000/api/teams?university_id=cal_poly"
```

---

#### POST /api/teams
Create a new team

**Request Body:**
```json
{
  "name": "Avionics Team",
  "university_id": "cal_poly",
  "project_id": "cadence",
  "discipline": "Electrical Engineering",
  "description": "Team focused on avionics subsystem"
}
```

**Required Fields:**
- `name` (string)
- `project_id` (string)

**Optional Fields:**
- `university_id` (string)
- `discipline` (string)
- `description` (string)
- `meta` (object)

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "team-002",
    "name": "Avionics Team",
    "university_id": "cal_poly",
    "project_id": "cadence",
    "discipline": "Electrical Engineering",
    "description": "Team focused on avionics subsystem",
    "created_at": "2025-11-28T10:00:00Z"
  },
  "message": "Team created successfully"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/teams \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Avionics Team",
    "project_id": "cadence",
    "discipline": "Electrical Engineering"
  }'
```

---

#### GET /api/teams/:team_id
Get specific team details

**Path Parameters:**
- `team_id` (string, required): Team identifier

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "team-001",
    "name": "PROVES Core Team",
    "university_id": "cal_poly",
    "project_id": "proves",
    "discipline": "Multidisciplinary",
    "description": "Core team working on PROVES satellite",
    "created_at": "2025-01-15T10:00:00Z",
    "meta": {}
  }
}
```

**Example:**
```bash
curl http://localhost:5000/api/teams/team-001
```

---

#### PUT /api/teams/:team_id
Update team details

**Path Parameters:**
- `team_id` (string, required)

**Request Body:** (all fields optional)
```json
{
  "name": "PROVES Advanced Team",
  "discipline": "Aerospace Engineering",
  "description": "Updated description"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "team-001",
    "name": "PROVES Advanced Team",
    "discipline": "Aerospace Engineering",
    "description": "Updated description",
    "created_at": "2025-01-15T10:00:00Z"
  },
  "message": "Team updated successfully"
}
```

**Example:**
```bash
curl -X PUT http://localhost:5000/api/teams/team-001 \
  -H "Content-Type: application/json" \
  -d '{"name": "PROVES Advanced Team"}'
```

---

#### DELETE /api/teams/:team_id
Delete a team

**Path Parameters:**
- `team_id` (string, required)

**Response:**
```json
{
  "success": true,
  "message": "Team deleted successfully"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:5000/api/teams/team-001
```

---

### Students Management

#### GET /api/students
List all students

**Parameters:**
- `university_id` (query, optional): Filter by university
- `team_id` (query, optional): Filter by team

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "student-001",
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "university_id": "cal_poly",
      "team_id": "team-001",
      "year": "Junior",
      "major": "Aerospace Engineering",
      "created_at": "2025-01-15T10:00:00Z"
    }
  ]
}
```

---

#### POST /api/students
Create a new student

**Request Body:**
```json
{
  "name": "Bob Smith",
  "email": "bob@example.com",
  "university_id": "cal_poly",
  "team_id": "team-001",
  "year": "Sophomore",
  "major": "Computer Science"
}
```

**Required Fields:**
- `name` (string)
- `email` (string)

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "student-002",
    "name": "Bob Smith",
    "email": "bob@example.com",
    "university_id": "cal_poly",
    "team_id": "team-001",
    "year": "Sophomore",
    "major": "Computer Science",
    "created_at": "2025-11-28T10:00:00Z"
  },
  "message": "Student created successfully"
}
```

---

### LMS Modules

#### GET /api/lms/modules
Get all training modules

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "module_id": "mod-001",
      "title": "Avionics Team Onboarding",
      "slug": "avionics-team-onboarding",
      "description": "Complete onboarding for avionics hardware team",
      "category": "Hardware & Subsystems",
      "difficulty": "Intermediate",
      "estimated_minutes": 60,
      "target_audience": "Undergraduate",
      "status": "Published",
      "tags": ["avionics", "onboarding"]
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/lms/modules
```

---

#### GET /api/lms/modules/:module_id
Get specific module details

**Path Parameters:**
- `module_id` (string, required)

**Response:**
```json
{
  "success": true,
  "data": {
    "module_id": "mod-001",
    "title": "Avionics Team Onboarding",
    "slug": "avionics-team-onboarding",
    "description": "Complete onboarding for avionics hardware team",
    "category": "Hardware & Subsystems",
    "difficulty": "Intermediate",
    "estimated_minutes": 60,
    "target_audience": "Undergraduate",
    "status": "Published",
    "tags": ["avionics", "onboarding"],
    "learning_objectives": [
      "Identify key avionics subsystems",
      "Configure development environment",
      "Execute basic hardware tests"
    ],
    "sections": [
      {
        "title": "Introduction",
        "content": "...",
        "type": "reading"
      }
    ],
    "notion_page_id": "2b96b8ea-578a-8101-80f6-d78aea760980"
  }
}
```

---

#### POST /api/lms/modules/:module_id/progress
Track student progress on a module

**Path Parameters:**
- `module_id` (string, required)

**Request Body:**
```json
{
  "student_id": "student-001",
  "status": "in_progress",
  "completed_sections": ["intro", "setup"],
  "time_spent_minutes": 25,
  "score": null
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "module_id": "mod-001",
    "student_id": "student-001",
    "status": "in_progress",
    "progress_percentage": 40,
    "completed_sections": ["intro", "setup"],
    "time_spent_minutes": 25,
    "updated_at": "2025-11-28T10:30:00Z"
  },
  "message": "Progress updated successfully"
}
```

---

### Analytics

#### GET /analytics
Get analytics dashboard (HTML)

**Response:** HTML page with analytics visualizations

---

#### GET /api/analytics/summary
Get summary analytics

**Response:**
```json
{
  "success": true,
  "data": {
    "total_students": 150,
    "total_teams": 25,
    "total_faculty": 15,
    "total_projects": 8,
    "average_team_size": 6,
    "modules_completed": 342,
    "average_completion_rate": 0.78
  }
}
```

---

## Rate Limiting

**Current:** No rate limiting (development)

**Future:**
- 100 requests per minute per IP
- 1000 requests per hour per IP

**Headers:**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

---

## Examples

### Complete Workflow: Create Team → Add Students → Track Progress

**Step 1: Create Team**
```bash
curl -X POST http://localhost:5000/api/teams \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Power Systems Team",
    "project_id": "cadence",
    "discipline": "Electrical Engineering"
  }'

# Response: {"success": true, "data": {"id": "team-003", ...}}
```

**Step 2: Add Students**
```bash
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Charlie Davis",
    "email": "charlie@example.com",
    "team_id": "team-003"
  }'

# Response: {"success": true, "data": {"id": "student-003", ...}}
```

**Step 3: Track Module Progress**
```bash
curl -X POST http://localhost:5000/api/lms/modules/mod-001/progress \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "student-003",
    "status": "completed",
    "completed_sections": ["intro", "setup", "practice", "quiz"],
    "time_spent_minutes": 55,
    "score": 92
  }'

# Response: {"success": true, "data": {"progress_percentage": 100, ...}}
```

---

## Testing Endpoints

### Using cURL
```bash
# List all teams
curl http://localhost:5000/api/teams

# Create team
curl -X POST http://localhost:5000/api/teams \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Team", "project_id": "test"}'

# Update team
curl -X PUT http://localhost:5000/api/teams/team-001 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Team Name"}'
```

### Using Python
```python
import requests

# Get all modules
response = requests.get('http://localhost:5000/api/lms/modules')
modules = response.json()['data']

# Create team
team_data = {
    "name": "Software Team",
    "project_id": "cadence",
    "discipline": "Computer Science"
}
response = requests.post(
    'http://localhost:5000/api/teams',
    json=team_data
)
new_team = response.json()['data']
```

### Using JavaScript (fetch)
```javascript
// Get network data
fetch('http://localhost:5000/api/network-data')
  .then(res => res.json())
  .then(data => console.log(data));

// Create student
fetch('http://localhost:5000/api/students', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    name: 'Jane Doe',
    email: 'jane@example.com',
    team_id: 'team-001'
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## Deprecated Endpoints

_(None currently)_

---

## Changelog

### Version 1.0 (2025-11-28)
- Initial API documentation
- Teams CRUD endpoints
- Students management
- LMS module endpoints
- Analytics endpoints

---

**Last Updated:** 2025-11-28
**Maintained By:** Agent Beta
**Questions:** See [Developer Onboarding](DEVELOPER_ONBOARDING.md)
