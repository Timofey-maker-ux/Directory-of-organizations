from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.organization import Organization, organization_activities
from src.models.activity import Activity


async def list_by_building(
    db: AsyncSession, building_id: int
) -> list[Organization]:
    """Возвращает список организаций, расположенных в заданном здании."""
    res = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities),
        )
        .where(Organization.building_id == building_id)
    )
    return res.scalars().all()


async def get_activity_ids_by_name(db: AsyncSession, name: str) -> list[int]:
    """
    Находит все верхние активности, имя которых содержит name.
    Возвращает их id.
    """
    res = await db.execute(
        select(Activity.id).where(Activity.name.ilike(f"%{name}%"))
    )
    return [r[0] for r in res.all()]


async def get_organizations_by_activity_ids(
    db: AsyncSession, activity_ids: list[int]
) -> list[Organization]:
    """Возвращает организации, связанные с заданным списком идентификаторов активностей."""
    if not activity_ids:
        return []

    res = await db.execute(
        select(Organization)
        .join(organization_activities)
        .where(organization_activities.c.activity_id.in_(activity_ids))
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities)
            .selectinload(Activity.children)
            .selectinload(Activity.children),
        )
    )
    return res.scalars().all()


async def search_organizations_by_name(
    db: AsyncSession, query: str
) -> list[Organization]:
    """Выполняет поиск организаций по названию (частичное совпадение, без учёта регистра)."""
    res = await db.execute(
        select(Organization)
        .where(Organization.name.ilike(f"%{query}%"))
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities),
        )
    )
    return res.scalars().all()
