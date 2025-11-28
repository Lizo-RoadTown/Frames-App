# FRAMES Training Module Library

Collection of 68 training modules extracted from CADENCE project for the FRAMES Learning Management System.

---

## 📖 Overview

The Module Library contains:

- **68 Training Modules** from CADENCE multi-university satellite project
- **JSON Format** with complete Notion page content (recordMaps)
- **Dark Theme** optimized for react-notion-x rendering
- **Educational Patterns** following OAtutor framework

---

## 📂 Directory Structure

```
modules/
├── README.md                       # This file
├── exports/                        # Module JSON files (68 files)
│   ├── avionics-team-onboarding.json
│   ├── power-systems-intro.json
│   ├── structures-101.json
│   └── ...
├── schemas/                        # JSON schemas (planned)
│   └── module_schema.json
└── templates/                      # Module templates (planned)
    └── basic_module_template.json
```

---

## 📋 Module Categories

### Hardware & Subsystems (18 modules)

- Avionics Team Onboarding
- Power Systems Introduction
- Structures 101
- Thermal Analysis Basics
- Communications Hardware
- Payload Integration
- _(12 additional modules)_

### Software & Tools (15 modules)

- Git Version Control
- Python for CubeSats
- CAD Software Training
- MATLAB Basics
- Flight Software Overview
- _(10 additional modules)_

### Project Management (12 modules)

- CADENCE Project Overview
- Team Collaboration Tools
- Documentation Standards
- Design Review Process
- Risk Management
- _(7 additional modules)_

### Mission Design (10 modules)

- Orbital Mechanics Fundamentals
- Mission Requirements Analysis
- ConOps Development
- Link Budget Calculations
- _(6 additional modules)_

### Testing & Validation (8 modules)

- Environmental Testing
- Functional Testing Procedures
- Integration & Test Planning
- Qualification Process
- _(4 additional modules)_

### Professional Skills (5 modules)

- Technical Writing
- Presentation Skills
- Teamwork & Communication
- Time Management
- Ethics in Engineering

---

## 📄 Module JSON Format

Each module is stored as a JSON file with the following structure:

```json
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
  "tags": ["avionics", "onboarding", "hardware"],
  "learning_objectives": [
    "Identify key avionics subsystems",
    "Configure development environment",
    "Execute basic hardware tests"
  ],
  "prerequisites": ["mod-basics"],
  "sections": [
    {
      "title": "Introduction",
      "content": "...",
      "type": "reading"
    }
  ],
  "notion_page_id": "2b96b8ea-578a-8101-80f6-d78aea760980",
  "recordMap": {
    "block": { ... },
    "collection": { ... },
    "collection_view": { ... }
  }
}
```

### Key Fields

- **module_id** - Unique identifier (e.g., `mod-001`)
- **slug** - URL-friendly identifier (e.g., `avionics-team-onboarding`)
- **notion_page_id** - Original Notion page ID
- **recordMap** - Complete Notion page content for react-notion-x rendering
- **sections** - Module content structure
- **learning_objectives** - What students will learn
- **prerequisites** - Required prior modules

---

## 🔄 Module Lifecycle

### 1. Authoring (Notion)

Team leads create/edit content in Notion:

- Rich text formatting
- Images and diagrams
- Videos and embeds
- Code blocks
- Callouts and toggles

**Tool:** Notion web/desktop app
**Location:** CADENCE Hub → Module Library database

---

### 2. Export (JSON)

Modules exported from Notion to JSON with recordMaps:

```bash
# Export script (handles recordMap generation)
python scripts/export_modules_from_notion.py
```

**Output:** `modules/exports/{slug}.json`

---

### 3. Deployment (Postgres + Notion)

JSON deployed to both storage layers:

```bash
# Deploy to Notion Module Library
python scripts/deploy_modules_to_db.py

# Import metadata to Postgres
python scripts/import_modules_to_postgres.py  # (planned)
```

---

### 4. Runtime (React)

Student app fetches and renders modules:

```javascript
import { NotionRenderer } from 'react-notion-x'

// Fetch module JSON
const module = await fetch(`/api/modules/${slug}`)
const { recordMap } = await module.json()

// Render with dark theme
<NotionRenderer
  recordMap={recordMap}
  darkMode={true}
  components={customComponents}
/>
```

**App:** `apps/onboarding-lms/frontend-react/`

---

## 🎨 Module Standards

### Content Guidelines

1. **Learning Objectives** - Clear, measurable outcomes
2. **Estimated Time** - Realistic completion time (15-90 min)
3. **Prerequisites** - Explicitly list required prior knowledge
4. **Sections** - Logical progression (Intro → Content → Practice → Assessment)
5. **Media** - Include images, diagrams, videos where helpful
6. **Interactivity** - Use callouts, toggles, quizzes

### Technical Requirements

- **Notion Blocks** - Use supported block types (text, heading, image, code, etc.)
- **Dark Theme** - Test rendering in dark mode
- **Mobile-Friendly** - Content works on phones/tablets
- **Accessibility** - Alt text for images, clear headings

### Metadata Requirements

- **Category** - One of 6 categories (Hardware, Software, Project Mgmt, etc.)
- **Difficulty** - Beginner, Intermediate, or Advanced
- **Target Audience** - Undergraduate, Graduate, Faculty, or Mixed
- **Status** - Draft, Review, Published, or Archived
- **Tags** - 3-5 descriptive tags

---

## 📊 Module Statistics

### By Category

| Category | Count | Avg Minutes |
|----------|-------|-------------|
| Hardware & Subsystems | 18 | 55 |
| Software & Tools | 15 | 45 |
| Project Management | 12 | 40 |
| Mission Design | 10 | 60 |
| Testing & Validation | 8 | 50 |
| Professional Skills | 5 | 35 |

### By Difficulty

- **Beginner:** 25 modules (37%)
- **Intermediate:** 30 modules (44%)
- **Advanced:** 13 modules (19%)

### By Status

- **Published:** 68 modules (100%)
- **Draft:** 0 modules
- **Archived:** 0 modules

---

## 🔧 Working with Modules

### Add New Module

1. **Create in Notion**
   - Add page to Module Library database
   - Fill in all required properties
   - Write content using standard structure

2. **Export to JSON**
   ```bash
   python scripts/export_modules_from_notion.py --module-id <notion-page-id>
   ```

3. **Validate Schema**
   ```bash
   python scripts/validate_module_schema.py modules/exports/new-module.json
   ```

4. **Deploy**
   ```bash
   python scripts/deploy_modules_to_db.py
   ```

---

### Update Existing Module

1. **Edit in Notion** - Make changes to Notion page
2. **Re-export**
   ```bash
   python scripts/export_modules_from_notion.py --module-id <notion-page-id>
   ```
3. **Sync**
   ```bash
   python scripts/update_module_library_from_json.py
   ```

---

### Delete Module

1. **Archive in Notion** - Change status to "Archived"
2. **Update Database**
   ```bash
   python scripts/sync_notion.py
   ```
3. **Remove JSON** - (Optional) Delete from `exports/` directory

---

## 🎓 Educational Framework

### OAtutor Integration

Modules follow OAtutor educational patterns:

- **Scaffolding** - Progressive difficulty
- **Worked Examples** - Step-by-step demonstrations
- **Practice Problems** - Interactive exercises
- **Hints & Feedback** - Contextual guidance
- **Mastery Learning** - Complete before advancing

**Reference:** [OAtutor GitHub Repository](https://github.com/CAHLR/OATutor)

### Learning Paths

Modules organized into learning paths:

1. **Onboarding Path** (5-8 modules)
   - CADENCE Overview
   - Team Tools
   - Documentation Standards
   - Git Basics
   - First Contribution

2. **Hardware Path** (10-15 modules)
   - Hardware fundamentals
   - Subsystem-specific training
   - Testing procedures
   - Integration practices

3. **Software Path** (10-15 modules)
   - Programming fundamentals
   - Flight software overview
   - Testing frameworks
   - Deployment practices

---

## 🔍 Finding Modules

### By Category

```bash
# List all modules in category
ls modules/exports/ | grep -i "hardware"
```

### By Tag

```bash
# Search module JSONs for tag
grep -r "\"avionics\"" modules/exports/
```

### By Difficulty

```bash
# Find beginner modules
grep -r "\"difficulty\": \"Beginner\"" modules/exports/
```

---

## 📚 Additional Documentation

- **[Complete System Architecture](../docs/COMPLETE_SYSTEM_ARCHITECTURE.md)** - How modules fit in FRAMES
- **[Notion API Integration](../docs/NOTION_API_INTEGRATION.md)** - Export/import process
- **[Developer Onboarding](../docs/DEVELOPER_ONBOARDING.md)** - Working with modules locally
- **[Scripts README](../scripts/README.md)** - Module automation scripts

---

## 🐛 Troubleshooting

### Module Not Rendering

**Issue:** Dark theme rendering broken in react-notion-x

**Solution:**

1. Verify `recordMap` exists in JSON
2. Check for unsupported block types
3. Test in Notion Renderer sandbox

### Export Failed

**Issue:** `export_modules_from_notion.py` fails

**Solution:**

1. Verify Notion API token
2. Check page permissions
3. Ensure page is in Module Library database

### Schema Validation Failed

**Issue:** Module JSON doesn't match schema

**Solution:**

1. Check required fields (title, slug, category, etc.)
2. Validate `sections` array structure
3. Ensure `recordMap` is complete

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/Lizo-RoadTown/Frames-App/issues)
- **Documentation:** [docs/](../docs/)
- **Contact:** eosborn@cpp.edu

---

**Last Updated:** 2025-11-28
**Maintained By:** Agent Beta
**Total Modules:** 68
**Next Review:** After module schema updates
