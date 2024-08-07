from collections.abc import Generator

from fastapi.testclient import TestClient

from tests.constants import default_task
from tests.database_test_utils import DatabaseTestUtils


def test_post_task_move(client: TestClient, db: DatabaseTestUtils, mock_csrf: Generator[None, None, None]) -> None:
    db.given([default_task(), default_task(), default_task()])
    client.cookies["fastapi-csrf-token"] = "1"

    response = client.patch(
        "/tasks/",
        json={"taskId": "1", "statusId": "1", "previousSiblingId": "2", "nextSiblingId": "-1"},
        headers={"X-CSRF-Token": "1"},
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert b'id="card-content-1"' in response.content


def test_task_move_error(client: TestClient, db: DatabaseTestUtils, mock_csrf: Generator[None, None, None]) -> None:
    client.cookies["fastapi-csrf-token"] = "1"
    response = client.patch(
        "/tasks/",
        json={"taskId": "1", "statusId": "1", "previousSiblingId": "2", "nextSiblingId": "-1"},
        headers={"X-CSRF-Token": "1"},
    )
    assert response.status_code == 500
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert b"RepositoryError: Repository error" in response.content
