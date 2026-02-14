import pytest


class TestRegistration:

    async def test_register_success(self, client):
        response = await client.post(
            "/auth/register",
            json={"username": "newuser", "password": "password123"}
        )
        assert response.status_code == 201
        assert response.json()["username"] == "newuser"
        assert "id" in response.json()
        assert "hashed_password" not in response.json()

    async def test_register_duplicate_username(self, client, test_user):
        response = await client.post(
            "/auth/register",
            json={"username": "testuser", "password": "password123"}
        )
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    async def test_register_short_password(self, client):
        response = await client.post(
            "/auth/register",
            json={"username": "newuser", "password": "123"}
        )
        assert response.status_code == 422


class TestLogin:

    async def test_login_success(self, client, test_user):
        response = await client.post(
            "/auth/login",
            data={"username": "testuser", "password": "testpassword123"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    async def test_login_wrong_password(self, client, test_user):
        response = await client.post(
            "/auth/login",
            data={"username": "testuser", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    async def test_login_nonexistent_user(self, client):
        response = await client.post(
            "/auth/login",
            data={"username": "nouser", "password": "testpassword123"}
        )
        assert response.status_code == 401