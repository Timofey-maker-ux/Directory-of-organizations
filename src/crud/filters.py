from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.models.organization import Organization, organization_activities
from src.models.activity import Activity


async def list_by_building(
    db: AsyncSession, building_id: int, limit: int = 100, offset: int = 0
) -> List[Organization]:
    """Список организаций в конкретном здании."""
    res = await db.execute(
        select(Organization)
        .options(selectinload(Organization.activities))
        .where(Organization.building_id == building_id)
        .limit(limit)
        .offset(offset)
    )
    return list(res.scalars().all())


async def get_activity_ids_by_name(db: AsyncSession, name: str) -> list[int]:
    """
    Находит все активности с именем, похожим на name,
    и возвращает их id, включая дочерние.
    """
    res = await db.execute(
        select(Activity.path).where(Activity.name.ilike(f"%{name}%"))
    )
    paths = [r for r, in res.all()]
    if not paths:
        return []

    ids = []
    for path in paths:
        res2 = await db.execute(
            select(Activity.id).where(Activity.path.op("~")(f"^{path}(\\.|$)"))
        )
        ids.extend([r for r, in res2.all()])

    return list(set(ids))


async def get_organizations_by_activity_ids(
    db: AsyncSession,
    activity_ids: list[int],
    limit: int = 100,
    offset: int = 0,
):
    """
    Возвращает организации, связанные с указанными активностями.
    """
    if not activity_ids:
        return []

    q = (
        select(Organization)
        .join(organization_activities)
        .where(organization_activities.c.activity_id.in_(activity_ids))
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities),
        )
        .limit(limit)
        .offset(offset)
    )
    res = await db.execute(q)
    return res.scalars().all()


async def search_organizations_by_name(
    db: AsyncSession, query: str, limit: int = 100, offset: int = 0
) -> List[Organization | None]:
    """Поиск организаций по имени (ILIKE)."""
    if not query or len(query.strip()) < 2:
        return []
    query = query.strip()
    q = (
        select(Organization)
        .where(Organization.name.ilike(f"%{query}%"))
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities),
        )
        .limit(limit)
        .offset(offset)
    )
    res = await db.execute(q)
    return res.scalars().all()
