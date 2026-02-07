import pytest


class TestCreateCategory:
    """Тесты создания категорий"""
    
    def test_create_category_success(self, client, auth_headers):
        """Успешное создание категории"""
        response = client.post(
            "/categories/",
            json={"name": "Зарплата", "type": "Income"},
            headers=auth_headers
        )
        
        assert response.status_code == 201
        assert response.json()["name"] == "Зарплата"
        assert response.json()["type"] == "Income"
    
    def test_create_category_unauthorized(self, client):
        """Ошибка при отсутствии токена"""
        response = client.post(
            "/categories/",
            json={"name": "Зарплата", "type": "Income"}
        )
        
        assert response.status_code == 401
    
    def test_create_duplicate_category(self, client, auth_headers, test_category):
        """Ошибка при дублировании названия категории"""
        response = client.post(
            "/categories/",
            json={"name": "Food", "type": "Expense"},
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert "already exist" in response.json()["detail"].lower()


class TestGetCategories:
    """Тесты получения категорий"""
    
    def test_get_all_categories(self, client, auth_headers, test_category):
        """Получение всех категорий пользователя"""
        response = client.get("/categories/", headers=auth_headers)
        
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Food"
    
    def test_get_category_by_id(self, client, auth_headers, test_category):
        """Получение категории по ID"""
        response = client.get(f"/categories/{test_category.id}", headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["id"] == test_category.id
    
    def test_get_nonexistent_category(self, client, auth_headers):
        """Ошибка при запросе несуществующей категории"""
        response = client.get("/categories/9999", headers=auth_headers)
        
        assert response.status_code == 404