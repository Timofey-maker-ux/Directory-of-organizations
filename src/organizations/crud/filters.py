from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.organizations.models import Organization, organization_activities
from src.activity.models import Activity
from src.organizations.crud.utils import _get_activity_and_descendant_ids


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
    return res.scalars().all()


async def list_by_activity(
    db: AsyncSession,
    activity_id: int,
    include_descendants: bool = False,
    limit: int = 100,
    offset: int = 0,
) -> List[Organization]:
    """
    Список организаций, относящихся к виду деятельности.
    Если include_descendants=True, включаем все дочерние виды (по path).
    """
    if include_descendants:
        ids = await _get_activity_and_descendant_ids(db, activity_id)
        if not ids:
            return []
        q = (
            select(Organization)
            .join(
                organization_activities,
                Organization.id == organization_activities.c.organization_id,
            )
            .where(organization_activities.c.activity_id.in_(ids))
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
            )
            .limit(limit)
            .offset(offset)
        )
    else:
        q = (
            select(Organization)
            .join(
                organization_activities,
                Organization.id == organization_activities.c.organization_id,
            )
            .where(organization_activities.c.activity_id == activity_id)
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
