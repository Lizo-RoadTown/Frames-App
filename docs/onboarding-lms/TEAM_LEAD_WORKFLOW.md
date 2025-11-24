# Team Lead Content Workflow - SIMPLIFIED

## Overview

**Goal:** Make it EASY for team leads to contribute content without learning Git or coding.

**Team Lead Role:** Subject matter expert who provides raw training materials
**Your Role:** Content curator who builds modules from their materials
**AI Role:** Help process and structure content

---

## Three Content Submission Options for Team Leads

### Option 1: AI-Assisted (Recommended - Easiest)

**Team lead workflow:**
1. Gather their training materials (docs, slides, notes)
2. Paste into ChatGPT/Claude with prompt:
   ```
   Convert this training material into a structured module format:

   Module title: [topic]
   Sections needed: 5-7 bite-sized chunks
   For each section include:
   - Title
   - Main content (2-3 paragraphs max)
   - Estimated reading time
   - Any images/videos needed

   [Paste their materials]
   ```
3. AI outputs structured content
4. Team lead reviews and edits in the AI chat
5. Team lead sends you the final AI output (copy/paste email or shared doc)
6. **You build the module** in the system

**Time for team lead:** 30-45 minutes
**No Git, no JSON, no coding required!**

---

### Option 2: Direct Submission (Simplest)

**Team lead workflow:**
1. Fill out a simple Google Form/Microsoft Form:
   ```
   Module Title: ___________
   Category: [dropdown]
   Estimated Time: _____ minutes

   Section 1:
   - Title: ___________
   - Content: [text box]
   - Images: [upload]

   Section 2:
   - Title: ___________
   - Content: [text box]
   - Images: [upload]

   [Add more sections button]
   ```
2. Submit form
3. **You receive notification** and build module from submission

**Time for team lead:** 20-30 minutes
**Even simpler - just fill out a form!**

---

### Option 3: You Work With Them (Most Hands-On)

**Workflow:**
1. Schedule 30-minute call with team lead
2. They share screen / show their materials
3. You ask questions, take notes
4. **You build module** during or right after call
5. Send them preview for approval
6. Make any edits they request
7. Publish

**Time for team lead:** 30 minutes (just the call)
**You do all the technical work**

---

## Your Workflow (Building Modules)

### Step 1: Receive Content from Team Lead

You get content via:
- ✉️ Email with AI-generated structure
- 📋 Form submission (automated notification)
- 📞 Call notes + their original materials
- 📁 Shared folder (OneDrive/Google Drive)

---

### Step 2: Create Module Branch

```bash
cd "c:\Users\LizO5\FRAMES Python"
git checkout main
git pull origin main
git checkout -b content/module-lab-safety
```

---

### Step 3: Build Module (Three Approaches)

#### Approach A: You + AI Build It

1. Take team lead's content
2. Ask Claude Code (me!) to:
   ```
   Create a module JSON from this content:

   [Paste their materials or AI output]

   Module ID: lab-safety-101
   Category: Safety
   Target: incoming_students
   ```
3. I generate the JSON
4. You review and save to `backend/modules/lab_safety.json`

#### Approach B: Use Web Admin UI (Future)

1. Log into admin dashboard
2. Click "New Module"
3. Copy/paste content into rich text editor
4. Add images
5. Preview
6. Publish

*(This will be built in Phase 4-5)*

#### Approach C: Direct Database Entry (When API Ready)

```bash
# Use API to create module
curl -X POST http://localhost:5000/api/admin/modules \
  -H "Content-Type: application/json" \
  -d @team_lead_content.json
```

---

### Step 4: Add Images/Videos

```bash
# Copy images to static folder
cp ~/Downloads/lab_safety_images/* frontend/static/images/modules/lab-safety/

# Update JSON with paths
```

---

### Step 5: Preview Locally

```bash
# Run Flask app
python backend/app.py

# Open browser to module preview
# http://localhost:5000/modules/lab-safety-101
```

---

### Step 6: Get Team Lead Approval

**Send them:**
- Link to preview (if you can share your localhost via ngrok/tunneling)
- OR screenshots
- OR screen recording walking through module

**They reply:**
- ✅ "Looks good, publish!"
- ✏️ "Change X, Y, Z" (you make edits, send again)

---

### Step 7: Commit and Merge

```bash
git add backend/modules/lab_safety.json
git add frontend/static/images/modules/lab-safety/
git commit -m "Add lab safety onboarding module

Content provided by: John Doe (Lab Manager)
Estimated time: 20 minutes
Sections: 5 (intro, PPE, emergency, equipment, resources)

Module ready for student use."

git push origin content/module-lab-safety
```

Create pull request → Self-review → Merge to main

---

## Team Lead Onboarding (Simplified)

### What Team Leads Need to Know

**Meeting/Email to them:**

> Hi [Team Lead Name],
>
> We're building an onboarding system for students! I need your expertise on [TOPIC].
>
> **What I need from you:**
> - Your training materials on [TOPIC] (slides, docs, notes, whatever you have)
> - 30-45 minutes of your time
>
> **What you DON'T need:**
> - To learn Git ❌
> - To write code ❌
> - To format anything special ❌
>
> **Three ways you can provide content:**
>
> **Option 1 (AI-Assisted):**
> Paste your materials into ChatGPT/Claude, ask it to structure into module format, send me the output.
> [Here's a template prompt to use...]
>
> **Option 2 (Fill out form):**
> I'll send you a simple form, just fill in sections, upload any images.
>
> **Option 3 (We do it together):**
> 30-minute call, you show me materials, I take notes and build it.
>
> Which works best for you?

---

## Content Quality Guidelines for Team Leads

**Share this simple checklist:**

### Good Module Content:
- ✅ Broken into 5-7 short sections (not one long document)
- ✅ Each section is 2-5 minutes to read
- ✅ Written conversationally (like you're teaching them)
- ✅ Includes visuals when helpful (photos, diagrams)
- ✅ Ends with "what to do next" or resources
- ✅ Focuses on what students NEED to know (not nice-to-know)

### Tips:
- Imagine explaining to a new freshman who just walked in
- Use simple language (they're learning!)
- Include examples from real situations
- Add warnings/cautions for safety-critical items
- Link to additional resources if they want to learn more

---

## AI Prompt Templates for Team Leads

### Template 1: Basic Conversion

```
I need to convert this training content into a student onboarding module.

Original content:
[Paste their materials]

Please structure this as:

MODULE TITLE: [suggest one]

SECTION 1 - [Title]
Content: [2-3 paragraphs, simple language]
Estimated time: [X minutes]

SECTION 2 - [Title]
Content: [2-3 paragraphs, simple language]
Estimated time: [X minutes]

[Continue for 5-7 sections total]

FOR EACH SECTION:
- Keep it short and focused
- Write at undergraduate reading level
- Highlight critical safety/procedural items
- Note if images/videos would help
```

### Template 2: From Presentation Slides

```
Convert this PowerPoint/slide deck into an interactive onboarding module.

Slide content:
[Paste slide text]

Transform this into a step-by-step module where students:
1. Read short sections (not full slides)
2. See relevant images
3. Can check their understanding
4. Know what to do next

Format as:
- Module title
- 5-7 sections (combine slides where it makes sense)
- Each section: title, content (2-3 paragraphs), estimated time
- Note where images from slides should be included
- Add a final "knowledge check" section with 3-5 self-assessment questions
```

### Template 3: From Procedure Document

```
Turn this procedural document into a student-friendly onboarding module.

Procedure:
[Paste their SOP/procedure]

Create a module that:
- Explains WHY we do this (context)
- Breaks down steps clearly
- Highlights safety/critical points
- Includes what to do if something goes wrong
- Provides resources for more info

Structure as 5-7 short sections, each 2-5 minutes to read.
Use simple, direct language.
Note where photos/videos would be helpful.
```

---

## GitHub Workflow (You Only)

Team leads **do not need** GitHub access if you're building modules!

**Simplified workflow:**

```
Your Local Work:
├── Receive content from team lead
├── Create branch: content/module-[name]
├── Build module (JSON or via API later)
├── Add images to static folder
├── Preview locally
├── Get team lead approval (screenshot/demo)
├── Commit to branch
├── Push to GitHub
├── Create PR
├── Self-review (or have another dev review)
├── Merge to main
└── Module live for students!
```

**Team leads never touch GitHub!**

---

## Module Creation Form (Option 2 Implementation)

### Using Microsoft Forms (You Have Microsoft Account)

**Create form with:**

**Section 1: Basic Info**
- Module Title (text)
- Category (dropdown: Safety, Equipment, Software, Processes, Other)
- Who is this for? (dropdown: All incoming students, Specific team, Specific role)
- Estimated completion time (text: "X minutes")

**Section 2: Module Sections** (Repeating)
- Section 1 Title
- Section 1 Content (long text box)
- Section 1 Images (file upload)
- Section 1 Estimated time (text: "X minutes")

[+ Add another section button]

**Section 3: Additional**
- Prerequisites (text: "What should students know first?")
- What happens next? (text: "What do they do after this module?")
- Additional resources (text: "Links or references")
- Your name (text)
- Your role (text)

**Submit button**

**Form settings:**
- Send confirmation email to submitter
- Send notification to you
- Save responses to Excel/SharePoint

---

## Your Automation Opportunities

### Now (Manual):
1. Team lead sends content → Email/Form
2. You build module → Manual JSON or API call
3. You commit → Git
4. Module live → Students see it

### Later (Semi-Automated):
1. Team lead sends content → Form submission
2. **Form triggers webhook** → Your API receives data
3. **API auto-creates module** → Saves to database
4. You review and approve → Click "Publish"
5. Module live → Students see it

### Future (Fully Automated):
1. Team lead uses admin UI → Web form
2. Builds module visually → Drag-and-drop
3. Clicks publish → Instant
4. Module live → Students see it
5. You get notification → Just FYI

---

## Content Storage Strategy

### Raw Materials (Team Lead Submissions)

**Create folder structure:**
```
OneDrive/FRAMES Content/
├── Submissions/
│   ├── 2025-01-23_Lab_Safety_John_Doe/
│   │   ├── original_slides.pptx
│   │   ├── AI_structured_output.txt
│   │   ├── images/
│   │   └── approval_email.txt
│   │
│   ├── 2025-01-25_Equipment_Jane_Smith/
│   └── ...
│
├── Published_Modules/
│   ├── lab_safety_v1.json
│   ├── equipment_intro_v1.json
│   └── ...
│
└── Templates/
    ├── AI_prompts.txt
    └── form_template.docx
```

### In Git Repository
```
backend/modules/
├── lab_safety.json
├── equipment_intro.json
└── software_setup.json

frontend/static/images/modules/
├── lab-safety/
│   ├── ppe_required.jpg
│   ├── fire_extinguisher.jpg
│   └── emergency_exits.jpg
│
├── equipment/
└── software/
```

---

## Example: End-to-End Flow

### Real World Example

**Monday 9 AM:**
- Email from John (Lab Manager): "Here's the AI output for lab safety module"
- Attachment: structured_content.txt

**Monday 10 AM (You):**
- Read content, looks good
- Open terminal: `git checkout -b content/lab-safety`
- Ask Claude Code: "Create module JSON from this content" + paste
- Save output to `backend/modules/lab_safety.json`
- Copy John's images to `frontend/static/images/modules/lab-safety/`
- Update JSON with image paths

**Monday 10:30 AM:**
- Run Flask app locally
- Screenshot each section
- Email John: "Here's the preview, look good?"

**Monday 2 PM:**
- John replies: "Looks great! Just change the emergency exit location in section 3"
- You edit JSON, update one sentence
- Re-screenshot, send again

**Monday 3 PM:**
- John replies: "Perfect, publish it!"
- You: `git add .`
- You: `git commit -m "Add lab safety module"`
- You: `git push origin content/lab-safety`
- Create PR, merge to main

**Monday 3:15 PM:**
- Deploy to production (or just merge if auto-deployed)
- Module live for students!

**Total time:**
- John: 30 min (AI structuring) + 5 min (reviews)
- You: 30 min (build) + 10 min (edits) + 5 min (deploy)
- **Total: ~80 minutes from request to live**

---

## Communication Templates

### Initial Request to Team Lead

```
Subject: Need Your Expertise - [Module Topic] for Student Onboarding

Hi [Name],

I'm building an onboarding system to help new students get up to speed faster.
I need your expertise on [TOPIC].

This will be a 15-20 minute interactive module that students complete before
their first [lab session / team meeting / etc.]. It should cover the essentials
they absolutely need to know.

I'll handle all the technical work - I just need the content knowledge from you!

Three easy options:
1. Send me your materials (slides, docs, etc.) and I'll build it
2. Paste your materials into ChatGPT/Claude with this prompt [link], send me output
3. 30-min call where I interview you and take notes

Which works best for you? When could you provide this?

Thanks!
```

### Follow-Up After Submission

```
Subject: Preview - [Module Name] Onboarding Module

Hi [Name],

Thanks for providing the content! I've built the module based on your materials.

Please review:
[Screenshots or preview link]

Does this accurately represent what students need to know? Any changes needed?

Let me know and I'll make any edits before publishing!
```

### Module Published Notification

```
Subject: ✅ [Module Name] is Now Live!

Hi [Name],

The [module name] onboarding module is now live for students!

Module link: [URL]
Created by: You
Published: [Date]

Students will complete this before [next team meeting / lab session / etc.].

I'll send you analytics in a week showing:
- Completion rates
- Average time spent
- Where students paused (areas that might need clarification)

We can update the module anytime based on this data.

Thanks for your contribution!
```

---

## Success Metrics (Team Lead Satisfaction)

### Goal: Make This EASY for Team Leads

Track:
- ⏱️ Time from request to published: < 1 week
- 🕐 Time burden on team lead: < 1 hour
- 😊 Team lead satisfaction: "This was easy!"
- 🔄 Update frequency: Can make changes quickly
- 📊 Analytics usefulness: They actually use the data

### What Good Looks Like:

**Team lead says:**
> "I just sent you my notes and you turned it into a professional module.
> Took me 30 minutes. Way easier than I thought!"

**NOT:**
> "I had to learn Git and JSON just to create a simple training doc?
> I don't have time for this..."

---

## Your Roles Clarified

### You Are:
- ✅ Content curator (collect from team leads)
- ✅ Module builder (technical implementation)
- ✅ Quality reviewer (make sure it's good)
- ✅ Analytics interpreter (share insights with team leads)
- ✅ System maintainer (keep it running)

### Team Leads Are:
- ✅ Subject matter experts
- ✅ Content providers (raw materials)
- ✅ Reviewers (approve final modules)
- ✅ Data users (use analytics to improve)

### Team Leads Are NOT:
- ❌ Developers
- ❌ Git users
- ❌ JSON writers
- ❌ System administrators

---

## Next Steps

1. **Pick one team lead** for pilot module
2. **Choose easiest option** for them (probably AI-assisted or call)
3. **Build first module together** (learning process)
4. **Get student feedback** (does it work?)
5. **Refine workflow** based on what works
6. **Scale to other team leads** with proven process

---

**This approach is WAY more sustainable and respects everyone's time!**

Team leads focus on content (their expertise), you handle technical implementation (your expertise).

---

*Last updated: 2025-01-23*
