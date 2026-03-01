"""
Report sharing endpoint tests (BDD scenarios).
"""

import pytest
from fastapi import status
from datetime import datetime, timedelta


class TestGetReport:
    """BDD Scenario: View a generated report."""

    def test_get_report_success(self, client, auth_headers, test_session):
        """
        Given I have a completed session
        When I request the report
        Then I should see all 4 sections
        And extracted entities
        """
        response = client.get(
            f"/api/v1/reports/{test_session.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "report_ja" in data
        assert "entities" in data


class TestCreateShareLink:
    """BDD Scenario: Generate secure share link."""

    def test_create_share_link(self, client, auth_headers, test_session):
        """
        Given I have a completed report
        When I create a share link
        Then a unique token should be generated
        And an expiration date should be set
        """
        # Update session to complete
        from models import Session as DBSession
        test_session.status = "complete"
        test_session.report_ja = "# テストレポート\n\n内容です"
        test_session.transcript_ja = "テスト文字起こし"

        response = client.post(
            f"/api/v1/reports/{test_session.id}/share",
            json={"expires_in_days": 30},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "token" in data
        assert "url" in data
        assert "expires_at" in data

    def test_create_share_link_incomplete_session(self, client, auth_headers, test_session):
        """
        Given I have an incomplete session
        When I try to create a share link
        Then I should receive an error
        """
        response = client.post(
            f"/api/v1/reports/{test_session.id}/share",
            json={"expires_in_days": 30},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestViewSharedReport:
    """BDD Scenario: Public report viewing."""

    def test_view_shared_report_valid_token(self, client, db_session, test_patient):
        """
        Given I have a valid share link token
        When I open the link
        Then I should see the full report
        And no login should be required
        """
        from models import Session as DBSession, ShareLink
        import uuid

        # Create session and share link
        session = DBSession(
            id=str(uuid.uuid4()),
            patient_id=test_patient.id,
            date=datetime.utcnow(),
            status="complete",
            report_ja="# テストレポート\n\n内容です",
        )
        db_session.add(session)
        db_session.flush()

        link = ShareLink(
            id=str(uuid.uuid4()),
            session_id=session.id,
            token="test-token-123",
            expires_at=datetime.utcnow() + timedelta(days=30),
        )
        db_session.add(link)
        db_session.commit()

        response = client.get(f"/share/test-token-123")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "report_ja" in data

    def test_view_shared_report_expired_token(self, client, db_session, test_patient):
        """
        Given I have an expired share link
        When I open the link
        Then I should see an expiration message
        """
        from models import Session as DBSession, ShareLink
        import uuid

        session = DBSession(
            id=str(uuid.uuid4()),
            patient_id=test_patient.id,
            date=datetime.utcnow(),
            status="complete",
        )
        db_session.add(session)
        db_session.flush()

        link = ShareLink(
            id=str(uuid.uuid4()),
            session_id=session.id,
            token="expired-token",
            expires_at=datetime.utcnow() - timedelta(days=1),
        )
        db_session.add(link)
        db_session.commit()

        response = client.get("/share/expired-token")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_view_shared_report_revoked_token(self, client, db_session, test_patient):
        """
        Given I have a revoked share link
        When I open the link
        Then I should see a revocation message
        """
        from models import Session as DBSession, ShareLink
        import uuid

        session = DBSession(
            id=str(uuid.uuid4()),
            patient_id=test_patient.id,
            date=datetime.utcnow(),
            status="complete",
        )
        db_session.add(session)
        db_session.flush()

        link = ShareLink(
            id=str(uuid.uuid4()),
            session_id=session.id,
            token="revoked-token",
            expires_at=datetime.utcnow() + timedelta(days=30),
            revoked=True,
        )
        db_session.add(link)
        db_session.commit()

        response = client.get("/share/revoked-token")
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestRevokeShareLink:
    """BDD Scenario: Revoke a share link."""

    def test_revoke_share_link(self, client, auth_headers, db_session, test_patient):
        """
        Given I have an active share link
        When I revoke it
        Then the link should no longer work
        """
        from models import Session as DBSession, ShareLink
        import uuid

        session = DBSession(
            id=str(uuid.uuid4()),
            patient_id=test_patient.id,
            date=datetime.utcnow(),
            status="complete",
        )
        db_session.add(session)
        db_session.flush()

        link = ShareLink(
            id=str(uuid.uuid4()),
            session_id=session.id,
            token="revoke-test-token",
            expires_at=datetime.utcnow() + timedelta(days=30),
        )
        db_session.add(link)
        db_session.commit()

        response = client.delete(
            f"/api/v1/reports/shares/{link.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify link no longer works
        response = client.get("/share/revoke-test-token")
        assert response.status_code == status.HTTP_403_FORBIDDEN
