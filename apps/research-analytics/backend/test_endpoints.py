#!/usr/bin/env python
"""
Quick test script for multi-university endpoints using the hosted database.
"""

import os
import sys

# Ensure repo root is on sys.path for absolute imports
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app
from db_models import University, TeamModel, FacultyModel, ProjectModel, InterfaceModel  # noqa: F401


def test_endpoints() -> None:
    """Test key endpoints and print basic status."""

    app.config["TESTING"] = True
    app.config["PROPAGATE_EXCEPTIONS"] = True

    # Ensure routes run inside an application context so Flask-SQLAlchemy is bound
    with app.app_context(), app.test_client() as client:
        print("=" * 60)
        print("Testing Multi-University API Endpoints")
        print("=" * 60 + "\n")

        tests = [
            ("GET /api/universities", "/api/universities"),
            ("GET /api/teams", "/api/teams"),
            ("GET /api/teams?university_id=CalPolyPomona", "/api/teams?university_id=CalPolyPomona"),
            ("GET /api/projects", "/api/projects"),
            ("GET /api/dashboard/comparative", "/api/dashboard/comparative"),
            ("GET /api/interfaces?cross_university=true", "/api/interfaces?cross_university=true"),
        ]

        for label, url in tests:
            print(label)
            resp = client.get(url)
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.get_json(silent=True)
                preview = data
                if isinstance(data, list):
                    preview = data[:3]
                print(f"   Body preview: {preview}")
            else:
                print(f"   ERROR: {resp.data}")
            print()

        print("=" * 60)
        print("Testing Complete!")
        print("=" * 60)


if __name__ == "__main__":
    test_endpoints()
