from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.organizations.models import Organization
from src.buildings.models import Building
from src.activity.models import Activity


async def update_organization(
    db: AsyncSession,
    org_id: int,
    *,
    name: Optional[str] = None,
    phones: Optional[List[str]] = None,
    building_id: Optional[int] = None,
    activity_ids: Optional[List[int]] = None,
) -> Optional[Organization]:
    """
    Обновление организации. Проверяет existence FK, обновляет M2M.
    Возвращает обновлённый объект или None если не найден.
    """
    org = await db.get(Organization, org_id)
    if not org:
        return None

    if name is not None:
        org.name = name
    if phones is not None:
        org.phones = phones
    if building_id is not None:
        building = await db.get(Building, building_id)
        if not building:
            raise ValueError(f"Building with id={building_id} not found")
        org.building_id = building_id
    if activity_ids is not None:
        if activity_ids:
            res = await db.execute(
                select(Activity).where(Activity.id.in_(activity_ids))
            )
            activities = res.scalars().all()
            if len(activities) != len(activity_ids):
                raise ValueError("One or more activities not found")
            org.activities = activities
        else:
            org.activities = []

    try:
        db.add(org)
        await db.flush()
        await db.commit()
        await db.refresh(org)
    except IntegrityError as e:
        await db.rollback()
        raise ValueError(f"Integrity error updating organization: {e}") from e
    return org


async def delete_organization(db: AsyncSession, org_id: int) -> bool:
    org = await db.get(Organization, org_id)
    if not org:
        return False
    await db.delete(org)
    await db.flush()
    await db.commit()
    return True
