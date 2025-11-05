from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.models.organization import Organization


async def get_organization(
    db: AsyncSession, org_id: int
) -> Organization | None:
    """
    Возвращает организацию с её building и активностями (только верхний уровень),
    при этом подгружаются все дочерние активности через children.
    """
    res = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities),
        )
        .where(Organization.id == org_id)
    )
    org = res.scalars().first()
    return org
