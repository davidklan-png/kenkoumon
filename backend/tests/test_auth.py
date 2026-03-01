"""
Authentication endpoint tests (TDD).
"""

import pytest
from fastapi import status


class TestRegister:
    """Tests for user registration."""

    def test_register_success(self, client):
        """Test successful registration."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "password123",
                "full_name": "New User"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_register_duplicate_email(self, client, test_patient):
        """Test registration with duplicate email fails."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"]

    def test_register_short_password(self, client):
        """Test registration with short password fails."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "short@example.com",
                "password": "short",
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestLogin:
    """Tests for user login."""

    def test_login_success(self, client, test_patient):
        """Test successful login."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "testpass123"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data

    def test_login_wrong_email(self, client):
        """Test login with wrong email fails."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "wrong@example.com",
                "password": "testpass123"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_wrong_password(self, client, test_patient):
        """Test login with wrong password fails."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetCurrentPatient:
    """Tests for getting current patient info."""

    def test_get_me_authenticated(self, client, auth_headers):
        """Test getting current patient when authenticated."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["full_name"] == "Test Patient"

    def test_get_me_unauthenticated(self, client):
        """Test getting current patient without auth fails."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
