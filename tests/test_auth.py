import pytest


class TestRegistration:
    """Тест на регистрацию пользователей"""
    def test_register_success(self, client):
        """Проверка на успешную регистрацию"""
        response = client.post(
            "/auth/register",
            json={"username": "newuser", "password": "password123"}
        )
        
        assert response.status_code == 201
        assert response.json()["username"] == "newuser"
        assert "id" in response.json()
        assert "hashed_password" not in response.json() # пароль не возвращается
    
    
    def test_register_duplicate_username(self, client, test_user):
        """Проверка на существующего пользователя"""
        response = client.post(
            "/auth/register",
            json={"username": "testuser", "password": "password123"}
        )
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()
        
        
    def test_register_short_password(self, client):
        """Ошибка при коротком пароле (менее 8 символов)"""
        response = client.post(
            "/auth/register",
            json={"username": "newuser", "password": "123"}
        )
        
        assert response.status_code == 422
        

class TestLogin:
    """Тест для входа пользователей"""
    def test_login_success(self, client, test_user):
        """Успешный вход в профиль"""
        response = client.post(
            "/auth/login",
            data={"username": "testuser", "password": "testpassword123"}
        )
        
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
        
    
    def test_login_wrong_password(self, client, test_user):
        """Неправильный пароль"""
        response = client.post(
            "/auth/login",
            data={"username": "testuser", "password": "wrongpassword"}
        )
        
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()
        
    
    def test_login_nonexistent_user(self, client):
        """Несуществующий пользователь"""
        response = client.post(
            "/auth/login",
            data={"username": "nouser", "password": "testpassword123"}
        )
        
        assert response.status_code == 401