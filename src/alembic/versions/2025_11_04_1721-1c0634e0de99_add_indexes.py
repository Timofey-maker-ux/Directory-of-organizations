"""add indexes

Revision ID: 1c0634e0de99
Revises: 2b76071598c0
Create Date: 2025-11-04 17:21:19.044155

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1c0634e0de99"
down_revision: Union[str, Sequence[str], None] = "2b76071598c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index("ix_activities_name", "activities", ["name"])

    op.create_index("ix_activities_parent_id", "activities", ["parent_id"])

    op.create_index("ix_organizations_name", "organizations", ["name"])

    op.create_index(
        "ix_org_activities_activity_id",
        "organization_activities",
        ["activity_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_activities_name", table_name="activities")
    op.drop_index("ix_activities_parent_id", table_name="activities")
    op.drop_index("ix_organizations_name", table_name="organizations")
    op.drop_index(
        "ix_org_activities_activity_id", table_name="organization_activities"
    )
    op.execute("DROP INDEX IF EXISTS idx_buildings_geom")
