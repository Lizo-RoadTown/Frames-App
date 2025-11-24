# FRAMES - Multi-University Research & Training Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-316192.svg)](https://www.postgresql.org/)
[![Neon](https://img.shields.io/badge/Neon-PostgreSQL-00E599.svg)](https://neon.tech/)

> **A comprehensive platform combining AI-powered student onboarding, research analytics, and predictive modeling for multi-university space mission programs.**

---

## 🎯 What is FRAMES?

FRAMES (Framework for Resilience Assessment in Modular Engineering Systems) is a multi-application platform serving 8 universities collaborating on space missions. It provides:

### **Three Integrated Applications:**

#### 1. 📚 Student Onboarding LMS
AI-powered learning management system for training incoming students

- Interactive, mobile-friendly training modules
- AI assistant for team leads to manage content
- Comprehensive usage analytics
- Self-paced learning with progress tracking

**Status:** 🚧 Active Development | **Launch:** Next cohort
**Docs:** [Onboarding LMS Documentation](docs/onboarding-lms/)

---

#### 2. 📊 Research Analytics Dashboard
Faculty and researcher tools for analyzing team dynamics and knowledge transfer patterns

- Multi-university comparison dashboards
- NDA (Non-Decomposable Architecture) diagnostics
- Interface and energy loss analysis
- Predictive risk modeling

**Status:** ✅ Core Features Complete | **Users:** Faculty & Researchers
**Docs:** [Research Analytics Documentation](docs/research-analytics/)

---

#### 3. 🤖 AI Prediction Core _(Planned)_
Machine learning engine for mission success prediction

- Predictive models using team/interface data
- MLflow experiment tracking
- Automated risk assessment
- Research hypothesis testing

**Status:** 📅 Planned | **Timeline:** Post-LMS Launch
**Docs:** [AI Core Documentation](docs/ai-prediction-core/)

---

## 🏗️ Shared Infrastructure

All three applications connect to a **single PostgreSQL database** hosted on Neon:

```
┌──────────────────────────────────────────────────────────────┐
│              Neon PostgreSQL Database                         │
│  Universities │ Teams │ Students │ Modules │ Interfaces      │
└─────┬────────────────────┬───────────────────┬───────────────┘
      │                    │                   │
      ▼                    ▼                   ▼
┌─────────────┐   ┌─────────────────┐   ┌──────────────┐
│ Onboarding  │   │    Research     │   │  AI Engine   │
│     LMS     │   │    Analytics    │   │   (Future)   │
│  (React +   │   │  (React + Flask)│   │   (ML API)   │
│   Flask)    │   │                 │   │              │
└─────────────┘   └─────────────────┘   └──────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for React frontends)
- Neon account

### Get Started in 3 Steps

1. **[Monorepo Structure](MONOREPO_STRUCTURE.md)** - Understand the repository organization
2. **[Setup Complete](SETUP_COMPLETE.md)** - Quick start commands
3. **[Project Roadmap](docs/shared/PROJECT_ROADMAP.md)** - Development plan

### For Developers

```bash
# Clone repository
git clone https://github.com/Lizo-RoadTown/Frames-App.git
cd Frames-App

# Set up Python environment
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configure database connection
cp .env.example .env
# Edit .env with your Neon PostgreSQL connection string

# Run Flask backend
python backend/app.py

# Open browser: http://localhost:5000
```

---

## 📚 Documentation

### By Application
- **[Onboarding LMS](docs/onboarding-lms/)** - Student training system
- **[Research Analytics](docs/research-analytics/)** - Faculty/researcher tools
- **[AI Prediction Core](docs/ai-prediction-core/)** - ML prediction engine (planned)

### Shared Resources
- **[Project Roadmap](docs/shared/PROJECT_ROADMAP.md)** - Development timeline
- **[Monorepo Structure](MONOREPO_STRUCTURE.md)** - Repository organization
- **[Setup Guide](SETUP_COMPLETE.md)** - Quick start

### Full Documentation Index
See **[docs/README.md](docs/README.md)** for complete documentation overview.

---

## 🌟 Key Features

### For Students
- 📱 Mobile-friendly training modules
- ⏱️ Self-paced learning
- ✅ Progress tracking
- 🔄 Reusable reference materials

### For Team Leads
- 🤖 AI-assisted content creation
- 📊 Student progress analytics
- ✏️ Easy module updates
- 📈 Usage insights

### For Faculty & Researchers
- 🔬 Multi-university data analysis
- 📉 Risk factor modeling
- 🎯 NDA diagnostics
- 📑 Export capabilities

---

## 🛠️ Technology Stack

### Backend
- **Python 3.11+** with Flask
- **PostgreSQL 15+** (Neon hosted)
- **SQLAlchemy** ORM
- **Anthropic Claude API** (AI assistant)

### Frontend
- **React** (Student LMS & Analytics dashboards)
- **Vanilla JS** (Legacy analytics interface)
- **Chart.js** (Data visualization)

### Infrastructure

- **Neon PostgreSQL** (Database)
- **GitHub** (Version control & CI/CD)

### Machine Learning (Planned)
- **Scikit-learn** | **XGBoost** | **PyTorch**
- **MLflow** (Experiment tracking)
- **NetworkX** (Graph analysis)

---

## 📊 Current Status

### ✅ Completed
- [x] Multi-university database schema
- [x] Research analytics backend (NDA diagnostics, interfaces)
- [x] Comparative dashboard
- [x] Student/team/faculty management
- [x] Custom risk factor modeling

### 🚧 In Progress
- [ ] **Student Onboarding LMS** (Priority - Weeks 1-8)
  - [ ] AI-powered module generation
  - [ ] React student viewer
  - [ ] Team lead AI assistant
  - [ ] Analytics dashboard

### 📅 Planned
- [ ] React research analytics frontend
- [ ] AI prediction core development
- [ ] Multi-language support
- [ ] Mobile native apps

---

## 👥 Participating Universities

**Lead Institution:** California State Polytechnic University, Pomona

**Partner Universities:**
- Texas State University
- Columbia University
- _(5 additional universities)_

---

## 🎓 Research Background

FRAMES is based on research into **Non-Decomposable Architectures (NDA)** in space mission programs, using molecular modeling metaphors to understand knowledge transfer:

- **Teams/Faculty/Projects** = Molecules (nodes)
- **Interfaces** = Bonds (edges)
- **Energy Loss** = Knowledge transfer friction
- **Bond Strength** = Interface quality (codified vs. institutional knowledge)

### Research Questions
1. What interface patterns predict mission success?
2. How does knowledge transfer degrade during team transitions?
3. Can we predict program continuity across student cohorts?
4. What interventions strengthen weak interfaces?

---

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](docs/shared/CONTRIBUTING.md) for:

- Development workflow
- Git branching strategy
- Code style guidelines
- Pull request process

---

## 📞 Contact

- **Project Lead:** eosborn@cpp.edu
- **GitHub Issues:** [Report bugs or request features](https://github.com/Lizo-RoadTown/Frames-App/issues)
- **Documentation:** [docs/](docs/)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎓 Academic Citation

If you use FRAMES in your research, please cite:

```bibtex
@software{frames2025,
  title={FRAMES: Framework for Resilience Assessment in Modular Engineering Systems},
  author={Elizabeth Osborn, California State Polytechnic University, Pomona},
  year={2025},
  url={https://github.com/Lizo-RoadTown/Frames-App}
}
```

---

## 👥 Team

**Lead Institution:** California State Polytechnic University, Pomona

**Participating Universities:**
- Cal Poly Pomona (Lead)
- Texas State University
- Columbia University
- _(5 additional universities)_

**Principal Investigator:** Liz Osborn

---

## 📞 Contact

- **Project Lead:** eosborn@cpp.edu
- **GitHub Issues:** [Report bugs or request features](https://github.com/Lizo-RoadTown/Frames-App/issues)
- **Documentation:** [docs/](docs/)

---

## 🙏 Acknowledgments

- **NASA** - Research funding
- **USIP Program** - Multi-university collaboration framework
- **All participating universities** - Data sharing and collaboration
- **Cal Poly Pomona** - Lead institution and project management

---

<div align="center">

**[Documentation](docs/)** • **[Monorepo Structure](MONOREPO_STRUCTURE.md)** • **[Setup Guide](SETUP_COMPLETE.md)** • **[Project Roadmap](docs/shared/PROJECT_ROADMAP.md)**

Built for space mission research and student success 🚀

</div>
