# FRAMES Complete System Architecture

**Date:** 2025-11-28
**Version:** 2.0
**Status:** Canonical Reference
**Purpose:** Complete system overview for developers and AI agents

---

## Table of Contents

1. [System Overview](#system-overview)
2. [The Problem We're Solving](#the-problem-were-solving)
3. [Who This System Is For](#who-this-system-is-for)
4. [Three-Layer Architecture](#three-layer-architecture)
5. [CADENCE Integration](#cadence-integration)
6. [Data Flow](#data-flow)
7. [Educational Framework](#educational-framework)
8. [Technology Stack](#technology-stack)
9. [Component Architecture](#component-architecture)
10. [Deployment & Operations](#deployment--operations)

---

## System Overview

### What FRAMES Is

FRAMES is an **Onboarding & Training Engine** for large, complex student projects (multi-year NASA-style missions). It transforms team leads' existing Notion documentation into interactive, structured training modules for new students.

**Key Principle:** We don't replace team leads' existing process. We read what they're already doing and turn it into self-service onboarding.

### Core Capabilities

- **Multi-University Collaboration:** 8 universities (Cal Poly Pomona, Texas State, Columbia, and 5 others)
- **Module Library:** 68+ interactive training modules
- **Automated Onboarding:** Students complete training in days, not weeks
- **Progress Tracking:** Real-time analytics and leaderboards
- **Content Synchronization:** Notion → GitHub → PostgreSQL → React app

---

## The Problem We're Solving

### Before FRAMES

- ❌ Isolated training content (PDFs, Word docs, tribal knowledge)
- ❌ New students take weeks to onboard
- ❌ No way to track who learned what
- ❌ Team leads manually answer same questions repeatedly
- ❌ No standardization across universities
- ❌ Knowledge lost when students graduate

### After FRAMES

- ✅ Centralized module library with 68+ modules
- ✅ Students complete interactive onboarding in days
- ✅ Automatic progress tracking and analytics
- ✅ Team leads create content once, everyone benefits
- ✅ Consistent training across 8 universities
- ✅ Institutional knowledge preserved

---

## Who This System Is For

### 1. New Students/Recruits (50-100 per year)

**What they need:**
- Quick onboarding to complex research projects
- Hands-on, "do this in the real environment" training
- Less intimidating than being thrown into deep end

**What they use:**
- React onboarding app with dark theme
- Interactive modules (solo, sometimes competitive)
- Leaderboards and progress tracking

**What they see:**
- Beautiful react-notion-x rendered pages
- Real tools and environments (not simulations)
- Race against old cohorts or AI classmates

**What they DON'T see:**
- Notion directly
- Raw databases
- Backend complexity

### 2. Team Leads/Project Leads (8-15 people)

**What they need:**
- Easy content creation (no coding)
- Continue using existing Notion workflow
- Bring new cohorts onboard without losing momentum

**What they use:**
- Notion workspace (CADENCE Hub) for project management
- Module Library database to tag source content
- Familiar Notion interface

**What they see:**
- Embedded onboarding section in their dashboards
- Module catalog and student progress
- Simple tagging system for content

**What they DON'T see:**
- React app internals
- PostgreSQL database
- Automation scripts

### 3. Faculty/Researchers (20-30 people)

**What they need:**
- Evidence that onboarding is working
- Student progress visibility
- System that survives across semesters

**What they use:**
- Analytics dashboards
- Weekly reports
- Module effectiveness metrics

**What they see:**
- Completion rates
- Leaderboards
- Cohort comparisons

**What they DON'T see:**
- Individual student data (privacy)
- Technical implementation details

### 4. Solo Developer (You - 1 person)

**What you need:**
- Manage entire platform alone
- Maximum automation
- Minimal manual intervention

**What you use:**
- Three-agent system (Alpha, Beta, Gamma)
- Automation scripts
- GitHub Actions (future)

**What you see:**
- Full stack: Notion, GitHub, PostgreSQL, React
- Automation logs
- System health metrics

**What you maintain:**
- Keep system running
- Deploy updates
- Monitor and fix issues

---

## Three-Layer Architecture

FRAMES follows a **3-layer architecture** from the system overview specification:

### Layer 1: Authoring (Notion)

**Purpose:** Where humans work normally

**Components:**
- **CADENCE Hub:** Main dashboard/project management page
- **Module Library DB:** 68+ module catalog
- **Development Tasks DB:** Team work tracking
- **Technical Decisions DB:** Architecture decisions
- **Team Members DB:** People and roles
- **Projects DB:** Subsystem tracking
- **Documents DB:** Reference materials

**Key Principle:** Dashboards are read-only layouts. Only databases can be modified.

### Layer 2: Transformation (AI + Backend)

**Purpose:** Extract, normalize, structure

**Components:**
- **Postgres (Neon):** Canonical source of truth (5 tables)
- **Agent Alpha:** Database architect & module engineer
- **Agent Beta:** Notion sync & documentation
- **Agent Gamma:** Data import & cleanup
- **Sync Scripts:** Notion ↔ Postgres automation

**Key Principle:** Postgres is authoritative. Notion is presentation layer.

**Data Flow:**
```
Notion (authoring)
  → Extract/Normalize
    → Postgres (canonical)
      → Notion DBs (presentation)
        → Dashboards (views)
```

### Layer 3: Runtime (Student Experience)

**Purpose:** Where students consume modules

**Components:**
- **React App:** Main student interface
- **react-notion-x:** Renders Notion pages with dark theme
- **Module Player:** Runs steps, checks, quizzes
- **Progress Tracker:** Logs completion
- **Leaderboard:** Race/competition features

**Key Principle:** No live AI. Deterministic execution.

---

## CADENCE Integration

### What is CADENCE?

**CADENCE** is a multi-university CubeSat project (8 universities collaborating on satellite development). It's a perfect use case for FRAMES because:
- Large team (50+ students)
- Complex technical content (avionics, power, propulsion, software)
- Multi-year project (knowledge continuity critical)
- Real documentation already exists in Notion

### CADENCE Export

We have **1,417 Notion pages** exported from the CADENCE project:
- **Structural Docs:** CAD files, ICDs, mass budgets (120 files)
- **Technical Docs:** Datasheets, fabrication guides (200 files)
- **Workflow Docs:** SOPs, plans, meetings (350 files)
- **Program Docs:** Mission materials, proposals (600 files)
- **Miscellaneous:** Personal notes - excluded (147 files)

### CADENCE → Training Modules

From 1,417 files, we extract:
- **68 training modules** (core educational content)
- **280 tasks** (project todos and milestones)
- **180 meetings** (notes and action items)
- **765 documents** (reference materials)
- **30 people** (team members)
- **15 projects** (subsystem tracking)

**Total:** 1,270 structured records (147 excluded per spec)

---

## Data Flow

### Complete End-to-End Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   PHASE 1: CONTENT CREATION                 │
│                                                              │
│  Team Lead creates content in Notion:                       │
│  • Writes procedure doc                                     │
│  • Tags as "Module Source"                                  │
│  • Publishes in Module Library DB                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    Agent Alpha/Gamma
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   PHASE 2: EXTRACTION                        │
│                                                              │
│  Agents extract and normalize:                              │
│  • Read Notion pages via API                                │
│  • Parse markdown and metadata                              │
│  • Map to canonical schema                                  │
│  • Validate against specs                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    Import Scripts
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              PHASE 3: CANONICAL STORAGE (Postgres)          │
│                                                              │
│  5 Canonical Tables (per CADENCE spec):                     │
│  • people (30 records)                                      │
│  • projects (15 records)                                    │
│  • tasks (280 records)                                      │
│  • meetings (180 records)                                   │
│  • documents (765 records)                                  │
│                                                              │
│  Postgres = Single Source of Truth                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    Sync Scripts (Agent Beta)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│            PHASE 4: PRESENTATION (Notion Databases)         │
│                                                              │
│  5 Notion Databases (synced from Postgres):                 │
│  • Team Members DB (people table)                           │
│  • Projects DB (projects table)                             │
│  • Tasks DB (tasks table)                                   │
│  • Meetings DB (meetings table)                             │
│  • Documents DB (documents table)                           │
│                                                              │
│  CADENCE Dashboard shows linked views                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    GitHub Export
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              PHASE 5: VERSION CONTROL (GitHub)              │
│                                                              │
│  modules/exports/*.json (68 files):                         │
│  • Complete module data                                     │
│  • Notion recordMaps for rendering                          │
│  • Metadata (difficulty, tags, etc.)                        │
│                                                              │
│  GitHub = Approved Content Repository                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    React App Deployment
                            ↓
┌─────────────────────────────────────────────────────────────┐
│               PHASE 6: STUDENT RUNTIME (React)              │
│                                                              │
│  Student Experience:                                        │
│  • Browse module catalog                                    │
│  • Select module                                            │
│  • Complete steps in real environment                       │
│  • Pass checks and quizzes                                  │
│  • See progress and leaderboard                             │
│  • Race old cohorts or AI classmates                        │
│                                                              │
│  React app queries Postgres for module data                 │
│  Renders pages using react-notion-x                         │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Principles

1. **Notion → Postgres:** Extract and normalize via agents
2. **Postgres → Notion DBs:** Sync for dashboard presentation
3. **Postgres → GitHub:** Export approved content
4. **GitHub → React:** Deploy to student app
5. **React → Postgres:** Log student progress

**Key:** Postgres is canonical. Notion and GitHub are derivatives.

---

## Educational Framework

### OAtutor Integration

FRAMES uses the **OAtutor framework** for educational module structure:

**OAtutor Principles:**
- Learning by doing (hands-on)
- Real project context
- Progressive difficulty
- Immediate feedback
- Social learning (races, leaderboards)

### Module Anatomy

Every module has:

1. **Learning Objectives** (3-5 measurable goals)
   - "Understand X"
   - "Apply Y technique"
   - "Evaluate Z approach"

2. **Prerequisites** (what to know first)
   - Links to previous modules
   - Expected knowledge level

3. **Content Sections**
   - **Reading:** Theory and context
   - **Practice:** Hands-on steps with checks
   - **Quiz:** Knowledge verification
   - **Reflection:** "What did you learn?"

4. **Metadata**
   - Category (Hardware, Software, Mission Ops)
   - Difficulty (Beginner, Intermediate, Advanced)
   - Estimated time
   - Target audience

5. **Race Features** (optional)
   - Time targets (beginner: 90min, advanced: 45min)
   - Ghost data (race past students)
   - AI classmates (scripted competitors)

### Module Types

1. **Solo Core Modules:** Individual learning
2. **Challenge/Race Modules:** Timed with competition
3. **Collaborative Modules:** Team exercises
4. **Mood-Lightening Modules:** Humor and engagement

### Student Progression

```
New Student
  → Foundation Modules (Beginner)
    → Practice Modules (Intermediate)
      → Challenge Modules (Advanced)
        → Collaborative Projects
          → Ready for Real Work
```

---

## Technology Stack

### Backend

- **Language:** Python 3.14
- **Framework:** Flask (REST API)
- **Database:** PostgreSQL (Neon hosted)
- **ORM:** SQLAlchemy
- **Migration:** Alembic (future)

### Frontend

- **Framework:** React 18
- **Rendering:** react-notion-x (Notion page renderer)
- **Theme:** Dark mode custom
- **Build:** Create React App (CRA)
- **Deployment:** Netlify/Vercel (future)

### Databases

**Postgres (Neon):**
- Canonical schema (5 CADENCE tables)
- Existing tables (teams, faculty, interfaces)
- Module progress tracking
- Leaderboard data

**Notion:**
- Team Members DB
- Projects DB
- Tasks DB
- Meetings DB
- Documents DB
- Module Library DB

### Integrations

- **Notion API:** v2022-06-28 (REST)
- **GitHub:** 2 repos (Frames-App, OAtutor)
- **OAtutor:** Educational framework reference

### Development Tools

- **Version Control:** Git + GitHub
- **Automation:** Python scripts (future: GitHub Actions)
- **AI Agents:** Claude (Alpha, Beta, Gamma)
- **Documentation:** Markdown

---

## Component Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                             │
│                                                              │
│  ┌──────────────┐       ┌──────────────┐                   │
│  │ Module       │       │ Progress     │                   │
│  │ Browser      │◄─────►│ Tracker      │                   │
│  └──────────────┘       └──────────────┘                   │
│         │                        │                          │
│         │                        │                          │
│  ┌──────▼────────────────────────▼──────┐                  │
│  │   react-notion-x Renderer            │                  │
│  │   (Dark theme, module player)        │                  │
│  └──────────────────────────────────────┘                  │
│                      │                                      │
└──────────────────────┼──────────────────────────────────────┘
                       │ HTTP/REST
┌──────────────────────▼──────────────────────────────────────┐
│                      BACKEND API                             │
│                                                              │
│  ┌────────────────┐    ┌────────────────┐                  │
│  │ Module         │    │ Progress       │                  │
│  │ Endpoints      │    │ Endpoints      │                  │
│  └────────┬───────┘    └────────┬───────┘                  │
│           │                     │                           │
│  ┌────────▼─────────────────────▼──────┐                   │
│  │     Flask Application               │                   │
│  │     (app.py)                        │                   │
│  └────────┬────────────────────────────┘                   │
│           │ SQLAlchemy ORM                                 │
└───────────┼────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│                  POSTGRESQL (Neon)                         │
│                                                            │
│  Canonical Tables:          Module Tables:                │
│  • people                   • module_progress             │
│  • projects                 • leaderboard                 │
│  • tasks                    • student_sessions            │
│  • meetings                                               │
│  • documents                                              │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                    NOTION WORKSPACE                        │
│                                                            │
│  Authoring:                 Presentation:                 │
│  • Module Library DB        • Team Members DB             │
│  • CADENCE Hub              • Projects DB                 │
│                             • Tasks DB                     │
│                             • Meetings DB                  │
│                             • Documents DB                 │
│                                                            │
│          ▲                           │                     │
│          │                           │                     │
│    Agents Edit               Agents Sync                  │
│          │                           ▼                     │
└──────────┼─────────────────────────────────────────────────┘
           │
┌──────────▼─────────────────────────────────────────────────┐
│                    AUTOMATION LAYER                        │
│                                                            │
│  • Agent Alpha: Module enhancement, DB architect          │
│  • Agent Beta: Notion sync, documentation                 │
│  • Agent Gamma: Data import, file cleanup                 │
│                                                            │
│  Scripts:                                                  │
│  • sync_postgres_to_notion.py                             │
│  • import_cadence_to_postgres.py                          │
│  • enhance_modules.py                                     │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                      GITHUB REPOS                          │
│                                                            │
│  Frames-App:                OAtutor:                      │
│  • Application code         • Module schema               │
│  • Module exports           • Educational patterns        │
│  • Documentation            • Framework reference         │
│  • Automation scripts                                     │
└────────────────────────────────────────────────────────────┘
```

### Key Components

**1. React Frontend**
- Location: `apps/onboarding-lms/frontend-react/`
- Entry: `src/App.js`
- Components: ModuleBrowser, ModulePlayer, ProgressTracker
- Styling: Dark theme, react-notion-x custom CSS

**2. Flask Backend**
- Location: `backend/app.py`
- Routes: `/modules`, `/progress`, `/leaderboard`
- Database: SQLAlchemy models in `shared/database/`
- Connection: Neon via DATABASE_URL

**3. Agent System**
- Location: `agent_coordination/`
- Alpha: Educational modules, database design
- Beta: Notion sync, documentation
- Gamma: Data import, file organization

**4. Module Storage**
- GitHub: `modules/exports/*.json` (68 files)
- Format: JSON with Notion recordMaps
- Schema: OAtutor-compatible structure

---

## Deployment & Operations

### Environment Setup

**Required Environment Variables (.env):**
```
DATABASE_URL=postgresql://user:pass@host:5432/frames
NOTION_TOKEN=ntn_xxxxxxxxxxxxx
NOTION_MODULE_DB_ID=eac1ce58-6169-4dc3-a821-29858ae59e76
```

### Local Development

1. **Clone Repository:**
   ```bash
   git clone https://github.com/Lizo-RoadTown/Frames-App.git
   cd Frames-App
   ```

2. **Backend Setup:**
   ```bash
   pip install -r requirements.txt
   python backend/app.py
   # Runs on http://localhost:5000
   ```

3. **Frontend Setup:**
   ```bash
   cd apps/onboarding-lms/frontend-react
   npm install
   npm start
   # Runs on http://localhost:3000
   ```

4. **Database Setup:**
   ```bash
   python shared/database/migrations/create_cadence_schema.py
   ```

### Automation Scripts

**Daily Sync (Manual trigger):**
```bash
python scripts/sync_postgres_to_notion.py
```

**Module Enhancement:**
```bash
python scripts/enhance_modules.py
```

**Data Import:**
```bash
python scripts/import_cadence_to_postgres.py
```

### Future: GitHub Actions

**Planned Workflows:**
- Daily Notion sync (cron: 0 0 * * *)
- Module validation on PR
- Automated deployment to Netlify
- Weekly analytics report

---

## Appendix

### Related Documentation

- [CADENCE Spec Compliance](CADENCE_SPEC_COMPLIANCE.md)
- [API Reference](API_REFERENCE.md)
- [Database Schema Reference](DATABASE_SCHEMA_REFERENCE.md)
- [Notion API Integration](NOTION_API_INTEGRATION.md)
- [Developer Onboarding](DEVELOPER_ONBOARDING.md)
- [Educational Framework](EDUCATIONAL_FRAMEWORK.md)
- [Module Schema](MODULE_SCHEMA.md)

### External References

- [Notion API Documentation](https://developers.notion.com/)
- [react-notion-x GitHub](https://github.com/NotionX/react-notion-x)
- [OAtutor Repository](https://github.com/Lizo-RoadTown/OATutor)
- [Neon PostgreSQL](https://neon.tech)

### Glossary

- **CADENCE:** Multi-university CubeSat project (source of training content)
- **Module:** Interactive training unit with objectives, steps, checks, quizzes
- **OAtutor:** Educational framework for structured learning modules
- **recordMap:** Notion's internal page structure for rendering
- **react-notion-x:** Library for rendering Notion pages in React
- **Agent:** Autonomous AI assistant (Alpha, Beta, Gamma)
- **Canonical:** Single source of truth (Postgres for data, GitHub for code)

---

**Last Updated:** 2025-11-28
**Maintained By:** Agent Beta
**Questions:** See Developer Onboarding guide or CADENCE specs
