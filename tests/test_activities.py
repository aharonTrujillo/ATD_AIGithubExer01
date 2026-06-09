"""
Tests for the GET /activities endpoint.
Tests the retrieval of all available activities.
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client, fresh_activities):
        """
        Test that GET /activities returns all available activities.

        AAA Pattern:
        - Arrange: Test client and activities fixture ready
        - Act: Make GET request to /activities
        - Assert: Response status is 200 and contains all activities
        """
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert set(data.keys()) == set(expected_activities)

    def test_get_activities_returns_correct_structure(self, client, fresh_activities):
        """
        Test that each activity has the correct structure.

        AAA Pattern:
        - Arrange: Test client and activities fixture ready
        - Act: Make GET request to /activities
        - Assert: Each activity has required fields (description, schedule, max_participants, participants)
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data, dict)
            assert set(activity_data.keys()) == required_fields

    def test_get_activities_includes_participants(self, client, fresh_activities):
        """
        Test that activities include participant information.

        AAA Pattern:
        - Arrange: Test client and activities fixture ready
        - Act: Make GET request to /activities
        - Assert: Chess Club includes michael@mergington.edu and daniel@mergington.edu
        """
        # Arrange
        expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        chess_club = data["Chess Club"]
        assert chess_club["participants"] == expected_participants

    def test_get_activities_max_participants_correct(self, client, fresh_activities):
        """
        Test that max_participants values are correct.

        AAA Pattern:
        - Arrange: Expected max participants for each activity
        - Act: Make GET request to /activities
        - Assert: max_participants matches expected values
        """
        # Arrange
        expected_max = {
            "Chess Club": 12,
            "Programming Class": 20,
            "Gym Class": 30
        }

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, max_count in expected_max.items():
            assert data[activity_name]["max_participants"] == max_count
