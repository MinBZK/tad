from collections.abc import Generator
from unittest.mock import MagicMock, Mock

import pytest
from fastapi.testclient import TestClient
from tad.schema.project import ProjectNew
from tad.schema.system_card import SystemCard
from tad.services.instruments import InstrumentsService
from tad.services.storage import FileSystemStorageService

from tests.constants import default_instrument


@pytest.fixture()
def init_instruments() -> Generator[None, None, None]:  # noqa: PT004
    origin = InstrumentsService.fetch_instruments
    InstrumentsService.fetch_instruments = Mock(
        return_value=[default_instrument(urn="urn1", name="name1"), default_instrument(urn="urn2", name="name2")]
    )
    yield
    InstrumentsService.fetch_instruments = origin


def test_get_new_projects(client: TestClient, init_instruments: Generator[None, None, None]) -> None:
    # when
    response = client.get("/projects/new")

    # then
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert (
        b'<input type="checkbox" id="urn1" name="instruments" value="urn1" /><label for="urn1">name1</label>'
        in response.content
    )
    assert (
        b'<input type="checkbox" id="urn2" name="instruments" value="urn2" /><label for="urn2">name2</label>'
        in response.content
    )


def test_post_new_projects_bad_request(client: TestClient) -> None:
    # when
    response = client.post("/projects/new", json={})

    # then
    assert response.status_code == 400
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert b"name: Field required" in response.content


def test_post_new_projects(client: TestClient) -> None:
    new_project = ProjectNew(name="default project")

    # when
    response = client.post("/projects/new", json=new_project.model_dump())

    # then
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.headers["HX-Redirect"] == "/project/1"


def test_post_new_projects_write_system_card(client: TestClient) -> None:
    # Given
    origin = FileSystemStorageService.write
    FileSystemStorageService.write = MagicMock()
    project_new = ProjectNew(name="name1")
    system_card = SystemCard(name=project_new.name, selected_instruments=[])

    # when
    client.post("/projects/new", json=project_new.model_dump())

    # then
    FileSystemStorageService.write.assert_called_with(system_card.model_dump())
    FileSystemStorageService.write = origin
