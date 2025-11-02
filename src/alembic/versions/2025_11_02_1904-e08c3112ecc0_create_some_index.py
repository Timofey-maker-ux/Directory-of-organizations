"""create some index

Revision ID: e08c3112ecc0
Revises: 261012e54089
Create Date: 2025-11-02 19:04:46.960279

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e08c3112ecc0"
down_revision: Union[str, Sequence[str], None] = "261012e54089"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_activities_path_unique", "activities", ["path"], unique=True
    )

    op.create_index(
        "ix_org_activities_activity_id",
        "organization_activities",
        ["activity_id"],
    )

    op.create_index(
        "ix_organizations_name_pattern",
        "organizations",
        ["name"],
        postgresql_ops={"name": "text_pattern_ops"},
    )

    op.execute(
        "CREATE INDEX idx_buildings_geog ON buildings USING GIST ((geom::geography))"
    )


def downgrade() -> None:
    op.drop_index("ix_activities_path_unique", table_name="activities")
    op.drop_index(
        "ix_org_activities_activity_id", table_name="organization_activities"
    )
    op.drop_index("ix_organizations_name_pattern", table_name="organizations")
    op.execute("DROP INDEX IF EXISTS idx_buildings_geog")
