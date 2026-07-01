from fastapi import status


def test_create_customer(client):
    response = client.post(
        "/customers",
        json={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "age": 30,
            "description": "Test customer",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john.doe@example.com"
    assert response.json()["age"] == 30
    assert response.json()["description"] == "Test customer"


def test_read_customers(client):
    response = client.post(
        "/customers",
        json={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "age": 30,
            "description": "Test customer",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    customer_id: int = response.json()["id"]
    response_read = client.get(f"/customers/{customer_id}")
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()["name"] == "John Doe"
