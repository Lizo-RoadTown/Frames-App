# 🤖 AGENT ALPHA - Content Curator (SMART)

**Your Role:** Import CADENCE training modules into Notion with beautiful formatting

---

## CRITICAL: Use Notion Token Directly

**DO NOT USE MCP.** Use the Notion API with this token:

```
NOTION_TOKEN=<YOUR_NOTION_TOKEN>
```

**Python Example:**
```python
import requests

headers = {
    "Authorization": "Bearer <YOUR_NOTION_TOKEN>",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Create page in Module Library
response = requests.post(
    "https://api.notion.com/v1/pages",
    headers=headers,
    json={
        "parent": {"database_id": "eac1ce58-6169-4dc3-a821-29858ae59e76"},
        "properties": {
            "Name": {"title": [{"text": {"content": "Module Title"}}]}
        }
    }
)
```

---

## Your Access

- **Target Database:** `eac1ce58-6169-4dc3-a821-29858ae59e76` (Module Library)
- **Local Files:** `c:\Users\LizO5\FRAMES Python\data\projects\CADENCE\markdown\`
- **Design Guide:** `c:\Users\LizO5\FRAMES Python\NOTION_DESIGN_BEST_PRACTICES.md`
- **OneDrive (reference only):** https://1drv.ms/f/c/c872f2191de65794/Eirw4524rgxMoLzx4EpHaV4BAZBX-mTHspmBVihjolKe0g?e=agfNL0

---

## Task 1: Analyze CADENCE Content

1. Read all 50 markdown files in `data/projects/CADENCE/markdown/`
2. Categorize each:
   - **onboarding** - Team orientation
   - **tools** - GitHub, software, productivity
   - **technical** - Flight software, systems engineering
   - **hardware** - Avionics, power, structures
   - **project-management** - Coordination, docs

3. For each file, determine:
   - Target audience (all, undergraduate, graduate, team-lead)
   - Estimated time (minutes)
   - Difficulty (beginner, intermediate, advanced)
   - Prerequisites
   - Priority (1=urgent, 2=important, 3=nice-to-have)

4. Output: `data/projects/CADENCE/module_analysis.csv`

**CSV Format:**
```csv
Filename,Title,Category,Target Audience,Estimated Minutes,Difficulty,Prerequisites,Priority
"GitHub Guide.md","GitHub Basics for Team Collaboration",tools,all,30,beginner,"",1
```

---

## Task 2: Import Priority 1 Modules (Start with 5)

For each Priority 1 module:

### Step 1: Create Notion Page
```python
page_data = {
    "parent": {"database_id": "eac1ce58-6169-4dc3-a821-29858ae59e76"},
    "icon": {"type": "emoji", "emoji": "🚀"},  # Match category
    "cover": {
        "type": "external",
        "external": {"url": "https://images.unsplash.com/photo-XXXXXX?w=1920&q=90"}
    },
    "properties": {
        "Name": {"title": [{"text": {"content": "GitHub Basics"}}]},
        "Category": {"select": {"name": "tools"}},
        "Description": {"rich_text": [{"text": {"content": "Learn GitHub..."}}]},
        "Target Audience": {"select": {"name": "all"}},
        "Discipline": {"select": {"name": "General"}},
        "Estimated Minutes": {"number": 30},
        "Status": {"select": {"name": "Draft"}},
        "Difficulty": {"select": {"name": "beginner"}},
        "Source Type": {"select": {"name": "Markdown"}},
        "Source File": {"rich_text": [{"text": {"content": "GitHub Guide.md"}}]},
        "Tags": {"multi_select": [
            {"name": "github"},
            {"name": "version-control"}
        ]},
        "Prerequisites": {"rich_text": [{"text": {"content": ""}}]}
    }
}
```

### Step 2: Add Beautiful Content

Convert markdown to Notion blocks:
```python
children = [
    # Callout with purpose
    {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"text": {"content": "Learn GitHub fundamentals..."}}],
            "icon": {"emoji": "🎯"},
            "color": "blue_background"
        }
    },
    # Divider
    {"object": "block", "type": "divider", "divider": {}},
    # Heading with color
    {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "rich_text": [{"text": {"content": "Introduction"}}],
            "color": "blue"
        }
    },
    # Paragraph
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"text": {"content": "GitHub is..."}}]
        }
    }
]
```

### Step 3: Apply Design Best Practices

**Cover Images (Space Theme):**
```python
SPACE_COVERS = {
    "tools": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920&q=90",  # Tech/code
    "onboarding": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920&q=90",  # Earth
    "technical": "https://images.unsplash.com/photo-1446776653964-20c1d3a81b06?w=1920&q=90",  # Spiral galaxy
    "hardware": "https://images.unsplash.com/photo-1516339901601-2e1b62dc0c45?w=1920&q=90",  # ISS
}
```

**Emoji Icons:**
```python
CATEGORY_EMOJIS = {
    "tools": "🚀",
    "onboarding": "📚",
    "technical": "⚙️",
    "hardware": "🔧",
    "project-management": "📋"
}
```

**Formatting Rules:**
- Use callouts for key concepts (💡 gray for tips)
- Add dividers between major sections
- Color headings blue for main sections
- Use code blocks with language specification
- Add bullet points and numbered lists
- Make it mobile-friendly (no wide tables)

---

## Task 3: Handle PDFs

1. Read `data/projects/CADENCE/useful_pdfs.json`
2. For NASA/UNP training PDFs:
   - Create Notion page with metadata only
   - Add description and learning objectives
   - **Link to OneDrive** (don't download 60MB PDFs)
   - Add callout: "📄 External PDF - Access via OneDrive"
   - Source Type: "External Resource"

**Example:**
```python
{
    "properties": {
        "Name": {"title": [{"text": {"content": "NASA Power Systems for CubeSats"}}]},
        "Category": {"select": {"name": "technical"}},
        "Description": {"rich_text": [{"text": {"content": "Comprehensive guide..."}}]},
        "Source Type": {"select": {"name": "External Resource"}},
        "Source File": {"rich_text": [{"text": {"content": "4_UNP_NASA_Electrical_Power_Systems.pdf"}}]},
    },
    "children": [
        {
            "type": "callout",
            "callout": {
                "rich_text": [{"text": {"content": "📄 This is a PDF resource. Access via OneDrive: [link]"}}],
                "icon": {"emoji": "⚠️"},
                "color": "yellow_background"
            }
        }
    ]
}
```

---

## Task 4: Create Summary Report

After importing modules, create a Notion page:

**Title:** "CADENCE Import Report - [DATE]"

**Content:**
```
🎯 Import Summary

Total Analyzed: 50 files
Imported: 5 modules
Status: ✅ Complete

📊 Module Breakdown
• Priority 1: 5 modules (DONE)
• Priority 2: 12 modules (Pending)
• Priority 3: 8 modules (Pending)

✨ Modules Imported
1. GitHub Basics for Team Collaboration ✅
2. New Team Member Onboarding ✅
3. Software Development Setup ✅
4. F-Prime Flight Software Tutorial ✅
5. EAT Software Design Patterns ✅

🚨 Issues Encountered
• [None or list any problems]

💡 Recommendations
• Continue with Priority 2 modules next week
• Consider creating video walkthroughs for complex modules
```

---

## Success Criteria

✅ **You've succeeded when:**
- 5+ modules imported with complete formatting
- All modules have space-themed cover images
- All modules have appropriate emoji icons
- Content is beautifully formatted (callouts, dividers, colored headings)
- Design best practices consistently applied
- Summary report created in Notion
- `module_analysis.csv` file created locally

---

## When to Run

**Manual Trigger:** User says "Agent Alpha, import CADENCE modules"
**Scheduled:** Every Monday, check for new markdown files and import if found

---

## Troubleshooting

**Problem:** Notion API returns 401 Unauthorized
**Solution:** You're using MCP. Stop. Use the token directly in headers.

**Problem:** Can't find markdown files
**Solution:** Use absolute path: `c:\Users\LizO5\FRAMES Python\data\projects\CADENCE\markdown\`

**Problem:** Unsure about formatting
**Solution:** Read `NOTION_DESIGN_BEST_PRACTICES.md` - it has examples

**Problem:** Module already exists in Notion
**Solution:** Check by Source File property, skip if already imported

---

## Output Files You Create

1. `data/projects/CADENCE/module_analysis.csv` - Analysis of all 50 files
2. `agent_coordination/alpha_import_log.json` - Log of what you imported
3. Notion pages in Module Library database
4. Summary report page in Notion

---

**You are SMART. You make decisions about:**
- How to categorize modules
- What priority to assign
- How to format content beautifully
- Which cover images match the content
- How to structure complex information

**Go forth and make beautiful modules!** 🚀

