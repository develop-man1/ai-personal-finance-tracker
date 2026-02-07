import pytest
from decimal import Decimal


class TestCreateTransaction:
    """Тесты создания транзакций"""
    
    def test_create_transaction_success(self, client, auth_headers, test_category):
        """Успешное создание транзакции"""
        response = client.post(
            "/transactions/",
            json={
                "amount": 100.50,
                "description": "Покупка продуктов",
                "category_id": test_category.id
            },
            headers=auth_headers
        )
        
        assert response.status_code == 201
        assert float(response.json()["amount"]) == 100.50
        assert response.json()["description"] == "Покупка продуктов"
    
    def test_create_transaction_invalid_category(self, client, auth_headers):
        """Ошибка при несуществующей категории"""
        response = client.post(
            "/transactions/",
            json={
                "amount": 100,
                "category_id": 9999
            },
            headers=auth_headers
        )
        
        assert response.status_code == 404


class TestGetTransactions:
    """Тесты получения транзакций"""
    
    def test_get_all_transactions(self, client, auth_headers, test_category):
        """Получение всех транзакций"""
        # Создаём транзакцию
        client.post(
            "/transactions/",
            json={"amount": 50, "category_id": test_category.id},
            headers=auth_headers
        )
        
        response = client.get("/transactions/", headers=auth_headers)
        
        assert response.status_code == 200
        assert len(response.json()) == 1


class TestDeleteTransaction:
    """Тесты удаления транзакций"""
    
    def test_delete_transaction_success(self, client, auth_headers, test_category):
        """Успешное удаление транзакции"""
        # Создаём транзакцию
        create_response = client.post(
            "/transactions/",
            json={"amount": 50, "category_id": test_category.id},
            headers=auth_headers
        )
        transaction_id = create_response.json()["id"]
        
        # Удаляем
        response = client.delete(f"/transactions/{transaction_id}", headers=auth_headers)
        
        assert response.status_code == 204
    
    def test_delete_nonexistent_transaction(self, client, auth_headers):
        """Ошибка при удалении несуществующей транзакции"""
        response = client.delete("/transactions/9999", headers=auth_headers)
        
        assert response.status_code == 404


class TestBalance:
    """Тесты подсчёта баланса"""
    
    def test_calculate_balance(self, client, auth_headers, db, test_user):
        """Правильный расчёт баланса"""
        # Создаём категории
        income_cat = client.post(
            "/categories/",
            json={"name": "Зарплата", "type": "Income"},
            headers=auth_headers
        ).json()
        
        expense_cat = client.post(
            "/categories/",
            json={"name": "Еда", "type": "Expense"},
            headers=auth_headers
        ).json()
        
        # Создаём транзакции
        client.post(
            "/transactions/",
            json={"amount": 1000, "category_id": income_cat["id"]},
            headers=auth_headers
        )
        client.post(
            "/transactions/",
            json={"amount": 300, "category_id": expense_cat["id"]},
            headers=auth_headers
        )
        
        # Проверяем баланс
        response = client.get("/transactions/balance", headers=auth_headers)
        
        assert response.status_code == 200
        assert float(response.json()["income"]) == 1000
        assert float(response.json()["expense"]) == 300
        assert float(response.json()["balance"]) == 700