from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from amt.models.base import Base


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    sort_order: Mapped[float]
    status_id: Mapped[int | None] = mapped_column(default=None)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"))
    # TODO: (Christopher) SQLModel does not allow to give the below restraint an name
    #       which is needed for alembic. This results in changing the migration file
    #       manually to give the restrain a name.
    project_id: Mapped[int | None] = mapped_column(ForeignKey("project.id"))
    # todo(robbert) Tasks probably are grouped (and sub-grouped), so we probably need a reference to a group_id
