# FRAMES AI Prediction Core

AI prediction engine for mission success forecasting using Non-Decomposable Architecture (NDA) framework.

## Status: 📅 Planned

**Priority:** LOW - Planned for after LMS launch
**Timeline:** Post-onboarding-lms deployment

## Overview

The AI Core will provide predictive analytics for mission success based on team dynamics, risk factors, and historical data using the Non-Decomposable Architecture (NDA) framework.

## Non-Decomposable Architecture (NDA)

NDA uses molecular modeling metaphors to analyze complex system interactions:

- **Atoms:** Individual factors/metrics
- **Bonds:** Relationships between factors
- **Molecules:** Factor clusters that work together
- **Energy States:** System stability and performance
- **Reactions:** Changes and transitions in team dynamics

Unlike traditional decomposable models that treat factors independently, NDA recognizes that:
- Factors interact in complex ways
- Relationships between factors matter more than individual values
- System behavior emerges from interactions, not just components

## Planned Features

### Prediction Capabilities
- Mission success probability
- Risk factor impact analysis
- Team performance forecasting
- Optimal team composition recommendations
- Early warning system for team issues

### Analysis Tools
- Factor interaction mapping
- Energy state visualization
- Historical pattern recognition
- What-if scenario modeling
- Counterfactual analysis

### Integration Points
- Pull data from research-analytics app
- Provide predictions back to analytics dashboards
- Store models and validations in shared database

## Tech Stack (Planned)

- **Backend:** Python, Flask
- **ML Framework:** scikit-learn, PyTorch, or TensorFlow
- **Database:** PostgreSQL (shared with other FRAMES apps)
- **Visualization:** D3.js for molecular-style visualizations
- **API:** RESTful API for predictions

## Database Schema (Planned)

Will use existing tables:
- `factor_models` - Trained prediction models
- `model_factors` - Factors included in each model
- `model_validations` - Model performance metrics
- `risk_factors` - Input data for predictions
- `factor_values` - Historical factor measurements
- `outcomes` - Mission success outcomes for training

May add new tables:
- `predictions` - Stored prediction results
- `prediction_explanations` - Interpretable AI explanations
- `factor_interactions` - Measured interactions between factors

## Research Foundation

Based on Dr. Osborn's research in:
- Complex systems modeling
- Team dynamics analysis
- Risk factor assessment in engineering projects
- Multi-university collaboration patterns

## Development Phases (Future)

### Phase 1: Research & Design (4-6 weeks)
- Literature review on NDA applications
- Framework architecture design
- Data requirements analysis
- Model selection and validation approach

### Phase 2: Core Framework (8-10 weeks)
- Implement NDA framework
- Build factor interaction engine
- Create energy state calculator
- Develop visualization tools

### Phase 3: Machine Learning (6-8 weeks)
- Collect historical training data
- Train prediction models
- Validate model accuracy
- Fine-tune hyperparameters

### Phase 4: Integration (4-6 weeks)
- Build REST API
- Integrate with research-analytics
- Create prediction dashboards
- Deploy to production

## Getting Started (When Built)

```bash
cd apps/ai-core
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python backend/app.py
```

## Documentation

Planning documents available in:
- `../../docs/ai-prediction-core/NDA_FRAMEWORK.md` (to be created)
- `../../docs/ai-prediction-core/ARCHITECTURE.md` (to be created)

## Example Use Cases

1. **Pre-Mission Assessment:**
   - Input: Team composition, university mix, project type
   - Output: Success probability, risk factors to monitor

2. **Mid-Mission Intervention:**
   - Input: Current team metrics, communication patterns
   - Output: Recommended interventions, factor adjustments

3. **Post-Mission Analysis:**
   - Input: Final outcomes, team journey data
   - Output: Lessons learned, best practices identified

4. **Team Optimization:**
   - Input: Available students, skills, universities
   - Output: Optimal team configurations for success

## Current Status

- [ ] Framework research and design
- [ ] NDA implementation
- [ ] Factor interaction engine
- [ ] Energy modeling
- [ ] ML model development
- [ ] API development
- [ ] Integration with analytics
- [ ] Visualization tools
- [ ] Testing and validation
- [ ] Deployment

## Future Enhancements

- Real-time prediction updates
- Automated alert system
- Mobile app for predictions
- Interactive what-if scenarios
- Explainable AI interface
- Integration with student onboarding data

## Contact

Elizabeth Osborn, Ph.D. - eosborn@cpp.edu
California State Polytechnic University, Pomona
