# FRAMES Project Roadmap 2025

## Executive Summary

**Major Pivot:** Shifting primary focus from research analytics dashboard to student onboarding and learning management system (LMS), while maintaining existing research functionality.

**New Primary Goal:** Create interactive, mobile-friendly onboarding modules for incoming students with comprehensive usage analytics to improve training effectiveness.

**Timeline:** 8-10 weeks to MVP, ongoing iterations based on student feedback

---

## Current State (January 2025)

### What We Have ✅
- Multi-university research platform (Flask backend)
- 16 HTML template pages
- Team/student/faculty management systems
- Knowledge transfer tracking (interfaces)
- Analytics and NDA diagnostics
- PostgreSQL migration infrastructure ready
- Database running on local SQLite

### What's Changing 🔄
- **Database:** Moving from local SQLite to Neon PostgreSQL (free tier)
- **Frontend:** Transitioning from vanilla JS to React
- **Primary Feature:** Adding student onboarding module system
- **Documentation:** Complete cleanup and reorganization
- **Collaboration:** Opening up to team leads for module creation

---

## Phase 1: Foundation Setup (Week 1-2)

### Database Migration to Neon
**Priority:** CRITICAL - Must complete first

**Tasks:**
- [ ] Create Neon project + primary branch
  - Use the Neon free tier (1 project, up to 3 branches)
  - Start with the default compute size; upgrade only if needed
  - Setup guide: [NEON_DATABASE_SETUP.md](NEON_DATABASE_SETUP.md)

- [ ] Configure connection
  - Update `.env` with the Neon connection string
  - Test connection from local machine
  - Configure firewall rules

- [ ] Migrate existing data
  - Run `python backend/migrate_to_postgres.py`
  - Verify all tables created
  - Test all existing functionality

**Deliverables:**
- â Database running on Neon
- ✅ All team members can connect
- ✅ Existing features still work
- ✅ Backup strategy documented

**Estimated Time:** 2-3 days

---

### GitHub Collaboration Setup
**Priority:** HIGH - Needed for team leads

**Tasks:**
- [ ] Add team leads as collaborators
  - Send GitHub invitations
  - Create onboarding checklist

- [ ] Set up branch protection
  - Require pull requests for main
  - Require 1 approval for merges

- [ ] Create issue templates
  - Module creation template
  - Bug report template
  - Feature request template

- [ ] Documentation
  - Team leads read [GITHUB_COLLABORATION_GUIDE.md](GITHUB_COLLABORATION_GUIDE.md)
  - Practice workflow with test branch

**Deliverables:**
- ✅ Team leads have access
- ✅ Branch protection enabled
- ✅ Issue templates created
- ✅ First test PR completed

**Estimated Time:** 2-3 days

---

## Phase 2: Database Schema for Modules (Week 2)

### Create Module System Tables
**Priority:** HIGH - Foundation for new feature

**Tasks:**
- [ ] Create migration script
  - `backend/migrations/add_module_system.sql`
  - Include all tables from [STUDENT_ONBOARDING_SYSTEM_DESIGN.md](STUDENT_ONBOARDING_SYSTEM_DESIGN.md)

- [ ] Create SQLAlchemy models
  - `backend/models/module.py`
  - `backend/models/module_section.py`
  - `backend/models/module_progress.py`
  - `backend/models/module_analytics.py`

- [ ] Run migration
  - Apply to Neon database
  - Verify all tables created
  - Test foreign key constraints

**Tables to Create:**
1. `modules` - Core module metadata
2. `module_sections` - Individual sections within modules
3. `module_assignments` - Assign modules to teams/students
4. `module_progress` - Track student progress
5. `module_analytics_events` - Granular usage tracking
6. `module_feedback` - Student feedback (optional)

**Deliverables:**
- â All tables created in Neon database
- ✅ SQLAlchemy models working
- ✅ Can CRUD modules via Python

**Estimated Time:** 3-4 days

---

## Phase 3: Backend API Development (Week 3-4)

### Student-Facing Endpoints
**Priority:** HIGH - Core functionality

**Tasks:**
- [ ] Module browsing
  - `GET /api/modules` - List all modules
  - `GET /api/modules/:id` - Get specific module
  - Filter by category, tags, assigned status

- [ ] Progress tracking
  - `POST /api/modules/:id/start` - Start module
  - `POST /api/modules/:id/sections/:sid/complete` - Complete section
  - `POST /api/modules/:id/complete` - Complete module
  - `GET /api/students/:id/progress` - Get student progress

- [ ] Analytics tracking
  - `POST /api/modules/:id/sections/:sid/events` - Track events
  - Support: start, pause, resume, scroll, click
  - Include session tracking

**Deliverables:**
- ✅ All student endpoints working
- ✅ Postman collection for testing
- ✅ API documentation updated

**Estimated Time:** 4-5 days

---

### Admin/Team Lead Endpoints
**Priority:** HIGH - Team lead needs

**Tasks:**
- [ ] Module management
  - `POST /api/admin/modules` - Create module
  - `PUT /api/admin/modules/:id` - Update module
  - `DELETE /api/admin/modules/:id` - Delete module
  - `POST /api/admin/modules/:id/publish` - Publish module

- [ ] Section management
  - `POST /api/admin/modules/:id/sections` - Add section
  - `PUT /api/admin/modules/:id/sections/:sid` - Update section
  - `DELETE /api/admin/modules/:id/sections/:sid` - Delete section

- [ ] Assignment management
  - `POST /api/admin/modules/:id/assign` - Assign to teams
  - `GET /api/admin/teams/:id/progress` - View team progress

- [ ] Analytics access
  - `GET /api/admin/modules/:id/analytics` - Module analytics
  - `GET /api/admin/analytics/overview` - System-wide analytics

**Deliverables:**
- ✅ All admin endpoints working
- ✅ Permission checks implemented
- ✅ API documentation complete

**Estimated Time:** 4-5 days

---

## Phase 4: React Frontend - MVP (Week 5-6)

### Student Module Viewer
**Priority:** CRITICAL - Core user experience

**Tasks:**
- [ ] Setup React app
  - Create React App or Vite
  - Configure routing (React Router)
  - Setup state management (Context API or Redux)

- [ ] Module browsing
  - ModuleList component
  - ModuleCard component
  - Filter/search functionality

- [ ] Module viewer
  - ModuleViewer component
  - SectionRenderer component
  - Support content types:
    - Text (with Markdown)
    - Images
    - Basic checklists

- [ ] Progress tracking
  - Progress bar component
  - Navigation controls (next/prev)
  - Complete button

- [ ] Analytics tracking (invisible)
  - Time tracking hook
  - Scroll tracking component
  - Event sender service

**Deliverables:**
- ✅ Students can browse modules
- ✅ Students can view module content
- ✅ Progress is tracked automatically
- ✅ Mobile-responsive design

**Estimated Time:** 6-7 days

---

### Admin Module Builder
**Priority:** HIGH - Team lead workflow

**Tasks:**
- [ ] Module creation form
  - Basic module info
  - Category, tags, estimated time
  - Draft/publish workflow

- [ ] Section builder
  - Add sections interface
  - Simple text editor (Markdown)
  - Image upload
  - Section reordering

- [ ] Module preview
  - Preview as student would see
  - Test navigation

- [ ] Publishing
  - Publish button
  - Confirmation dialog

**Deliverables:**
- ✅ Team leads can create modules
- ✅ Team leads can preview modules
- ✅ Team leads can publish modules

**Estimated Time:** 5-6 days

---

## Phase 5: Analytics Dashboard (Week 7)

### Team Lead Analytics View
**Priority:** MEDIUM - Important for iteration

**Tasks:**
- [ ] Module analytics page
  - Completion rates
  - Average time spent
  - Dropout analysis
  - Section-by-section breakdown

- [ ] Team progress page
  - Student-by-student progress
  - Overall team metrics
  - Identify struggling students

- [ ] Visualizations
  - Charts (Chart.js or Recharts)
  - Progress bars
  - Heatmaps for pause points (optional)

**Deliverables:**
- ✅ Team leads can see module effectiveness
- ✅ Team leads can see student progress
- ✅ Data presented clearly

**Estimated Time:** 4-5 days

---

## Phase 6: Content Creation & Testing (Week 8)

### First Module Development
**Priority:** HIGH - Validate system with real content

**Tasks:**
- [ ] Identify first module topics
  - Lab Safety Fundamentals (priority 1)
  - Equipment Introduction (priority 2)
  - Software Setup (priority 3)

- [ ] Gather content
  - Collect existing training materials
  - Interview subject matter experts
  - Take photos/videos of equipment

- [ ] Create modules
  - Team leads build modules using system
  - Review and iterate
  - Get feedback from other leads

- [ ] Test with students
  - Pilot with small group (5-10 students)
  - Gather feedback
  - Monitor analytics

**Deliverables:**
- ✅ 3 modules published
- ✅ Tested with real students
- ✅ Feedback collected
- ✅ Analytics data flowing

**Estimated Time:** 5-7 days (ongoing)

---

## Phase 7: Refinement & Enhancement (Week 9-10)

### Based on Student Feedback
**Priority:** MEDIUM - Iterate based on data

**Tasks:**
- [ ] Analyze analytics
  - Where do students struggle?
  - Which sections need improvement?
  - Are time estimates accurate?

- [ ] Improve modules
  - Rewrite confusing sections
  - Add more visuals
  - Break up long sections

- [ ] Enhance features
  - Add video support
  - Better mobile experience
  - Offline capability (PWA)

**Deliverables:**
- ✅ Improved module completion rates
- ✅ Better user experience
- ✅ More accurate time estimates

**Estimated Time:** Ongoing

---

## Ongoing: Documentation Cleanup

### Parallel to Development
**Priority:** MEDIUM - Important for new contributors

**Tasks:**
- [ ] Create documentation branch
  - `git checkout -b cleanup/documentation`

- [ ] Audit all .md files
  - Identify actual documentation vs brainstorming
  - Categorize by relevance

- [ ] Rewrite README.md
  - Clear project description
  - Current working features only
  - Quick start guide
  - How to contribute

- [ ] Consolidate setup guides
  - One comprehensive SETUP.md
  - Move old guides to archive/

- [ ] Move brainstorming to NOTES.md
  - .gitignore NOTES.md
  - Keep for reference but not in repo

- [ ] Delete obsolete files
  - Old migration guides (already migrated)
  - Phase planning docs (phases complete)
  - Session summaries (historical only)

**Deliverables:**
- ✅ Clean, organized documentation
- ✅ New contributors can onboard easily
- ✅ README accurately reflects current state

**Estimated Time:** 3-4 days (can be done alongside development)

---

## Future Enhancements (Post-MVP)

### Advanced Module Features
- Rich text editor (WYSIWYG)
- Drag-and-drop module builder
- Interactive simulations
- Embedded quizzes (optional, for practice)
- Branching paths (different content based on role)

### Enhanced Analytics
- Machine learning insights
- Predictive analytics (identify at-risk students)
- A/B testing different module formats
- Personalized recommendations

### Mobile App
- Native iOS/Android apps
- Push notifications for assignments
- Offline-first architecture
- Camera integration (scan QR codes for equipment modules)

### Integration
- Calendar integration (sync deadlines)
- Slack/Discord notifications
- Email digests (weekly progress reports)
- Badge/achievement system (optional gamification)

### Multi-Language Support
- Spanish translations
- Accessibility improvements (screen readers)
- Internationalization (i18n)

---

## Success Metrics

### Technical Metrics
- [ ] 99% uptime for database
- [ ] < 2s page load time
- [ ] < 100ms API response time
- [ ] Zero data loss

### Student Metrics
- [ ] > 80% module completion rate
- [ ] > 90% student satisfaction
- [ ] Average time within 20% of estimate
- [ ] > 50% revisit rate (shows it's useful reference)

### Team Lead Metrics
- [ ] < 30 minutes to create new module
- [ ] > 90% team lead satisfaction with tools
- [ ] Analytics viewed weekly
- [ ] Modules updated based on data

### Project Metrics
- [ ] Reduced onboarding time by 30%
- [ ] Improved student preparedness (measured by faculty)
- [ ] Scalable to all 8 universities
- [ ] 20+ modules created in first semester

---

## Resource Requirements

### People
- **Project Lead:** You (overall direction, admin work)
- **Team Leads:** 3-5 (content creation, testing)
- **Developer:** You + Claude Code (implementation)
- **Students:** 10-20 (pilot testing)

### Budget
- **Database:** $0/month (Neon free tier)
- **Hosting:** ~$0/month (Render or Cloud Run free tier for MVP)
- **Domain:** $12/year (optional, frames.edu or similar)
- **Total:** ~$0-15/year for MVP

### Time Commitment
- **Development:** 8-10 weeks to MVP (part-time)
- **Content Creation:** Ongoing (2-3 hours/week per team lead)
- **Maintenance:** 2-5 hours/week after launch

---

## Risk Management

### Technical Risks
**Risk:** Database costs exceed free tier
**Mitigation:** Monitor usage, optimize queries, upgrade if needed (~$10/month)

**Risk:** React learning curve for team leads
**Mitigation:** Start with JSON-based module creation, add UI builder later

**Risk:** Mobile performance issues
**Mitigation:** Test early and often on real devices, optimize assets

### Organizational Risks
**Risk:** Team leads too busy to create content
**Mitigation:** Start with converting existing materials, make tools very easy to use

**Risk:** Students don't use modules
**Mitigation:** Make required for team participation, assign due dates, make genuinely useful

**Risk:** Analytics overwhelming/confusing
**Mitigation:** Start simple, add complexity gradually, focus on actionable insights

### Data Risks
**Risk:** Student privacy concerns
**Mitigation:** Anonymize data in aggregate reports, comply with FERPA, clear privacy policy

**Risk:** Database failure/data loss
**Mitigation:** Neon point-in-time restore (7 days), export critical data weekly

---

## Decision Log

### January 23, 2025

**Decision:** Use Neon Database for PostgreSQL
**Rationale:** Free tier, branching workflow, easy SSL connections

**Decision:** React for frontend (replacing vanilla JS)
**Rationale:** Better component architecture, easier mobile optimization, modern tooling

**Decision:** GitHub collaboration via pull requests
**Rationale:** Code review ensures quality, teaches best practices, protects main branch

**Decision:** Module system takes priority over research dashboard
**Rationale:** Immediate student need, more impactful for day-to-day operations

**Decision:** No quizzes/grades in modules
**Rationale:** Focus on learning not testing, reduce student stress, analytics provide insights

---

## Communication Plan

### Weekly Updates
- **Who:** Project lead → Team leads
- **Format:** Email or Slack message
- **Content:** Progress this week, what's next, blockers

### Bi-Weekly Demos
- **Who:** Development team → Stakeholders
- **Format:** Live demo or video
- **Content:** New features, request feedback

### Monthly Metrics Review
- **Who:** Project lead → All participants
- **Format:** Dashboard + brief report
- **Content:** Usage stats, completion rates, improvements made

---

## Next Actions (This Week)

### You (Project Lead)
1. ✅ Review all documentation created today:
   - NEON_DATABASE_SETUP.md
   - GITHUB_COLLABORATION_GUIDE.md
   - STUDENT_ONBOARDING_SYSTEM_DESIGN.md
   - PROJECT_ROADMAP_2025.md

2. [ ] Set up Neon Database
   - Follow NEON_DATABASE_SETUP.md step-by-step
   - Save connection string securely
   - Test connection

3. [ ] Identify team leads
   - Who will create modules?
   - Get their GitHub usernames
   - Send invitations

4. [ ] Gather first module content
   - What's the most urgent training need?
   - Collect existing materials
   - Outline 3 priority modules

### Development (You + Claude Code)
1. [ ] Create database migration script
   - Add module system tables
   - Test locally first

2. [ ] Update SQLAlchemy models
   - Create model files
   - Test CRUD operations

3. [ ] Begin API development
   - Start with student endpoints
   - Test thoroughly

### Team Leads (Once Onboarded)
1. [ ] Complete GitHub onboarding
   - Read GITHUB_COLLABORATION_GUIDE.md
   - Practice with test branch
   - Create first test PR

2. [ ] Review module template
   - Understand JSON structure
   - Plan first module outline
   - Gather content (text, images)

---

## Questions to Answer This Week

### Database
- [x] Cloud provider? â **Neon (purpose-built Postgres)**
- [ ] What's the actual connection string? → (copy from the Neon dashboard)
- [ ] Can team leads connect remotely? → (add their IPs to firewall)

### GitHub
- [ ] Who are the team leads? → (get names/GitHub usernames)
- [ ] Public or private repo? → (currently public, keep or change?)
- [ ] Need GitHub Organization? → (optional, can add later)

### Content
- [ ] What's the first module topic? → (lab safety? equipment? software?)
- [ ] Who's the subject matter expert? → (who has the knowledge?)
- [ ] Do we have existing materials to convert? → (videos, PDFs, presentations?)

### Timeline
- [ ] When do students need first module? → (sets urgency)
- [ ] How much time can team leads commit? → (affects how fast we create content)
- [ ] Any immovable deadlines? → (academic calendar constraints?)

---

## Appendix: File Structure (Proposed)

```
FRAMES Python/
├── backend/
│   ├── app.py                          # Main Flask app
│   ├── db_models.py                    # SQLAlchemy models (existing)
│   ├── models/                         # NEW: Organized models
│   │   ├── module.py
│   │   ├── module_section.py
│   │   ├── module_progress.py
│   │   └── module_analytics.py
│   ├── routes/                         # NEW: API routes organized
│   │   ├── modules.py                  # Student endpoints
│   │   ├── admin_modules.py            # Admin endpoints
│   │   ├── analytics.py                # Analytics endpoints
│   │   └── progress.py                 # Progress endpoints
│   ├── migrations/                     # Database migrations
│   │   └── add_module_system.sql
│   └── instance/
│       └── frames.db                   # Local SQLite (deprecated, hosted DB is source of truth)
│
├── frontend/                            # Existing vanilla JS (keep for now)
│   ├── templates/
│   └── static/
│
├── react-frontend/                      # NEW: React app
│   ├── src/
│   │   ├── components/
│   │   │   ├── modules/
│   │   │   ├── sections/
│   │   │   ├── admin/
│   │   │   └── common/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── pages/
│   │   └── App.jsx
│   ├── public/
│   └── package.json
│
├── docs/                                # CLEANED UP: Essential docs only
│   ├── SYSTEM_ARCHITECTURE.md          # Consolidated
│   ├── API_DOCUMENTATION.md
│   └── SETUP.md                        # Consolidated setup guide
│
├── archive/                             # NEW: Old docs moved here
│   ├── PHASE1_*.md
│   ├── SESSION*.md
│   └── old_guides/
│
├── .env                                 # LOCAL: Your configuration (gitignored)
├── .env.example                         # UPDATED: Template with Neon
├── README.md                            # REWRITTEN: Current state only
├── CONTRIBUTING.md                      # NEW: How to contribute
├── NEON_DATABASE_SETUP.md              # NEW: Neon setup guide
├── GITHUB_COLLABORATION_GUIDE.md        # NEW: Team lead guide
├── STUDENT_ONBOARDING_SYSTEM_DESIGN.md  # NEW: Technical design
└── PROJECT_ROADMAP_2025.md              # NEW: This file
```

---

**Ready to begin?** Start with Neon database setup, then we'll tackle the database schema and API development.

---

*Last updated: 2025-01-23*
*Next review: 2025-01-30 (or after Phase 1 completion)*
