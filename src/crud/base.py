from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.models.activity import Activity
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
            selectinload(Organization.activities)
            .selectinload(Activity.children)
            .selectinload(Activity.children)
            .selectinload(Activity.children),
        )
        .where(Organization.id == org_id)
    )
    return res.scalars().first()
