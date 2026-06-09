"""
Pytest configuration and fixtures for FastAPI tests.
Provides test client and fresh activity state for each test.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance for making test requests.
    """
    return TestClient(app)


@pytest.fixture
def fresh_activities(monkeypatch):
    """
    Fixture that provides a fresh copy of activities for each test.
    Uses monkeypatch to override the global activities dict,
    ensuring test isolation.
    """
    # Define fresh test data
    test_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }

    # Clear existing activities and add test data
    activities.clear()
    activities.update(test_activities)

    yield activities

    # Cleanup: restore or clear (pytest handles fixture cleanup automatically)
