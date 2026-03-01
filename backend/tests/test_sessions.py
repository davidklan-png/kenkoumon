"""
Session endpoint tests (BDD scenarios).
"""

import pytest
from fastapi import status
from datetime import datetime


class TestCreateSession:
    """BDD Scenario: Create a new recording session."""

    def test_create_session_authenticated(self, client, auth_headers):
        """
        Given I am authenticated
        When I create a new session
        Then the session should be created
        And it should have a unique ID
        """
        response = client.post(
            "/api/v1/sessions",
            json={"date": datetime.utcnow().isoformat()},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "id" in data
        assert data["status"] == "uploading"

    def test_create_session_unauthenticated(self, client):
        """
        Given I am not authenticated
        When I try to create a session
        Then I should receive a 401 error
        """
        response = client.post(
            "/api/v1/sessions",
            json={"date": datetime.utcnow().isoformat()}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestListSessions:
    """BDD Scenario: View session history."""

    def test_list_sessions(self, client, auth_headers, test_session):
        """
        Given I have recorded sessions
        When I view my session history
        Then I should see all my sessions
        And they should be sorted by date
        """
        response = client.get("/api/v1/sessions", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        sessions = response.json()
        assert len(sessions) >= 1
        assert any(s["id"] == test_session.id for s in sessions)


class TestGetSession:
    """BDD Scenario: View a specific session."""

    def test_get_session_success(self, client, auth_headers, test_session):
        """
        Given I have a session
        When I request that session by ID
        Then I should see the session details
        """
        response = client.get(
            f"/api/v1/sessions/{test_session.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_session.id
        assert data["transcript_ja"] == test_session.transcript_ja

    def test_get_session_not_found(self, client, auth_headers):
        """
        Given I request a non-existent session
        When I make the request
        Then I should receive a 404 error
        """
        response = client.get(
            "/api/v1/sessions/nonexistent",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateSession:
    """BDD Scenario: Update patient notes."""

    def test_update_patient_notes(self, client, auth_headers, test_session):
        """
        Given I have a completed session
        When I add patient notes
        Then the notes should be saved
        """
        response = client.patch(
            f"/api/v1/sessions/{test_session.id}",
            json={"patient_notes": "これは患者のメモです。"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["patient_notes"] == "これは患者のメモです。"


class TestDeleteSession:
    """BDD Scenario: Delete a session."""

    def test_delete_session(self, client, auth_headers, db_session):
        """
        Given I have a session
        When I delete it
        Then the session should be removed
        """
        from models import Session as DBSession
        import uuid

        session = DBSession(
            id=str(uuid.uuid4()),
            patient_id="test-patient",
            date=datetime.utcnow(),
            status="uploaded",
        )
        db_session.add(session)
        db_session.commit()

        response = client.delete(
            f"/api/v1/sessions/{session.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify deleted
        response = client.get(
            f"/api/v1/sessions/{session.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
