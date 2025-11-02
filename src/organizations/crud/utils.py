import re
from typing import List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.activity.models import Activity


async def _get_activity_and_descendant_ids(
    db: AsyncSession, activity_id: int
) -> List[int]:
    """
    Возвращает список id активности: сама + все её потомки (по materialized path).
    Использует regex для точного совпадения пути (например, '1.2' не захватывает '1.23').
    """
    res = await db.execute(
        select(Activity.path).where(Activity.id == activity_id)
    )
    path = res.scalar_one_or_none()
    if not path:
        return []

    regex_pattern = f"^({re.escape(path)})(\\.|$)"
    q = select(Activity.id).where(Activity.path.op("~")(regex_pattern))

    res2 = await db.execute(q)
    ids = [r for r, in res2.all()]
    return ids
