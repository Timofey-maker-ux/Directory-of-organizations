"""test data

Revision ID: 2cc807807c7b
Revises: 1c0634e0de99
Create Date: 2025-11-04 17:24:49.978718

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2cc807807c7b"
down_revision: Union[str, Sequence[str], None] = "1c0634e0de99"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()

    # ----------------- Активности -----------------
    connection.execute(
        sa.text(
            """
        INSERT INTO activities (id, name, parent_id) VALUES
        (1, 'Еда', NULL),
        (2, 'Мясная продукция', 1),
        (3, 'Колбасы', 2),
        (4, 'Молочная продукция', 1),
        (5, 'Сыры', 4),
        (6, 'Развлечения', NULL),
        (7, 'Кино', 6),
        (8, 'Бары', 6);
        """
        )
    )

    # ----------------- Здания -----------------
    connection.execute(
        sa.text(
            """
        INSERT INTO buildings (id, address, latitude, longitude, geom) VALUES
        (1, 'ул. Ленина, 1', 55.7558, 37.6176, ST_GeomFromText('POINT(37.6176 55.7558)', 4326)),
        (2, 'ул. Пушкина, 10', 55.7517, 37.6178, ST_GeomFromText('POINT(37.6178 55.7517)', 4326)),
        (3, 'Невский проспект, 5', 59.9343, 30.3351, ST_GeomFromText('POINT(30.3351 59.9343)', 4326));
        """
        )
    )

    # ----------------- Организации -----------------
    connection.execute(
        sa.text(
            """
        INSERT INTO organizations (id, name, phones, building_id) VALUES
        (1, 'Мясной дом', ARRAY['+7-999-111-22-33'], 1),
        (2, 'Сырная лавка', ARRAY['+7-999-111-44-55'], 1),
        (3, 'Бар "Кружка"', ARRAY['+7-999-222-11-22'], 2),
        (4, 'Кинотеатр "Луч"', ARRAY['+7-999-555-77-88'], 3);
        """
        )
    )

    # ----------------- Связи организация-активности -----------------
    connection.execute(
        sa.text(
            """
        INSERT INTO organization_activities (organization_id, activity_id) VALUES
        (1, 1),  -- Мясной дом → Еда (верхний уровень)
        (1, 2),  -- Мясной дом → Мясная продукция
        (1, 3),  -- Мясной дом → Колбасы
        (2, 1),  -- Сырная лавка → Еда
        (2, 4),  -- Сырная лавка → Молочная продукция
        (2, 5),  -- Сырная лавка → Сыры
        (3, 6),  -- Бар "Кружка" → Развлечения
        (3, 8),  -- Бар "Кружка" → Бары
        (4, 6),  -- Кинотеатр "Луч" → Развлечения
        (4, 7);  -- Кинотеатр "Луч" → Кино
        """
        )
    )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(sa.text("DELETE FROM organization_activities;"))
    connection.execute(sa.text("DELETE FROM organizations;"))
    connection.execute(sa.text("DELETE FROM buildings;"))
    connection.execute(sa.text("DELETE FROM activities;"))
