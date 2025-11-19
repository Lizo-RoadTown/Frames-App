# FRAMES Research Dashboard

## Overview

The **Research Dashboard** is a powerful tool for configuring, testing, and validating the knowledge transfer risk model that drives the FRAMES visualization system. Unlike the Operations Dashboard (which is for program managers to view their university's data), the Research Dashboard gives the researcher full control over:

- **Risk Factor Configuration**: Define new factors that contribute to knowledge loss
- **Factor Weighting**: Adjust how much each factor impacts energy calculations
- **Model Creation & Testing**: Create multiple predictive models and compare their accuracy
- **Cross-University Analysis**: Access the complete database across all universities
- **Validation & Refinement**: Compare model predictions against actual outcomes

## Key Concept: Flexible, Research-Driven Modeling

The core innovation of this system is that **nothing is hardcoded**. The energy loss calculations are based on a flexible factor model where:

1. **Factors are configurable**: Add, remove, or modify risk factors as your research evolves
2. **Weights are adjustable**: Test different weightings to find which best predict outcomes
3. **Models are comparative**: Run multiple models side-by-side to see which performs best
4. **Historical tracking**: All changes are logged so you can trace how your understanding evolved

## Architecture

### Database Schema

#### Core Tables

**`risk_factors`** - Defines what variables matter for knowledge transfer
- `factor_name`: Machine-readable identifier (e.g., "knowledge_type")
- `display_name`: Human-readable label (e.g., "Knowledge Type")
- `category`: Grouping (e.g., "NDA_Dimension", "Interface_Property")
- `confidence_level`: Research maturity ("established", "provisional", "exploratory")
- `active`: Whether this factor is currently in use

**`factor_values`** - Possible values for each factor
- `factor_id`: Which factor this belongs to
- `value_name`: Machine-readable (e.g., "codified")
- `display_name`: Human-readable (e.g., "Codified Knowledge")
- `energy_loss_contribution`: Base contribution to energy loss (0.0 to 1.0)

**`factor_models`** - Different theoretical models being tested
- `model_name`: Unique identifier
- `is_active`: Only one model can be active at a time (used by Operations Dashboard)
- `is_baseline`: Baseline model for comparison
- `hypothesis`: What this model is testing
- `validation_status`: "testing", "validated", "rejected"

**`model_factors`** - Links models to factors with specific weights
- `model_id`: Which model
- `factor_id`: Which factor
- `weight`: Multiplier for this factor (1.0 = normal, <1.0 = reduced, >1.0 = increased)
- `enabled`: Whether this factor is active in this model

**`interface_factor_values`** - Assigns factor values to actual interfaces
- `interface_id`: The connection between entities
- `factor_id`: Which factor
- `factor_value_id`: Which value this interface has for this factor

### Energy Calculation Engine

Located in `backend/energy_engine.py`, the `EnergyCalculationEngine` class:

```python
def calculate_interface_energy_loss(interface_id, model_id):
    # 1. Get all factor values assigned to this interface
    # 2. Get the weights for those factors in the specified model
    # 3. Calculate: sum(factor_contribution * model_weight)
    # 4. Return energy loss (0.0 to 1.0)
```

**Example Calculation:**

Given an interface with:
- Knowledge Type = "institutional" (base contribution: 0.40)
- Bond Strength = "weak" (base contribution: 0.35)

In Model A (weights: knowledge_type=1.0, bond_strength=1.0):
```
Energy Loss = (0.40 × 1.0) + (0.35 × 1.0) = 0.75 (75%)
```

In Model B (weights: knowledge_type=1.5, bond_strength=0.5):
```
Energy Loss = (0.40 × 1.5) + (0.35 × 0.5) = 0.775 (77.5%)
```

This allows you to test which weighting best predicts actual knowledge loss.

## Research Workflow

### Phase 1: Establish Baseline

1. **Start with NDA Theory**: The system comes with baseline factors from Nearly Decomposable Architecture theory:
   - Knowledge Type (codified vs. institutional)
   - Bond Strength (strong, moderate, weak)
   - Temporal Alignment (aligned vs. misaligned)
   - Actor Autonomy (high vs. low)

2. **Create Baseline Model**: A default model is created with all factors weighted equally (weight = 1.0)

3. **Migrate Legacy Data**: Use the migration endpoint to auto-assign factors to existing interfaces based on their `bond_type`

### Phase 2: Discover New Factors

As your research progresses, you may discover new factors that matter:

**Example: Communication Frequency**
```json
{
  "factor_name": "communication_frequency",
  "display_name": "Communication Frequency",
  "category": "Interface_Property",
  "confidence_level": "provisional",
  "values": [
    {
      "value_name": "daily",
      "display_name": "Daily Communication",
      "energy_loss_contribution": 0.05
    },
    {
      "value_name": "weekly",
      "display_name": "Weekly Communication",
      "energy_loss_contribution": 0.15
    },
    {
      "value_name": "monthly",
      "display_name": "Monthly or Less",
      "energy_loss_contribution": 0.30
    }
  ]
}
```

### Phase 3: Test Different Models

Create multiple models with different hypotheses:

**Model: "Knowledge-Dominant"**
- Hypothesis: "Knowledge type is the primary predictor of transfer success"
- Weights: knowledge_type=2.0, bond_strength=0.5, communication_frequency=0.5

**Model: "Relationship-Dominant"**
- Hypothesis: "Bond strength and communication matter more than knowledge type"
- Weights: knowledge_type=0.5, bond_strength=2.0, communication_frequency=1.5

**Model: "Balanced"**
- Hypothesis: "All factors contribute equally"
- Weights: All factors = 1.0

### Phase 4: Validate & Refine

1. **Run all models** against the same dataset
2. **Compare predictions** to actual outcomes (from `outcomes` table)
3. **Identify which model** most accurately predicts knowledge loss
4. **Refine weights** based on results
5. **Iterate**

## API Endpoints

### Factor Management

**GET /api/research/factors**
- Returns all active risk factors with their values

**POST /api/research/factors**
- Create a new risk factor
```json
{
  "factor_name": "team_overlap_duration",
  "display_name": "Team Overlap Duration",
  "description": "How long incoming and outgoing teams worked together",
  "category": "Temporal_Property",
  "confidence_level": "exploratory",
  "values": [
    {"value_name": "none", "display_name": "No Overlap", "energy_loss_contribution": 0.50},
    {"value_name": "one_term", "display_name": "One Term", "energy_loss_contribution": 0.25},
    {"value_name": "two_terms", "display_name": "Two+ Terms", "energy_loss_contribution": 0.10}
  ]
}
```

**PUT /api/research/factors/:id**
- Update an existing factor (description, confidence level, research notes)

### Model Management

**GET /api/research/models**
- Returns all factor models with their factor weights

**POST /api/research/models**
- Create a new model
```json
{
  "model_name": "hypothesis_3_communication",
  "display_name": "Communication-Centric Model v3",
  "hypothesis": "Communication frequency is the strongest predictor when controlling for knowledge type",
  "is_active": false,
  "factors": [
    {"factor_id": 1, "weight": 1.0, "enabled": true},
    {"factor_id": 2, "weight": 2.5, "enabled": true},
    {"factor_id": 3, "weight": 0.8, "enabled": true}
  ]
}
```

**POST /api/research/models/:id/activate**
- Set a model as the active model (used by Operations Dashboard)

**PUT /api/research/models/:model_id/factors/:factor_id/weight**
- Adjust a single factor's weight in a model
```json
{
  "weight": 1.75
}
```

### Energy Calculation

**GET /api/research/energy/interface/:id?model_id=X**
- Calculate energy loss for a specific interface using a specific model
- Returns detailed breakdown of how each factor contributed

**GET /api/research/energy/network?university_id=X&model_id=Y**
- Calculate energy loss across entire network (or filtered by university)
- Returns aggregated statistics and per-interface results

**POST /api/research/interface/:id/factors**
- Assign factor values to an interface
```json
{
  "factors": [
    {"factor_id": 1, "factor_value_id": 2},
    {"factor_id": 2, "factor_value_id": 5}
  ]
}
```

**POST /api/research/migrate-legacy-interfaces**
- Auto-migrate all legacy interfaces to use the factor system
- Returns count of migrated/failed

### Model Comparison

**POST /api/research/compare-models**
- Run multiple models on the same dataset and compare results
```json
{
  "model_ids": [1, 2, 3],
  "university_id": "CalPolyPomona"
}
```

Returns comparison of average energy loss, risk distribution, etc. for each model.

## Research Dashboard UI (To Be Built)

The Research Dashboard will have these sections:

### 1. Factor Library
- **Table view** of all risk factors
- **Add Factor** button with form
- **Edit Factor** to update confidence level, description, notes
- **Factor Values** expandable to show/edit values and their contributions
- **Category filters** to group factors by type

### 2. Model Builder
- **Model list** with active/baseline indicators
- **Create Model** wizard:
  - Name and hypothesis
  - Select factors to include
  - Set initial weights with sliders
- **Weight Tuner**: Interactive sliders to adjust factor weights
- **Clone Model** to create variations
- **Activate Model** to deploy to Operations Dashboard

### 3. Energy Calculator
- **Interface Search**: Find specific interfaces
- **Calculate Energy**: Run calculation with selected model
- **Factor Breakdown**: Visual breakdown showing contribution of each factor
- **Network Analysis**: Calculate for entire university or cross-university

### 4. Model Comparison Lab
- **Select Models**: Checkbox to pick 2-5 models
- **Run Comparison**: Calculate energy across same dataset
- **Results Table**: Side-by-side comparison of:
  - Average energy loss
  - Risk distribution (low/moderate/high/critical)
  - Specific interface differences
- **Export Results**: Download CSV for analysis

### 5. Validation Dashboard
- **Outcome Tracking**: Link predictions to actual outcomes
- **Accuracy Metrics**: Show which models predicted best
- **Confidence Intervals**: Statistical validation
- **Research Notes**: Document findings and insights

## Integration with Operations Dashboard

The Operations Dashboard (`/dashboard`) uses the **active model** to display energy-based visualizations:

1. **Energy Loss Calculation**: Uses `EnergyCalculationEngine` with `is_active=True` model
2. **Color Coding**: Edges colored based on energy loss (green = low, red = high)
3. **Particle Animations**: Flow speed/density reflects knowledge transfer health
4. **What-If Scenarios**: When user drags nodes, recalculate with hypothetical changes

The researcher can:
- Test new models in Research Dashboard
- When confident, set model as active
- Operations users immediately see updated visualizations
- Compare old vs. new model predictions

## Use Cases

### Use Case 1: Testing "Overlap Duration" Hypothesis

**Research Question**: Does longer team overlap reduce knowledge loss?

**Steps**:
1. Create new factor: `team_overlap_duration`
2. Assign values to interfaces based on actual overlap data
3. Create two models:
   - Model A: Without overlap factor (baseline)
   - Model B: With overlap factor (weight = 1.5)
4. Compare predictions
5. Validate against actual graduation outcomes
6. If Model B is more accurate, keep the factor and refine weight

### Use Case 2: Cross-University Comparison

**Research Question**: Do cross-university interfaces have higher knowledge loss?

**Steps**:
1. Use existing `is_cross_university` field from interfaces
2. Calculate network energy for each university separately
3. Calculate energy for cross-university interfaces only
4. Compare averages
5. If significantly different, create factor for university boundary crossing

### Use Case 3: Temporal Evolution Tracking

**Research Question**: How do programs improve over time?

**Steps**:
1. Snapshot energy calculations at different time points
2. Track how factor values change (e.g., bond strength improving)
3. Correlate with program interventions
4. Identify which interventions reduce energy loss most effectively

## Future Enhancements

### Machine Learning Integration
- Train ML models using factor data as features
- Auto-suggest factor weights based on outcome data
- Anomaly detection for unusual interfaces

### Predictive Analytics
- Forecast future knowledge loss based on current trends
- Alert when interfaces are deteriorating
- Recommend interventions

### External Data Integration
- Pull communication data from Discord/Slack
- Import task completion from project management tools
- Correlate with academic performance data

## Technical Notes

### Performance Considerations
- Factor calculations are cached where possible
- Use database indexes on `interface_factor_values` for fast lookups
- Batch calculations for network-level analysis

### Data Integrity
- Foreign key constraints ensure factor assignments reference valid factors/values
- Audit logging tracks all model changes
- Soft deletes (active=False) preserve historical data

### Extensibility
- Factor categories are extensible (add new categories as research evolves)
- `meta` JSON fields on all tables allow storing arbitrary research data
- Model validation framework supports custom metrics

## Accessing the Research Dashboard

**URL**: `/research`

**Authentication**: (To be added) - Should be restricted to researcher only

**Data Access**: Full cross-university access to all tables

## Support & Questions

This is a living research system. As you discover new factors, develop new hypotheses, or need new features, the architecture supports extension without requiring code changes to the core calculation engine.

For technical questions, refer to:
- `backend/db_models.py` - Database schema
- `backend/energy_engine.py` - Calculation logic
- `backend/app.py` - API endpoints (lines 1623-1976)
