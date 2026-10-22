import pytest


def test_create_and_list_categories(client):
    response = client.post("/categories", json={"name": "Учеба"})

    assert response.status_code == 201
    assert client.get("/categories").json() == [response.json()]


def test_rename_category(client):
    category_id = client.post("/categories", json={"name": "Учеба"}).json()["id"]

    response = client.patch(f"/categories/{category_id}", json={"name": "Работа"})

    assert response.status_code == 200
    assert response.json()["name"] == "Работа"


def test_delete_category(client):
    category_id = client.post("/categories", json={"name": "Учеба"}).json()["id"]

    assert client.delete(f"/categories/{category_id}").status_code == 204
    assert client.get("/categories").json() == []


@pytest.mark.parametrize(
    "method, kwargs",
    [
        ("patch", {"json": {"name": "x"}}),
        ("delete", {}),
    ],
)
def test_missing_category_returns_404(client, method, kwargs):
    response = getattr(client, method)("/categories/not-exists", **kwargs)

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}
