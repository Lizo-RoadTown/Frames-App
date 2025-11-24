# FRAMES Student Onboarding LMS

AI-powered student onboarding and learning management system for the FRAMES multi-university research collaboration.

## Status: 🚧 In Development

**Priority:** HIGH - Must be ready before next cohort arrives
**Timeline:** 10 weeks to launch

## Overview

This LMS will provide:
- AI-powered training module generation (10-20 modules)
- Mobile-first Progressive Web App (PWA)
- Team lead content workflow (no Git/coding required)
- Comprehensive module analytics
- Embedded AI assistant for post-launch updates

## Development Phases

### Phase 1: AI-Powered Bulk Generation (Weeks 1-6)
- Admin (Dr. Osborn) + AI generate 10-20 training modules from existing documentation
- Modules cover: lab safety, equipment training, software setup, team processes
- Content sourced from presentations, docs, emails

### Phase 2: AI Assistant for Team Leads (Weeks 7-10)
- Embedded AI assistant in admin dashboard
- Team leads can update/modify modules via conversation
- No Git or coding knowledge required

## Planned Features

### For Students
- Mobile-friendly module interface
- Progress tracking
- Completion certificates
- Pause/resume capability
- Offline support (PWA)

### For Team Leads
- AI-assisted content creation
- Form-based module submission
- Conversational AI for updates
- Analytics dashboard

### For Administrators
- Bulk module generation via AI
- Module assignment management
- Completion tracking
- Usage analytics (time, pauses, navigation patterns)

## Tech Stack (Planned)

- **Backend:** Flask, SQLAlchemy, PostgreSQL
- **Frontend:** React (Progressive Web App)
- **AI Integration:** Claude API for module generation and assistant
- **Database:** Neon PostgreSQL (shared with other FRAMES apps)
- **Mobile:** PWA with service workers

## Database Schema (Planned)

New tables to be added:
- `modules` - Training module metadata
- `module_sections` - Content sections within modules
- `module_assignments` - Student-module assignments
- `module_progress` - Student progress tracking
- `module_analytics_events` - Detailed usage analytics
- `module_feedback` - Student feedback

## Team Lead Workflow

Team leads will have 3 options:

### Option 1: AI-Assisted (Recommended)
1. Team lead uses ChatGPT/Claude with their training materials
2. AI structures content into module format
3. Team lead sends JSON to admin
4. Admin imports into system

### Option 2: Form Submission
1. Team lead fills out web form with content
2. Includes: title, learning objectives, content sections, assessments
3. System processes and creates module

### Option 3: Interview/Call
1. Admin interviews team lead about their training content
2. Admin takes notes and builds module
3. Team lead reviews and approves

**Post-Launch:** Team leads use embedded AI assistant to modify modules conversationally (no technical skills needed)

## Getting Started (When Built)

```bash
cd apps/onboarding-lms
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python backend/app.py
```

## Current Status

- [ ] Project structure setup
- [ ] Database schema design
- [ ] Backend API development
- [ ] React frontend development
- [ ] AI module generation system
- [ ] PWA implementation
- [ ] Analytics tracking
- [ ] Team lead workflow tools
- [ ] AI assistant integration
- [ ] Testing and deployment

## Documentation

Planning documents available in:
- `../../docs/onboarding-lms/AI_POWERED_MODULES.md`
- `../../docs/onboarding-lms/ARCHITECTURE.md`
- `../../docs/onboarding-lms/TEAM_LEAD_WORKFLOW.md`

## Roadmap

See `../../docs/shared/PROJECT_ROADMAP.md` for detailed 10-week timeline.

## Contact

Elizabeth Osborn, Ph.D. - eosborn@cpp.edu
California State Polytechnic University, Pomona
