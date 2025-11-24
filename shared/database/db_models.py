"""
SQLAlchemy declarative models for FRAMES migration (Milestone A)

These models mirror the lightweight dataclasses in `models.py` and are
intended for use by the migration CLI and future DB-backed endpoints.
"""
from datetime import datetime
from backend.database import db


class TeamModel(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.String, primary_key=True)
    university_id = db.Column(db.String, nullable=True, index=True)  # Nullable for backwards compat during migration
    project_id = db.Column(db.String, nullable=False, index=True)  # Teams belong to projects
    discipline = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    meta = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'university_id': self.university_id,
            'project_id': self.project_id,
            'discipline': self.discipline,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'meta': self.meta,
        }


class FacultyModel(db.Model):
    __tablename__ = 'faculty'
    id = db.Column(db.String, primary_key=True)
    university_id = db.Column(db.String, nullable=True, index=True)
    name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    meta = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'university_id': self.university_id,
            'name': self.name,
            'role': self.role,
            'description': self.description,
            'created_at': self.created_at,
            'meta': self.meta,
        }


class ProjectModel(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.String, primary_key=True)
    university_id = db.Column(db.String, nullable=True, index=True)  # NULL for PROVES shared project
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    is_collaborative = db.Column(db.Boolean, default=False)  # TRUE for PROVES
    duration = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    meta = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'university_id': self.university_id,
            'name': self.name,
            'type': self.type,
            'is_collaborative': self.is_collaborative,
            'duration': self.duration,
            'description': self.description,
            'created_at': self.created_at,
            'meta': self.meta,
        }


class InterfaceModel(db.Model):
    __tablename__ = 'interfaces'
    id = db.Column(db.String, primary_key=True)
    from_entity = db.Column(db.String, nullable=False)
    to_entity = db.Column(db.String, nullable=False)
    interface_type = db.Column(db.String, nullable=True)
    bond_type = db.Column(db.String, nullable=True)
    energy_loss = db.Column(db.Integer, nullable=True)
    # Denormalized for cross-university querying
    from_university = db.Column(db.String, nullable=True, index=True)
    to_university = db.Column(db.String, nullable=True, index=True)
    is_cross_university = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    meta = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'from': self.from_entity,
            'to': self.to_entity,
            'interfaceType': self.interface_type,
            'bondType': self.bond_type,
            'energyLoss': self.energy_loss,
            'from_university': self.from_university,
            'to_university': self.to_university,
            'is_cross_university': self.is_cross_university,
            'created_at': self.created_at,
            'meta': self.meta,
        }


class University(db.Model):
    __tablename__ = 'universities'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    is_lead = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    meta = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.String, default=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_lead': self.is_lead,
            'active': self.active,
            'meta': self.meta,
            'created_at': self.created_at,
        }


class Outcome(db.Model):
    __tablename__ = 'outcomes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.String, nullable=False)
    project_id = db.Column(db.String, nullable=True)
    outcome_type = db.Column(db.String, nullable=False)  # 'mission_success' or 'program_success'
    success = db.Column(db.Boolean, nullable=False)
    cohort_year = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    recorded_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    meta = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'university_id': self.university_id,
            'project_id': self.project_id,
            'outcome_type': self.outcome_type,
            'success': self.success,
            'cohort_year': self.cohort_year,
            'notes': self.notes,
            'recorded_at': self.recorded_at,
            'meta': self.meta,
        }


class StudentModel(db.Model):
    """Individual student tracking for term-based rotation analysis"""
    __tablename__ = 'students'

    id = db.Column(db.String, primary_key=True)
    university_id = db.Column(db.String, nullable=False, index=True)
    name = db.Column(db.String, nullable=False)
    team_id = db.Column(db.String, nullable=True)  # Foreign key to teams (which belong to projects)
    expertise_area = db.Column(db.String, nullable=True)  # e.g., "Electrical", "Software"
    graduation_term = db.Column(db.String, nullable=True)  # e.g., "Spring 2026"
    terms_remaining = db.Column(db.Integer, nullable=False, default=4)  # Auto-decrements each term
    status = db.Column(db.String, nullable=True)  # Auto-calculated: incoming/established/outgoing
    is_lead = db.Column(db.Boolean, default=False)  # Team lead designation
    active = db.Column(db.Boolean, default=True)  # False when graduated
    created_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    graduated_at = db.Column(db.String, nullable=True)  # Set when terms_remaining hits 0
    meta = db.Column(db.JSON, nullable=True)

    def calculate_status(self):
        """Auto-calculate student status based on terms remaining"""
        if self.terms_remaining >= 4:
            return 'incoming'
        elif self.terms_remaining >= 2:
            return 'established'
        else:
            return 'outgoing'

    def to_dict(self):
        return {
            'id': self.id,
            'university_id': self.university_id,
            'name': self.name,
            'team_id': self.team_id,
            'expertise_area': self.expertise_area,
            'graduation_term': self.graduation_term,
            'terms_remaining': self.terms_remaining,
            'status': self.status or self.calculate_status(),
            'is_lead': self.is_lead,
            'active': self.active,
            'created_at': self.created_at,
            'graduated_at': self.graduated_at,
            'meta': self.meta,
        }


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    actor = db.Column(db.String, nullable=False, default='system')
    action = db.Column(db.String, nullable=False)
    entity_type = db.Column(db.String, nullable=False)
    entity_id = db.Column(db.String, nullable=True)
    university_id = db.Column(db.String, nullable=True)
    payload_before = db.Column(db.Text, nullable=True)
    payload_after = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.String, default=lambda: datetime.now().isoformat())
    meta = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'actor': self.actor,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'university_id': self.university_id,
            'payload_before': self.payload_before,
            'payload_after': self.payload_after,
            'timestamp': self.timestamp,
            'meta': self.meta,
        }


class RiskFactor(db.Model):
    """
    Configurable risk factors for energy loss calculation.
    Researchers can define, weight, and test different factors that contribute to knowledge transfer degradation.
    """
    __tablename__ = 'risk_factors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    factor_name = db.Column(db.String, nullable=False, unique=True)  # e.g., "knowledge_type", "bond_strength"
    display_name = db.Column(db.String, nullable=False)  # Human-readable name
    description = db.Column(db.Text, nullable=True)  # What this factor measures
    category = db.Column(db.String, nullable=False)  # e.g., "NDA_Dimension", "Interface_Property", "Entity_Attribute"

    # Research metadata
    confidence_level = db.Column(db.String, nullable=False, default='provisional')  # 'established', 'provisional', 'exploratory'
    research_notes = db.Column(db.Text, nullable=True)  # Researcher's notes on this factor

    # Active/inactive (allows deprecating factors without deleting historical data)
    active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    updated_at = db.Column(db.String, default=lambda: datetime.now().isoformat(), onupdate=lambda: datetime.now().isoformat())
    meta = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'factor_name': self.factor_name,
            'display_name': self.display_name,
            'description': self.description,
            'category': self.category,
            'confidence_level': self.confidence_level,
            'research_notes': self.research_notes,
            'active': self.active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'meta': self.meta,
        }


class FactorValue(db.Model):
    """
    Possible values for each risk factor with their energy loss contributions.
    Example: For factor "knowledge_type", values might be "codified" (5%) and "institutional" (35%)
    """
    __tablename__ = 'factor_values'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    factor_id = db.Column(db.Integer, db.ForeignKey('risk_factors.id'), nullable=False)

    value_name = db.Column(db.String, nullable=False)  # e.g., "codified", "institutional", "strong", "weak"
    display_name = db.Column(db.String, nullable=False)  # Human-readable
    description = db.Column(db.Text, nullable=True)

    # Base energy loss contribution (0.0 to 1.0 representing 0% to 100%)
    energy_loss_contribution = db.Column(db.Float, nullable=False, default=0.0)

    # Ordering for display purposes
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    meta = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'factor_id': self.factor_id,
            'value_name': self.value_name,
            'display_name': self.display_name,
            'description': self.description,
            'energy_loss_contribution': self.energy_loss_contribution,
            'sort_order': self.sort_order,
            'created_at': self.created_at,
            'meta': self.meta,
        }


class FactorModel(db.Model):
    """
    A research model combining multiple risk factors with specific weights.
    Allows researchers to create, test, and compare different predictive models.
    """
    __tablename__ = 'factor_models'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String, nullable=False, unique=True)
    display_name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Model status
    is_active = db.Column(db.Boolean, default=False)  # Only one model can be active at a time
    is_baseline = db.Column(db.Boolean, default=False)  # Baseline model for comparison

    # Research metadata
    hypothesis = db.Column(db.Text, nullable=True)  # What this model is testing
    validation_status = db.Column(db.String, nullable=True)  # 'testing', 'validated', 'rejected'

    created_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    updated_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    meta = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'model_name': self.model_name,
            'display_name': self.display_name,
            'description': self.description,
            'is_active': self.is_active,
            'is_baseline': self.is_baseline,
            'hypothesis': self.hypothesis,
            'validation_status': self.validation_status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'meta': self.meta,
        }


class ModelFactor(db.Model):
    """
    Join table linking models to factors with specific weights.
    This allows each model to weight factors differently.
    """
    __tablename__ = 'model_factors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_id = db.Column(db.Integer, db.ForeignKey('factor_models.id'), nullable=False)
    factor_id = db.Column(db.Integer, db.ForeignKey('risk_factors.id'), nullable=False)

    # Weight multiplier for this factor in this model (typically 0.0 to 2.0)
    # 1.0 = normal weight, <1.0 = reduced importance, >1.0 = increased importance
    weight = db.Column(db.Float, nullable=False, default=1.0)

    # Whether this factor is enabled in this model
    enabled = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    meta = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'model_id': self.model_id,
            'factor_id': self.factor_id,
            'weight': self.weight,
            'enabled': self.enabled,
            'created_at': self.created_at,
            'meta': self.meta,
        }


class InterfaceFactorValue(db.Model):
    """
    Records which factor values apply to each interface.
    This is the junction between actual interfaces and the risk factor model.
    """
    __tablename__ = 'interface_factor_values'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interface_id = db.Column(db.String, db.ForeignKey('interfaces.id'), nullable=False)
    factor_id = db.Column(db.Integer, db.ForeignKey('risk_factors.id'), nullable=False)
    factor_value_id = db.Column(db.Integer, db.ForeignKey('factor_values.id'), nullable=False)

    # Timestamp for tracking changes over time
    assigned_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    meta = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'interface_id': self.interface_id,
            'factor_id': self.factor_id,
            'factor_value_id': self.factor_value_id,
            'assigned_at': self.assigned_at,
            'meta': self.meta,
        }


class ModelValidation(db.Model):
    """
    Tracks validation results when comparing model predictions against actual outcomes.
    Used to evaluate which models are most accurate.
    """
    __tablename__ = 'model_validations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_id = db.Column(db.Integer, db.ForeignKey('factor_models.id'), nullable=False)
    outcome_id = db.Column(db.Integer, db.ForeignKey('outcomes.id'), nullable=True)  # Link to actual outcome

    # Prediction vs actual
    predicted_risk_score = db.Column(db.Float, nullable=False)  # Model's prediction (0.0 to 1.0)
    actual_outcome = db.Column(db.Boolean, nullable=True)  # Was there knowledge loss? (if known)

    # Validation metrics
    prediction_accuracy = db.Column(db.Float, nullable=True)  # How close was the prediction?

    validated_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    notes = db.Column(db.Text, nullable=True)
    meta = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'model_id': self.model_id,
            'outcome_id': self.outcome_id,
            'predicted_risk_score': self.predicted_risk_score,
            'actual_outcome': self.actual_outcome,
            'prediction_accuracy': self.prediction_accuracy,
            'validated_at': self.validated_at,
            'notes': self.notes,
            'meta': self.meta,
        }


# ============================================================================
# LMS Module Models (Student Onboarding System)
# ============================================================================

class Module(db.Model):
    """Training modules for student onboarding"""
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), index=True)
    estimated_minutes = db.Column(db.Integer, default=10)

    # Ownership
    created_by_id = db.Column(db.String, db.ForeignKey('faculty.id'))
    university_id = db.Column(db.String, db.ForeignKey('universities.id'))

    # Status
    status = db.Column(db.String(50), default='draft', index=True)

    # Organization (JSON fields)
    prerequisites = db.Column(db.JSON, default=list)
    related_modules = db.Column(db.JSON, default=list)
    tags = db.Column(db.JSON, default=list)

    # Metadata
    target_audience = db.Column(db.String(100), default='incoming_students')
    revision = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'estimated_minutes': self.estimated_minutes,
            'created_by_id': self.created_by_id,
            'university_id': self.university_id,
            'status': self.status,
            'prerequisites': self.prerequisites or [],
            'related_modules': self.related_modules or [],
            'tags': self.tags or [],
            'target_audience': self.target_audience,
            'revision': self.revision,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None,
        }


class ModuleSection(db.Model):
    """Content sections within a module"""
    __tablename__ = 'module_sections'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id', ondelete='CASCADE'), nullable=False, index=True)
    section_number = db.Column(db.Integer, nullable=False)
    section_type = db.Column(db.String(50), nullable=False)  # text, video, image, checklist, etc.
    title = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(500))
    duration_seconds = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'section_number': self.section_number,
            'section_type': self.section_type,
            'title': self.title,
            'content': self.content,
            'media_url': self.media_url,
            'duration_seconds': self.duration_seconds,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class ModuleAssignment(db.Model):
    """Assignment of modules to students"""
    __tablename__ = 'module_assignments'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id', ondelete='CASCADE'), nullable=False, index=True)
    student_id = db.Column(db.String, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False, index=True)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    required = db.Column(db.Boolean, default=True)
    assigned_by_id = db.Column(db.String, db.ForeignKey('faculty.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'student_id': self.student_id,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'required': self.required,
            'assigned_by_id': self.assigned_by_id,
        }


class ModuleProgress(db.Model):
    """Student progress through modules"""
    __tablename__ = 'module_progress'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id', ondelete='CASCADE'), nullable=False, index=True)
    student_id = db.Column(db.String, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False, index=True)

    # Progress tracking
    status = db.Column(db.String(50), default='not_started')  # not_started, in_progress, completed
    progress_percent = db.Column(db.Integer, default=0)
    current_section = db.Column(db.Integer, default=1)

    # Time tracking
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    total_time_seconds = db.Column(db.Integer, default=0)
    last_accessed_at = db.Column(db.DateTime)

    # Analytics
    pause_count = db.Column(db.Integer, default=0)
    resume_count = db.Column(db.Integer, default=0)
    completed_sections = db.Column(db.JSON, default=list)

    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'student_id': self.student_id,
            'status': self.status,
            'progress_percent': self.progress_percent,
            'current_section': self.current_section,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'total_time_seconds': self.total_time_seconds,
            'last_accessed_at': self.last_accessed_at.isoformat() if self.last_accessed_at else None,
            'pause_count': self.pause_count,
            'resume_count': self.resume_count,
            'completed_sections': self.completed_sections or [],
        }


class ModuleAnalyticsEvent(db.Model):
    """Detailed analytics events for module usage"""
    __tablename__ = 'module_analytics_events'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id', ondelete='CASCADE'), nullable=False, index=True)
    student_id = db.Column(db.String, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False, index=True)

    event_type = db.Column(db.String(50), nullable=False, index=True)  # start, pause, resume, section_complete, complete
    section_number = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Additional context
    scroll_depth_percent = db.Column(db.Integer)
    time_on_section_seconds = db.Column(db.Integer)
    device_type = db.Column(db.String(50))
    meta = db.Column(db.JSON)

    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'student_id': self.student_id,
            'event_type': self.event_type,
            'section_number': self.section_number,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'scroll_depth_percent': self.scroll_depth_percent,
            'time_on_section_seconds': self.time_on_section_seconds,
            'device_type': self.device_type,
            'meta': self.meta,
        }


class ModuleFeedback(db.Model):
    """Student feedback on modules"""
    __tablename__ = 'module_feedback'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id', ondelete='CASCADE'), nullable=False, index=True)
    student_id = db.Column(db.String, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)

    # Ratings
    rating = db.Column(db.Integer)  # 1-5 stars
    difficulty = db.Column(db.String(50))  # too_easy, just_right, too_hard
    clarity = db.Column(db.Integer)  # 1-5
    usefulness = db.Column(db.Integer)  # 1-5

    # Comments
    feedback_text = db.Column(db.Text)
    suggestions = db.Column(db.Text)

    # Metadata
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'student_id': self.student_id,
            'rating': self.rating,
            'difficulty': self.difficulty,
            'clarity': self.clarity,
            'usefulness': self.usefulness,
            'feedback_text': self.feedback_text,
            'suggestions': self.suggestions,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
        }


