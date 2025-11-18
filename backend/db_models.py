"""
SQLAlchemy declarative models for FRAMES migration (Milestone A)

These models mirror the lightweight dataclasses in `models.py` and are
intended for use by the migration CLI and future DB-backed endpoints.
"""
from datetime import datetime
from app import db


class TeamModel(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.String, primary_key=True)
    university_id = db.Column(db.String, nullable=True, index=True)  # Nullable for backwards compat during migration
    discipline = db.Column(db.String, nullable=True)
    lifecycle = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=True)
    experience = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    meta = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'university_id': self.university_id,
            'discipline': self.discipline,
            'lifecycle': self.lifecycle,
            'name': self.name,
            'size': self.size,
            'experience': self.experience,
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


