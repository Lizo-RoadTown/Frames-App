# CADENCE Team Dashboard Content
## Ready to paste into each team dashboard after the divider (---)

---

## 1. Avionics & Flight Software Dashboard

### Team Overview

**Mission:** The Avionics & Flight Software team designs and integrates the spacecraft's core hardware and flight software systems, focusing on radiation-hardened computing, sensor integration, and onboard data processing capabilities.

### Team Roster

**Team Lead:** Pragun

**Team Members:**
- Michael Pham - Systems Engineer
- Zach Karazin - PCB Design / CMOS Integration
- Ibrahim Elsousi - CosmicWatch Payload Integration
- William - PCB Design
- Anthony S - Radiation Analysis
- Johann - Hardware Engineering

### Active Projects

- **CosmicWatch Payload Board PCB v1** - Custom PCB design for muon detector integration
- **Baby CADENCE Prototype** - 2U satellite prototype for SmallSat 2025 demonstration
- **CMOS Image Sensor Trade Study** - Evaluating sensor options for space imaging (Lucid Phoenix 5.0 MP IMX568)
- **Component Selection** - iMX8x OBC with ECC memory, radiation-tolerant systems
- **NO BACKPLANE Architecture** - Direct SOM integration approach for Baby CADENCE
- **Electrical ICD Development** - Interface Control Documents for subsystem integration
- **Space-Grade Avionics Research** - Commercial COTS component evaluation for radiation environment

### Key Responsibilities

- Onboard computer (OBC) selection and integration
- Sensor systems (CMOS, IMU, radiation detectors)
- PCB design and manufacturing coordination
- Power budget analysis (2.5W typical, 3.1W max for imaging)
- Radiation shielding design (aluminum enclosures for sensitive components)
- Electrical interface definitions (RS-422, I2C, SPI)
- Component procurement and testing

### Technical Focus Areas

- **Computing Platform:** PhyCORE iMX8x SOM with ECC memory
- **Imaging:** CMOS image sensor connectivity and power management
- **Radiation:** RadFET integration, shielding strategies, commercial COTS resilience
- **Interfaces:** Gecko connectors (G125-MH10605M4P for RS-422, G125-MH10605L3P for RADFET boards)
- **Integration:** NO BACKPLANE approach - direct connections to SOM
- **Payload:** CosmicWatch muon detector hardware/software interface

---

## 2. Communications & RF Dashboard

### Team Overview

**Mission:** The Communications & RF team develops the satellite's communication systems, including ground station infrastructure, link budget analysis, antenna design, and Software Defined Radio (SDR) implementation for reliable data transmission.

### Team Roster

**Team Lead:** Tri Do

**Team Members:**
- Bryton King - Link Budget Analysis
- Kaushik Veli - Antenna Design / Pointing Budget
- Lukas Sandau - GNU Radio Development

### Active Projects

- **GNU Radio Ground Station** - Virtual modeling and SDR implementation
- **Link Budget Analysis** - Orbital pass calculations and communication link performance
- **Antenna Trade Study** - Evaluating antenna options for mission requirements
- **Amateur Radio Licensing** - Team certification for ground station operations
- **Ground Station Rebuild** - 2.4m dish infrastructure upgrade
- **Pointing Budget** - Engineering datalink pointing requirements and accuracy
- **SatNOGS-COMMS SDR** - Open-source ground station software integration

### Key Responsibilities

- Communication link design and analysis
- Ground station hardware and software development
- RF system design and testing
- Link budget modeling (uplink/downlink)
- Antenna selection and integration
- SDR programming and configuration
- Amateur radio operations coordination

### Technical Focus Areas

- **Ground Station:** GNU Radio SDR platform, SatNOGS-COMMS integration
- **Link Analysis:** Orbital pass modeling, signal budget calculations
- **Hardware:** 2.4m dish antenna, RF transceivers, Orion B16 GNSS/GPS
- **Software:** GNU Radio flowgraphs, FSK demodulation, link budget tools
- **Standards:** Amateur radio compliance, NASA SOA communications

---

## 3. Power and Energy Systems Dashboard

### Team Overview

**Mission:** The Power and Energy Systems team designs the satellite's electrical power system, including solar arrays, battery management, power distribution, and energy budget modeling for all mission phases.

### Team Roster

**Team Lead:** Naomi

**Team Members:**
- Brandon Chie - Schematics and PCB Design
- Braeden Fontejon - Power Systems Analysis
- Michael - Battery Board Support

### Active Projects

- **Solar Panel Selection** - Array sizing and panel selection for orbital requirements
- **Battery Board Design** - LG INR18650 cell integration for 2U constraints
- **Power Budget Modeling** - Energy balance for charging/nominal/eclipse/payload modes
- **Baby CADENCE Power System** - Power subsystem coordination for 2U prototype
- **Average Power Analysis** - Realistic energy consumption modeling

### Key Responsibilities

- Solar array design and sizing
- Battery system design and management
- Power budget development and tracking
- Power distribution architecture
- Energy storage analysis
- Component selection (solar cells, batteries, regulators)
- Power system testing and validation

### Technical Focus Areas

- **Solar:** Panel selection, array configuration, power generation modeling
- **Energy Storage:** LG INR18650 batteries, 2U form factor constraints
- **Power Budget:** Multi-mode analysis (charging, nominal, eclipse, payload)
- **Distribution:** Power conditioning, regulation, fault protection
- **Integration:** Baby CADENCE power subsystem coordination

---

## 4. Structures and Mechanical Dashboard

### Team Overview

**Mission:** The Structures and Mechanical team develops the physical spacecraft structure, including CAD modeling, mechanical design, component mounting solutions, and mass budget management for multiple CubeSat form factors.

### Team Roster

**Team Lead:** Giselle Revolorio

**Team Members:**
- Ben Mudgett - Structural Analysis
- Ethan Guzman - CAD Design
- Michael P. Hawkins - CAD Mentor
- Harrison Chung - CAD Development
- Alex Martinez - CAD Development
- Christopher Huizar - CAD/Thermal Integration
- Javier A. Martinez Montoya - Structures/Mission Ops

### Active Projects

- **2U Structure for Baby CADENCE** - SmallSat 2025 priority structure design
- **12U CAD Model** - Preliminary Big CADENCE structure
- **CAD Practice Task** - 1U BLADE mission modeling exercise
- **Sheet Metal Design** - Bend radii optimization, Fabworks/Onshape integration
- **Structural ICD** - Interface Control Documentation for subsystem integration
- **Component Mounting** - Bracket design, PC104 stack integration
- **Mass Budget Tracking** - Component mass accounting and balance analysis

### Key Responsibilities

- CAD modeling and design (2U, 12U, and other form factors)
- Structural analysis and verification
- Component mounting solutions
- Mass budget management
- Interface Control Documentation (ICD)
- Sheet metal fabrication design
- Integration with thermal and other subsystems

### Technical Focus Areas

- **CAD Tools:** Onshape, Fabworks for sheet metal
- **Form Factors:** 2U (Baby CADENCE priority), 12U (Big CADENCE), 1U (practice)
- **Standards:** PC104 stacking, CubeSat design specification
- **Integration:** Thermal interfaces, component mounting, mass balance
- **Manufacturing:** Sheet metal bend radii, fabrication constraints

---

## 5. Thermal Systems Dashboard

### Team Overview

**Mission:** The Thermal Systems team develops thermal control systems and analysis models to maintain spacecraft components within operational temperature ranges across all mission phases and orbital conditions.

### Team Roster

**Team Lead:** CJ

**Team Members:**
- Alex - Thermal Analysis
- Ceir - Thermal Modeling
- Christopher Huizar - Thermal/Structures Integration

### Active Projects

- **Preliminary Thermal Model** - PDR (Preliminary Design Review) thermal analysis
- **Thermal Desktop Modeling** - Professional thermal analysis software implementation (license obtained Tuesday)
- **One Thermal Node Analysis** - PMR analysis on 12U configuration
- **Elementary 1U Thermal System** - Baseline thermal control for small form factor
- **Multi-Formfactor Systems** - Detailed analysis for 2U/3U/6U/12U configurations
- **CAD to Thermal Conversion** - Converting mechanical models to thermal analysis models
- **Passive and Active Heating Methods** - Exploring thermal control options

### Key Responsibilities

- Thermal analysis and modeling
- Temperature prediction for all mission phases
- Thermal control system design
- CAD integration for thermal models
- Passive thermal design (coatings, insulation)
- Active thermal control evaluation (heaters)
- Multi-formfactor thermal analysis

### Technical Focus Areas

- **Software:** Thermal Desktop (recently acquired license)
- **Analysis:** Single-node and multi-node thermal modeling
- **Form Factors:** 1U baseline, 2U/3U/6U/12U detailed systems
- **Methods:** Passive (coatings, MLI) and active (heaters) thermal control
- **Integration:** CAD model conversion, structures coordination

---

## 6. Flight Software Dashboard

### Team Overview

**Mission:** The Flight Software team develops the onboard software architecture, integrating F-Prime framework components, payload software, and system-level control for autonomous spacecraft operations.

### Team Roster

**Team Lead:** Kai (GitHub Admin)

**Team Members:**
- Ella Shepherd - FSW Lead Developer
- Lukas Sandau - FSW Developer / Comms Crossover

### Active Projects

- **F-Prime Integration** - CircuitPython to F-Prime conversion and framework adoption
- **Baby CADENCE Preliminary Software** - Flight software for 2U prototype
- **CosmicWatch Payload Software** - Python implementation for RP2040 muon detector
- **System Architecture Block Diagram** - Software architecture documentation
- **Software Design Document (SDD)** - MEDOS and F-Prime architecture documentation
- **Data Collection Loop** - CircuitPython sensor data acquisition
- **On-Command Data Display** - Beaconing and state of health (SoH) telemetry
- **F-Prime Sensor Notifications** - Event-driven sensor monitoring
- **PROVES CircuitPython Study** - Reference mission software analysis

### Key Responsibilities

- Flight software architecture design
- F-Prime framework implementation
- Payload software integration
- CircuitPython development for embedded systems
- GitHub repository management
- Software documentation (SDD, architecture diagrams)
- Sensor data collection and processing
- Telemetry and command handling

### Technical Focus Areas

- **Framework:** F-Prime (NASA JPL flight software framework)
- **Languages:** Python, CircuitPython for RP2040/RP2350
- **Payload:** CosmicWatch muon detector software interface
- **Architecture:** MEDOS integration, component-based design
- **Data Flow:** Sensor collection loops, telemetry beaconing, SoH monitoring
- **Version Control:** GitHub administration and workflow

---

## 7. Mission Operations Dashboard

### Team Overview

**Mission:** The Mission Operations team plans and analyzes the satellite's orbital mission, including GMAT orbital simulations, mission planning, pass scheduling, and space weather anomaly detection strategy.

### Team Roster

**Team Lead:** Javier (also Structures)

**Team Members:**
- Jordy Samaniego - Orbital Analysis
- Alex Ammon - Mission Planning
- Angel R - Operations Support

### Active Projects

- **GMAT Orbital Simulations** - Calculate nominal mission parameters and TBD values
- **IEEE Paper Preparation** - Potential SmallSat 2025 submission (pending simulation completion)
- **Mission Operations Plan** - CDR (Critical Design Review) deliverable
- **Orbit Description** - Polar LEO for space weather anomaly detection
- **Pass Scheduling** - Contact window analysis, >2 passes/day requirement
- **Chaos Model Documentation** - GMAT region overlays for space weather

### Key Responsibilities

- Orbital mechanics analysis and simulation
- Mission timeline planning
- Ground station pass scheduling
- Mission requirements documentation
- Space weather monitoring strategy
- Conference paper preparation
- GMAT simulation development

### Technical Focus Areas

- **Software:** GMAT (General Mission Analysis Tool)
- **Orbit:** Polar Low Earth Orbit (LEO) for anomaly detection
- **Analysis:** Pass scheduling, contact windows, ground track
- **Mission:** Space weather anomaly detection over South Atlantic Anomaly
- **Requirements:** Minimum 2 passes/day contact frequency
- **Documentation:** Mission Ops plan (CDR deliverable), IEEE paper

---

## 8. Payload Software Integrations Dashboard

### Team Overview

**Mission:** The Payload Software Integrations team develops and integrates payload-specific software, focusing on CosmicWatch muon detector and Cygnet payload systems using F-Prime components and CircuitPython for embedded development.

### Team Roster

**Core Focus Areas:**
- CosmicWatch integration lead
- F-Prime components specialist
- CircuitPython embedded developer

### Active Projects

- **CosmicWatch Integration** - Muon detector hardware/software interface
- **Cygnet Payload Software** - F-Prime components discussion and implementation
- **CircuitPython Practice** - RP2040/RP2350 embedded development
- **F-Prime Tutorials and Workshops** - Framework learning and implementation
- **Circuit Python Practice** - Embedded development for payload processors
- **Radiation Dose Rate Accumulation** - South Atlantic Anomaly data collection

### Key Responsibilities

- Payload software architecture
- Hardware/software interface development
- F-Prime component integration for payloads
- CircuitPython embedded programming
- Muon detector data processing
- Radiation measurement software
- Payload testing and validation

### Technical Focus Areas

- **Payloads:** CosmicWatch muon detector, Cygnet payload system
- **Framework:** F-Prime component architecture for payloads
- **Languages:** CircuitPython for RP2040/RP2350 microcontrollers
- **Science:** Radiation dose rate accumulation, South Atlantic Anomaly detection
- **Integration:** Hardware/software interface design, data collection pipelines
- **Development:** Embedded systems programming, component-based architecture

---

## Instructions for Use

1. Navigate to each team dashboard in Notion
2. Scroll down to the divider (horizontal line) after the databases
3. Click below the divider to add content
4. Copy and paste the relevant team section from above
5. Format as needed using Notion's formatting tools:
   - Use "Callout" block for Team Overview (Mission statement)
   - Use headings (## or ###) for section titles
   - Use bullet lists for team members, projects, and responsibilities
   - Bold (**text**) for emphasis on roles and key terms

## Next Steps - Subpages

After populating dashboard content, consider populating the three subpages for each team:

### OKR Tracker Subpage
- Add team-specific Objectives and Key Results
- Align with active projects listed above
- Track progress on deliverables (PDR, CDR, SmallSat 2025)

### Documents Subpage
- Add links to technical documents (ICDs, trade studies, analyses)
- Include relevant meeting notes and design documents
- Link to external resources (datasheets, reference docs)

### Team Member Dashboard
- Customize with individual team member cards/profiles
- Include roles, responsibilities, and contact info
