# 🚀 FRAMES - Framework for Resilience Assessment in Modular Engineering Systems

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-316192.svg)](https://www.postgresql.org/)
[![Status: Active Development](https://img.shields.io/badge/status-active%20development-green.svg)]()

> **A multi-university research platform for analyzing knowledge transfer patterns in space mission programs and predicting mission success through AI-powered interface analysis.**

---

## 📖 What is FRAMES?

FRAMES is a collaborative research instrument designed to study **knowledge transfer dynamics** across 8 universities working on space missions. By capturing real-time data from Discord, GitHub, and project management tools, FRAMES uses **molecular modeling metaphors** to visualize team structures and predict mission outcomes.

### 🎯 Core Capabilities

- **🔬 Knowledge Transfer Analysis** - Track how information flows between teams, faculty, and projects
- **🤖 AI-Powered Predictions** - Machine learning models predict mission and program success
- **🌐 Multi-University Collaboration** - 8 universities share data transparently for collective learning
- **📊 Real-Time Monitoring** - Live dashboards show team health and interface strength
- **📱 Mobile-First Design** - Students and team leads access data on-the-go
- **🧪 Research Platform** - Faculty analyze patterns and test hypotheses about knowledge transfer

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                              │
│  Discord  │  GitHub  │  Custom PM Tool  │  Manual Input     │
└─────┬───────────┬──────────────┬────────────────┬───────────┘
      │           │              │                │
      ▼           ▼              ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│              INTEGRATION LAYER (Python)                      │
│  Discord Bot  │  GitHub API  │  PM Webhooks  │  Flask API   │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  PostgreSQL DATABASE                         │
│  Teams │ Faculty │ Projects │ Interfaces │ ML Models        │
└─────────────────────────────┬───────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
┌───────────────────────────┐   ┌──────────────────────────┐
│   ML TRAINING PIPELINE    │   │   APPLICATION LAYER      │
│  - Feature Engineering    │   │  - Flask REST API        │
│  - Model Training         │   │  - WebSocket (real-time) │
│  - MLflow Tracking        │   │  - Authentication        │
└───────────────────────────┘   └──────────┬───────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND LAYER                           │
│  Student App (PWA)  │  Faculty Dashboard  │  Researcher UI  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Node.js 18+ (for frontend)
- Discord Bot Token (for Discord integration)
- GitHub Personal Access Token (for GitHub integration)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/frames-python.git
cd frames-python

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Initialize database
python backend/init_db.py

# Run the Flask server
cd backend
python app.py
```

The application will be available at `http://localhost:5000`

### Docker Setup (Alternative)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access at http://localhost:5000
```

---

## 📚 Documentation

- **[System Architecture](docs/SYSTEM_ARCHITECTURE_COMPLETE.md)** - Complete technical architecture
- **[Implementation Roadmap](docs/IMPLEMENTATION_ROADMAP.md)** - Phase-by-phase development plan
- **[API Documentation](docs/API_DOCUMENTATION.md)** - REST API reference
- **[Database Schema](docs/DATABASE_SCHEMA.md)** - PostgreSQL table structures
- **[Discord Integration Guide](docs/DISCORD_INTEGRATION.md)** - Set up Discord bot
- **[GitHub Integration Guide](docs/GITHUB_INTEGRATION.md)** - Set up GitHub data collection

---

## 🎓 Research Background

FRAMES is based on research into **Non-Decomposable Architectures (NDA)** in space mission programs. The system models knowledge transfer as a molecular structure where:

- **Teams, Faculty, Projects** = Molecules (nodes)
- **Interfaces** = Bonds (edges)
- **Energy Loss** = Knowledge transfer friction
- **Bond Strength** = Interface quality (codified vs institutional knowledge)

### Key Research Questions

1. **What interface patterns predict mission success?**
2. **How does knowledge transfer degrade during team transitions?**
3. **Can we predict program continuity across student cohorts?**
4. **What interventions strengthen weak interfaces?**

### NDA Diagnostic Dimensions

- 🎯 **Actor Autonomy** - Degree of independent operation
- 📚 **Partitioned Knowledge** - Knowledge siloing across disciplines
- 🎲 **Emergent Outputs** - Shifting/undefined project goals
- ⏰ **Temporal Misalignment** - Timing differences across teams
- 💰 **Integration Cost** - Coordination effort required
- 🔗 **Coupling Degradation** - Weakening relationships over time

---

## 🌟 Key Features

### For Students & Team Leads 📱

- **Mobile-First PWA** - Works on any phone, no app store needed
- **My Team Dashboard** - See your team's structure and interfaces
- **Activity Logging** - Record knowledge transfer events
- **Offline Support** - Works without internet connection
- **Push Notifications** - Stay updated on team changes

### For Faculty & Staff 💻

- **Multi-University Comparison** - See all 8 universities side-by-side
- **Approval Workflows** - Review and approve student submissions
- **Live Monitoring** - Real-time team health indicators
- **Mobile Quick Views** - Approve on-the-go from your phone
- **Export & Reporting** - Generate reports for stakeholders

### For Researchers 🔬

- **Factor Model Management** - Define and test risk factors
- **ML Experiment Tracking** - MLflow integration for model versioning
- **Custom Analytics** - Jupyter notebooks for deep analysis
- **A/B Testing** - Compare different prediction models
- **Data Export** - CSV, JSON, SQL for external analysis

---

## 🛠️ Technology Stack

### Backend
- **Python 3.11+** - Core language
- **Flask** - REST API framework
- **FastAPI** - High-performance webhooks
- **PostgreSQL 15+** - Primary database
  - pgvector - AI embeddings
  - TimescaleDB - Time-series data
- **Redis** - Message queue and caching
- **Celery** - Async task processing
- **SQLAlchemy** - ORM

### Machine Learning
- **Scikit-learn** - Traditional ML algorithms
- **XGBoost** - Gradient boosting
- **PyTorch** - Deep learning (optional)
- **MLflow** - Experiment tracking
- **NetworkX** - Graph analysis
- **Sentence Transformers** - Text embeddings

### Frontend
- **React Native (Expo)** - Student mobile app (PWA)
- **React** - Faculty/researcher dashboard
- **Chart.js** - Data visualization
- **AG-Grid** - Advanced tables
- **Socket.IO** - Real-time updates

### Integrations
- **discord.py** - Discord bot
- **PyGithub** - GitHub API
- **APScheduler** - Scheduled tasks

### DevOps
- **Docker** - Containerization
- **GitHub Actions** - CI/CD
- **Railway/Heroku** - Hosting (development)
- **AWS/GCP** - Production hosting (future)

---

## 📊 Current Status

### ✅ Completed (Phase 1)
- [x] Multi-university database schema
- [x] REST API with CRUD operations
- [x] Permission system (header-based auth)
- [x] Comparative dashboard backend
- [x] Student roster management
- [x] Research dashboard with factor models
- [x] Custom NDA analytics engine

### 🚧 In Progress (Phase 2)
- [ ] Discord bot integration
- [ ] GitHub data collection
- [ ] PostgreSQL migration (from SQLite)
- [ ] Frontend-backend integration

### 📅 Planned (Phase 3+)
- [ ] Student mobile PWA
- [ ] Faculty desktop dashboard
- [ ] AI model training pipeline
- [ ] Real-time WebSocket updates
- [ ] Production deployment

---

## 🤝 Contributing

We welcome contributions from researchers, developers, and space mission practitioners!

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python
- Write tests for new features
- Update documentation
- Keep commits atomic and descriptive

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎓 Academic Citation

If you use FRAMES in your research, please cite:

```bibtex
@software{frames2025,
  title={FRAMES: Framework for Resilience Assessment in Modular Engineering Systems},
  author={Elizabeth Osborn, California Statue Polytechnic University, Pomona},
  year={2025},
  url={https://github.com/yourusername/frames-python}
}
```

---

## 👥 Team

**Lead Institution:** Cal Poly Pomona

**Participating Universities:**
- Cal Poly Pomona (Lead)
- Texas State University
- Columbia University
- [5 additional universities]

**Principal Investigator:** Liz Osborn

---

## 📞 Contact

- **Project Lead:** eosborn@cpp.edu
- **Issues:** [GitHub Issues](https://github.com/yourusername/frames-python/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/frames-python/discussions)
- **Discord:** [Join our Discord server](#)

---

## 🙏 Acknowledgments

- **NASA** - Research funding and mission data
- **JPL** - CubeSat mission collaboration
- **PROVES Program** - Multi-university collaboration framework
- **All participating universities** - Data sharing and collaboration

---

## 📈 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/frames-python?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/frames-python?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/frames-python)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/frames-python)

---

<div align="center">

**[Documentation](docs/)** • **[Roadmap](docs/IMPLEMENTATION_ROADMAP.md)** • **[API Docs](docs/API_DOCUMENTATION.md)** • **[Contributing](#-contributing)**

Made with ❤️ for space mission research

</div>
