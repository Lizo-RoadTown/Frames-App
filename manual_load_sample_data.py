#!/usr/bin/env python
"""Manually load sample data directly into the database"""
import sqlite3
import os

# Path to database
db_path = 'backend/frames.db'

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Clearing existing data...")
cursor.execute("DELETE FROM teams")
cursor.execute("DELETE FROM faculty")
cursor.execute("DELETE FROM projects")
cursor.execute("DELETE FROM interfaces")

# Insert teams
print("Inserting teams...")
teams = [
    ('team_1', 'electrical', 'established', 'Power Systems', 4, 18, 'Power and avionics systems - experienced team'),
    ('team_2', 'electrical', 'incoming', 'Electrical Beta', 3, 6, 'New electrical team in training phase'),
    ('team_3', 'software', 'established', 'Flight Software', 5, 24, 'Flight software and data processing'),
    ('team_4', 'software', 'outgoing', 'Software Legacy', 2, 36, 'Graduating software team with critical knowledge'),
    ('team_5', 'mission-ops', 'incoming', 'Mission Ops New', 3, 3, 'New mission operations team'),
    ('team_6', 'mission-ops', 'established', 'Mission Ops Core', 4, 15, 'Established operations team'),
    ('team_7', 'mechanical', 'established', 'Mechanical Systems', 3, 12, 'Mechanical systems and structures'),
    ('team_8', 'communications', 'incoming', 'Comm Systems', 2, 4, 'New communications team')
]
cursor.executemany(
    "INSERT INTO teams (id, discipline, lifecycle, name, size, experience, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
    teams
)

# Insert faculty
print("Inserting faculty...")
faculty = [
    ('faculty_1', 'Dr. Principal Investigator', 'Principal Investigator', 'Project oversight and coordination, institutional interface'),
    ('faculty_2', 'Dr. Technical Lead', 'Technical Lead', 'Technical guidance and mentoring, knowledge transfer'),
    ('faculty_3', 'Program Director', 'Program Director', 'Program continuity and institutional support')
]
cursor.executemany(
    "INSERT INTO faculty (id, name, role, description) VALUES (?, ?, ?, ?)",
    faculty
)

# Insert projects
print("Inserting projects...")
projects = [
    ('project_1', 'JPL CubeSat Mission', 'jpl-contract', 3, 'Primary satellite mission with JPL contract'),
    ('project_2', 'Multi-University Research', 'multiversity', 2, 'Multi-university collaborative research project'),
    ('project_3', 'Contract Pursuit', 'contract-pursuit', 1, 'New contract opportunity being pursued')
]
cursor.executemany(
    "INSERT INTO projects (id, name, type, duration, description) VALUES (?, ?, ?, ?, ?)",
    projects
)

# Insert interfaces
print("Inserting interfaces...")
interfaces = [
    ('interface_1', 'team_1', 'faculty_1', 'team-to-faculty', 'codified-strong', 5),
    ('interface_2', 'team_3', 'faculty_2', 'team-to-faculty', 'codified-strong', 5),
    ('interface_3', 'team_6', 'faculty_3', 'team-to-faculty', 'codified-moderate', 15),
    ('interface_4', 'team_4', 'team_3', 'team-to-team', 'institutional-weak', 35),
    ('interface_5', 'team_2', 'team_1', 'team-to-team', 'institutional-weak', 35),
    ('interface_6', 'team_5', 'team_6', 'team-to-team', 'institutional-weak', 35),
    ('interface_7', 'team_1', 'project_1', 'team-to-project', 'codified-strong', 5),
    ('interface_8', 'team_3', 'project_1', 'team-to-project', 'codified-strong', 5),
    ('interface_9', 'team_6', 'project_2', 'team-to-project', 'codified-moderate', 15),
    ('interface_10', 'team_7', 'project_2', 'team-to-project', 'codified-moderate', 15),
    ('interface_11', 'team_8', 'project_3', 'team-to-project', 'fragile-temporary', 60)
]
cursor.executemany(
    "INSERT INTO interfaces (id, from_entity, to_entity, interface_type, bond_type, energy_loss) VALUES (?, ?, ?, ?, ?, ?)",
    interfaces
)

conn.commit()

# Verify
print("\nVerifying data...")
cursor.execute("SELECT COUNT(*) FROM teams")
print(f"Teams: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM faculty")
print(f"Faculty: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM projects")
print(f"Projects: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM interfaces")
print(f"Interfaces: {cursor.fetchone()[0]}")

conn.close()
print("\n✓ Sample data loaded successfully!")
