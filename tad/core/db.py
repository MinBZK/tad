import logging
from functools import lru_cache

from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool, StaticPool
from sqlmodel import Session, SQLModel, create_engine, delete, select

from tad.core.config import get_settings
from tad.models import Status, Task, User

logger = logging.getLogger(__name__)


@lru_cache(maxsize=8)
def get_engine() -> Engine:
    connect_args = (
        {"check_same_thread": False, "isolation_level": None} if get_settings().APP_DATABASE_SCHEME == "sqlite" else {}
    )
    poolclass = StaticPool if get_settings().APP_DATABASE_SCHEME == "sqlite" else QueuePool

    return create_engine(
        str(get_settings().SQLALCHEMY_DATABASE_URI),
        connect_args=connect_args,
        poolclass=poolclass,
        echo=get_settings().SQLALCHEMY_ECHO,
    )


def check_db():
    logger.info("Checking database connection")
    with Session(get_engine()) as session:
        session.exec(select(1))

    logger.info("Finisch Checking database connection")


def init_db():
    logger.info("Initializing database")

    if get_settings().AUTO_CREATE_SCHEMA:
        logger.info("Creating database schema")
        SQLModel.metadata.create_all(get_engine())

    with Session(get_engine()) as session:
        if get_settings().ENVIRONMENT == "demo":
            if get_settings().TRUNCATE_TABLES:
                truncate_tables(session)

            logger.info("Creating demo data")
            add_demo_users(session)
            add_demo_statuses(session)
            todo_status = session.exec(select(Status).where(Status.name == "todo")).first()
            if todo_status is not None:
                add_demo_tasks(session, todo_status)
            session.commit()
    logger.info("Finished initializing database")


def truncate_tables(session: Session) -> None:
    logger.info("Truncating tables")
    session.exec(delete(Task))  # type: ignore
    session.exec(delete(User))  # type: ignore
    session.exec(delete(Status))  # type: ignore


def add_demo_users(session: Session) -> None:
    user = session.exec(select(User).where(User.name == "Robbert")).first()
    if not user:
        user = User(name="Robbert", avatar=None)
        session.add(user)


def add_demo_tasks(session: Session, status: Status) -> None:
    for index in range(1, 4):
        task = session.exec(select(Task).where(Task.title == "Example task " + str(index))).first()
        if not task:
            task = Task(
                title="Example task " + str(index),
                description="Example description " + str(index),
                sort_order=index,
                status_id=status.id,
            )
            session.add(task)


def add_demo_statuses(session: Session) -> None:
    for index, status_name in enumerate(["todo", "review", "in_progress", "done"]):
        status = session.exec(select(Status).where(Status.name == status_name)).first()
        if not status:
            status = Status(name=status_name, sort_order=index + 1)
            session.add(status)
            session.commit()
