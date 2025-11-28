# FRAMES Documentation

Welcome to the FRAMES documentation! This guide will help you navigate the comprehensive documentation for the entire platform.

---

## 🚨 Start Here

### For New Developers

1. **[DEVELOPER_ONBOARDING.md](DEVELOPER_ONBOARDING.md)** - Complete setup guide (2-3 hours)
2. **[COMPLETE_SYSTEM_ARCHITECTURE.md](COMPLETE_SYSTEM_ARCHITECTURE.md)** - Understand how FRAMES works
3. **[API_REFERENCE.md](API_REFERENCE.md)** - Backend API endpoints

### For AI Agents

1. **[COMPLETE_SYSTEM_ARCHITECTURE.md](COMPLETE_SYSTEM_ARCHITECTURE.md)** - Canonical system reference
2. **[CADENCE_SPEC_COMPLIANCE.md](CADENCE_SPEC_COMPLIANCE.md)** - Agent behavior contracts
3. **[DEVELOPER_ONBOARDING.md](DEVELOPER_ONBOARDING.md)** - Environment setup

---

## 📖 Core Documentation

### System Architecture & Design

- **[COMPLETE_SYSTEM_ARCHITECTURE.md](COMPLETE_SYSTEM_ARCHITECTURE.md)** - Complete system overview
  - Three-layer architecture (Authoring → Transformation → Runtime)
  - CADENCE integration (68 training modules)
  - Educational framework (OAtutor patterns)
  - Component architecture and data flow

- **[CADENCE_SPEC_COMPLIANCE.md](CADENCE_SPEC_COMPLIANCE.md)** - Specification compliance
  - Data intent compliance (5 canonical tables)
  - Data mapping (Postgres ↔ Notion)
  - Agent behavior contracts
  - Workflow compliance (7-step sync)

### Technical References

- **[API_REFERENCE.md](API_REFERENCE.md)** - Flask REST API documentation
  - All endpoints (teams, students, faculty, modules, analytics)
  - Request/response formats
  - Error handling
  - Code examples (cURL, Python, JavaScript)

- **[DATABASE_SCHEMA_REFERENCE.md](DATABASE_SCHEMA_REFERENCE.md)** - PostgreSQL schema
  - Existing tables (teams, faculty, projects, etc.)
  - CADENCE canonical tables (people, projects, tasks, meetings, documents)
  - Module & progress tables
  - Relationships and indexes

- **[NOTION_API_INTEGRATION.md](NOTION_API_INTEGRATION.md)** - Notion integration guide
  - Authentication and setup
  - Database and page operations
  - 7-step sync workflow
  - Rate limiting and error handling

### Developer Guides

- **[DEVELOPER_ONBOARDING.md](DEVELOPER_ONBOARDING.md)** - New developer setup
  - Prerequisites and environment setup
  - Understanding the codebase
  - Running locally (backend + frontend)
  - Common tasks and troubleshooting

---

## 📚 Documentation by Application

### [Student Onboarding LMS](onboarding-lms/)
AI-powered learning management system for training incoming students.

**Key Documents:**
- [Architecture](onboarding-lms/ARCHITECTURE.md) - Technical design and database schema
- [AI-Powered Modules](onboarding-lms/AI_POWERED_MODULES.md) - How the AI assistant works
- [Team Lead Workflow](onboarding-lms/TEAM_LEAD_WORKFLOW.md) - Content contribution guide

**Status:** 🚧 Active Development

---

### [Research Analytics](research-analytics/)
Faculty and researcher tools for analyzing team dynamics and knowledge transfer.

**Key Documents:**
- [Architecture](research-analytics/ARCHITECTURE.md) - Complete system design
- [API Reference](research-analytics/API_REFERENCE.md) - REST API documentation
- [Implementation Roadmap](research-analytics/IMPLEMENTATION_ROADMAP.md) - Development phases

**Status:** ✅ Core Features Complete

---

### [AI Prediction Core](ai-prediction-core/)
Machine learning engine for mission success prediction _(Coming soon)_.

**Status:** 📅 Planned for post-LMS launch

---

## 🔧 Shared Resources

### [Azure Setup](shared/AZURE_SETUP.md)
Complete guide to setting up free Azure PostgreSQL database.

### [Project Roadmap](shared/PROJECT_ROADMAP.md)
10-week development timeline and project milestones.

### [Contributing Guide](shared/CONTRIBUTING.md)
How to contribute to the FRAMES project.

---

## 📖 Quick Links

### Getting Started
- [Main Getting Started Guide](../GETTING_STARTED.md)
- [Azure Database Setup](shared/AZURE_SETUP.md)
- [Environment Configuration](../env.example)

### For Developers
- [Project Roadmap](shared/PROJECT_ROADMAP.md)
- [Repository Organization](../REPOSITORY_REORGANIZATION_PLAN.md)
- [Contributing Guidelines](shared/CONTRIBUTING.md)

### For Researchers
- [System Architecture](research-analytics/ARCHITECTURE.md)
- [API Documentation](research-analytics/API_REFERENCE.md)
- [NDA Diagnostics](research-analytics/ARCHITECTURE.md#nda-diagnostics)

### For Team Leads
- [Team Lead Workflow](onboarding-lms/TEAM_LEAD_WORKFLOW.md)
- [Module Creation Guide](onboarding-lms/AI_POWERED_MODULES.md)

---

## 📦 Archive

Historical documentation and planning materials are stored in [archive/](archive/).

- [Planning Documents](archive/planning/) - Phase planning and session notes
- [Migration Guides](archive/migrations/) - Old migration documentation

---

## 🔍 Documentation Index

### Root Level
- [README.md](../README.md) - Main project overview
- [GETTING_STARTED.md](../GETTING_STARTED.md) - Quick start guide
- [.env.example](../.env.example) - Environment configuration template

### Application Documentation
- [Onboarding LMS](onboarding-lms/)
- [Research Analytics](research-analytics/)
- [AI Prediction Core](ai-prediction-core/)

### Shared Documentation
- [Azure Setup](shared/AZURE_SETUP.md)
- [Project Roadmap](shared/PROJECT_ROADMAP.md)
- [Contributing Guide](shared/CONTRIBUTING.md)

---

## 📝 Documentation Standards

When contributing documentation:

1. **Use clear, simple language** - Write for developers new to the project
2. **Include examples** - Code snippets and screenshots when helpful
3. **Keep it current** - Update docs when features change
4. **Organize logically** - Place docs in the appropriate application folder

---

## 💬 Questions or Feedback?

- **GitHub Issues:** Report documentation issues
- **Pull Requests:** Suggest improvements
- **Contact:** See main [README.md](../README.md) for contact info

---

*Last updated: 2025-01-23*
