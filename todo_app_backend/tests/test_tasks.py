def test_list_tasks_empty(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Do the task"})

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Do the task"
    assert data["completed"] is False
    assert len(data["id"]) == 36  # UUID


def test_created_task_appears_in_list(client):
    client.post("/tasks", json={"title": "Do the task"})

    tasks = client.get("/tasks").json()

    assert [t["title"] for t in tasks] == ["Do the task"]


def test_create_task_without_title_returns_422(client):
    response = client.post("/tasks", json={})

    assert response.status_code == 422


def test_update_task_completed(client):
    task_id = client.post("/tasks", json={"title": "A"}).json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"completed": True})

    assert response.status_code == 200
    assert response.json()["completed"] is True
    assert response.json()["title"] == "A"  # не присланное поле не изменилось


def test_update_task_can_unmark_completed(client):
    task_id = client.post("/tasks", json={"title": "A"}).json()["id"]
    client.patch(f"/tasks/{task_id}", json={"completed": True})

    response = client.patch(f"/tasks/{task_id}", json={"completed": False})

    assert response.json()["completed"] is False


def test_update_missing_task_returns_404(client):
    response = client.patch("/tasks/not-exists", json={"title": "x"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_task(client):
    task_id = client.post("/tasks", json={"title": "A"}).json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert client.get("/tasks").json() == []


def test_delete_missing_task_returns_404(client):
    response = client.delete("/tasks/not-exists")

    assert response.status_code == 404
