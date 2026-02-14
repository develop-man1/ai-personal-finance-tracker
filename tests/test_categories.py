import pytest


class TestCreateCategory:

    async def test_create_category_success(self, client, auth_headers):
        response = await client.post(
            "/categories/",
            json={"name": "Зарплата", "type": "Income"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["name"] == "Зарплата"
        assert response.json()["type"] == "Income"

    async def test_create_category_unauthorized(self, client):
        response = await client.post(
            "/categories/",
            json={"name": "Зарплата", "type": "Income"}
        )
        assert response.status_code == 401

    async def test_create_duplicate_category(self, client, auth_headers, test_category):
        response = await client.post(
            "/categories/",
            json={"name": "Food", "type": "Expense"},
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "already exist" in response.json()["detail"].lower()


class TestGetCategories:

    async def test_get_all_categories(self, client, auth_headers, test_category):
        response = await client.get("/categories/", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Food"

    async def test_get_category_by_id(self, client, auth_headers, test_category):
        response = await client.get(
            f"/categories/{test_category.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["id"] == test_category.id

    async def test_get_nonexistent_category(self, client, auth_headers):
        response = await client.get("/categories/9999", headers=auth_headers)
        assert response.status_code == 404