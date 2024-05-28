import os
from collections.abc import Generator
from multiprocessing import Process
from time import sleep

import pytest
import uvicorn
from fastapi.testclient import TestClient
from playwright.sync_api import sync_playwright
from sqlmodel import Session
from tad.core.config import settings
from tad.core.db import get_engine
from tad.main import app


class TestSettings:
    HTTP_SERVER_SCHEME: str = "http://"
    HTTP_SERVER_HOST: str = "127.0.0.1"
    HTTP_SERVER_PORT: int = 8000


def run_server():
    uvicorn.run(app, host=TestSettings.HTTP_SERVER_HOST, port=TestSettings.HTTP_SERVER_PORT)


def wait_for_server_ready(url: str, timeout: int = 30):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for _ in range(timeout):
            try:
                page.goto(url)
                browser.close()
                return True  # noqa
            # todo (robbert) find out what exception to catch
            except Exception:
                sleep(1)
        browser.close()
        raise Exception(f"Server at {url} did not become ready within {timeout} seconds")  # noqa: TRY003 TRY002


@pytest.fixture(scope="module")
def start_server():
    # todo (robbert) use a better way to get the test database in the app configuration
    os.environ["APP_DATABASE_FILE"] = "database.sqlite3.test"
    process = Process(target=run_server)
    process.start()
    server_address = (
        TestSettings.HTTP_SERVER_SCHEME + TestSettings.HTTP_SERVER_HOST + ":" + str(TestSettings.HTTP_SERVER_PORT)
    )
    wait_for_server_ready(server_address)
    yield server_address
    process.terminate()
    del os.environ["APP_DATABASE_FILE"]


@pytest.fixture(scope="session")
def get_session() -> Session:
    with Session(get_engine()) as session:
        yield session


def pytest_configure():
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    # todo (robbert) creating an in memory database does not work right, tables seem to get lost?
    settings.APP_DATABASE_FILE = "database.sqlite3.test"  # set to none so we'll use an in memory database


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app, raise_server_exceptions=True) as c:
        c.timeout = 5
        yield c
