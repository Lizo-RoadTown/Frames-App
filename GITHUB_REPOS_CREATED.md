# GitHub Repositories Created ✅

Three separate GitHub repositories have been created for the FRAMES project applications:

## Created Repositories

### 1. 📚 Student Onboarding LMS
**Repository:** https://github.com/Lizo-RoadTown/frames-onboarding-lms
**Description:** AI-powered student onboarding and learning management system for the FRAMES multi-university research collaboration
**Status:** Empty (ready for initial development)
**Priority:** HIGH - Needs to be ready before next cohort

**What goes here:**
- AI-powered module generation system
- Student onboarding modules (10-20 modules)
- Team lead content workflow tools
- Progressive Web App (PWA) for mobile access
- Module analytics tracking
- Documentation from `docs/onboarding-lms/`

### 2. 📊 Research Analytics Dashboard
**Repository:** https://github.com/Lizo-RoadTown/frames-research-analytics
**Description:** Faculty and researcher analytics dashboard for analyzing team dynamics and collaboration patterns in the FRAMES multi-university research project
**Status:** Empty (will receive existing code)
**Priority:** MEDIUM - Core features already complete in current repo

**What goes here:**
- Current `backend/` code (Flask API, analytics.py, models.py, etc.)
- Current `frontend/` code (React dashboards, templates, static files)
- University dashboards
- Team analytics
- Risk factor analysis
- Documentation from `docs/research-analytics/`
- **This is basically your CURRENT Frames-App repository code!**

### 3. 🤖 AI Prediction Core
**Repository:** https://github.com/Lizo-RoadTown/frames-ai-core
**Description:** AI prediction engine for mission success forecasting using Non-Decomposable Architecture (NDA) framework - FRAMES research project
**Status:** Empty (future development)
**Priority:** LOW - Planned for after LMS launch

**What goes here:**
- Non-Decomposable Architecture (NDA) framework
- Machine learning models
- Prediction algorithms
- Energy modeling engine (possibly `backend/energy_engine.py`)
- Documentation from `docs/ai-prediction-core/`

## Shared Resources

**Database:** All three applications will connect to the same Neon PostgreSQL database
- Connection string in each repo's `.env` file
- Schema managed centrally
- Migration scripts can live in `frames-research-analytics` since that's the core repo

## Current Repository (Frames-App)

Your current repository `Frames-App` contains the research analytics code. You have two options:

### Option 1: Keep Frames-App as Research Analytics (Recommended)
- Rename `Frames-App` → `frames-research-analytics` on GitHub
- Keep all existing code in place
- Just add remote for the new empty repo
- This preserves all Git history

### Option 2: Fresh Start
- Copy code from `Frames-App` to new `frames-research-analytics`
- Start each repo fresh
- Loses Git history but cleaner separation

## Next Steps for Project Management

Now that you have separate repos, you can:

1. **Enable GitHub Projects** for each repo
   - Go to each repo → Projects tab → Create project
   - Use built-in kanban board templates

2. **Create Issues** for each application
   - Tag issues with labels: `enhancement`, `bug`, `documentation`
   - Assign to milestones

3. **Set up Milestones**
   - frames-onboarding-lms: "Pre-Cohort Launch", "Module System v1.0"
   - frames-research-analytics: "Production Deployment", "v2.0 Features"
   - frames-ai-core: "NDA Framework", "Initial Model"

4. **Create initial branches**
   - Each repo can have: `main`, `development`, `feature/*`

## Repository URLs

- Onboarding LMS: https://github.com/Lizo-RoadTown/frames-onboarding-lms
- Research Analytics: https://github.com/Lizo-RoadTown/frames-research-analytics
- AI Core: https://github.com/Lizo-RoadTown/frames-ai-core
- Current (Frames-App): https://github.com/Lizo-RoadTown/Frames-App

Would you like me to help you:
1. Migrate the existing code to frames-research-analytics?
2. Set up GitHub Projects for each repo?
3. Create initial issues and milestones?
4. Set up the onboarding-lms initial structure?
