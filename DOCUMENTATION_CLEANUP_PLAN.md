# Documentation Cleanup Plan

## Current State: 32 Markdown Files (Too Many!)

### Root Level: 32 files
### docs/ folder: 6 files
### **Total:** 38 documentation files

**Problem:** Overwhelming, redundant, outdated content. Hard to find what's needed.

---

## Cleanup Strategy

### ✅ KEEP (Essential Documentation)
### 🔄 CONSOLIDATE (Merge similar docs)
### 🗑️ DELETE (Outdated/redundant)
### 📦 ARCHIVE (Historical reference only)

---

## File-by-File Analysis

### ✅ **KEEP - Core Documentation (11 files)**

1. **README.md** - Root (REWRITE - currently outdated)
2. **AI_POWERED_MODULE_SYSTEM.md** → Move to `docs/onboarding-lms/`
3. **AZURE_DATABASE_SETUP.md** → Move to `docs/shared/`
4. **STUDENT_ONBOARDING_SYSTEM_DESIGN.md** → Move to `docs/onboarding-lms/ARCHITECTURE.md`
5. **TEAM_LEAD_CONTENT_WORKFLOW.md** → Move to `docs/onboarding-lms/`
6. **PROJECT_ROADMAP_2025.md** → Move to `docs/shared/`
7. **REPOSITORY_REORGANIZATION_PLAN.md** → Keep at root (active planning)
8. **docs/API_DOCUMENTATION.md** - Keep (comprehensive API ref)
9. **docs/SYSTEM_ARCHITECTURE_COMPLETE.md** → Move to `docs/research-analytics/`
10. **docs/IMPLEMENTATION_ROADMAP.md** → Move to `docs/research-analytics/`
11. **.gitignore** - Keep at root

---

### 🔄 **CONSOLIDATE - Merge These**

#### PostgreSQL Setup Guides (5 files → 1 file)
- POSTGRESQL_SETUP.md
- POSTGRESQL_WINDOWS_SETUP.md
- POSTGRESQL_DOCKER_SETUP.md
- POSTGRES_MIGRATION_CHECKLIST.md
- DOCKER_QUICKSTART.md

**Action:** Consolidate into `docs/shared/AZURE_DATABASE_SETUP.md` (already comprehensive)

---

#### Migration Guides (3 files → Delete all)
- MIGRATION_GUIDE.md (HTML to Flask - DONE, no longer needed)
- MIGRATION_QUICKSTART.md (Redundant with checklist)
- docs/PHASE1_MIGRATION.md (Outdated)

**Action:** DELETE - migrations complete

---

#### Planning/Session Docs (8 files → Archive)
- PHASE_ANALYSIS.md
- PHASE1_CORRECTED.md
- PHASE1_FINAL.md
- PARALLEL_TASKS.md
- PARALLEL_TASKS_REVIEW.md
- SESSION1_COMPLETE.md
- SESSION2_COMPLETE.md
- CONVERSION_SUMMARY.md

**Action:** ARCHIVE to `docs/archive/planning/` (historical only)

---

#### Getting Started Guides (3 files → 1 file)
- GETTING_STARTED_CHECKLIST.md
- IMMEDIATE_ACTION_PLAN.md
- START_HERE.md

**Action:** Merge into one comprehensive **GETTING_STARTED.md**

---

### 🗑️ **DELETE - Outdated/Redundant**

1. **DEPLOYMENT_GUIDE.md** - PythonAnywhere specific, outdated (using Azure now)
2. **WINDOWS_SETUP.md** - Redundant (covered in getting started)
3. **ANALYTICS_DASHBOARD.md** - Outdated (part of system architecture now)
4. **RESEARCH_DASHBOARD.md** - Redundant with system architecture
5. **REACT_LEARNING_ROADMAP.md** - Planning doc, not needed
6. **UI_INTEGRATION_PLAN.md** - Planning doc, superseded by roadmap
7. **GITHUB_COLLABORATION_GUIDE.md** - Superseded by TEAM_LEAD_CONTENT_WORKFLOW.md
8. **docs/ARCHITECTURE_DESIGN.md** - Redundant with SYSTEM_ARCHITECTURE_COMPLETE.md
9. **docs/CODEBASE_AUDIT_2025-11-18.md** - Point-in-time audit, archive it

---

## Target Structure (Clean!)

```
FRAMES/
│
├── README.md                              # ✨ NEW: Clear project overview
├── GETTING_STARTED.md                     # ✨ NEW: Quick start guide
├── REPOSITORY_REORGANIZATION_PLAN.md      # Active planning (temporary)
│
├── docs/
│   ├── README.md                          # ✨ NEW: Docs overview
│   │
│   ├── onboarding-lms/
│   │   ├── README.md                      # ✨ NEW: What is the LMS?
│   │   ├── ARCHITECTURE.md                # From STUDENT_ONBOARDING_SYSTEM_DESIGN.md
│   │   ├── AI_POWERED_MODULES.md          # From AI_POWERED_MODULE_SYSTEM.md
│   │   └── TEAM_LEAD_WORKFLOW.md          # From TEAM_LEAD_CONTENT_WORKFLOW.md
│   │
│   ├── research-analytics/
│   │   ├── README.md                      # ✨ NEW: What are the analytics?
│   │   ├── ARCHITECTURE.md                # From SYSTEM_ARCHITECTURE_COMPLETE.md
│   │   ├── API_REFERENCE.md               # From API_DOCUMENTATION.md
│   │   └── IMPLEMENTATION_ROADMAP.md      # Keep as-is
│   │
│   ├── ai-prediction-core/
│   │   ├── README.md                      # ✨ NEW: What is AI core? (future)
│   │   └── (to be created when we build this)
│   │
│   ├── shared/
│   │   ├── AZURE_SETUP.md                 # From AZURE_DATABASE_SETUP.md
│   │   ├── DATABASE_SCHEMA.md             # ✨ NEW: Complete schema ref
│   │   ├── PROJECT_ROADMAP.md             # From PROJECT_ROADMAP_2025.md
│   │   └── CONTRIBUTING.md                # ✨ NEW: How to contribute
│   │
│   └── archive/
│       ├── planning/                      # Old planning docs
│       │   ├── PHASE_ANALYSIS.md
│       │   ├── PARALLEL_TASKS.md
│       │   └── ... (8 files)
│       │
│       └── migrations/                    # Old migration guides
│           ├── MIGRATION_GUIDE.md
│           └── ... (3 files)
│
├── .gitignore
└── ... (code files)
```

**From 38 files → 15 active files + archived reference**

---

## Execution Plan

### **Step 1: Create New Structure** (5 minutes)

```bash
# Create docs structure
mkdir -p docs/onboarding-lms
mkdir -p docs/research-analytics
mkdir -p docs/ai-prediction-core
mkdir -p docs/shared
mkdir -p docs/archive/planning
mkdir -p docs/archive/migrations

# Create placeholder READMEs
touch docs/README.md
touch docs/onboarding-lms/README.md
touch docs/research-analytics/README.md
touch docs/ai-prediction-core/README.md
```

---

### **Step 2: Move Files to New Locations** (10 minutes)

```bash
# Onboarding LMS docs
mv STUDENT_ONBOARDING_SYSTEM_DESIGN.md docs/onboarding-lms/ARCHITECTURE.md
mv AI_POWERED_MODULE_SYSTEM.md docs/onboarding-lms/AI_POWERED_MODULES.md
mv TEAM_LEAD_CONTENT_WORKFLOW.md docs/onboarding-lms/TEAM_LEAD_WORKFLOW.md

# Research Analytics docs
mv docs/SYSTEM_ARCHITECTURE_COMPLETE.md docs/research-analytics/ARCHITECTURE.md
mv docs/API_DOCUMENTATION.md docs/research-analytics/API_REFERENCE.md
# IMPLEMENTATION_ROADMAP.md stays in docs/research-analytics/

# Shared docs
mv AZURE_DATABASE_SETUP.md docs/shared/AZURE_SETUP.md
mv PROJECT_ROADMAP_2025.md docs/shared/PROJECT_ROADMAP.md

# Archive planning docs
mv PHASE_ANALYSIS.md docs/archive/planning/
mv PHASE1_CORRECTED.md docs/archive/planning/
mv PHASE1_FINAL.md docs/archive/planning/
mv PARALLEL_TASKS.md docs/archive/planning/
mv PARALLEL_TASKS_REVIEW.md docs/archive/planning/
mv SESSION1_COMPLETE.md docs/archive/planning/
mv SESSION2_COMPLETE.md docs/archive/planning/
mv CONVERSION_SUMMARY.md docs/archive/planning/

# Archive migration docs
mv MIGRATION_GUIDE.md docs/archive/migrations/
mv MIGRATION_QUICKSTART.md docs/archive/migrations/
mv docs/PHASE1_MIGRATION.md docs/archive/migrations/
```

---

### **Step 3: Delete Redundant Files** (2 minutes)

```bash
# Delete PostgreSQL duplicates (keeping AZURE_SETUP.md)
rm POSTGRESQL_SETUP.md
rm POSTGRESQL_WINDOWS_SETUP.md
rm POSTGRESQL_DOCKER_SETUP.md
rm POSTGRES_MIGRATION_CHECKLIST.md
rm DOCKER_QUICKSTART.md

# Delete outdated docs
rm DEPLOYMENT_GUIDE.md
rm WINDOWS_SETUP.md
rm ANALYTICS_DASHBOARD.md
rm RESEARCH_DASHBOARD.md
rm REACT_LEARNING_ROADMAP.md
rm UI_INTEGRATION_PLAN.md
rm GITHUB_COLLABORATION_GUIDE.md
rm docs/ARCHITECTURE_DESIGN.md

# Archive point-in-time audit
mv docs/CODEBASE_AUDIT_2025-11-18.md docs/archive/
```

---

### **Step 4: Create New Documentation** (We'll do together)

Files to create with Claude Code:

1. **README.md** (Root) - Complete rewrite
2. **GETTING_STARTED.md** - Consolidated from 3 files
3. **docs/README.md** - Documentation overview
4. **docs/onboarding-lms/README.md** - LMS intro
5. **docs/research-analytics/README.md** - Analytics intro
6. **docs/shared/DATABASE_SCHEMA.md** - Complete schema
7. **docs/shared/CONTRIBUTING.md** - Contribution guide

---

### **Step 5: Update .gitignore** (1 minute)

```bash
# Add to .gitignore
echo "" >> .gitignore
echo "# Temporary planning docs (delete when done)" >> .gitignore
echo "REPOSITORY_REORGANIZATION_PLAN.md" >> .gitignore
echo "DOCUMENTATION_CLEANUP_PLAN.md" >> .gitignore
```

---

### **Step 6: Commit Changes** (2 minutes)

```bash
git checkout -b docs/cleanup-and-reorganize

git add .
git commit -m "Clean up and reorganize documentation

Changes:
- Organize docs by application (onboarding-lms, research-analytics, shared)
- Archive old planning and migration docs
- Delete redundant PostgreSQL setup guides
- Remove outdated deployment and setup docs
- Prepare for new comprehensive documentation

Files changed: 38 → 15 active docs
"

git push origin docs/cleanup-and-reorganize
```

---

## New Documentation Content

### 1. Root README.md (Rewrite)

**Structure:**
```markdown
# FRAMES - Multi-University Research Platform

Quick overview of what FRAMES is

## Three Applications, One Database

1. Student Onboarding LMS
2. Research Analytics Dashboard
3. AI Prediction Core (future)

## Quick Start

- [Getting Started Guide](GETTING_STARTED.md)
- [Onboarding LMS Docs](docs/onboarding-lms/)
- [Research Analytics Docs](docs/research-analytics/)

## For Developers

- [Project Roadmap](docs/shared/PROJECT_ROADMAP.md)
- [Database Setup](docs/shared/AZURE_SETUP.md)
- [Contributing Guide](docs/shared/CONTRIBUTING.md)

## Current Status

What's working, what's in progress

## Contact & Support
```

---

### 2. GETTING_STARTED.md (Consolidated)

**Merge from:**
- GETTING_STARTED_CHECKLIST.md
- IMMEDIATE_ACTION_PLAN.md
- START_HERE.md

**Structure:**
```markdown
# Getting Started with FRAMES

## Prerequisites

## Quick Start (5 minutes)

## Setup Azure Database (30 minutes)

## Building the Onboarding LMS (Weeks 1-8)

## Next Steps
```

---

### 3. docs/README.md (New)

```markdown
# FRAMES Documentation

## Documentation Structure

### By Application
- [Onboarding LMS](onboarding-lms/) - Student training modules
- [Research Analytics](research-analytics/) - Faculty/researcher tools
- [AI Prediction Core](ai-prediction-core/) - ML prediction engine

### Shared Resources
- [Project Roadmap](shared/PROJECT_ROADMAP.md)
- [Azure Setup](shared/AZURE_SETUP.md)
- [Database Schema](shared/DATABASE_SCHEMA.md)
- [Contributing](shared/CONTRIBUTING.md)

### Archive
- [Planning Documents](archive/planning/) - Historical planning
- [Migration Guides](archive/migrations/) - Old migration docs
```

---

### 4. docs/onboarding-lms/README.md (New)

```markdown
# Student Onboarding LMS

## What is it?

AI-powered learning management system for student onboarding

## Key Features

- Interactive training modules
- Mobile-first design
- AI assistant for team leads
- Comprehensive analytics

## Documentation

- [Architecture](ARCHITECTURE.md) - Technical design
- [AI-Powered Modules](AI_POWERED_MODULES.md) - How AI works
- [Team Lead Workflow](TEAM_LEAD_WORKFLOW.md) - Content contribution

## Quick Links

- API Endpoints: (link)
- Database Schema: (link)
- Deployment Guide: (link)
```

---

### 5. docs/research-analytics/README.md (New)

```markdown
# Research Analytics Dashboard

## What is it?

Faculty/researcher dashboard for analyzing team dynamics and knowledge transfer

## Key Features

- Multi-university comparison
- NDA diagnostics
- Interface analysis
- Predictive modeling

## Documentation

- [Architecture](ARCHITECTURE.md) - System design
- [API Reference](API_REFERENCE.md) - REST API docs
- [Implementation Roadmap](IMPLEMENTATION_ROADMAP.md) - Development plan

## Quick Links

- Live Dashboard: (link)
- Database Schema: (link)
```

---

### 6. docs/shared/DATABASE_SCHEMA.md (New)

Complete, consolidated database schema documentation:

```markdown
# FRAMES Database Schema

## Overview

PostgreSQL database on Azure shared by all three applications

## Tables by Application

### Core Tables (All Apps)
- universities
- teams
- students
- faculty
- projects

### Onboarding LMS Tables
- modules
- module_sections
- module_progress
- module_analytics_events

### Research Analytics Tables
- interfaces
- outcomes
- risk_factors
- factor_models

### AI Prediction Core Tables (Future)
- predictions
- trained_models
- model_evaluations

## Complete Schema

[Full SQL CREATE statements]

## Migrations

[Migration history and how to run]
```

---

### 7. docs/shared/CONTRIBUTING.md (New)

```markdown
# Contributing to FRAMES

## Getting Started

## Development Workflow

## Git Branching Strategy

## Code Style

## Testing

## Pull Request Process

## Questions?
```

---

## Timeline

### Today (2-3 hours):
1. ✅ Create folder structure (5 min)
2. ✅ Move files (10 min)
3. ✅ Delete redundant files (2 min)
4. ✅ Create new README.md with Claude Code (30 min)
5. ✅ Create GETTING_STARTED.md (30 min)
6. ✅ Create docs/README.md (15 min)
7. ✅ Create app-specific READMEs (30 min)
8. ✅ Commit and push (5 min)

### Tomorrow:
- Create DATABASE_SCHEMA.md
- Create CONTRIBUTING.md
- Final review and polish

---

## Success Criteria

After cleanup:
- ✅ Clear documentation structure
- ✅ No redundant files
- ✅ Easy to find what you need
- ✅ Professional, not "thinking out loud"
- ✅ New contributors can onboard quickly
- ✅ Each app has dedicated docs

---

**Ready to execute this plan?** Let's start with Step 1!

