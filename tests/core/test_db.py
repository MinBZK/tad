import logging
from unittest.mock import MagicMock

import pytest
from sqlmodel import Session, delete, select
from tad.core.config import Settings
from tad.core.db import check_db, init_db
from tad.models import Status, Task, User

logger = logging.getLogger(__name__)

expected_selects = [
    (select(User).where(User.name == "Robbert"),),
    (select(Status).where(Status.name == "todo"),),
    (select(Status).where(Status.name == "in_progress"),),
    (select(Status).where(Status.name == "review"),),
    (select(Status).where(Status.name == "done"),),
    (select(Status).where(Status.name == "done"),),
    (select(Task).where(Task.title == "Test task 1"),),
    (select(Task).where(Task.title == "Test task 2"),),
    (select(Task).where(Task.title == "Test task 3"),),
]


def test_check_database():
    org_exec = Session.exec
    Session.exec = MagicMock()
    check_db()

    assert Session.exec.call_args is not None
    assert str(select(1)) == str(Session.exec.call_args.args[0])
    Session.exec = org_exec


@pytest.mark.parametrize(
    "patch_settings",
    [{"ENVIRONMENT": "demo", "AUTO_CREATE_SCHEMA": True}],
    indirect=True,
)
def test_init_database_none(patch_settings: Settings):
    org_exec = Session.exec
    Session.exec = MagicMock()
    Session.exec.return_value.first.return_value = None

    init_db()

    for i, call_args in enumerate(Session.exec.call_args_list):
        assert str(expected_selects[i][0]) == str(call_args.args[0])

    Session.exec = org_exec


@pytest.mark.parametrize(
    "patch_settings",
    [{"ENVIRONMENT": "demo", "AUTO_CREATE_SCHEMA": True}],
    indirect=True,
)
def test_init_database_none_with_todo_status(patch_settings: Settings):
    org_exec = Session.exec
    Session.exec = MagicMock()
    todo_status = Status(id=1, name="todo", sort_order=1)
    Session.exec.return_value.first.side_effect = [None, None, None, None, None, todo_status, None, None, None]

    init_db()

    for i, call_args in enumerate(Session.exec.call_args_list):
        assert str(expected_selects[i][0]) == str(call_args.args[0])

    Session.exec = org_exec


@pytest.mark.parametrize(
    "patch_settings",
    [{"ENVIRONMENT": "demo", "AUTO_CREATE_SCHEMA": True}],
    indirect=True,
)
def test_init_database(patch_settings: Settings):
    org_exec = Session.exec
    Session.exec = MagicMock()

    init_db()

    for i, call_args in enumerate(Session.exec.call_args_list):
        assert str(expected_selects[i][0]) == str(call_args.args[0])

    Session.exec = org_exec


@pytest.mark.parametrize(
    "patch_settings",
    [{"ENVIRONMENT": "demo", "AUTO_CREATE_SCHEMA": True, "TRUNCATE_TABLES": True}],
    indirect=True,
)
def test_truncate_database(patch_settings: Settings):
    org_exec = Session.exec
    Session.exec = MagicMock()

    init_db()

    expected = [
        (delete(Task),),
        (delete(User),),
        (delete(Status),),
        *expected_selects,
    ]

    for i, call_args in enumerate(Session.exec.call_args_list):
        assert str(expected[i][0]) == str(call_args.args[0])

    Session.exec = org_exec
