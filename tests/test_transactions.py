import pytest


class TestCreateTransaction:

    async def test_create_transaction_success(self, client, auth_headers, test_category):
        response = await client.post(
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

    async def test_create_transaction_invalid_category(self, client, auth_headers):
        response = await client.post(
            "/transactions/",
            json={"amount": 100, "category_id": 9999},
            headers=auth_headers
        )
        assert response.status_code == 404


class TestGetTransactions:

    async def test_get_all_transactions(self, client, auth_headers, test_category):
        await client.post(
            "/transactions/",
            json={"amount": 50, "category_id": test_category.id},
            headers=auth_headers
        )
        response = await client.get("/transactions/", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 1


class TestDeleteTransaction:

    async def test_delete_transaction_success(self, client, auth_headers, test_category):
        create_response = await client.post(
            "/transactions/",
            json={"amount": 50, "category_id": test_category.id},
            headers=auth_headers
        )
        transaction_id = create_response.json()["id"]

        response = await client.delete(
            f"/transactions/{transaction_id}",
            headers=auth_headers
        )
        assert response.status_code == 204

    async def test_delete_nonexistent_transaction(self, client, auth_headers):
        response = await client.delete("/transactions/9999", headers=auth_headers)
        assert response.status_code == 404


class TestBalance:

    async def test_calculate_balance(self, client, auth_headers):
        income_cat = (await client.post(
            "/categories/",
            json={"name": "Зарплата", "type": "Income"},
            headers=auth_headers
        )).json()

        expense_cat = (await client.post(
            "/categories/",
            json={"name": "Еда", "type": "Expense"},
            headers=auth_headers
        )).json()

        await client.post(
            "/transactions/",
            json={"amount": 1000, "category_id": income_cat["id"]},
            headers=auth_headers
        )
        await client.post(
            "/transactions/",
            json={"amount": 300, "category_id": expense_cat["id"]},
            headers=auth_headers
        )

        response = await client.get("/transactions/balance", headers=auth_headers)
        assert response.status_code == 200
        assert float(response.json()["income"]) == 1000
        assert float(response.json()["expense"]) == 300
        assert float(response.json()["balance"]) == 700