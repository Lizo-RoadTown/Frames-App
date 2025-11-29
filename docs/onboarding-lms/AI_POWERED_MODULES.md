# AI-Powered Module System - Complete Architecture

## Vision Statement

**Goal:** Create a fully automated student onboarding system where:
1. Initial modules are auto-generated from existing documentation
2. Team leads can modify modules conversationally via embedded AI
3. System continuously improves based on usage analytics
4. Zero technical knowledge required for content management

---

## Two-Phase Rollout

### Phase 1: Pre-Cohort Setup (You + AI Build Everything)

**Timeline:** Before next student cohort arrives

**Process:**
1. **Document Scraping**
   - Gather all existing training materials
   - SOPs, presentations, wikis, shared drives
   - Video transcripts, email instructions
   - Informal notes and checklists

2. **AI-Assisted Module Generation**
   - You feed documents to Claude/GPT
   - AI structures into module format
   - You review and refine
   - Publish to system

3. **Beta Deployment**
   - Full module library ready
   - New cohort uses it immediately
   - Collect analytics from day 1

**Deliverable:** Complete onboarding system with 10-20 modules ready

---

### Phase 2: AI-Embedded Team Lead Interface (Post-Launch)

**Timeline:** After initial cohort starts using modules

**Features:**
1. **Conversational AI Module Editor**
   - Built into admin dashboard
   - Team leads chat with AI naturally
   - AI generates/modifies content
   - Team lead reviews and publishes

2. **Continuous Improvement**
   - Analytics show where students struggle
   - AI suggests improvements
   - Team leads approve changes
   - System gets better over time

**Deliverable:** Self-improving, AI-managed training system

---

## Phase 1 Architecture: AI-Assisted Initial Build

### Your Workflow (Pre-Cohort)

#### Step 1: Document Collection

**Gather all training materials:**
```
Training Materials/
├── Safety/
│   ├── lab_safety_2023.pptx
│   ├── ppe_requirements.pdf
│   ├── emergency_procedures.docx
│   └── safety_video_transcript.txt
│
├── Equipment/
│   ├── oscilloscope_guide.pdf
│   ├── soldering_station_sop.docx
│   ├── 3d_printer_training.pptx
│   └── equipment_photos/
│
├── Software/
│   ├── solidworks_setup.md
│   ├── matlab_basics.pptx
│   ├── git_quickstart.pdf
│   └── team_wiki_backup.html
│
├── Processes/
│   ├── project_workflow.docx
│   ├── meeting_protocols.pdf
│   ├── documentation_standards.md
│   └── communication_guidelines.txt
│
└── Misc/
    ├── first_week_checklist.xlsx
    ├── onboarding_emails/
    └── faq_collection.txt
```

---

#### Step 2: Bulk AI Processing

**Use Claude Code (me!) to process documents:**

**Command to me:**
```
Process these training documents into onboarding modules:

[Upload/paste all documents]

For each topic area:
1. Identify natural module boundaries
2. Create module structure (5-7 sections each)
3. Extract content from documents
4. Simplify language for undergrads
5. Note where images/videos from originals should go
6. Generate JSON for each module

Output:
- Module list with topics
- JSON file for each module
- Image/asset requirements
- Estimated reading times
```

**I'll generate:**
```json
{
  "modules_created": 15,
  "module_list": [
    {
      "id": "lab-safety-fundamentals",
      "title": "Lab Safety Fundamentals",
      "source_docs": ["lab_safety_2023.pptx", "ppe_requirements.pdf"],
      "sections": 6,
      "estimated_minutes": 18
    },
    ...
  ],
  "files_generated": [
    "backend/modules/lab_safety.json",
    "backend/modules/oscilloscope_basics.json",
    ...
  ]
}
```

---

#### Step 3: Review & Refine

**You review each module:**
1. Read through generated content
2. Verify accuracy (check against source docs)
3. Add/update images from source materials
4. Test locally (preview as student would see)
5. Make adjustments

**Iterate with AI:**
```
"Module lab-safety section 3 is too technical.
Simplify for incoming freshmen."

"Add a section to equipment module about what to do
if machine breaks."

"Combine software modules 2 and 3, they overlap."
```

---

#### Step 4: Bulk Import to Database

```bash
# Once all modules reviewed and approved
python backend/scripts/import_modules.py --directory backend/modules/

# Output:
# ✓ Imported 15 modules
# ✓ Created 87 sections
# ✓ Uploaded 124 images
# ✓ All modules published and ready
```

---

### Automation Scripts (We'll Build These)

#### 1. Document Processor
```python
# backend/scripts/process_documents.py

"""
Takes folder of training documents
Calls AI API to structure into modules
Outputs JSON files ready for import
"""

import anthropic
import os
import json

def process_document_to_module(file_path):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    with open(file_path, 'r') as f:
        content = f.read()

    prompt = f"""
    Convert this training document into a student onboarding module:

    {content}

    Output JSON format:
    {{
      "module_id": "...",
      "title": "...",
      "sections": [...]
    }}
    """

    response = client.messages.create(
        model="claude-3-5-sonnet-20250929",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.content[0].text)

# Process all documents in folder
for doc in os.listdir("training_materials/"):
    module = process_document_to_module(doc)
    # Save to backend/modules/
```

#### 2. Bulk Module Importer
```python
# backend/scripts/import_modules.py

"""
Reads all JSON files from modules directory
Imports into PostgreSQL database
Publishes automatically
"""

import json
import os
from backend.app import db
from backend.models.module import Module, ModuleSection

def import_all_modules(directory="backend/modules/"):
    for file in os.listdir(directory):
        if file.endswith('.json'):
            with open(os.path.join(directory, file)) as f:
                data = json.load(f)

                # Create module
                module = Module(
                    module_id=data['module_id'],
                    title=data['title'],
                    category=data['category'],
                    status='published'  # Auto-publish
                )
                db.session.add(module)

                # Create sections
                for section_data in data['sections']:
                    section = ModuleSection(
                        module=module,
                        section_id=section_data['section_id'],
                        title=section_data['title'],
                        content=section_data['content'],
                        # ... other fields
                    )
                    db.session.add(section)

                db.session.commit()
                print(f"✓ Imported {data['title']}")

if __name__ == "__main__":
    import_all_modules()
```

---

## Phase 2 Architecture: AI-Embedded Team Lead Interface

### Conversational Module Editor

**Team lead experience:**

```
┌─────────────────────────────────────────┐
│  FRAMES Admin Dashboard                  │
│                                          │
│  Modules: [List View] [AI Assistant]    │
│                                          │
│  💬 AI Module Assistant                  │
│  ┌────────────────────────────────────┐ │
│  │ How can I help with modules today?│ │
│  └────────────────────────────────────┘ │
│                                          │
│  Team Lead: "Update lab safety module   │
│  to include the new fire suppression    │
│  system we just installed"              │
│                                          │
│  AI: "I'll update the Emergency          │
│  Procedures section. Here's what I'll    │
│  add: [preview]. Should I also update   │
│  the equipment photos section?"         │
│                                          │
│  Team Lead: "Yes, and add a note about  │
│  the evacuation route change"           │
│                                          │
│  AI: "Done. Here's the preview:          │
│  [shows updated module]                 │
│  Ready to publish?"                     │
│                                          │
│  Team Lead: [Publish] [Edit More]       │
└─────────────────────────────────────────┘
```

---

### AI Assistant Capabilities

#### 1. Module Modification
**User says:** "Update oscilloscope module with new model number"
**AI does:**
- Finds oscilloscope module
- Locates sections mentioning model
- Updates text with new info
- Shows preview
- Waits for approval

#### 2. Content Generation
**User says:** "Create a module for the new laser cutter"
**AI does:**
- Asks clarifying questions ("What's the make/model?")
- Generates module structure
- Creates safety sections
- Adds operation procedures
- Requests photos from user
- Shows preview

#### 3. Analytics-Driven Suggestions
**AI proactively:** "Analytics show students are pausing at 67% through the soldering module. The section on flux application might be confusing. Would you like me to simplify it?"

**User:** "Yes, show me"

**AI:** [Generates simpler version with step-by-step photos]

#### 4. Multi-Module Updates
**User says:** "We changed the lab access hours. Update all modules that mention hours."
**AI does:**
- Searches all modules for references to hours
- Lists what it found
- Shows proposed changes
- Bulk updates after approval

---

### Technical Implementation (Phase 2)

#### Backend: AI Service Layer

```python
# backend/services/ai_assistant.py

import anthropic
import os

class ModuleAIAssistant:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def chat(self, user_message, context=None):
        """
        Handle conversational module editing

        context includes:
        - Current module being edited (if any)
        - User's role/permissions
        - Recent analytics data
        - Full module library for reference
        """

        system_prompt = """
        You are an AI assistant helping team leads manage student onboarding modules.

        You can:
        - Modify existing modules
        - Create new modules from descriptions
        - Suggest improvements based on analytics
        - Search and update multiple modules

        Current module library: {module_list}
        Recent analytics: {analytics_summary}

        Always show previews before making changes.
        Ask clarifying questions when needed.
        Be conversational and helpful.
        """

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20250929",
            max_tokens=2000,
            system=system_prompt.format(
                module_list=context.get('modules'),
                analytics_summary=context.get('analytics')
            ),
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        return self.parse_ai_response(response)

    def parse_ai_response(self, response):
        """
        Parse AI response into actions

        Returns:
        - text: Message to show user
        - actions: What AI wants to do (modify_module, create_section, etc.)
        - preview: Preview of changes
        - requires_approval: Whether user needs to approve
        """
        # Parse response for action commands
        # Generate previews
        # Return structured data
```

#### Frontend: AI Chat Interface

```jsx
// react-frontend/src/components/admin/AIAssistant.jsx

import { useState, useEffect } from 'react';
import { sendAIMessage } from '../../services/aiService';

export const AIModuleAssistant = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [preview, setPreview] = useState(null);

  const handleSend = async () => {
    const response = await sendAIMessage(input, {
      modules: getAllModules(),
      analytics: getRecentAnalytics()
    });

    setMessages([...messages,
      { role: 'user', text: input },
      { role: 'assistant', text: response.text }
    ]);

    if (response.preview) {
      setPreview(response.preview);
    }
  };

  return (
    <div className="ai-assistant">
      <div className="chat-history">
        {messages.map((msg, i) => (
          <ChatMessage key={i} {...msg} />
        ))}
      </div>

      {preview && (
        <ModulePreview
          module={preview}
          onApprove={handleApproveChanges}
          onReject={handleReject}
        />
      )}

      <div className="input-area">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="How can I help with modules?"
        />
        <button onClick={handleSend}>Send</button>
      </div>

      {/* Suggested prompts */}
      <QuickActions
        suggestions={[
          "Update lab safety module",
          "Create new module",
          "Show analytics insights",
          "Find modules mentioning..."
        ]}
      />
    </div>
  );
};
```

---

### API Endpoints for AI Assistant

```python
# backend/routes/ai_assistant.py

@app.route('/api/admin/ai/chat', methods=['POST'])
@require_auth
def ai_chat():
    """
    POST /api/admin/ai/chat

    Request:
    {
      "message": "Update lab safety module to include...",
      "context": {
        "current_module_id": "lab-safety-101",
        "conversation_history": [...]
      }
    }

    Response:
    {
      "reply": "I'll update the Emergency Procedures section...",
      "actions": [
        {
          "type": "modify_section",
          "module_id": "lab-safety-101",
          "section_id": "emergency",
          "changes": {...}
        }
      ],
      "preview": {...},
      "requires_approval": true
    }
    """

    data = request.json
    assistant = ModuleAIAssistant()

    response = assistant.chat(
        data['message'],
        context={
            'modules': get_all_modules(),
            'analytics': get_recent_analytics(),
            'user_role': current_user.role,
            'history': data.get('context', {}).get('conversation_history', [])
        }
    )

    return jsonify(response)


@app.route('/api/admin/ai/approve', methods=['POST'])
@require_auth
def approve_ai_changes():
    """
    Approve changes suggested by AI

    Request:
    {
      "actions": [...],  # From AI response
      "publish": true    # Publish immediately or save as draft
    }
    """

    actions = request.json['actions']

    # Execute each action
    for action in actions:
        if action['type'] == 'modify_section':
            update_module_section(
                action['module_id'],
                action['section_id'],
                action['changes']
            )
        elif action['type'] == 'create_module':
            create_new_module(action['module_data'])
        # ... other action types

    if request.json.get('publish'):
        publish_modules([a['module_id'] for a in actions])

    return jsonify({'status': 'success'})
```

---

## Data Flow: End-to-End

### Phase 1: Initial Build

```
Existing Docs → You collect → Paste to Claude Code (me) →
I generate JSONs → You review → Import to database →
System ready with 10-20 modules → New cohort arrives →
Students use immediately → Analytics start flowing
```

### Phase 2: Continuous Improvement

```
Analytics show pause point → AI suggests improvement →
Team lead sees notification → Opens AI assistant →
"Simplify section 3 of soldering module" →
AI generates simplified version → Team lead previews →
Approves → Published → Students see improved version →
Analytics confirm improvement → Loop continues
```

---

## Implementation Roadmap

### Week 1-2: Foundation
- ✅ Neon database setup
- ✅ Database schema (existing + module tables)
- ✅ Basic API endpoints

### Week 3: Phase 1 - Bulk Module Creation
- [ ] Document collection script
- [ ] AI document processor (calls Claude API)
- [ ] Bulk module importer
- [ ] **You process all existing docs with AI**
- [ ] Review and publish 10-20 modules

### Week 4-5: Student-Facing Frontend
- [ ] React module viewer
- [ ] Progress tracking
- [ ] Analytics collection
- [ ] Mobile optimization

### Week 6-7: Team Lead Dashboard
- [ ] Basic admin UI
- [ ] Module list/view
- [ ] Analytics dashboard
- [ ] Manual edit interface (backup if AI not ready)

### Week 8-9: AI Assistant Integration
- [ ] AI service layer (backend)
- [ ] Chat interface (frontend)
- [ ] Action parsing and execution
- [ ] Preview generation
- [ ] Approval workflow

### Week 10: Beta Launch
- [ ] Deploy to production
- [ ] New cohort onboards with modules
- [ ] Monitor analytics
- [ ] Team leads start using AI assistant

---

## Cost Breakdown

### Infrastructure
- **Database:** $0/month (Neon free tier)
- **Hosting:** TBD (Render/Cloud Run free tier)
- **Domain:** $12/year (optional)

### AI API Costs
- **Anthropic Claude API:** Pay-as-you-go
  - Initial module generation (one-time): ~$5-20
    - 15 modules × avg 3000 tokens each = 45K tokens
    - Input: $3/million tokens = ~$0.15
    - Output: $15/million tokens = ~$0.75
    - **Total one-time: ~$1**

  - Ongoing AI assistant usage: ~$10-30/month
    - Assume 50 AI interactions/month
    - Avg 2000 tokens per interaction
    - **~$2-5/month during active use**

### Total Cost
- **Initial setup:** ~$1 (one-time AI generation)
- **Monthly:** $0-5 (only if AI assistant heavily used)
- **Annual:** ~$10-60

**Incredibly affordable for what you're getting!**

---

## Sample AI Prompts for Phase 1

### Master Prompt for Document Processing

```
I'm creating student onboarding modules from existing training documents.

Process these documents and create structured modules:

[Paste all documents]

For each module:
1. Identify clear topic boundaries (don't combine unrelated topics)
2. Create 5-7 bite-sized sections per module
3. Write content at undergraduate level (simple, clear language)
4. Estimated reading time per section (2-5 minutes)
5. Note where images/videos from source docs should be included
6. Add "What's Next?" or "Additional Resources" section at end

Output format:
For each module, provide JSON in this structure:
{
  "module_id": "kebab-case-id",
  "title": "Human Readable Title",
  "category": "Safety|Equipment|Software|Processes",
  "description": "1-2 sentence overview",
  "estimated_minutes": 15,
  "sections": [
    {
      "section_id": "intro",
      "order": 1,
      "title": "Introduction",
      "content_type": "text",
      "content": "Markdown formatted content here...",
      "estimated_minutes": 2,
      "images_needed": ["Description of what image to include"]
    }
  ],
  "prerequisites": [],
  "related_modules": [],
  "tags": ["safety", "required"]
}

Prioritize:
- Clarity over completeness (students need essentials, not everything)
- Practical over theoretical (what they need to DO)
- Safety-critical information (highlight warnings)
- Step-by-step instructions (not just descriptions)
```

---

### Example Interaction (Phase 2)

**Team Lead:** "Students keep asking about the sign-out procedure for equipment. Can we add that to the equipment module?"

**AI:** "I'll add a new section to the Equipment Introduction module. Here's what I'm proposing:

**New Section 4: Equipment Sign-Out Procedure**

Content:
- How to reserve equipment (online system)
- Sign-out process at lab
- Return procedure and inspection
- Late return policy

Should I add this after the 'Equipment Safety' section? Also, should I create a similar section for the other equipment modules (Oscilloscope, Soldering Station, etc.)?"

**Team Lead:** "Yes to both. Also mention you need to complete the training module first."

**AI:** "Updated! I've added the sign-out section to all 4 equipment modules and included the prerequisite requirement. Ready to preview?"

---

## Success Metrics

### Phase 1 (Initial Build)
- ✅ 10-20 modules published before cohort arrives
- ✅ All critical topics covered (safety, equipment, software, processes)
- ✅ Total estimated completion time: 3-5 hours for full onboarding
- ✅ 100% of source materials incorporated

### Phase 2 (AI Assistant)
- ✅ Team leads use AI assistant weekly
- ✅ Average module update time: < 5 minutes
- ✅ Team lead satisfaction: "This is easy!"
- ✅ Modules stay current (updated within days of changes)
- ✅ AI suggestions based on analytics lead to measurable improvements

### Student Outcomes
- ✅ 80%+ module completion rate
- ✅ Reduced onboarding time by 30%
- ✅ Fewer repetitive questions to team leads
- ✅ Students report feeling better prepared

---

## Next Actions

### This Week (You):
1. **Set up Neon database** (foundation for everything)
2. **Collect all training documents** into organized folder structure
3. **Identify 10-15 critical modules** needed for next cohort

### Next Week (We build together):
1. **Process documents with AI** (I'll help you do this in bulk)
2. **Generate module JSONs** (we'll iterate until they're perfect)
3. **Import to database** (one command to load everything)
4. **Preview and test** (make sure it works!)

### Following Weeks:
1. **Build student frontend** (React viewer)
2. **Build admin dashboard** (team lead interface)
3. **Integrate AI assistant** (conversational editor)
4. **Beta launch** with next cohort

---

**This is an incredibly ambitious but totally achievable system!**

The key insight: Do the heavy lifting upfront (Phase 1 with AI bulk generation), then give team leads an easy interface (Phase 2 with embedded AI) to maintain it going forward.

**Ready to start collecting those training documents?** 🚀

---

*Last updated: 2025-01-23*
