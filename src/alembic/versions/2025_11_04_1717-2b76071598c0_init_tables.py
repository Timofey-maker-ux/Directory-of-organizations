"""init tables

Revision ID: 2b76071598c0
Revises:
Create Date: 2025-11-04 17:17:35.304442

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision: str = "2b76071598c0"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "activities",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column(
            "parent_id",
            sa.Integer,
            sa.ForeignKey("activities.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.UniqueConstraint(
            "name", "parent_id", name="uq_activity_name_parent"
        ),
    )

    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("address", sa.String(500), nullable=False, unique=True),
        sa.Column("latitude", sa.Float, nullable=False),
        sa.Column("longitude", sa.Float, nullable=False),
        sa.Column(
            "geom", Geometry(geometry_type="POINT", srid=4326), nullable=False
        ),
        sa.CheckConstraint(
            "latitude >= -90 AND latitude <= 90", name="chk_latitude"
        ),
        sa.CheckConstraint(
            "longitude >= -180 AND longitude <= 180", name="chk_longitude"
        ),
    )

    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("phones", sa.ARRAY(sa.String), nullable=True),
        sa.Column(
            "building_id",
            sa.Integer,
            sa.ForeignKey("buildings.id", ondelete="RESTRICT"),
            nullable=False,
        ),
    )

    op.create_table(
        "organization_activities",
        sa.Column(
            "organization_id",
            sa.Integer,
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "activity_id",
            sa.Integer,
            sa.ForeignKey("activities.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("organization_activities")
    op.drop_table("organizations")
    op.drop_table("buildings")
    op.drop_table("activities")
