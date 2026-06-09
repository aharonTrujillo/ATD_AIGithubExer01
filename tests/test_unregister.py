"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.
Tests student unregistration functionality, including success and error cases.
"""

import pytest


class TestUnregister:
    """Test suite for DELETE unregister endpoint."""

    def test_unregister_student_success(self, client, fresh_activities):
        """
        Test that a signed-up student can be successfully unregistered.

        AAA Pattern:
        - Arrange: Student already in participants list
        - Act: DELETE unregister request
        - Assert: Response is 200 and student is removed from participants
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {student_email} from {activity_name}"
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert student_email not in participants

    def test_unregister_nonexistent_student_fails(self, client, fresh_activities):
        """
        Test that unregistering a non-existent student returns 400 error.

        AAA Pattern:
        - Arrange: Student email not in participants list
        - Act: DELETE unregister request for non-existent student
        - Assert: Response is 400 with "Student is not signed up"
        """
        # Arrange
        activity_name = "Chess Club"
        nonexistent_email = "not_signed_up@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": nonexistent_email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is not signed up for this activity"

    def test_unregister_from_invalid_activity_returns_404(self, client, fresh_activities):
        """
        Test that unregistering from a non-existent activity returns 404.

        AAA Pattern:
        - Arrange: Invalid activity name
        - Act: DELETE unregister request for non-existent activity
        - Assert: Response is 404 with "Activity not found"
        """
        # Arrange
        invalid_activity = "Non-existent Activity"
        student_email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{invalid_activity}/unregister",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_one_student_others_remain(self, client, fresh_activities):
        """
        Test that unregistering one student doesn't affect others.

        AAA Pattern:
        - Arrange: Activity with multiple participants
        - Act: DELETE unregister request for one student
        - Assert: Only that student is removed, others remain
        """
        # Arrange
        activity_name = "Chess Club"
        student_to_remove = "michael@mergington.edu"
        student_to_keep = "daniel@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_to_remove}
        )

        # Assert
        assert response.status_code == 200
        
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert student_to_remove not in participants
        assert student_to_keep in participants

    def test_unregister_then_signup_again_allowed(self, client, fresh_activities):
        """
        Test that a student can re-signup after being unregistered.

        AAA Pattern:
        - Arrange: Student in participants
        - Act: DELETE unregister, then POST signup
        - Assert: Second signup succeeds, student is added back
        """
        # Arrange
        activity_name = "Programming Class"
        student_email = "emma@mergington.edu"  # Already in Programming Class

        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )

        # Act - Sign up again
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )

        # Assert
        assert unregister_response.status_code == 200
        assert signup_response.status_code == 200
        
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert student_email in participants

    def test_unregister_empty_email_not_found(self, client, fresh_activities):
        """
        Test unregister behavior with empty email string.

        AAA Pattern:
        - Arrange: Empty email string
        - Act: DELETE unregister request with empty email
        - Assert: Returns 400 "not signed up" error
        """
        # Arrange
        activity_name = "Gym Class"
        empty_email = ""

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": empty_email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is not signed up for this activity"
