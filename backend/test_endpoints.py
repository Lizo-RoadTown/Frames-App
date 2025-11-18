#!/usr/bin/env python
"""
Quick test script for new multi-university endpoints
"""

from app import app, db
from db_models import University, TeamModel, FacultyModel, ProjectModel, InterfaceModel
import json

def test_endpoints():
    """Test all new multi-university endpoints"""

    with app.test_client() as client:
        print("="*60)
        print("Testing Multi-University API Endpoints")
        print("="*60 + "\n")

        # Test 1: GET /api/universities
        print("1. GET /api/universities")
        response = client.get('/api/universities')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   Universities: {len(data)}")
            for uni in data[:3]:
                print(f"     - {uni['id']}: {uni['name']}")
        else:
            print(f"   ERROR: {response.data}")
        print()

        # Test 2: GET /api/teams (database-backed with university_id)
        print("2. GET /api/teams")
        response = client.get('/api/teams')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   Teams: {len(data)}")
            if data:
                first_team = data[0]
                print(f"     First team: {first_team.get('id')}")
                print(f"     University ID: {first_team.get('university_id')}")
        else:
            print(f"   ERROR: {response.data}")
        print()

        # Test 3: GET /api/teams?university_id=CalPolyPomona
        print("3. GET /api/teams?university_id=CalPolyPomona")
        response = client.get('/api/teams?university_id=CalPolyPomona')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   Cal Poly Pomona teams: {len(data)}")
            for team in data:
                print(f"     - {team['id']}: {team['name']}")
        else:
            print(f"   ERROR: {response.data}")
        print()

        # Test 4: GET /api/projects
        print("4. GET /api/projects")
        response = client.get('/api/projects')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   Projects: {len(data)}")
            for proj in data:
                print(f"     - {proj['id']}: {proj['name']} (uni: {proj.get('university_id')})")
        else:
            print(f"   ERROR: {response.data}")
        print()

        # Test 5: GET /api/dashboard/comparative
        print("5. GET /api/dashboard/comparative")
        response = client.get('/api/dashboard/comparative')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   Universities: {len(data.get('universities', {}))}")
            print(f"   Cross-university interfaces: {len(data.get('cross_university_interfaces', []))}")
            print(f"   PROVES project: {data.get('proves_project', {}).get('id')}")
            print("\n   Aggregate metrics:")
            for key, value in data.get('aggregate_metrics', {}).items():
                print(f"     {key}: {value}")
        else:
            print(f"   ERROR: {response.data}")
        print()

        # Test 6: GET /api/interfaces?cross_university=true
        print("6. GET /api/interfaces?cross_university=true")
        response = client.get('/api/interfaces?cross_university=true')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   Cross-university interfaces: {len(data)}")
            for interface in data[:3]:
                print(f"     - {interface['from']} <-> {interface['to']}")
        else:
            print(f"   ERROR: {response.data}")
        print()

        print("="*60)
        print("Testing Complete!")
        print("="*60)


if __name__ == '__main__':
    test_endpoints()
