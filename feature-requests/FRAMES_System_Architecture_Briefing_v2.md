# FRAMES System: Complete Architecture Briefing (v2)

## Document Purpose

This briefing provides the full scope of the FRAMES system evolution. You (the implementing agent) should read this completely before making any architectural decisions. The system is being built iteratively, but you need to understand the end state to make good decisions now.

---

## Table of Contents

1. [Current State](#current-state)
2. [Target State](#target-state)
3. [Theoretical Foundation](#theoretical-foundation)
4. [Core Concepts](#core-concepts)
5. [Data Architecture](#data-architecture)
6. [System Components](#system-components)
7. [Integration Points](#integration-points)
8. [The Iterative Discovery Process](#the-iterative-discovery-process)
9. [Implementation Sequence](#implementation-sequence)
10. [Decision Points Requiring Human Input](#decision-points-requiring-human-input)
11. [Technical Constraints](#technical-constraints)

---

## Current State

### What Exists

**File: `index.html`** - A single-page visualization tool with:
- Form-based creation of teams, faculty, projects
- Interface definition with bond types (codified-strong, institutional-weak, etc.)
- Fixed energy-loss values (5%, 15%, 35%, 60%)
- Molecular visualization with animated energy particles
- Static metrics (energy flow efficiency, decomposition risk)

**Data structures** (in JavaScript):
```javascript
let teams = [];        // {id, discipline, lifecycle, name, size, experience, description}
let faculty = [];      // {id, name, role, description}
let projects = [];     // {id, name, type, description}
let interfaces = [];   // {id, from, to, interfaceType, bondType, energyLoss}
```

### Limitations of Current State

- Single organization only
- Fixed categories and coefficients
- No persistence (data lost on refresh)
- No real-time data input
- No learning or adaptation
- Visualization is display-only (not bidirectional)

---

## Target State

### End Vision

A **multi-university research instrument** that:

1. **Connects 8 universities** with shared visibility into cross-institutional interfaces
2. **Captures real-time data** from Discord interactions
3. **Discovers patterns** through iterative observation
4. **Evolves its own schema** as new categories and layers are identified
5. **Learns coefficients** through embedded AI analyzing outcomes
6. **Enables bidirectional interaction** where visualization changes modify underlying data
7. **Supports two modes**: Operations (per-university dashboard) and Research (cross-university analysis)
8. **Predicts mission and program success** based on interface characteristics

### Key Architectural Shifts

| Aspect | Current | Target |
|--------|---------|--------|
| Scope | 1 university | 8 universities |
| Data persistence | None (JS arrays) | Database with versioning |
| Categories | Fixed (4 bond types) | Extensible, discovered from data |
| Coefficients | Hardcoded | Learned by AI |
| Data input | Manual forms | Manual + Discord automation |
| Visualization | Display only | Bidirectional (drag = edit) |
| Updates | Static | Real-time sync across users |
| Matrix type | Single DSM | Multi-Domain Matrix (MDM) |

---

## Theoretical Foundation

### System Classification

FRAMES is a **Multi-Domain Matrix (MDM)** system as defined by Maurer (2007) and Browning (2016). It integrates:

**Design Structure Matrices (DSMs):**
- Organization DSM: Universities, teams, faculty, individuals and their relationships
- Process DSM: Projects, missions, activities with temporal dependencies

**Domain Mapping Matrices (DMMs):**
- Person-to-Project: Who works on what
- Team-to-University: Team membership
- Project-to-University: Which projects belong where
- Cross-university collaboration mappings

### Matrix Convention

The system uses the **"inputs in columns" (IC) convention**:
- Row element receives from column element
- source_node provides to target_node
- Example: An edge from `TexasState.Software` to `Columbia.CommsRF` means Texas State's Software team provides knowledge/output to Columbia's CommsRF team

This convention must be maintained consistently throughout all visualizations and analyses.

### Prediction Model

The system builds toward a predictive model for knowledge transfer failure:

**Level 1 - Mission Success:**
- Payload successfully launched
- Proposal accepted
- Contract fulfilled

**Level 2 - Program Persistence:**
- Successful generational knowledge transfer
- Subsequent cohort achieves mission-level success
- Program continues beyond founding generation

The prediction formula will take the form:
```
P(failure) = f(actor_autonomy, partitioned_knowledge, emergent_outputs, 
               temporal_misalignment, integration_cost, coupling_degradation,
               knowledge_type, [discovered_layers...])
```

Where coefficients are learned from outcome data across all participating universities.

---

## Core Concepts

### Nearly Decomposable Architecture (NDA)

The theoretical foundation from Herbert Simon (1962). Complex systems are composed of:
- **Modules**: Semi-autonomous units (universities, teams, projects)
- **Interfaces**: Connection points between modules where knowledge/resources transfer
- **Couplings**: Strength of connections (strong internally, weaker externally)

Key insight: Weaker external bonds can erode if not reinforced, leading to system fragmentation.

### Six NDA Diagnostic Dimensions

Every interface is assessed across these dimensions:

1. **Actor autonomy**: Degree of independent operation; conflicting objectives between connected modules
2. **Partitioned knowledge domains**: Knowledge siloing; specialization gaps that impede transfer
3. **Emergent/ambiguous outputs**: Shifting or undefined goals that make transfer targets unclear
4. **Temporal misalignment**: Timing differences (academic calendar vs. project needs, cohort cycles vs. mission timelines)
5. **Integration cost**: Effort required to coordinate and synthesize work across the interface
6. **Coupling degradation**: Weakening of relationships over time without active reinforcement

### Knowledge Type Risk

Base risk classification for each interface:
- **Institutional knowledge**: High risk (tacit, held by individuals, lost when they leave)
- **Codified knowledge**: Low risk (documented, transferable independent of individuals)
- **Mixed**: Contains both types with different risk profiles

### Organizational Hierarchy

```
University (e.g., Texas State)
  ├── Project A (internal mission)
  ├── Project B (internal mission)
  ├── Project C (collaborative inter-university mission)
  └── Project D (internal mission)
       ├── Team (Software)
       ├── Team (CommsRF)
       └── Team (MissionOps)
            ├── Individual (incoming)
            ├── Individual (established)
            └── Individual (outgoing)
```

**Key structural points:**
- Each university has multiple projects
- One project per university is the inter-university collaborative (connects to partner universities)
- Teams work across projects within their university
- Knowledge flows across internal projects—this must be tracked to understand actual knowledge topology

### Intergenerational Cohort Structure

Three temporal positions exist simultaneously in healthy programs:

- **Incoming**: New to the project, being onboarded
- **Established/Current**: Actively working, holding operational knowledge
- **Outgoing**: Graduating, transferring knowledge before departure

This creates multiple interface types:
- **Outgoing → Established**: Senior members transferring leadership and deep context
- **Established → Incoming**: Active members onboarding new members
- **Outgoing → Incoming**: Direct transfer (risky—skips context holders)

**Diagnostic indicator**: The presence or absence of each position signals program health:
- All three present with documented handoffs → lower risk
- Outgoing present, established absent, incoming present → high risk (context stripping)
- Outgoing absent, established present, incoming present → moderate risk (loss of historical rationale)

### Interface Categories

1. **Intergenerational interfaces** (within project): Knowledge transfer across cohort generations
2. **Concurrent interfaces** (within university): Parallel teams/projects sharing resources and knowledge
3. **Cross-university interfaces** (between universities): Collaborative network providing mutual support and resilience

Cross-university interfaces serve different functions than internal ones:
- Redundant expertise (if your expert graduates, partner university can consult)
- Institutional memory beyond any single university's cohort cycle
- Shared documentation repositories
- External validation and review

### The Matrix

A directed graph rendered as an MDM where:
- **Nodes** = universities, projects, teams, faculty, individuals, external partners
- **Edges** = directed interfaces showing knowledge/task flow

Example edges:
```
TexasState.Software → TexasState.MissionOps (internal code handoff)
TexasState.Faculty.Advisor → Columbia.Faculty.Advisor (cross-university coordination)
Columbia.PROVES.Lead → TexasState.PROVES.Lead (collaborative project interface)
```

### Layers and Categories

Each edge is assessed through multiple **layers**. Each layer contains **categories**.

**Critical concept**: Categories are NOT fixed. They are discovered through observation of Discord data and outcomes. The system must support adding new layers and categories without code changes.

**Category confidence levels:**
- **Established**: High confidence, validated by outcomes
- **Provisional**: Moderate confidence, consistent with observations
- **Emergent**: Low confidence, newly identified pattern

### Iterative Discovery

The research methodology:
```
Observe data → Notice patterns → Create category → Apply across edges → 
Observe outcomes → Refine categories (split, merge, promote, deprecate) →
Notice category clusters → May reveal new layer → Repeat
```

Example progression:
1. Initial category: "after" (transfer happens late)
2. Observation: Some "after" transfers succeed, others fail
3. Discovery: New category "rushed" (late AND compressed time)
4. Validation: "rushed" correlates with failure; "after-deliberate" does not
5. Further observation: "rushed" appears across multiple dimensions
6. Discovery: "Transfer quality" becomes new layer with categories: rushed, deliberate, iterative, fragmented

---

## Data Architecture

### Node Schema

```javascript
{
  node_id: "TexasState.Software.JohnDoe",
  university_id: "TexasState",
  node_type: "individual",  // university | project | team | faculty | individual | external
  
  // Hierarchy
  parent_node: "TexasState.Software",
  
  // Type-specific attributes
  attributes: {
    // For individuals:
    lifecycle_stage: "established",  // incoming | established | outgoing
    join_date: "2024-09-01",
    expected_departure: "2026-05-15",
    
    // For teams:
    discipline: "software",
    size: 5,
    experience_months: 18,

 (file continues...)
