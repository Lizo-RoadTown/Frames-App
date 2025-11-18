#!/usr/bin/env python
"""
Seed multi-university data for FRAMES Phase 1

Populates:
- 8 universities (Cal Poly Pomona as lead + 7 others)
- PROVES shared collaborative project
- Sample teams, faculty, projects for 3 universities
- Cross-university interfaces for PROVES collaboration
"""

from app import app, db
from db_models import University, TeamModel, FacultyModel, ProjectModel, InterfaceModel
from datetime import datetime

def seed_universities():
    """Create 8 universities"""
    universities = [
        {'id': 'CalPolyPomona', 'name': 'Cal Poly Pomona', 'is_lead': True},
        {'id': 'TexasState', 'name': 'Texas State University', 'is_lead': False},
        {'id': 'Columbia', 'name': 'Columbia University', 'is_lead': False},
        {'id': 'Uni_D', 'name': 'University D', 'is_lead': False},
        {'id': 'Uni_E', 'name': 'University E', 'is_lead': False},
        {'id': 'Uni_F', 'name': 'University F', 'is_lead': False},
        {'id': 'Uni_G', 'name': 'University G', 'is_lead': False},
        {'id': 'Uni_H', 'name': 'University H', 'is_lead': False},
    ]

    print("Creating universities...")
    for uni_data in universities:
        uni = University(**uni_data)
        db.session.merge(uni)
        print(f"  - {uni_data['name']} ({uni_data['id']})")

    db.session.commit()
    print(f"[OK] Created {len(universities)} universities\n")


def seed_proves_project():
    """Create PROVES shared collaborative project"""
    proves = ProjectModel(
        id='PROVES',
        university_id=None,  # Shared across all universities
        name='PROVES - Multi-University Collaborative Mission',
        type='proves',
        is_collaborative=True,
        duration=36,  # 3 years
        description='Shared collaborative space mission across 8 universities studying program resilience and knowledge transfer'
    )

    print("Creating PROVES shared project...")
    db.session.merge(proves)
    db.session.commit()
    print("[OK] Created PROVES project\n")


def seed_university_data(uni_id, uni_name):
    """Seed sample data for one university"""
    print(f"Seeding data for {uni_name}...")

    # Teams
    teams = [
        {'id': f'{uni_id}_team_software', 'university_id': uni_id, 'discipline': 'software',
         'lifecycle': 'established', 'name': f'{uni_name} Software', 'size': 5, 'experience': 24,
         'description': 'Flight software and data processing team'},

        {'id': f'{uni_id}_team_electrical', 'university_id': uni_id, 'discipline': 'electrical',
         'lifecycle': 'established', 'name': f'{uni_name} Electrical', 'size': 4, 'experience': 18,
         'description': 'Power and avionics systems team'},

        {'id': f'{uni_id}_team_missionops', 'university_id': uni_id, 'discipline': 'mission-ops',
         'lifecycle': 'incoming', 'name': f'{uni_name} Mission Ops', 'size': 3, 'experience': 6,
         'description': 'Mission operations and ground systems team'},

        {'id': f'{uni_id}_team_proves', 'university_id': uni_id, 'discipline': 'interdisciplinary',
         'lifecycle': 'established', 'name': f'{uni_name} PROVES Team', 'size': 6, 'experience': 12,
         'description': 'Interdisciplinary team for PROVES collaboration'},
    ]

    for team_data in teams:
        team = TeamModel(**team_data)
        db.session.add(team)

    print(f"  [OK] Created {len(teams)} teams")

    # Faculty
    faculty = [
        {'id': f'{uni_id}_faculty_pi', 'university_id': uni_id,
         'name': f'Dr. {uni_name} PI', 'role': 'Principal Investigator',
         'description': 'Project oversight and coordination'},

        {'id': f'{uni_id}_faculty_tech', 'university_id': uni_id,
         'name': f'Dr. {uni_name} Tech Lead', 'role': 'Technical Lead',
         'description': 'Technical guidance and mentoring'},
    ]

    for fac_data in faculty:
        fac = FacultyModel(**fac_data)
        db.session.add(fac)

    print(f"  [OK] Created {len(faculty)} faculty")

    # Internal Projects (besides PROVES)
    projects = [
        {'id': f'{uni_id}_project_cubesat', 'university_id': uni_id,
         'name': f'{uni_name} CubeSat Mission', 'type': 'jpl-contract',
         'is_collaborative': False, 'duration': 24,
         'description': 'Primary satellite mission with JPL contract'},

        {'id': f'{uni_id}_project_research', 'university_id': uni_id,
         'name': f'{uni_name} Research Initiative', 'type': 'internal',
         'is_collaborative': False, 'duration': 12,
         'description': 'Internal research and development project'},
    ]

    for proj_data in projects:
        proj = ProjectModel(**proj_data)
        db.session.add(proj)

    print(f"  [OK] Created {len(projects)} projects")

    # Internal Interfaces
    interfaces = [
        # Team to Faculty
        {'id': f'{uni_id}_int_1', 'from_entity': f'{uni_id}_team_software',
         'to_entity': f'{uni_id}_faculty_pi', 'interface_type': 'team-to-faculty',
         'bond_type': 'codified-strong', 'energy_loss': 5,
         'from_university': uni_id, 'to_university': uni_id, 'is_cross_university': False},

        # Team to Team
        {'id': f'{uni_id}_int_2', 'from_entity': f'{uni_id}_team_software',
         'to_entity': f'{uni_id}_team_electrical', 'interface_type': 'team-to-team',
         'bond_type': 'codified-moderate', 'energy_loss': 15,
         'from_university': uni_id, 'to_university': uni_id, 'is_cross_university': False},

        # Team to Project
        {'id': f'{uni_id}_int_3', 'from_entity': f'{uni_id}_team_software',
         'to_entity': f'{uni_id}_project_cubesat', 'interface_type': 'team-to-project',
         'bond_type': 'codified-strong', 'energy_loss': 5,
         'from_university': uni_id, 'to_university': uni_id, 'is_cross_university': False},
    ]

    for int_data in interfaces:
        interface = InterfaceModel(**int_data)
        db.session.add(interface)

    print(f"  [OK] Created {len(interfaces)} internal interfaces\n")


def seed_cross_university_interfaces():
    """Create PROVES collaboration interfaces between universities"""
    print("Creating cross-university PROVES interfaces...")

    cross_interfaces = [
        # Cal Poly Pomona <-> Texas State
        {'id': 'cross_cpp_texas_1',
         'from_entity': 'CalPolyPomona_team_proves',
         'to_entity': 'TexasState_team_proves',
         'interface_type': 'team-to-team', 'bond_type': 'codified-strong', 'energy_loss': 5,
         'from_university': 'CalPolyPomona', 'to_university': 'TexasState', 'is_cross_university': True},

        # Texas State <-> Columbia
        {'id': 'cross_texas_columbia_1',
         'from_entity': 'TexasState_team_proves',
         'to_entity': 'Columbia_team_proves',
         'interface_type': 'team-to-team', 'bond_type': 'codified-moderate', 'energy_loss': 15,
         'from_university': 'TexasState', 'to_university': 'Columbia', 'is_cross_university': True},

        # Cal Poly Pomona <-> Columbia
        {'id': 'cross_cpp_columbia_1',
         'from_entity': 'CalPolyPomona_team_proves',
         'to_entity': 'Columbia_team_proves',
         'interface_type': 'team-to-team', 'bond_type': 'codified-strong', 'energy_loss': 5,
         'from_university': 'CalPolyPomona', 'to_university': 'Columbia', 'is_cross_university': True},

        # Faculty collaboration
        {'id': 'cross_faculty_cpp_texas',
         'from_entity': 'CalPolyPomona_faculty_pi',
         'to_entity': 'TexasState_faculty_pi',
         'interface_type': 'faculty-to-faculty', 'bond_type': 'institutional-weak', 'energy_loss': 35,
         'from_university': 'CalPolyPomona', 'to_university': 'TexasState', 'is_cross_university': True},
    ]

    for int_data in cross_interfaces:
        interface = InterfaceModel(**int_data)
        db.session.add(interface)

    db.session.commit()
    print(f"[OK] Created {len(cross_interfaces)} cross-university interfaces\n")


def main():
    """Run all seeding operations"""
    print("\n" + "="*60)
    print("FRAMES Multi-University Data Seeding")
    print("="*60 + "\n")

    with app.app_context():
        # Recreate tables with new schema
        print("Updating database schema...")
        db.create_all()
        print("[OK] Schema updated\n")

        # Seed universities
        seed_universities()

        # Seed PROVES
        seed_proves_project()

        # Seed data for 3 universities
        seed_university_data('CalPolyPomona', 'Cal Poly Pomona')
        seed_university_data('TexasState', 'Texas State')
        seed_university_data('Columbia', 'Columbia')

        # Seed cross-university PROVES interfaces
        seed_cross_university_interfaces()

        # Summary
        print("="*60)
        print("SEEDING COMPLETE!")
        print("="*60)

        # Print counts
        uni_count = University.query.count()
        team_count = TeamModel.query.count()
        faculty_count = FacultyModel.query.count()
        project_count = ProjectModel.query.count()
        interface_count = InterfaceModel.query.count()
        cross_int_count = InterfaceModel.query.filter_by(is_cross_university=True).count()

        print(f"\nDatabase Summary:")
        print(f"  Universities:            {uni_count}")
        print(f"  Teams:                   {team_count}")
        print(f"  Faculty:                 {faculty_count}")
        print(f"  Projects:                {project_count} (including PROVES)")
        print(f"  Total Interfaces:        {interface_count}")
        print(f"  Cross-University Links:  {cross_int_count}")
        print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    main()
