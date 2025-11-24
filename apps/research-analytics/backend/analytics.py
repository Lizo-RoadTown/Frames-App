"""
Analytics and diagnostic functions for FRAMES
Ported from JavaScript to Python
"""

from typing import Dict, List, Tuple
from models import SystemState, Team, Faculty, Project, Interface


class FramesAnalytics:
    """Analytics engine for FRAMES system diagnostics"""

    def __init__(self, system_state: SystemState):
        self.state = system_state

    def calculate_statistics(self) -> Dict:
        """Calculate overall system statistics"""
        total_molecules = len(self.state.teams) + len(self.state.faculty) + len(self.state.projects)
        total_bonds = len(self.state.interfaces)

        # Calculate energy flow efficiency (percentage of strong bonds)
        strong_bonds = sum(1 for i in self.state.interfaces if i.energy_loss <= 15)
        energy_flow = (strong_bonds / total_bonds * 100) if total_bonds > 0 else 0

        # Calculate decomposition risk (percentage of weak/fragile bonds)
        weak_bonds = sum(1 for i in self.state.interfaces if i.energy_loss >= 35)
        decomposition_risk = (weak_bonds / total_bonds * 100) if total_bonds > 0 else 0

        # Calculate average energy loss
        total_energy_loss = sum(i.energy_loss for i in self.state.interfaces)
        avg_energy_loss = (total_energy_loss / total_bonds) if total_bonds > 0 else 0

        return {
            'totalMolecules': total_molecules,
            'totalBonds': total_bonds,
            'energyFlow': round(energy_flow, 1),
            'decompositionRisk': round(decomposition_risk, 1),
            'totalEnergyLoss': round(avg_energy_loss, 1)
        }

    def analyze_actor_autonomy(self) -> Dict:
        """
        NDA Dimension: Actor Autonomy
        Degree of independent operation
        """
        team_count = len(self.state.teams)
        faculty_count = len(self.state.faculty)

        team_faculty_ratio = team_count / max(faculty_count, 1)

        codified_interfaces = sum(1 for i in self.state.interfaces if 'codified' in i.bond_type)
        institutional_interfaces = sum(1 for i in self.state.interfaces if 'institutional' in i.bond_type)

        autonomy_score = 0
        analysis = ""

        if team_faculty_ratio > 3:
            autonomy_score += 30
            analysis += "High team-to-faculty ratio suggests independent operation. "

        if institutional_interfaces > codified_interfaces:
            autonomy_score += 40
            analysis += "More institutional than codified interfaces indicates high autonomy. "

        outgoing_teams = sum(1 for t in self.state.teams if t.lifecycle == 'outgoing')
        if outgoing_teams > team_count * 0.3:
            autonomy_score += 30
            analysis += "High proportion of outgoing teams suggests independent operation. "

        return {
            'dimension': 'Actor Autonomy',
            'score': autonomy_score,
            'analysis': analysis,
            'icon': '🎯'
        }

    def analyze_partitioned_knowledge(self) -> Dict:
        """
        NDA Dimension: Partitioned Knowledge Domains
        Knowledge siloing across modules
        """
        disciplines = list(set(t.discipline for t in self.state.teams))
        discipline_count = len(disciplines)

        # Count cross-discipline interfaces
        cross_discipline_interfaces = 0
        for interface in self.state.interfaces:
            from_team = self.state.get_team(interface.from_entity)
            to_team = self.state.get_team(interface.to_entity)
            if from_team and to_team and from_team.discipline != to_team.discipline:
                cross_discipline_interfaces += 1

        partition_score = 0
        analysis = ""

        if discipline_count > 4:
            partition_score += 25
            analysis += "High number of disciplines suggests knowledge siloing. "

        if cross_discipline_interfaces < discipline_count * 2:
            partition_score += 35
            analysis += "Limited cross-discipline interfaces indicate knowledge partitioning. "

        institutional_interfaces = sum(1 for i in self.state.interfaces if 'institutional' in i.bond_type)
        if institutional_interfaces > len(self.state.interfaces) * 0.5:
            partition_score += 40
            analysis += "High proportion of institutional knowledge interfaces suggests tacit knowledge silos. "

        return {
            'dimension': 'Partitioned Knowledge',
            'score': partition_score,
            'analysis': analysis,
            'icon': '📚'
        }

    def analyze_emergent_outputs(self) -> Dict:
        """
        NDA Dimension: Emergent or Ambiguous Outputs
        Shifting/undefined project goals
        """
        multiversity_projects = sum(1 for p in self.state.projects if p.type == 'multiversity')
        contract_projects = sum(1 for p in self.state.projects if p.type == 'jpl-contract')
        research_projects = sum(1 for p in self.state.projects if p.type == 'research')

        emergent_score = 0
        analysis = ""

        if multiversity_projects > 0:
            emergent_score += 30
            analysis += "Multi-university projects often have emergent goals. "

        if research_projects > contract_projects:
            emergent_score += 40
            analysis += "Research-focused projects more likely to have shifting objectives. "

        incoming_teams = sum(1 for t in self.state.teams if t.lifecycle == 'incoming')
        if incoming_teams > len(self.state.teams) * 0.4:
            emergent_score += 30
            analysis += "High proportion of incoming teams may lead to goal ambiguity. "

        return {
            'dimension': 'Emergent Outputs',
            'score': emergent_score,
            'analysis': analysis,
            'icon': '🎲'
        }

    def analyze_temporal_misalignment(self) -> Dict:
        """
        NDA Dimension: Temporal Misalignment
        Timing differences across modules
        """
        incoming_teams = sum(1 for t in self.state.teams if t.lifecycle == 'incoming')
        outgoing_teams = sum(1 for t in self.state.teams if t.lifecycle == 'outgoing')
        established_teams = sum(1 for t in self.state.teams if t.lifecycle == 'established')

        temporal_score = 0
        analysis = ""

        if incoming_teams > outgoing_teams:
            temporal_score += 25
            analysis += "More incoming than outgoing teams suggests temporal misalignment. "

        if outgoing_teams > established_teams * 0.5:
            temporal_score += 35
            analysis += "High proportion of outgoing teams indicates turnover timing issues. "

        if self.state.projects:
            avg_duration = sum(p.duration for p in self.state.projects) / len(self.state.projects)
            if avg_duration > 3:
                temporal_score += 40
                analysis += "Long project durations increase temporal misalignment risk. "

        return {
            'dimension': 'Temporal Misalignment',
            'score': temporal_score,
            'analysis': analysis,
            'icon': '⏰'
        }

    def analyze_integration_cost(self) -> Dict:
        """
        NDA Dimension: Integration Cost
        Coordination effort required
        """
        total_interfaces = len(self.state.interfaces)
        total_molecules = len(self.state.teams) + len(self.state.faculty) + len(self.state.projects)
        interface_density = total_interfaces / max(total_molecules, 1)

        integration_score = 0
        analysis = ""

        if interface_density > 2:
            integration_score += 30
            analysis += "High interface density suggests high integration cost. "

        weak_interfaces = sum(1 for i in self.state.interfaces if i.energy_loss > 30)
        if weak_interfaces > total_interfaces * 0.5:
            integration_score += 40
            analysis += "High proportion of weak interfaces increases coordination effort. "

        # Count cross-discipline interfaces
        cross_discipline_interfaces = 0
        for interface in self.state.interfaces:
            from_team = self.state.get_team(interface.from_entity)
            to_team = self.state.get_team(interface.to_entity)
            if from_team and to_team and from_team.discipline != to_team.discipline:
                cross_discipline_interfaces += 1

        if cross_discipline_interfaces > total_interfaces * 0.3:
            integration_score += 30
            analysis += "High cross-discipline integration requires significant coordination. "

        return {
            'dimension': 'Integration Cost',
            'score': integration_score,
            'analysis': analysis,
            'icon': '💰'
        }

    def analyze_coupling_degradation(self) -> Dict:
        """
        NDA Dimension: Coupling Degradation
        Weakening relationships over time
        """
        fragile_interfaces = sum(1 for i in self.state.interfaces if i.bond_type == 'fragile-temporary')
        institutional_interfaces = sum(1 for i in self.state.interfaces if 'institutional' in i.bond_type)
        outgoing_teams = sum(1 for t in self.state.teams if t.lifecycle == 'outgoing')

        coupling_score = 0
        analysis = ""

        if fragile_interfaces > len(self.state.interfaces) * 0.2:
            coupling_score += 35
            analysis += "High proportion of fragile interfaces indicates coupling degradation risk. "

        if institutional_interfaces > len(self.state.interfaces) * 0.4:
            coupling_score += 30
            analysis += "High proportion of institutional knowledge interfaces vulnerable to degradation. "

        if outgoing_teams > len(self.state.teams) * 0.3:
            coupling_score += 35
            analysis += "High proportion of outgoing teams suggests imminent coupling degradation. "

        return {
            'dimension': 'Coupling Degradation',
            'score': coupling_score,
            'analysis': analysis,
            'icon': '🔗'
        }

    def get_nda_diagnostic_analysis(self) -> Dict:
        """Get complete NDA diagnostic analysis"""
        return {
            'actorAutonomy': self.analyze_actor_autonomy(),
            'partitionedKnowledge': self.analyze_partitioned_knowledge(),
            'emergentOutputs': self.analyze_emergent_outputs(),
            'temporalMisalignment': self.analyze_temporal_misalignment(),
            'integrationCost': self.analyze_integration_cost(),
            'couplingDegradation': self.analyze_coupling_degradation()
        }

    def calculate_backward_tracing_risk(self, failure_type: str) -> int:
        """Calculate risk level for specific failure type"""
        risk = 0

        if failure_type == 'documentation':
            codified_interfaces = sum(1 for i in self.state.interfaces if 'codified' in i.bond_type)
            risk = 100 - (codified_interfaces / max(len(self.state.interfaces), 1) * 100)

        elif failure_type == 'communication':
            cross_team_interfaces = 0
            for interface in self.state.interfaces:
                from_team = self.state.get_team(interface.from_entity)
                to_team = self.state.get_team(interface.to_entity)
                if from_team and to_team and from_team.discipline != to_team.discipline:
                    cross_team_interfaces += 1
            risk = 100 - (cross_team_interfaces / max(len(self.state.teams), 1) * 50)

        elif failure_type == 'rationale':
            institutional_interfaces = sum(1 for i in self.state.interfaces if 'institutional' in i.bond_type)
            risk = institutional_interfaces / max(len(self.state.interfaces), 1) * 100

        elif failure_type == 'handoff':
            outgoing_teams = sum(1 for t in self.state.teams if t.lifecycle == 'outgoing')
            incoming_teams = sum(1 for t in self.state.teams if t.lifecycle == 'incoming')
            risk = max(outgoing_teams, incoming_teams) / max(len(self.state.teams), 1) * 100

        return round(min(100, max(0, risk)))

    def get_backward_tracing_analysis(self) -> Dict:
        """Get backward tracing analysis for common failure scenarios"""
        scenarios = [
            {
                'failure': 'Students repeating completed work',
                'cause': 'Missing documentation interface',
                'solution': 'Strengthen codified knowledge interfaces',
                'type': 'documentation'
            },
            {
                'failure': 'Teams unaware of prior technical choices',
                'cause': 'Weak cross-team communication interfaces',
                'solution': 'Establish formal design review processes',
                'type': 'communication'
            },
            {
                'failure': 'Integration problems from undocumented rationale',
                'cause': 'Institutional knowledge not codified',
                'solution': 'Convert tacit knowledge to structured documentation',
                'type': 'rationale'
            },
            {
                'failure': 'New cohorts unable to operate systems',
                'cause': 'Outgoing teams left incomplete handoffs',
                'solution': 'Implement structured onboarding and handoff procedures',
                'type': 'handoff'
            }
        ]

        results = []
        for scenario in scenarios:
            risk = self.calculate_backward_tracing_risk(scenario['type'])
            results.append({
                **scenario,
                'risk': risk,
                'riskLevel': 'HIGH' if risk > 70 else 'MEDIUM' if risk > 40 else 'LOW'
            })

        return {
            'scenarios': results,
            'methodology': [
                'Identify observable failures',
                'Trace backward to knowledge transfer points',
                'Identify interface mechanism responsible',
                'Determine why transfer failed',
                'Design interventions to strengthen interfaces'
            ]
        }

    def analyze_team_lifecycle(self) -> Dict:
        """Analyze team lifecycle distribution"""
        incoming = sum(1 for t in self.state.teams if t.lifecycle == 'incoming')
        established = sum(1 for t in self.state.teams if t.lifecycle == 'established')
        outgoing = sum(1 for t in self.state.teams if t.lifecycle == 'outgoing')
        total = len(self.state.teams)

        return {
            'incoming': {'count': incoming, 'percentage': round(incoming / max(total, 1) * 100, 1)},
            'established': {'count': established, 'percentage': round(established / max(total, 1) * 100, 1)},
            'outgoing': {'count': outgoing, 'percentage': round(outgoing / max(total, 1) * 100, 1)},
            'total': total
        }
