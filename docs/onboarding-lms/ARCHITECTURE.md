# Student Onboarding Module System - Technical Design

## Project Overview

**Purpose:** Create an interactive learning management system (LMS) for student onboarding with comprehensive analytics tracking.

**Key Features:**
- Interactive, mobile-friendly learning modules
- Team lead content management
- Granular usage analytics (time tracking, pause points, navigation patterns)
- No quizzes/grades - self-paced learning and reference
- Data-driven module improvement

---

## System Architecture

```
┌─────────────────┐
│   Students      │ ← View/consume modules on phone or desktop
│   (Mobile/Web)  │ ← Track progress, revisit content
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  React Frontend │ ← Progressive Web App (PWA)
│  (Module View)  │ ← Responsive design
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask Backend  │ ← REST API
│  (Python)       │ ← Module CRUD
└────────┬────────┘ ← Analytics processing
         │
         ▼
┌─────────────────┐
│  PostgreSQL     │ ← Modules, progress, analytics
│  (Neon)        │ ← 32GB free tier
└─────────────────┘

┌─────────────────┐
│   Team Leads    │ ← Create/edit modules
│   (Web Admin)   │ ← View team analytics
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ React Admin UI  │ ← Module builder
│ (Dashboard)     │ ← Analytics dashboard
└────────┬────────┘
         │
         ▼
     (Same Backend)
```

---

## Database Schema

### New Tables

#### 1. modules
```sql
CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    module_id VARCHAR(100) UNIQUE NOT NULL,  -- 'lab-safety-101'
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),  -- 'Safety', 'Equipment', 'Software', etc.
    estimated_minutes INTEGER NOT NULL DEFAULT 10,

    -- Ownership
    created_by INTEGER REFERENCES faculty(id),  -- Team lead
    university_id INTEGER REFERENCES universities(id),

    -- Status
    status VARCHAR(50) DEFAULT 'draft',  -- draft/published/archived

    -- Organization
    prerequisites JSONB DEFAULT '[]',  -- ['module-id-1', 'module-id-2']
    related_modules JSONB DEFAULT '[]',
    tags JSONB DEFAULT '[]',  -- ['required', 'safety', 'lab']

    -- Metadata
    target_audience VARCHAR(100) DEFAULT 'incoming_students',
    revision INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP,

    -- Full-text search
    search_vector TSVECTOR
);

CREATE INDEX idx_modules_status ON modules(status);
CREATE INDEX idx_modules_category ON modules(category);
CREATE INDEX idx_modules_university ON modules(university_id);
CREATE INDEX idx_modules_tags ON modules USING GIN(tags);
CREATE INDEX idx_modules_search ON modules USING GIN(search_vector);
```

#### 2. module_sections
```sql
CREATE TABLE module_sections (
    id SERIAL PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id) ON DELETE CASCADE,
    section_id VARCHAR(100) NOT NULL,  -- 'intro', 'ppe', 'emergency'

    -- Organization
    order_num INTEGER NOT NULL,  -- Display order
    title VARCHAR(255) NOT NULL,

    -- Content
    content_type VARCHAR(50) NOT NULL,  -- 'text', 'video', 'checklist', etc.
    content TEXT,  -- Main text content (supports Markdown)
    content_data JSONB,  -- Additional data (images, videos, etc.)

    -- Time
    estimated_minutes INTEGER DEFAULT 5,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(module_id, section_id),
    UNIQUE(module_id, order_num)
);

CREATE INDEX idx_sections_module ON module_sections(module_id);
CREATE INDEX idx_sections_order ON module_sections(module_id, order_num);
```

#### 3. module_assignments
```sql
CREATE TABLE module_assignments (
    id SERIAL PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id),

    -- Assignment scope
    team_id INTEGER REFERENCES teams(id),  -- NULL = all students
    university_id INTEGER REFERENCES universities(id),  -- For university-wide

    -- Requirements
    priority VARCHAR(50) DEFAULT 'recommended',  -- 'required', 'recommended', 'optional'
    due_date TIMESTAMP,

    -- Context
    assigned_by INTEGER REFERENCES faculty(id),
    assignment_reason TEXT,  -- "Complete before first lab session"

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CHECK (team_id IS NOT NULL OR university_id IS NOT NULL)
);

CREATE INDEX idx_assignments_team ON module_assignments(team_id);
CREATE INDEX idx_assignments_university ON module_assignments(university_id);
CREATE INDEX idx_assignments_module ON module_assignments(module_id);
```

#### 4. module_progress
```sql
CREATE TABLE module_progress (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    module_id INTEGER REFERENCES modules(id) ON DELETE CASCADE,
    section_id INTEGER REFERENCES module_sections(id),  -- NULL = module-level

    -- Progress tracking
    status VARCHAR(50) DEFAULT 'not_started',  -- not_started/in_progress/completed
    completion_percentage INTEGER DEFAULT 0,  -- 0-100

    -- Time tracking
    started_at TIMESTAMP,
    last_accessed_at TIMESTAMP,
    completed_at TIMESTAMP,
    total_time_seconds INTEGER DEFAULT 0,

    -- Session tracking
    session_count INTEGER DEFAULT 0,  -- How many times they've visited

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(student_id, module_id, section_id)
);

CREATE INDEX idx_progress_student ON module_progress(student_id);
CREATE INDEX idx_progress_module ON module_progress(module_id);
CREATE INDEX idx_progress_status ON module_progress(status);
CREATE INDEX idx_progress_completion ON module_progress(completion_percentage);
```

#### 5. module_analytics_events
```sql
CREATE TABLE module_analytics_events (
    id SERIAL PRIMARY KEY,

    -- Who and what
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    module_id INTEGER REFERENCES modules(id) ON DELETE CASCADE,
    section_id INTEGER REFERENCES module_sections(id) ON DELETE CASCADE,

    -- Event tracking
    event_type VARCHAR(50) NOT NULL,  -- 'start', 'pause', 'resume', 'complete', 'scroll', 'click', 'revisit'
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Session tracking
    session_id VARCHAR(100),  -- Groups events in same session

    -- Duration (for pause events)
    duration_seconds INTEGER,  -- How long they were active before pause

    -- Position tracking
    scroll_position INTEGER,  -- % of section scrolled
    element_id VARCHAR(100),  -- Specific element interacted with

    -- Context
    metadata JSONB,  -- {device_type, browser, screen_size, etc.}

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_events_student ON module_analytics_events(student_id);
CREATE INDEX idx_events_module ON module_analytics_events(module_id);
CREATE INDEX idx_events_section ON module_analytics_events(section_id);
CREATE INDEX idx_events_type ON module_analytics_events(event_type);
CREATE INDEX idx_events_timestamp ON module_analytics_events(timestamp);
CREATE INDEX idx_events_session ON module_analytics_events(session_id);
```

#### 6. module_feedback (Optional - for future)
```sql
CREATE TABLE module_feedback (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    module_id INTEGER REFERENCES modules(id),

    -- Feedback
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    helpful BOOLEAN,
    comments TEXT,

    -- Issues reported
    reported_issues JSONB,  -- [{type: 'broken_link', section_id: 'xxx', description: '...'}]

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_feedback_module ON module_feedback(module_id);
CREATE INDEX idx_feedback_rating ON module_feedback(rating);
```

---

## REST API Endpoints

### Public Endpoints (Students)

#### GET /api/modules
Get list of available modules
```json
Query params:
  - category: Filter by category
  - tag: Filter by tag
  - status: published (default), draft (admin only)
  - assigned_to_me: true (show only assigned modules)

Response:
{
  "modules": [
    {
      "id": 1,
      "module_id": "lab-safety-101",
      "title": "Lab Safety Fundamentals",
      "category": "Safety",
      "estimated_minutes": 20,
      "sections_count": 5,
      "my_progress": {
        "status": "in_progress",
        "completion_percentage": 60,
        "last_accessed": "2025-01-23T10:30:00Z"
      },
      "is_assigned": true,
      "priority": "required",
      "due_date": "2025-02-01T00:00:00Z"
    }
  ]
}
```

#### GET /api/modules/:module_id
Get specific module with all sections
```json
Response:
{
  "id": 1,
  "module_id": "lab-safety-101",
  "title": "Lab Safety Fundamentals",
  "description": "Essential safety procedures...",
  "category": "Safety",
  "estimated_minutes": 20,
  "sections": [
    {
      "id": 1,
      "section_id": "intro",
      "order": 1,
      "title": "Introduction",
      "content_type": "text",
      "content": "Welcome to lab safety...",
      "estimated_minutes": 2,
      "my_progress": {
        "status": "completed",
        "completed_at": "2025-01-23T10:15:00Z"
      }
    },
    ...
  ],
  "prerequisites": [],
  "related_modules": ["equipment-training"],
  "my_overall_progress": {
    "status": "in_progress",
    "completion_percentage": 60,
    "started_at": "2025-01-23T10:00:00Z",
    "last_accessed_at": "2025-01-23T10:30:00Z",
    "total_time_seconds": 720,
    "session_count": 2
  }
}
```

#### POST /api/modules/:module_id/start
Start a module (creates initial progress record)
```json
Request: {}
Response:
{
  "status": "started",
  "session_id": "abc123",
  "started_at": "2025-01-23T10:00:00Z"
}
```

#### POST /api/modules/:module_id/sections/:section_id/events
Track analytics event
```json
Request:
{
  "event_type": "pause",  // start, pause, resume, complete, scroll
  "duration_seconds": 120,  // For pause events
  "scroll_position": 75,  // % scrolled
  "session_id": "abc123",
  "metadata": {
    "device_type": "mobile",
    "browser": "Safari",
    "screen_width": 390
  }
}

Response:
{
  "status": "recorded",
  "event_id": 12345
}
```

#### POST /api/modules/:module_id/sections/:section_id/complete
Mark section as complete
```json
Request:
{
  "time_spent_seconds": 180,
  "session_id": "abc123"
}

Response:
{
  "section_completed": true,
  "module_completion_percentage": 80,
  "next_section": {
    "section_id": "emergency",
    "title": "Emergency Procedures"
  }
}
```

#### POST /api/modules/:module_id/complete
Mark entire module as complete
```json
Request:
{
  "total_time_seconds": 1200,
  "session_id": "abc123"
}

Response:
{
  "module_completed": true,
  "completed_at": "2025-01-23T10:45:00Z",
  "next_recommended_module": {
    "module_id": "equipment-training",
    "title": "Equipment Training Basics"
  }
}
```

#### GET /api/students/:student_id/progress
Get student's overall progress across all modules
```json
Response:
{
  "total_modules": 10,
  "completed": 3,
  "in_progress": 2,
  "not_started": 5,
  "total_time_minutes": 180,
  "modules": [
    {
      "module_id": "lab-safety-101",
      "title": "Lab Safety Fundamentals",
      "status": "completed",
      "completion_percentage": 100,
      "completed_at": "2025-01-23T10:45:00Z",
      "time_spent_minutes": 20
    },
    ...
  ]
}
```

---

### Admin Endpoints (Team Leads)

#### POST /api/admin/modules
Create new module
```json
Request:
{
  "module_id": "lab-safety-101",
  "title": "Lab Safety Fundamentals",
  "description": "Essential safety procedures",
  "category": "Safety",
  "estimated_minutes": 20,
  "status": "draft",
  "tags": ["safety", "required", "lab"]
}

Response:
{
  "id": 1,
  "module_id": "lab-safety-101",
  "status": "draft",
  "created_at": "2025-01-23T09:00:00Z"
}
```

#### PUT /api/admin/modules/:id
Update module
```json
Request: (same as POST, any fields)
Response: (updated module)
```

#### POST /api/admin/modules/:id/sections
Add section to module
```json
Request:
{
  "section_id": "intro",
  "order": 1,
  "title": "Introduction",
  "content_type": "text",
  "content": "Welcome...",
  "estimated_minutes": 2
}

Response: (created section)
```

#### PUT /api/admin/modules/:module_id/sections/:section_id
Update section
```json
Request: (same as POST sections, any fields)
Response: (updated section)
```

#### DELETE /api/admin/modules/:module_id/sections/:section_id
Delete section
```json
Response: {"status": "deleted"}
```

#### POST /api/admin/modules/:id/publish
Publish module (makes available to students)
```json
Request: {}
Response:
{
  "status": "published",
  "published_at": "2025-01-23T12:00:00Z"
}
```

#### POST /api/admin/modules/:id/assign
Assign module to team(s)
```json
Request:
{
  "team_ids": [1, 2, 3],  // Or null for all teams
  "priority": "required",
  "due_date": "2025-02-01T00:00:00Z",
  "assignment_reason": "Complete before first lab session"
}

Response:
{
  "assignments_created": 3,
  "students_notified": 15
}
```

#### GET /api/admin/modules/:module_id/analytics
Get analytics for specific module
```json
Response:
{
  "module_id": "lab-safety-101",
  "total_students_assigned": 50,
  "total_started": 45,
  "total_completed": 30,
  "completion_rate": 60,
  "average_time_minutes": 22,
  "average_sessions": 1.5,

  "section_analytics": [
    {
      "section_id": "intro",
      "title": "Introduction",
      "completion_rate": 100,
      "average_time_seconds": 120,
      "pause_points": [
        {"position": "30%", "count": 5},
        {"position": "60%", "count": 8}
      ]
    },
    ...
  ],

  "dropout_points": [
    {"section_id": "ppe", "dropout_count": 10, "dropout_rate": 22},
    {"section_id": "emergency", "dropout_count": 5, "dropout_rate": 11}
  ],

  "time_distribution": {
    "0-10min": 5,
    "10-20min": 20,
    "20-30min": 15,
    "30+min": 5
  }
}
```

#### GET /api/admin/teams/:team_id/progress
Get progress for entire team
```json
Response:
{
  "team_id": 1,
  "team_name": "Bronco Satellite Team",
  "students": [
    {
      "student_id": 1,
      "name": "John Doe",
      "modules_assigned": 5,
      "modules_completed": 3,
      "modules_in_progress": 1,
      "total_time_minutes": 90,
      "last_activity": "2025-01-23T10:45:00Z"
    },
    ...
  ],
  "team_summary": {
    "average_completion_rate": 65,
    "average_time_per_module": 18,
    "modules_with_low_completion": ["advanced-soldering"]
  }
}
```

---

## Analytics Insights

### Metrics Tracked

#### Module-Level
- Total views
- Unique students
- Start rate (viewed vs started)
- Completion rate
- Average time to complete
- Average sessions per completion
- Dropout rate and points

#### Section-Level
- Completion rate
- Average time spent
- Pause points (where students stop)
- Scroll depth
- Revisit frequency

#### Student-Level
- Modules assigned
- Modules started
- Modules completed
- Total learning time
- Preferred learning times (time of day)
- Device preferences (mobile vs desktop)
- Engagement patterns

### Analytics Queries

#### Find "Pause Points" (Where Students Stop)
```sql
SELECT
    section_id,
    scroll_position,
    COUNT(*) as pause_count
FROM module_analytics_events
WHERE event_type = 'pause'
    AND module_id = :module_id
GROUP BY section_id, scroll_position
ORDER BY pause_count DESC
LIMIT 10;
```

#### Average Time Per Section
```sql
SELECT
    s.title,
    AVG(p.total_time_seconds) as avg_seconds
FROM module_progress p
JOIN module_sections s ON p.section_id = s.id
WHERE s.module_id = :module_id
    AND p.status = 'completed'
GROUP BY s.id, s.title
ORDER BY s.order_num;
```

#### Dropout Analysis
```sql
WITH section_starts AS (
    SELECT section_id, COUNT(DISTINCT student_id) as started
    FROM module_analytics_events
    WHERE module_id = :module_id AND event_type = 'start'
    GROUP BY section_id
),
section_completions AS (
    SELECT section_id, COUNT(DISTINCT student_id) as completed
    FROM module_progress
    WHERE module_id = :module_id AND status = 'completed'
    GROUP BY section_id
)
SELECT
    s.title,
    st.started,
    COALESCE(sc.completed, 0) as completed,
    st.started - COALESCE(sc.completed, 0) as dropped_off,
    ROUND((st.started - COALESCE(sc.completed, 0))::numeric / st.started * 100, 2) as dropout_rate
FROM module_sections s
JOIN section_starts st ON st.section_id = s.id
LEFT JOIN section_completions sc ON sc.section_id = s.id
ORDER BY dropout_rate DESC;
```

#### Revisit Patterns
```sql
SELECT
    student_id,
    module_id,
    COUNT(*) as revisit_count,
    ARRAY_AGG(DATE(timestamp) ORDER BY timestamp) as revisit_dates
FROM module_analytics_events
WHERE event_type = 'revisit'
GROUP BY student_id, module_id
HAVING COUNT(*) > 1
ORDER BY revisit_count DESC;
```

---

## Frontend Implementation

### React Component Structure

```
src/
├── components/
│   ├── modules/
│   │   ├── ModuleList.jsx          # List all available modules
│   │   ├── ModuleCard.jsx          # Single module card
│   │   ├── ModuleViewer.jsx        # Main module viewing interface
│   │   ├── SectionRenderer.jsx     # Renders different section types
│   │   ├── ProgressBar.jsx         # Visual progress indicator
│   │   └── NavigationControls.jsx  # Next/Previous/Complete buttons
│   │
│   ├── sections/
│   │   ├── TextSection.jsx         # Render text content
│   │   ├── VideoSection.jsx        # Render video
│   │   ├── ChecklistSection.jsx    # Interactive checklist
│   │   ├── SelfCheckSection.jsx    # Self-assessment questions
│   │   ├── LinksSection.jsx        # External resources
│   │   └── ImageSection.jsx        # Images with captions
│   │
│   ├── admin/
│   │   ├── ModuleBuilder.jsx       # Create/edit modules
│   │   ├── SectionEditor.jsx       # Edit individual sections
│   │   ├── ModuleAssignment.jsx    # Assign to teams
│   │   ├── AnalyticsDashboard.jsx  # View analytics
│   │   └── TeamProgress.jsx        # View team progress
│   │
│   └── common/
│       ├── Timer.jsx               # Invisible time tracker
│       ├── AnalyticsTracker.jsx    # Track user events
│       └── ScrollTracker.jsx       # Track scroll position
│
├── hooks/
│   ├── useModuleProgress.js        # Track module progress
│   ├── useAnalytics.js             # Send analytics events
│   └── useTimer.js                 # Track time spent
│
├── services/
│   ├── moduleService.js            # API calls for modules
│   ├── analyticsService.js         # API calls for analytics
│   └── progressService.js          # API calls for progress
│
└── pages/
    ├── ModulesPage.jsx             # Student: Browse modules
    ├── ModuleViewPage.jsx          # Student: View single module
    ├── MyProgressPage.jsx          # Student: See their progress
    ├── AdminModulesPage.jsx        # Admin: Manage modules
    └── AdminAnalyticsPage.jsx      # Admin: View analytics
```

### Key React Features

#### 1. Time Tracking (Invisible)
```jsx
// hooks/useTimer.js
export const useTimer = (moduleId, sectionId) => {
  const [startTime, setStartTime] = useState(Date.now());
  const [totalTime, setTotalTime] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setTotalTime(Date.now() - startTime);
    }, 1000);

    return () => clearInterval(interval);
  }, [startTime]);

  const pause = () => {
    // Send analytics event with duration
    analyticsService.trackEvent({
      event_type: 'pause',
      duration_seconds: Math.floor(totalTime / 1000)
    });
  };

  return { totalTime, pause };
};
```

#### 2. Scroll Tracking
```jsx
// components/common/ScrollTracker.jsx
export const ScrollTracker = ({ sectionId }) => {
  const [scrollPosition, setScrollPosition] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const position = Math.round(
        (window.scrollY / document.body.scrollHeight) * 100
      );
      setScrollPosition(position);

      // Debounced analytics update
      debouncedTrack(position);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const debouncedTrack = useCallback(
    debounce((position) => {
      analyticsService.trackEvent({
        event_type: 'scroll',
        scroll_position: position
      });
    }, 2000),
    []
  );

  return null; // Invisible component
};
```

#### 3. Progressive Web App (PWA)
```javascript
// serviceWorker.js
// Allow offline access to completed modules
```

---

## Mobile Optimization

### Responsive Design Breakpoints
```css
/* Mobile-first approach */
.module-content {
  font-size: 16px;
  line-height: 1.6;
  padding: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
  .module-content {
    font-size: 18px;
    padding: 2rem;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .module-content {
    max-width: 800px;
    margin: 0 auto;
  }
}
```

### Touch-Friendly UI
- Minimum tap target: 48x48px
- Swipe gestures for navigation
- Large, clear buttons
- No hover-only interactions

### Performance
- Lazy load images
- Compress videos
- Minimize bundle size
- Service worker caching

---

## Implementation Phases

### Phase 1: MVP (2 weeks)
- [ ] Database schema creation
- [ ] Basic API endpoints (CRUD modules)
- [ ] Simple React module viewer
- [ ] Basic progress tracking (start/complete)
- [ ] Team lead can create modules via JSON

### Phase 2: Analytics (2 weeks)
- [ ] Time tracking implementation
- [ ] Event tracking (pause/resume)
- [ ] Scroll position tracking
- [ ] Basic analytics dashboard
- [ ] Progress reporting

### Phase 3: Rich Content (2 weeks)
- [ ] Video section support
- [ ] Image galleries
- [ ] Interactive checklists
- [ ] Self-check questions
- [ ] Rich text editor for team leads

### Phase 4: Advanced Features (2 weeks)
- [ ] Module builder UI (drag-and-drop)
- [ ] Advanced analytics (heatmaps, funnels)
- [ ] Mobile PWA optimization
- [ ] Push notifications (module assignments)
- [ ] Offline mode

### Phase 5: Refinement (Ongoing)
- [ ] A/B testing different module formats
- [ ] Machine learning insights
- [ ] Personalized recommendations
- [ ] Gamification (optional)

---

## Next Steps

1. **Database Setup:** Use Neon PostgreSQL (see NEON_DATABASE_SETUP.md)
2. **Create Migration:** Add these tables to your database
3. **API Development:** Implement endpoints in Flask
4. **Frontend:** Start with simple React module viewer
5. **Test:** Create first module (Lab Safety) and test with real students
6. **Iterate:** Use analytics to improve modules

---

## Example Module Flow

### Student Experience

1. **Browse Modules** (ModulesPage)
   - See assigned modules highlighted
   - Filter by category
   - See progress on each

2. **Start Module** (ModuleViewPage)
   - Click "Start Module"
   - Timer begins invisibly
   - First section loads

3. **Progress Through Sections**
   - Read content
   - Watch videos
   - Complete checklists
   - System tracks:
     - Time per section
     - Scroll depth
     - Pause points
     - Clicks/interactions

4. **Complete Module**
   - Final section complete button
   - Congratulations message
   - Suggested next module

5. **Revisit Later**
   - Can return anytime
   - Progress saved
   - Marked as "revisit" in analytics

### Team Lead Experience

1. **Create Module** (AdminModulesPage)
   - Click "New Module"
   - Fill in basic info
   - Save as draft

2. **Add Sections** (ModuleBuilder)
   - Add sections one by one
   - Choose content type
   - Upload images/videos
   - Preview

3. **Publish Module**
   - Review final preview
   - Click "Publish"
   - Module now visible to students

4. **Assign to Team**
   - Select module
   - Choose team(s)
   - Set priority and due date
   - Students get notification

5. **Monitor Progress** (AnalyticsDashboard)
   - See completion rates
   - Identify struggling students
   - Find problematic sections
   - Iterate and improve

---

## Data Privacy & Security

### Student Data Protection
- Analytics are aggregated for reporting
- Individual data only visible to:
  - Student themselves
  - Their team lead
  - Admin
- No selling or sharing of data
- Compliant with FERPA (education records)

### Security Measures
- HTTPS only (SSL/TLS)
- Secure authentication
- Role-based access control
- API rate limiting
- SQL injection prevention (parameterized queries)
- XSS protection

---

## Success Metrics

### For Students
- Module completion rate > 80%
- Average time close to estimated time
- Low dropout rates
- High revisit rates (good - means it's useful reference)

### For Team Leads
- Easy module creation (< 30 min per module)
- Actionable analytics
- Clear student progress visibility

### For Project
- Improved student preparedness
- Reduced onboarding time
- Data-driven training improvements
- Scalable across all universities

---

*Last updated: 2025-01-23*
