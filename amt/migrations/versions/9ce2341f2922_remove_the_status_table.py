"""Remove the status table

Revision ID: 9ce2341f2922
Revises: 2c84c4ad5b68
Create Date: 2024-07-26 08:41:52.338277

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9ce2341f2922"
down_revision: str | None = "2c84c4ad5b68"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # fix unnamed foreign keys:
    #  https://alembic.sqlalchemy.org/en/latest/batch.html#dropping-unnamed-or-named-foreign-key-constraints
    naming_convention = {
        "fk":
            "%(table_name)s_%(column_0_name)s_fkey"
    }
    with op.batch_alter_table("task", naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint(
            "task_status_id_fkey", type_="foreignkey")

    op.drop_table("status")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("task", schema=None) as batch_op:
        batch_op.create_foreign_key("task_status_id_fkey", "status", ["status_id"], ["id"])

    op.create_table(
        "status",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column("sort_order", sa.FLOAT(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###
