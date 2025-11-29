# FRAMES Complete System Architecture
**Date:** 2025-11-19
**Purpose:** Comprehensive architecture covering all integration points, data flows, and technology choices

---

## 🎯 System Overview

FRAMES is a **multi-university research platform** that:
1. **Captures** real-time data from Discord, project management tools, and manual input
2. **Stores** structured and unstructured data for analysis
3. **Analyzes** knowledge transfer patterns using custom NDA diagnostics
4. **Trains** AI models to predict mission/program success
5. **Serves** three user types: Students/Teams (mobile), Faculty (desktop+mobile), Researchers (advanced analytics)

---

## 🗄️ Database Architecture Decision

### **Why NOT SQL Server?**

**SQL Server (Microsoft):**
- ❌ **Cost:** $931/year minimum (Express is free but limited to 10GB)
- ❌ **Licensing:** Complex licensing for multi-university deployment
- ❌ **Platform:** Windows-centric (your dev environment, but limits deployment)
- ✅ **Pros:** Excellent for enterprise Windows environments, great tooling

**Why PostgreSQL Instead:**
- ✅ **Cost:** FREE and open source
- ✅ **Features:** More advanced than SQL Server for your use case
- ✅ **JSON Support:** Native JSONB for flexible schema (critical for evolving data)
- ✅ **AI/ML Integration:** Better Python ecosystem integration
- ✅ **Scalability:** Used by Instagram, Spotify, Reddit (proven at scale)
- ✅ **Extensions:** PostGIS (spatial), pg_vector (AI embeddings), TimescaleDB (time-series)
- ✅ **Cloud:** Supported everywhere (AWS RDS, Google Cloud SQL, Neon, Heroku)

### **Recommended Database Stack**

```
Primary Database: PostgreSQL 15+
├── Structured Data (teams, faculty, projects, interfaces)
├── JSONB columns for flexible/evolving schema
├── Full-text search for documentation
└── Extensions:
    ├── pg_vector: Store AI model embeddings
    ├── TimescaleDB: Time-series data (Discord activity over time)
    └── PostGIS: If you need spatial data later

Time-Series Database: TimescaleDB (PostgreSQL extension)
├── Discord message timestamps
├── Interface activity logs
├── Student engagement metrics
└── Real-time monitoring data

Document Store: PostgreSQL JSONB (no separate DB needed)
├── Discord message payloads
├── Project management tool data
├── Flexible research annotations
└── AI model metadata

Vector Database: pgvector (PostgreSQL extension)
├── AI embeddings for semantic search
├── Document similarity
├── Knowledge graph embeddings
└── Recommendation engine data
```

**Why This Works:**
- **Single database** (PostgreSQL) handles everything
- **No data synchronization** between multiple databases
- **Simpler deployment** and maintenance
- **Lower cost** (one database to manage)

---

## 🔌 Integration Architecture

### **1. Discord Integration**

**Purpose:** Capture real-time team communication and collaboration patterns

**Architecture:**
```
Discord Server(s)
    ↓ (Discord Bot API)
Discord Bot (Python: discord.py)
    ↓ (Webhook/Queue)
Message Processing Pipeline
    ├── Parse message content
    ├── Extract entities (users, channels, mentions)
    ├── Detect interface events (knowledge sharing, questions, handoffs)
    ├── Calculate engagement metrics
    └── Store in PostgreSQL
```

**Technology Stack:**
- **discord.py** (Python library) - Official Discord API wrapper
- **Celery** (Task queue) - Process messages asynchronously
- **Redis** (Message broker) - Queue for Celery tasks
- **PostgreSQL** - Store processed data

**Data Captured:**
```sql
-- Discord messages table
CREATE TABLE discord_messages (
    id BIGINT PRIMARY KEY,
    channel_id BIGINT,
    author_id BIGINT,
    content TEXT,
    timestamp TIMESTAMPTZ,
    university_id TEXT,
    team_id TEXT,
    message_type TEXT, -- question, answer, handoff, documentation
    metadata JSONB -- reactions, attachments, thread info
);

-- Derived interfaces from Discord
CREATE TABLE discord_interfaces (
    id SERIAL PRIMARY KEY,
    from_user_id BIGINT,
    to_user_id BIGINT,
    interaction_type TEXT, -- mention, reply, thread, dm
    knowledge_transfer_score FLOAT,
    timestamp TIMESTAMPTZ,
    message_ids BIGINT[]
);
```

**FREE Tools:**
- Discord Bot (free)
- discord.py library (free)
- Redis (free, open source)
- Celery (free, open source)

**PAID (when scaling):**
- Redis Cloud: $0-200/month depending on volume
- Celery workers: Compute costs on your hosting platform

---

### **2. Project Management Tool Integration**

**Purpose:** Track project milestones, task completion, team assignments

**Common Tools to Integrate:**
- **Jira** (API available)
- **Asana** (API available)
- **Trello** (API available)
- **GitHub Projects** (API available)
- **Monday.com** (API available)

**Architecture:**
```
Project Management Tool
    ↓ (REST API / Webhook)
Integration Service (Python)
    ├── Poll for updates (or receive webhooks)
    ├── Map PM data to FRAMES entities
    │   ├── Projects → FRAMES Projects
    │   ├── Tasks → Interface activities
    │   ├── Assignments → Team-Project interfaces
    │   └── Comments → Knowledge transfer events
    └── Store in PostgreSQL
```

**Technology Stack:**
- **Python requests** - API calls
- **APScheduler** - Scheduled polling (if no webhooks)
- **FastAPI webhooks** - Receive real-time updates
- **PostgreSQL** - Store normalized data

**Data Model:**
```sql
-- Project management tasks
CREATE TABLE pm_tasks (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    title TEXT,
    description TEXT,
    assigned_to TEXT[], -- user IDs
    status TEXT,
    created_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    metadata JSONB -- tool-specific data
);

-- Derived interfaces from PM tools
CREATE TABLE pm_interfaces (
    id SERIAL PRIMARY KEY,
    task_id TEXT,
    from_entity TEXT, -- team or person
    to_entity TEXT,
    interface_type TEXT, -- task_assignment, collaboration, handoff
    timestamp TIMESTAMPTZ
);
```

**FREE:**
- Most PM tools have free API access
- Python libraries (free)

**PAID:**
- PM tool subscriptions (varies: $0-50/user/month)
- Rate limits may require paid tiers for high volume

---

### **3. AI Model Training Pipeline**

**Purpose:** Train models to predict mission/program success based on interface patterns

**Architecture:**
```
PostgreSQL (Training Data)
    ↓
Feature Engineering Pipeline
    ├── Extract interface patterns
    ├── Calculate NDA metrics
    ├── Time-series features
    └── Graph features (network topology)
    ↓
Model Training (Python)
    ├── Scikit-learn (traditional ML)
    ├── PyTorch/TensorFlow (deep learning)
    ├── XGBoost (gradient boosting)
    └── Graph Neural Networks (PyTorch Geometric)
    ↓
Model Storage
    ├── MLflow (experiment tracking)
    ├── Model Registry
    └── Versioned models in PostgreSQL
    ↓
Inference API (Flask/FastAPI)
    └── Real-time predictions
```

**Technology Stack:**

**Data Science:**
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Traditional ML algorithms
- **XGBoost/LightGBM** - Gradient boosting (often best for tabular data)
- **PyTorch** - Deep learning (if needed)
- **NetworkX** - Graph analysis

**ML Operations:**
- **MLflow** - Experiment tracking, model registry
- **DVC** - Data version control
- **Weights & Biases** - Experiment tracking (alternative to MLflow)

**Model Serving:**
- **FastAPI** - High-performance API for predictions
- **Celery** - Batch predictions
- **PostgreSQL** - Store predictions

**Vector Embeddings (for semantic search):**
- **pgvector** - Store embeddings in PostgreSQL
- **Sentence Transformers** - Generate text embeddings
- **OpenAI Embeddings API** - Alternative (paid)

**Data Model:**
```sql
-- ML experiments
CREATE TABLE ml_experiments (
    id SERIAL PRIMARY KEY,
    experiment_name TEXT,
    model_type TEXT,
    hyperparameters JSONB,
    training_data_query TEXT,
    metrics JSONB, -- accuracy, precision, recall, etc.
    created_at TIMESTAMPTZ
);

-- Trained models
CREATE TABLE ml_models (
    id SERIAL PRIMARY KEY,
    experiment_id INTEGER REFERENCES ml_experiments(id),
    model_version TEXT,
    model_path TEXT, -- S3/filesystem path
    is_active BOOLEAN,
    deployed_at TIMESTAMPTZ
);

-- Predictions
CREATE TABLE ml_predictions (
    id SERIAL PRIMARY KEY,
    model_id INTEGER REFERENCES ml_models(id),
    university_id TEXT,
    project_id TEXT,
    prediction_type TEXT, -- mission_success, program_success
    predicted_probability FLOAT,
    confidence_interval JSONB,
    features_used JSONB,
    predicted_at TIMESTAMPTZ
);

-- Vector embeddings (for semantic search)
CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    entity_type TEXT, -- interface, project, team
    entity_id TEXT,
    embedding vector(1536), -- pgvector type
    model_name TEXT,
    created_at TIMESTAMPTZ
);

-- Index for similarity search
CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops);
```

**FREE:**
- Scikit-learn, PyTorch, XGBoost (all free)
- MLflow (free, open source)
- pgvector (free PostgreSQL extension)

**PAID (optional):**
- OpenAI API: $0.0001-0.002 per 1K tokens (for embeddings)
- Weights & Biases: Free tier → $50+/month for teams
- GPU compute: $0.50-3.00/hour (AWS, Google Cloud, Lambda Labs)

---

## 📊 Analytics & Visualization Stack

### **For Researchers (Advanced Analytics)**

**Option 1: Jupyter Notebooks + Plotly**
- **Jupyter Lab** - Interactive analysis
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation
- **Seaborn/Matplotlib** - Statistical plots
- **FREE** and most flexible

**Option 2: Metabase (Recommended for Non-Technical Users)**
- Drag-and-drop dashboards
- SQL query builder
- Connects directly to PostgreSQL
- **FREE** (open source)

**Option 3: Apache Superset**
- More powerful than Metabase
- Better for large datasets
- **FREE** (open source)

**Custom Dashboards (Your NDA Analytics):**
- **Backend:** Flask API (already built)
- **Frontend:** React + Chart.js
- **Real-time:** WebSockets (Socket.IO)

---

## 🏗️ Complete System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                              │
├─────────────────────────────────────────────────────────────────┤
│  Discord  │  Jira/Asana  │  Manual Input  │  GitHub  │  Slack   │
└─────┬───────────┬──────────────┬────────────────┬────────────┬──┘
      │           │              │                │            │
      ▼           ▼              ▼                ▼            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INTEGRATION LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  Discord Bot  │  PM Integrations  │  Flask API  │  Webhooks    │
│  (discord.py) │  (REST APIs)      │  (Manual)   │  (FastAPI)   │
└─────┬───────────────┬───────────────────┬──────────────────┬───┘
      │               │                   │                  │
      └───────────────┴───────────────────┴──────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MESSAGE QUEUE (Redis + Celery)                │
│  - Async processing                                              │
│  - Rate limiting                                                 │
│  - Retry logic                                                   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    POSTGRESQL DATABASE                           │
├─────────────────────────────────────────────────────────────────┤
│  Core Tables:                                                    │
│  ├── universities, teams, faculty, projects, interfaces         │
│  ├── students, outcomes, audit_logs                             │
│  │                                                               │
│  Integration Tables:                                             │
│  ├── discord_messages, discord_interfaces                       │
│  ├── pm_tasks, pm_interfaces                                    │
│  │                                                               │
│  ML Tables:                                                      │
│  ├── ml_experiments, ml_models, ml_predictions                  │
│  ├── embeddings (pgvector)                                      │
│  │                                                               │
│  Time-Series (TimescaleDB):                                     │
│  └── activity_metrics, engagement_scores                        │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
┌───────────────────────────┐   ┌──────────────────────────┐
│   ML TRAINING PIPELINE    │   │   APPLICATION LAYER      │
├───────────────────────────┤   ├──────────────────────────┤
│  - Feature Engineering    │   │  Flask API (Backend)     │
│  - Model Training         │   │  ├── REST endpoints      │
│  - MLflow Tracking        │   │  ├── WebSocket (real-time)│
│  - Model Registry         │   │  └── Authentication      │
│  - Batch Predictions      │   │                          │
└───────────┬───────────────┘   └──────────┬───────────────┘
            │                              │
            └──────────────┬───────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  Student/Team App (PWA)  │  Faculty Dashboard  │  Researcher    │
│  - React Native/Expo     │  - React/Vue.js     │  - Jupyter     │
│  - Mobile-first          │  - Desktop + Mobile │  - Metabase    │
│  - Offline support       │  - Approvals        │  - Custom viz  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Technology Stack Summary

### **Database**
- **PostgreSQL 15+** (primary database)
  - Extensions: pgvector, TimescaleDB, PostGIS (optional)
- **Redis** (message queue, caching)

### **Backend**
- **Python 3.11+**
- **Flask** (current API)
- **FastAPI** (for high-performance endpoints, webhooks)
- **Celery** (async task processing)
- **SQLAlchemy** (ORM)

### **Integrations**
- **discord.py** (Discord bot)
- **requests** (REST API calls)
- **APScheduler** (scheduled tasks)

### **Machine Learning**
- **Pandas, NumPy** (data manipulation)
- **Scikit-learn** (traditional ML)
- **XGBoost/LightGBM** (gradient boosting)
- **PyTorch** (deep learning, optional)
- **NetworkX** (graph analysis)
- **MLflow** (experiment tracking)
- **Sentence Transformers** (embeddings)

### **Frontend**
- **Student App:** React Native (Expo) or Flutter
- **Faculty Dashboard:** React or Vue.js
- **Charts:** Chart.js or Plotly
- **Tables:** AG-Grid Community

### **Analytics**
- **Metabase** (drag-and-drop dashboards)
- **Jupyter Lab** (researcher notebooks)
- **Plotly** (interactive visualizations)

### **Deployment**
- **Docker** (containerization)
- **Docker Compose** (local development)
- **Kubernetes** (production, optional)
- **GitHub Actions** (CI/CD)

### **Hosting Options**
- **Railway** (easiest, $5-20/month)
- **Heroku** (classic, $7-25/month)
- **AWS** (most flexible, varies)
- **Google Cloud** (good ML support, varies)
- **Neon** (specialized Postgres, free tier)

---

## 💰 Cost Breakdown

### **FREE Tier (Development)**
- PostgreSQL (local or free tier)
- Redis (local or free tier)
- All Python libraries
- Metabase
- Discord Bot
- GitHub (code hosting)

**Total: $0/month**

### **Production (Small Scale - 8 Universities, <1000 Users)**
- **Database:** Railway PostgreSQL ($5-10/month)
- **Redis:** Railway Redis ($5/month) or Redis Cloud free tier
- **Hosting:** Railway/Heroku ($10-20/month)
- **Domain:** $12/year
- **SSL:** Free (Let's Encrypt)
- **Discord Bot:** Free
- **PM Tool APIs:** Free (within rate limits)

**Total: ~$25-40/month**

### **Production (Medium Scale - Growing)**
- **Database:** AWS RDS PostgreSQL ($50-100/month)
- **Redis:** AWS ElastiCache ($15-30/month)
- **Hosting:** AWS ECS/Fargate ($50-100/month)
- **ML Compute:** AWS EC2 spot instances ($20-50/month)
- **Storage:** AWS S3 ($5-10/month)
- **Monitoring:** Datadog/New Relic ($0-50/month)

**Total: ~$150-350/month**

### **Optional Paid Services**
- **OpenAI API:** $10-100/month (for embeddings/GPT features)
- **Weights & Biases:** $50+/month (ML experiment tracking)
- **Sentry:** $26+/month (error tracking)
- **Auth0:** $23+/month (authentication service)

---

## 🚀 Deployment Strategy

### **Phase 1: Development (Current)**
- Local PostgreSQL
- Local Redis
- Flask development server
- SQLite for quick testing

### **Phase 2: Staging**
- Railway/Heroku PostgreSQL
- Railway/Heroku Redis
- Docker containers
- GitHub Actions CI/CD

### **Phase 3: Production**
- AWS/GCP PostgreSQL (managed)
- AWS/GCP Redis (managed)
- Kubernetes or managed containers
- Load balancing
- Auto-scaling
- Monitoring and alerting

---

## 📝 Next Steps

1. **Confirm database choice:** PostgreSQL vs SQL Server
2. **Prioritize integrations:** Discord first? PM tools first?
3. **ML timeline:** When do you need AI predictions?
4. **Budget:** What's your monthly budget for hosting?
5. **Team:** Solo or team? Technical skills?

---

**Questions to Answer:**
1. Do you have an existing Neon project/branch ready for analytics?
2. Which project management tool(s) are you using?
3. When do you need Discord integration live?
4. What's your timeline for AI model training?
5. What's your hosting budget?