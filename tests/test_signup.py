"""
Tests for the POST /activities/{activity_name}/signup endpoint.
Tests student signup functionality, including success and error cases.
"""

import pytest


class TestSignup:
    """Test suite for POST signup endpoint."""

    def test_signup_new_student_success(self, client, fresh_activities):
        """
        Test that a new student can successfully sign up for an activity.

        AAA Pattern:
        - Arrange: New student email and activity name
        - Act: POST signup request
        - Assert: Response is 200 and student is added to participants
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = "new_student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {student_email} for {activity_name}"
        
        # Verify participant was added
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert student_email in participants

    def test_signup_duplicate_student_fails(self, client, fresh_activities):
        """
        Test that a student cannot sign up twice for the same activity.

        AAA Pattern:
        - Arrange: Student already in participants list
        - Act: POST signup request with same email twice
        - Assert: Second signup returns 400 error
        """
        # Arrange
        activity_name = "Chess Club"
        duplicate_email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": duplicate_email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is already signed up for this activity"

    def test_signup_invalid_activity_returns_404(self, client, fresh_activities):
        """
        Test that signing up for a non-existent activity returns 404.

        AAA Pattern:
        - Arrange: Invalid activity name
        - Act: POST signup request for non-existent activity
        - Assert: Response is 404 with "Activity not found"
        """
        # Arrange
        invalid_activity = "Non-existent Activity"
        student_email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_multiple_students_same_activity(self, client, fresh_activities):
        """
        Test that multiple different students can sign up for the same activity.

        AAA Pattern:
        - Arrange: Two different student emails
        - Act: POST signup requests for both students
        - Assert: Both students are in participants list
        """
        # Arrange
        activity_name = "Programming Class"
        student1_email = "new_student1@mergington.edu"
        student2_email = "new_student2@mergington.edu"

        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student1_email}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student2_email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert student1_email in participants
        assert student2_email in participants

    def test_signup_empty_email_allowed(self, client, fresh_activities):
        """
        Test signup behavior with empty email string.

        AAA Pattern:
        - Arrange: Empty email string
        - Act: POST signup request with empty email
        - Assert: Request is processed (email validation not in scope)
        """
        # Arrange
        activity_name = "Gym Class"
        empty_email = ""

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": empty_email}
        )

        # Assert
        # Empty email is allowed by the current implementation
        assert response.status_code == 200
