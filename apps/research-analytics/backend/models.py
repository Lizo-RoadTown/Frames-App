"""
Data models for FRAMES application
Represents Teams, Faculty, Projects, and Interfaces
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json


@dataclass
class Team:
    """Represents a team/micro-module in the system"""
    id: str
    discipline: str  # electrical, software, mechanical, etc.
    lifecycle: str  # incoming, established, outgoing
    name: str
    size: int
    experience: int  # in months
    description: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'discipline': self.discipline,
            'lifecycle': self.lifecycle,
            'name': self.name,
            'size': self.size,
            'experience': self.experience,
            'description': self.description,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Team':
        """Create Team from dictionary"""
        return cls(**data)


@dataclass
class Faculty:
    """Represents faculty/staff members in the system"""
    id: str
    name: str
    role: str
    description: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'description': self.description,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Faculty':
        """Create Faculty from dictionary"""
        return cls(**data)


@dataclass
class Project:
    """Represents a project in the system"""
    id: str
    name: str
    type: str  # multiversity, jpl-contract, contract-pursuit, research
    duration: int  # in years
    description: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'duration': self.duration,
            'description': self.description,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Project':
        """Create Project from dictionary"""
        return cls(**data)


@dataclass
class Interface:
    """Represents an interface/bond between entities"""
    id: str
    from_entity: str  # ID of source entity
    to_entity: str  # ID of target entity
    interface_type: str  # team-to-team, team-to-faculty, team-to-project
    bond_type: str  # codified-strong, codified-moderate, institutional-weak, fragile-temporary
    energy_loss: int  # percentage 5, 15, 35, 60
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'from': self.from_entity,
            'to': self.to_entity,
            'interfaceType': self.interface_type,
            'bondType': self.bond_type,
            'energyLoss': self.energy_loss,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Interface':
        """Create Interface from dictionary"""
        return cls(
            id=data['id'],
            from_entity=data.get('from', data.get('from_entity')),
            to_entity=data.get('to', data.get('to_entity')),
            interface_type=data.get('interfaceType', data.get('interface_type')),
            bond_type=data.get('bondType', data.get('bond_type')),
            energy_loss=data.get('energyLoss', data.get('energy_loss')),
            created_at=data.get('created_at', datetime.now().isoformat())
        )


class SystemState:
    """Manages the complete state of the FRAMES system"""

    def __init__(self):
        self.teams: List[Team] = []
        self.faculty: List[Faculty] = []
        self.projects: List[Project] = []
        self.interfaces: List[Interface] = []

    def add_team(self, team: Team) -> Team:
        """Add a team to the system"""
        self.teams.append(team)
        return team

    def add_faculty(self, faculty_member: Faculty) -> Faculty:
        """Add a faculty member to the system"""
        self.faculty.append(faculty_member)
        return faculty_member

    def add_project(self, project: Project) -> Project:
        """Add a project to the system"""
        self.projects.append(project)
        return project

    def add_interface(self, interface: Interface) -> Interface:
        """Add an interface to the system"""
        self.interfaces.append(interface)
        return interface

    def remove_team(self, team_id: str) -> bool:
        """Remove a team and its associated interfaces"""
        self.teams = [t for t in self.teams if t.id != team_id]
        self.interfaces = [i for i in self.interfaces if i.from_entity != team_id and i.to_entity != team_id]
        return True

    def remove_faculty(self, faculty_id: str) -> bool:
        """Remove a faculty member and associated interfaces"""
        self.faculty = [f for f in self.faculty if f.id != faculty_id]
        self.interfaces = [i for i in self.interfaces if i.from_entity != faculty_id and i.to_entity != faculty_id]
        return True

    def remove_project(self, project_id: str) -> bool:
        """Remove a project and associated interfaces"""
        self.projects = [p for p in self.projects if p.id != project_id]
        self.interfaces = [i for i in self.interfaces if i.from_entity != project_id and i.to_entity != project_id]
        return True

    def remove_interface(self, interface_id: str) -> bool:
        """Remove an interface"""
        self.interfaces = [i for i in self.interfaces if i.id != interface_id]
        return True

    def get_team(self, team_id: str) -> Optional[Team]:
        """Get a team by ID"""
        return next((t for t in self.teams if t.id == team_id), None)

    def get_faculty(self, faculty_id: str) -> Optional[Faculty]:
        """Get a faculty member by ID"""
        return next((f for f in self.faculty if f.id == faculty_id), None)

    def get_project(self, project_id: str) -> Optional[Project]:
        """Get a project by ID"""
        return next((p for p in self.projects if p.id == project_id), None)

    def to_dict(self) -> Dict:
        """Convert entire system state to dictionary"""
        return {
            'teams': [t.to_dict() for t in self.teams],
            'faculty': [f.to_dict() for f in self.faculty],
            'projects': [p.to_dict() for p in self.projects],
            'interfaces': [i.to_dict() for i in self.interfaces]
        }

    def from_dict(self, data: Dict):
        """Load system state from dictionary"""
        self.teams = [Team.from_dict(t) for t in data.get('teams', [])]
        self.faculty = [Faculty.from_dict(f) for f in data.get('faculty', [])]
        self.projects = [Project.from_dict(p) for p in data.get('projects', [])]
        self.interfaces = [Interface.from_dict(i) for i in data.get('interfaces', [])]

    def save_to_file(self, filename: str):
        """Save system state to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    def load_from_file(self, filename: str):
        """Load system state from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
            self.from_dict(data)
