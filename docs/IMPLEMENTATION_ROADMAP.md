# FRAMES Implementation Roadmap
**Solo Developer | Small Budget | PostgreSQL + Discord + GitHub**

**Date:** 2025-11-19
**Developer:** Solo (You)
**Budget:** Small/Flexible
**Priority:** Discord + GitHub integration ASAP

---

## 🎯 Technology Decisions (FINAL)

### **Database: PostgreSQL** ✅
- FREE and open source
- Better for your use case than SQL Server
- Extensions: pgvector (AI), TimescaleDB (time-series)
- Deploy on Railway ($5/month) or Heroku ($7/month)

### **Backend: Flask + FastAPI** ✅
- Flask: Your current API (keep it)
- FastAPI: Add for webhooks and high-performance endpoints
- Both Python, easy to maintain solo

### **Integrations Priority:**
1. **Discord** (ASAP) - Real-time team communication data
2. **GitHub** (ASAP) - Code collaboration patterns
3. **Custom PM Tool** (Later) - Need API documentation first

### **Frontend:**
- **Student/Team:** React Native (Expo) - PWA for mobile
- **Faculty/Researcher:** React - Desktop-first, mobile-responsive

---

## 📅 Phase-by-Phase Implementation Plan

### **PHASE 1: Foundation (Week 1-2) - CURRENT**

**Goal:** Clean up demo code, migrate to PostgreSQL, prepare for integrations

**Tasks:**
- [x] Backend API with SQLite ✅ DONE
- [x] Multi-university support ✅ DONE
- [ ] Migrate from SQLite to PostgreSQL
- [ ] Clean up demo/aspirational code
- [ ] Document what's real vs planned
- [ ] Set up Railway/Heroku for PostgreSQL hosting

**Deliverables:**
- PostgreSQL database deployed
- Clean, documented codebase
- Ready for integrations

**Time:** 1-2 weeks (solo)

---

### **PHASE 2: Discord Integration (Week 3-4)**

**Goal:** Capture real-time Discord data and derive interfaces

#### **Step 1: Discord Bot Setup (Day 1-2)**

**Create Discord Bot:**
```bash
# Install discord.py
pip install discord.py python-dotenv

# Create bot at https://discord.com/developers/applications
# Get bot token
# Invite bot to your Discord server(s)
```

**Bot Structure:**
```python
# backend/discord_bot.py
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Process message and store in database
    await process_message(message)
    
    await bot.process_commands(message)

async def process_message(message):
    """Extract data and store in PostgreSQL"""
    # TODO: Implement message processing
    pass

bot.run(os.getenv('DISCORD_TOKEN'))
```

**Database Schema:**
```sql
-- Discord messages
CREATE TABLE discord_messages (
    id BIGINT PRIMARY KEY,
    guild_id BIGINT,
    channel_id BIGINT,
    author_id BIGINT,
    author_name TEXT,
    content TEXT,
    timestamp TIMESTAMPTZ,
    university_id TEXT,
    team_id TEXT,
    message_type TEXT, -- question, answer, handoff, documentation, general
    mentions BIGINT[],
    reactions JSONB,
    thread_id BIGINT,
    metadata JSONB
);

-- Discord users (map to students/faculty)
CREATE TABLE discord_users (
    discord_id BIGINT PRIMARY KEY,
    username TEXT,
    university_id TEXT,
    student_id TEXT REFERENCES students(id),
    faculty_id TEXT REFERENCES faculty(id),
    role TEXT, -- student, faculty, staff
    joined_at TIMESTAMPTZ
);

-- Derived interfaces from Discord
CREATE TABLE discord_interfaces (
    id SERIAL PRIMARY KEY,
    from_user_id BIGINT REFERENCES discord_users(discord_id),
    to_user_id BIGINT REFERENCES discord_users(discord_id),
    interaction_type TEXT, -- mention, reply, thread, dm, reaction
    knowledge_transfer_score FLOAT,
    message_count INTEGER,
    first_interaction TIMESTAMPTZ,
    last_interaction TIMESTAMPTZ,
    channel_id BIGINT,
    metadata JSONB
);

-- Indexes for performance
CREATE INDEX idx_discord_messages_timestamp ON discord_messages(timestamp);
CREATE INDEX idx_discord_messages_author ON discord_messages(author_id);
CREATE INDEX idx_discord_messages_channel ON discord_messages(channel_id);
CREATE INDEX idx_discord_interfaces_users ON discord_interfaces(from_user_id, to_user_id);
```

#### **Step 2: Message Processing (Day 3-5)**

**Implement Message Analysis:**
```python
# backend/discord_processor.py
import re
from datetime import datetime
from sqlalchemy import create_engine
from db_models import DiscordMessage, DiscordInterface

class DiscordMessageProcessor:
    def __init__(self, db_session):
        self.db = db_session
    
    def process_message(self, message):
        """Process Discord message and extract knowledge transfer signals"""
        
        # Classify message type
        message_type = self.classify_message(message.content)
        
        # Extract mentions and interactions
        mentions = [user.id for user in message.mentions]
        
        # Store message
        db_message = DiscordMessage(
            id=message.id,
            guild_id=message.guild.id,
            channel_id=message.channel.id,
            author_id=message.author.id,
            author_name=str(message.author),
            content=message.content,
            timestamp=message.created_at,
            message_type=message_type,
            mentions=mentions,
            reactions={},
            metadata={
                'channel_name': message.channel.name,
                'guild_name': message.guild.name
            }
        )
        self.db.add(db_message)
        
        # Create/update interfaces
        if mentions:
            self.update_interfaces(message.author.id, mentions, message_type)
        
        self.db.commit()
    
    def classify_message(self, content):
        """Classify message type based on content"""
        content_lower = content.lower()
        
        # Question patterns
        if any(q in content_lower for q in ['?', 'how', 'what', 'why', 'when', 'where']):
            return 'question'
        
        # Documentation patterns
        if any(d in content_lower for d in ['documented', 'wiki', 'readme', 'guide']):
            return 'documentation'
        
        # Handoff patterns
        if any(h in content_lower for h in ['handoff', 'taking over', 'passing to', 'transfer']):
            return 'handoff'
        
        # Answer patterns (in reply to question)
        if any(a in content_lower for a in ['here\'s', 'you can', 'try this', 'solution']):
            return 'answer'
        
        return 'general'
    
    def update_interfaces(self, from_user, to_users, interaction_type):
        """Create or update interface records"""
        for to_user in to_users:
            # Check if interface exists
            interface = self.db.query(DiscordInterface).filter_by(
                from_user_id=from_user,
                to_user_id=to_user
            ).first()
            
            if interface:
                # Update existing
                interface.message_count += 1
                interface.last_interaction = datetime.now()
                interface.knowledge_transfer_score = self.calculate_kt_score(interface)
            else:
                # Create new
                interface = DiscordInterface(
                    from_user_id=from_user,
                    to_user_id=to_user,
                    interaction_type=interaction_type,
                    message_count=1,
                    first_interaction=datetime.now(),
                    last_interaction=datetime.now(),
                    knowledge_transfer_score=0.5
                )
                self.db.add(interface)
    
    def calculate_kt_score(self, interface):
        """Calculate knowledge transfer score based on interaction patterns"""
        # Simple scoring: more interactions = higher score
        # TODO: Enhance with NLP, sentiment analysis, etc.
        base_score = min(interface.message_count / 10, 1.0)
        return base_score
```

#### **Step 3: Deploy Discord Bot (Day 6-7)**

**Deployment Options:**

**Option A: Railway (Recommended for Solo)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init

# Deploy
railway up
```

**Option B: Heroku**
```bash
# Create Procfile
echo "worker: python backend/discord_bot.py" > Procfile

# Deploy
heroku create frames-discord-bot
git push heroku main
```

**Option C: Keep Running Locally (Simplest)**
```bash
# Run bot on your computer
python backend/discord_bot.py

# Use tmux/screen to keep it running
tmux new -s discord-bot
python backend/discord_bot.py
# Ctrl+B, D to detach
```

**Deliverables:**
- Discord bot capturing messages
- Messages stored in PostgreSQL
- Basic interface detection working

**Time:** 1 week (solo)

---

### **PHASE 3: GitHub Integration (Week 5-6)**

**Goal:** Capture code collaboration patterns from GitHub

#### **Step 1: GitHub API Setup (Day 1-2)**

**Install PyGithub:**
```bash
pip install PyGithub
```

**GitHub Data to Capture:**
- Commits (who, when, what files)
- Pull Requests (reviews, comments, approvals)
- Issues (assignments, discussions)
- Code Reviews (knowledge transfer events)

**Database Schema:**
```sql
-- GitHub repositories
CREATE TABLE github_repos (
    id BIGINT PRIMARY KEY,
    name TEXT,
    full_name TEXT,
    university_id TEXT,
    project_id TEXT REFERENCES projects(id),
    created_at TIMESTAMPTZ,
    metadata JSONB
);

-- GitHub commits
CREATE TABLE github_commits (
    sha TEXT PRIMARY KEY,
    repo_id BIGINT REFERENCES github_repos(id),
    author_id BIGINT,
    author_name TEXT,
    message TEXT,
    timestamp TIMESTAMPTZ,
    files_changed TEXT[],
    additions INTEGER,
    deletions INTEGER,
    metadata JSONB
);

-- GitHub pull requests
CREATE TABLE github_pull_requests (
    id BIGINT PRIMARY KEY,
    repo_id BIGINT REFERENCES github_repos(id),
    number INTEGER,
    title TEXT,
    author_id BIGINT,
    state TEXT,
    created_at TIMESTAMPTZ,
    merged_at TIMESTAMPTZ,
    reviewers BIGINT[],
    metadata JSONB
);

-- Derived interfaces from GitHub
CREATE TABLE github_interfaces (
    id SERIAL PRIMARY KEY,
    from_user_id BIGINT,
    to_user_id BIGINT,
    interaction_type TEXT, -- commit, review, comment, merge
    repo_id BIGINT,
    knowledge_transfer_score FLOAT,
    interaction_count INTEGER,
    first_interaction TIMESTAMPTZ,
    last_interaction TIMESTAMPTZ
);
```

#### **Step 2: GitHub Data Collection (Day 3-5)**

**Implement GitHub Collector:**
```python
# backend/github_collector.py
from github import Github
import os
from datetime import datetime, timedelta

class GitHubCollector:
    def __init__(self, access_token, db_session):
        self.gh = Github(access_token)
        self.db = db_session
    
    def collect_repo_data(self, repo_name):
        """Collect all data from a GitHub repository"""
        repo = self.gh.get_repo(repo_name)
        
        # Collect commits
        self.collect_commits(repo)
        
        # Collect pull requests
        self.collect_pull_requests(repo)
        
        # Derive interfaces
        self.derive_interfaces(repo)
    
    def collect_commits(self, repo, since_days=30):
        """Collect recent commits"""
        since = datetime.now() - timedelta(days=since_days)
        commits = repo.get_commits(since=since)
        
        for commit in commits:
            # Store commit in database
            db_commit = GitHubCommit(
                sha=commit.sha,
                repo_id=repo.id,
                author_id=commit.author.id if commit.author else None,
                author_name=commit.commit.author.name,
                message=commit.commit.message,
                timestamp=commit.commit.author.date,
                files_changed=[f.filename for f in commit.files],
                additions=commit.stats.additions,
                deletions=commit.stats.deletions
            )
            self.db.add(db_commit)
        
        self.db.commit()
    
    def collect_pull_requests(self, repo):
        """Collect pull requests and reviews"""
        prs = repo.get_pulls(state='all')
        
        for pr in prs:
            # Store PR
            db_pr = GitHubPullRequest(
                id=pr.id,
                repo_id=repo.id,
                number=pr.number,
                title=pr.title,
                author_id=pr.user.id,
                state=pr.state,
                created_at=pr.created_at,
                merged_at=pr.merged_at
            )
            self.db.add(db_pr)
            
            # Collect reviews (knowledge transfer events)
            reviews = pr.get_reviews()
            for review in reviews:
                self.create_interface(
                    from_user=review.user.id,
                    to_user=pr.user.id,
                    interaction_type='code_review',
                    repo_id=repo.id
                )
        
        self.db.commit()
    
    def derive_interfaces(self, repo):
        """Derive collaboration interfaces from GitHub activity"""
        # Find co-authors on same files
        # Find reviewers and reviewees
        # Find issue collaborators
        pass
```

#### **Step 3: Scheduled Collection (Day 6-7)**

**Set up APScheduler:**
```python
# backend/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from github_collector import GitHubCollector

scheduler = BackgroundScheduler()

def collect_github_data():
    """Scheduled task to collect GitHub data"""
    collector = GitHubCollector(os.getenv('GITHUB_TOKEN'), db_session)
    
    # List of repos to monitor
    repos = [
        'university1/project1',
        'university2/project2',
        # etc.
    ]
    
    for repo in repos:
        collector.collect_repo_data(repo)

# Run every hour
scheduler.add_job(collect_github_data, 'interval', hours=1)
scheduler.start()
```

**Deliverables:**
- GitHub data collection working
- Commits, PRs, reviews stored in PostgreSQL
- Interfaces derived from code collaboration

**Time:** 1 week (solo)

---

### **PHASE 4: Custom PM Tool Integration (Week 7-8)**

**Goal:** Integrate your custom PM tool

**Requirements from You:**
- API documentation for your PM tool
- Authentication method (API key, OAuth, etc.)
- Endpoints available
- Data format

**General Approach:**
```python
# backend/pm_collector.py
import requests

class CustomPMCollector:
    def __init__(self, api_key, base_url, db_session):
        self.api_key = api_key
        self.base_url = base_url
        self.db = db_session
    
    def collect_tasks(self):
        """Collect tasks from custom PM tool"""
        response = requests.get(
            f"{self.base_url}/api/tasks",
            headers={'Authorization': f'Bearer {self.api_key}'}
        )
        
        tasks = response.json()
        
        for task in tasks:
            # Store in database
            # Derive interfaces
            pass
```

**Time:** 1 week (depends on PM tool complexity)

---

### **PHASE 5: Student Mobile App (Week 9-12)**

**Goal:** Build mobile-first PWA for students/teams

**Technology:** React Native (Expo)

**Setup:**
```bash
# Install Expo CLI
npm install -g expo-cli

# Create project
expo init frames-student-app
cd frames-student-app

# Install dependencies
npm install axios react-navigation
```

**Features:**
- Login (simple auth)
- View my team
- View my project
- Log activities
- See interfaces
- Offline support

**Time:** 3-4 weeks (solo)

---

### **PHASE 6: Faculty Dashboard (Week 13-16)**

**Goal:** Desktop-first dashboard for faculty/researchers

**Technology:** React + Chart.js

**Features:**
- Multi-university comparison
- Factor model management
- Approval workflows
- Analytics dashboards
- Mobile-responsive quick views

**Time:** 3-4 weeks (solo)

---

### **PHASE 7: AI Model Training (Week 17-20)**

**Goal:** Train models to predict mission/program success

**Steps:**
1. Feature engineering from interface data
2. Train baseline models (Scikit-learn)
3. Experiment with XGBoost
4. Set up MLflow for tracking
5. Deploy prediction API

**Time:** 3-4 weeks (solo)

---

## 🛠️ Immediate Action Items (This Week)

### **Day 1-2: PostgreSQL Migration**
```bash
# Install PostgreSQL locally
# Or sign up for Railway/Heroku

# Update connection string
DATABASE_URL=postgresql://user:pass@host:5432/frames

# Run migrations
python backend/migrate_to_postgres.py
```

### **Day 3-4: Discord Bot Setup**
```bash
# Create Discord bot
# Get token
# Install discord.py
pip install discord.py

# Create basic bot
# Test message capture
```

### **Day 5-7: GitHub Integration**
```bash
# Get GitHub personal access token
# Install PyGithub
pip install PyGithub

# Test data collection
# Store in PostgreSQL
```

---

## 📊 Success Metrics

**Phase 2 (Discord):**
- [ ] Bot online 24/7
- [ ] Capturing 100% of messages
- [ ] Interfaces detected automatically
- [ ] Data queryable in PostgreSQL

**Phase 3 (GitHub):**
- [ ] Commits collected hourly
- [ ] PRs and reviews tracked
- [ ] Code collaboration interfaces derived
- [ ] Data integrated with Discord data

**Phase 4 (PM Tool):**
- [ ] Tasks synced
- [ ] Assignments tracked
- [ ] Project progress visible

---

## 💰 Budget Estimate

**Month 1-3 (Development):**
- Railway PostgreSQL: $5/month
- Railway Redis: $5/month
- Domain: $1/month
- **Total: ~$11/month**

**Month 4-6 (Production):**
- Railway/Heroku: $20/month
- Monitoring: $0 (free tier)
- **Total: ~$20/month**

**Month 7+ (Scaling):**
- AWS/GCP: $50-100/month
- ML compute: $20-50/month
- **Total: ~$70-150/month**

---

## 🚨 Risk Mitigation

**Solo Developer Risks:**
- **Burnout:** Take breaks, don't rush
- **Scope creep:** Stick to phases, don't add features mid-phase
- **Technical debt:** Write tests, document as you go
- **Bus factor:** Document everything, use version control

**Mitigation Strategies:**
- Work in 2-week sprints
- Deploy early and often
- Get user feedback frequently
- Keep it simple (KISS principle)

---

## 📝 Next Steps

1. **Confirm:** PostgreSQL as database ✅
2. **Set up:** Railway/Heroku account
3. **Migrate:** SQLite → PostgreSQL
4. **Create:** Discord bot
5. **Test:** Message capture
6. **Deploy:** Bot to Railway/Heroku
7. **Repeat:** For GitHub integration

**Start Date:** This week
**First Milestone:** Discord bot live in 2 weeks

---

**Questions?**
- Need help with Discord bot setup?
- Want code examples for GitHub integration?
- Need guidance on PostgreSQL migration?

Let me know and I'll provide detailed implementation guides!