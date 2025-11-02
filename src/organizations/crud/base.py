from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from src.organizations.models import Organization
from src.buildings.models import Building
from src.activity.models import Activity


async def create_organization(
    db: AsyncSession,
    name: str,
    building_id: int,
    phones: Optional[List[str]] = None,
    activity_ids: Optional[List[int]] = None,
) -> Organization:
    """
    Создать организацию:
    - Проверяет существование building
    - Проверяет существование всех activity_ids
    - Создаёт организацию в транзакции
    """
    building = await db.get(Building, building_id)
    if not building:
        raise ValueError(f"Building with id={building_id} not found")

    activities = []
    if activity_ids:
        res = await db.execute(
            select(Activity).where(Activity.id.in_(activity_ids))
        )
        activities = res.scalars().all()
        if len(activities) != len(activity_ids):
            raise ValueError("One or more activities not found")

    org = Organization(name=name, phones=phones or [], building_id=building_id)
    if activities:
        org.activities = activities

    try:
        db.add(org)
        await db.commit()
        await db.refresh(org)
    except IntegrityError as e:
        await db.rollback()
        raise ValueError(f"Integrity error creating organization: {e}") from e
    return org


async def get_organization(
    db: AsyncSession, org_id: int
) -> Optional[Organization]:
    """Возвращает организацию с её building и activities (или None)."""
    res = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities),
        )
        .where(Organization.id == org_id)
    )
    return res.scalars().first()


async def list_organizations(
    db: AsyncSession, limit: int = 100, offset: int = 0
) -> List[Organization]:
    """Простой список организаций с pagination."""
    res = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities),
        )
        .limit(limit)
        .offset(offset)
    )
    return res.scalars().all()
