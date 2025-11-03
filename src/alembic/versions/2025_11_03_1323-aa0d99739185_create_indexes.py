"""create indexes

Revision ID: aa0d99739185
Revises: d7532674dc68
Create Date: 2025-11-03 13:23:52.839449

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = "aa0d99739185"
down_revision: Union[str, Sequence[str], None] = "d7532674dc68"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- activities ---
    op.create_index(
        "ix_activities_name",
        "activities",
        ["name"],
    )
    op.create_index(
        "ix_activities_path",
        "activities",
        ["path"],
    )

    # --- organizations ---
    op.create_index(
        "ix_organizations_name_pattern",
        "organizations",
        ["name"],
        postgresql_ops={"name": "text_pattern_ops"},
    )
    op.create_index(
        "ix_organizations_building_id",
        "organizations",
        ["building_id"],
    )

    # --- organization_activities ---
    op.create_index(
        "ix_org_activities_activity_id",
        "organization_activities",
        ["activity_id"],
    )

    # --- buildings ---
    op.create_index(
        "idx_buildings_geog",
        "buildings",
        [text("(geom::geography)")],
        postgresql_using="gist",
    )
    op.create_index(
        "ix_buildings_lat_lon",
        "buildings",
        ["latitude", "longitude"],
    )

    # --- optional: ускорить поиск по имени (ILIKE '%еда%') ---
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    op.create_index(
        "ix_organizations_name_trgm",
        "organizations",
        ["name"],
        postgresql_using="gin",
        postgresql_ops={"name": "gin_trgm_ops"},
    )


def downgrade() -> None:
    # --- optional ---
    op.drop_index("ix_organizations_name_trgm", table_name="organizations")

    # --- buildings ---
    op.drop_index("ix_buildings_lat_lon", table_name="buildings")
    op.drop_index("idx_buildings_geog", table_name="buildings")

    # --- organization_activities ---
    op.drop_index(
        "ix_org_activities_activity_id",
        table_name="organization_activities",
    )

    # --- organizations ---
    op.drop_index("ix_organizations_building_id", table_name="organizations")
    op.drop_index("ix_organizations_name_pattern", table_name="organizations")

    # --- activities ---
    op.drop_index("ix_activities_path", table_name="activities")
    op.drop_index("ix_activities_name", table_name="activities")
