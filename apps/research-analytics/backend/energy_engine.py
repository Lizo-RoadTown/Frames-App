"""
Energy Loss Calculation Engine for FRAMES
Flexible, research-driven system for calculating knowledge transfer risk
"""

from typing import Dict, List, Optional, Tuple
from database import db
from db_models import (
    InterfaceModel, RiskFactor, FactorValue, FactorModel,
    ModelFactor, InterfaceFactorValue
)


class EnergyCalculationEngine:
    """
    Core engine for calculating energy loss at interfaces using configurable risk factors.

    This engine supports:
    - Multiple simultaneous models with different factor weightings
    - Dynamic factor addition/removal without code changes
    - Historical tracking of how factors evolve
    - Validation against actual outcomes
    """

    def __init__(self, model_id: Optional[int] = None):
        """
        Initialize the engine with a specific model.
        If no model_id provided, uses the currently active model.
        """
        self.model_id = model_id
        self.model = None
        self.factors_cache = None

    def get_active_model(self) -> Optional[FactorModel]:
        """Get the currently active model, or create a default if none exists."""
        if self.model_id:
            return FactorModel.query.get(self.model_id)

        # Find the active model
        active_model = FactorModel.query.filter_by(is_active=True).first()

        if not active_model:
            # Create a baseline model if none exists
            active_model = self._create_baseline_model()

        return active_model

    def _create_baseline_model(self) -> FactorModel:
        """
        Create a baseline model with default factors.
        This is used when the system starts fresh.
        """
        baseline = FactorModel(
            model_name='baseline_v1',
            display_name='Baseline Model (NDA-Based)',
            description='Initial model based on Nearly Decomposable Architecture theory',
            is_active=True,
            is_baseline=True,
            hypothesis='Knowledge transfer risk correlates with knowledge type and bond strength',
            validation_status='testing'
        )
        db.session.add(baseline)

        # Create baseline factors if they don't exist
        self._ensure_baseline_factors()

        db.session.commit()
        return baseline

    def _ensure_baseline_factors(self):
        """
        Ensure baseline risk factors exist in the database.
        These are the starting point from NDA theory.
        """
        baseline_factors = [
            {
                'factor_name': 'knowledge_type',
                'display_name': 'Knowledge Type',
                'description': 'Whether knowledge is codified (documented) or institutional (tacit)',
                'category': 'NDA_Dimension',
                'confidence_level': 'established',
                'values': [
                    {'value_name': 'codified', 'display_name': 'Codified',
                     'description': 'Documented, transferable knowledge', 'contribution': 0.10},
                    {'value_name': 'institutional', 'display_name': 'Institutional',
                     'description': 'Tacit, experience-based knowledge', 'contribution': 0.40},
                ]
            },
            {
                'factor_name': 'bond_strength',
                'display_name': 'Bond Strength',
                'description': 'Strength of relationship between entities',
                'category': 'Interface_Property',
                'confidence_level': 'established',
                'values': [
                    {'value_name': 'strong', 'display_name': 'Strong',
                     'description': 'Frequent, high-quality interactions', 'contribution': 0.05},
                    {'value_name': 'moderate', 'display_name': 'Moderate',
                     'description': 'Regular but limited interactions', 'contribution': 0.20},
                    {'value_name': 'weak', 'display_name': 'Weak',
                     'description': 'Infrequent or low-quality interactions', 'contribution': 0.35},
                ]
            },
            {
                'factor_name': 'temporal_alignment',
                'display_name': 'Temporal Alignment',
                'description': 'Timing of knowledge transfer relative to need',
                'category': 'NDA_Dimension',
                'confidence_level': 'provisional',
                'values': [
                    {'value_name': 'aligned', 'display_name': 'Well-Aligned',
                     'description': 'Knowledge transferred when needed', 'contribution': 0.05},
                    {'value_name': 'misaligned', 'display_name': 'Misaligned',
                     'description': 'Knowledge transferred too early or late', 'contribution': 0.25},
                ]
            },
            {
                'factor_name': 'actor_autonomy',
                'display_name': 'Actor Autonomy',
                'description': 'Degree of independence of entities at interface',
                'category': 'NDA_Dimension',
                'confidence_level': 'provisional',
                'values': [
                    {'value_name': 'high', 'display_name': 'High Autonomy',
                     'description': 'Entities operate independently', 'contribution': 0.15},
                    {'value_name': 'low', 'display_name': 'Low Autonomy',
                     'description': 'Entities are tightly coupled', 'contribution': 0.05},
                ]
            },
        ]

        for factor_def in baseline_factors:
            # Check if factor already exists
            existing = RiskFactor.query.filter_by(factor_name=factor_def['factor_name']).first()
            if existing:
                continue

            # Create the factor
            factor = RiskFactor(
                factor_name=factor_def['factor_name'],
                display_name=factor_def['display_name'],
                description=factor_def['description'],
                category=factor_def['category'],
                confidence_level=factor_def['confidence_level'],
                active=True
            )
            db.session.add(factor)
            db.session.flush()  # Get the factor ID

            # Create factor values
            for idx, value_def in enumerate(factor_def['values']):
                factor_value = FactorValue(
                    factor_id=factor.id,
                    value_name=value_def['value_name'],
                    display_name=value_def['display_name'],
                    description=value_def['description'],
                    energy_loss_contribution=value_def['contribution'],
                    sort_order=idx
                )
                db.session.add(factor_value)

    def calculate_interface_energy_loss(
        self,
        interface_id: str,
        model_id: Optional[int] = None
    ) -> Dict:
        """
        Calculate the energy loss for a specific interface using the specified model.

        Returns:
        {
            'interface_id': str,
            'model_id': int,
            'total_energy_loss': float (0.0 to 1.0),
            'energy_loss_percent': int (0 to 100),
            'factors_applied': [
                {
                    'factor_name': str,
                    'factor_value': str,
                    'contribution': float,
                    'weight': float,
                    'weighted_contribution': float
                },
                ...
            ],
            'risk_level': str ('low', 'moderate', 'high', 'critical')
        }
        """
        # Get the model
        model = self.get_active_model() if not model_id else FactorModel.query.get(model_id)
        if not model:
            raise ValueError("No model available for energy calculation")

        # Get interface factor values
        interface_factors = db.session.query(
            InterfaceFactorValue, RiskFactor, FactorValue
        ).join(
            RiskFactor, InterfaceFactorValue.factor_id == RiskFactor.id
        ).join(
            FactorValue, InterfaceFactorValue.factor_value_id == FactorValue.id
        ).filter(
            InterfaceFactorValue.interface_id == interface_id
        ).all()

        # Get model weights for factors
        model_factors = db.session.query(ModelFactor).filter_by(
            model_id=model.id,
            enabled=True
        ).all()

        weights_map = {mf.factor_id: mf.weight for mf in model_factors}

        # Calculate weighted energy loss
        total_loss = 0.0
        factors_applied = []

        for interface_factor, risk_factor, factor_value in interface_factors:
            # Get weight for this factor in this model (default 1.0 if not specified)
            weight = weights_map.get(risk_factor.id, 1.0)

            # Calculate weighted contribution
            base_contribution = factor_value.energy_loss_contribution
            weighted_contribution = base_contribution * weight

            total_loss += weighted_contribution

            factors_applied.append({
                'factor_name': risk_factor.factor_name,
                'factor_display_name': risk_factor.display_name,
                'factor_value': factor_value.value_name,
                'factor_value_display': factor_value.display_name,
                'contribution': base_contribution,
                'weight': weight,
                'weighted_contribution': weighted_contribution
            })

        # Cap at 100%
        total_loss = min(1.0, total_loss)

        # Determine risk level
        if total_loss < 0.15:
            risk_level = 'low'
        elif total_loss < 0.35:
            risk_level = 'moderate'
        elif total_loss < 0.60:
            risk_level = 'high'
        else:
            risk_level = 'critical'

        return {
            'interface_id': interface_id,
            'model_id': model.id,
            'model_name': model.model_name,
            'total_energy_loss': round(total_loss, 3),
            'energy_loss_percent': int(total_loss * 100),
            'factors_applied': factors_applied,
            'risk_level': risk_level
        }

    def calculate_network_energy(
        self,
        university_id: Optional[str] = None,
        model_id: Optional[int] = None
    ) -> Dict:
        """
        Calculate energy loss for all interfaces in a network (or specific university).

        Returns aggregated statistics and per-interface results.
        """
        # Query interfaces
        query = InterfaceModel.query
        if university_id:
            query = query.filter(
                (InterfaceModel.from_university == university_id) |
                (InterfaceModel.to_university == university_id)
            )

        interfaces = query.all()

        results = []
        total_loss = 0.0

        for interface in interfaces:
            try:
                loss_calc = self.calculate_interface_energy_loss(interface.id, model_id)
                results.append(loss_calc)
                total_loss += loss_calc['total_energy_loss']
            except Exception as e:
                # Skip interfaces without factor assignments
                print(f"Warning: Could not calculate energy for interface {interface.id}: {e}")
                continue

        avg_loss = total_loss / len(results) if results else 0.0

        # Count by risk level
        risk_counts = {'low': 0, 'moderate': 0, 'high': 0, 'critical': 0}
        for result in results:
            risk_counts[result['risk_level']] += 1

        return {
            'university_id': university_id,
            'total_interfaces': len(interfaces),
            'analyzed_interfaces': len(results),
            'average_energy_loss': round(avg_loss, 3),
            'average_energy_loss_percent': int(avg_loss * 100),
            'risk_distribution': risk_counts,
            'interfaces': results
        }

    def assign_factor_values_to_interface(
        self,
        interface_id: str,
        factor_assignments: List[Dict]
    ) -> bool:
        """
        Assign factor values to an interface.

        factor_assignments: [
            {'factor_id': int, 'factor_value_id': int},
            ...
        ]
        """
        # Clear existing assignments for this interface
        InterfaceFactorValue.query.filter_by(interface_id=interface_id).delete()

        # Add new assignments
        for assignment in factor_assignments:
            ifv = InterfaceFactorValue(
                interface_id=interface_id,
                factor_id=assignment['factor_id'],
                factor_value_id=assignment['factor_value_id']
            )
            db.session.add(ifv)

        db.session.commit()
        return True

    def auto_assign_factors_from_legacy(self, interface_id: str) -> bool:
        """
        Automatically assign factor values based on legacy bond_type field.
        This helps migrate existing interfaces to the new factor system.

        Legacy mapping:
        - codified-strong -> knowledge_type=codified, bond_strength=strong
        - codified-moderate -> knowledge_type=codified, bond_strength=moderate
        - institutional-weak -> knowledge_type=institutional, bond_strength=weak
        - fragile-temporary -> knowledge_type=institutional, bond_strength=weak, temporal_alignment=misaligned
        """
        interface = InterfaceModel.query.get(interface_id)
        if not interface or not interface.bond_type:
            return False

        # Parse legacy bond type
        bond_type = interface.bond_type.lower()

        assignments = []

        # Get factors
        knowledge_type_factor = RiskFactor.query.filter_by(factor_name='knowledge_type').first()
        bond_strength_factor = RiskFactor.query.filter_by(factor_name='bond_strength').first()
        temporal_factor = RiskFactor.query.filter_by(factor_name='temporal_alignment').first()

        if not knowledge_type_factor or not bond_strength_factor:
            return False

        # Map knowledge type
        if 'codified' in bond_type:
            kt_value = FactorValue.query.filter_by(
                factor_id=knowledge_type_factor.id,
                value_name='codified'
            ).first()
            if kt_value:
                assignments.append({'factor_id': knowledge_type_factor.id, 'factor_value_id': kt_value.id})
        elif 'institutional' in bond_type or 'fragile' in bond_type:
            kt_value = FactorValue.query.filter_by(
                factor_id=knowledge_type_factor.id,
                value_name='institutional'
            ).first()
            if kt_value:
                assignments.append({'factor_id': knowledge_type_factor.id, 'factor_value_id': kt_value.id})

        # Map bond strength
        if 'strong' in bond_type:
            bs_value = FactorValue.query.filter_by(
                factor_id=bond_strength_factor.id,
                value_name='strong'
            ).first()
        elif 'moderate' in bond_type:
            bs_value = FactorValue.query.filter_by(
                factor_id=bond_strength_factor.id,
                value_name='moderate'
            ).first()
        else:  # weak, fragile, etc.
            bs_value = FactorValue.query.filter_by(
                factor_id=bond_strength_factor.id,
                value_name='weak'
            ).first()

        if bs_value:
            assignments.append({'factor_id': bond_strength_factor.id, 'factor_value_id': bs_value.id})

        # Fragile bonds also have temporal misalignment
        if 'fragile' in bond_type or 'temporary' in bond_type:
            if temporal_factor:
                temp_value = FactorValue.query.filter_by(
                    factor_id=temporal_factor.id,
                    value_name='misaligned'
                ).first()
                if temp_value:
                    assignments.append({'factor_id': temporal_factor.id, 'factor_value_id': temp_value.id})

        # Assign the factors
        return self.assign_factor_values_to_interface(interface_id, assignments)
