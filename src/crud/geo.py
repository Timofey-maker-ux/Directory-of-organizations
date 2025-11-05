from geoalchemy2.functions import (
    ST_SetSRID,
    ST_Point,
    ST_DWithin,
    ST_MakeEnvelope,
    ST_Contains,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.activity import Activity
from src.models.organization import Organization
from src.models.building import Building


async def organizations_within_radius(
    db: AsyncSession, lat: float, lon: float, radius_meters: float
) -> list[Organization]:
    """
    Возвращает все организации, которые находятся в радиусе radius_meters от точки (lat, lon)
    """
    point = ST_SetSRID(ST_Point(lon, lat), 4326)
    stmt = (
        select(Organization)
        .join(Organization.building)
        .where(ST_DWithin(Building.geom, point, radius_meters))
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities),
        )
    )
    res = await db.execute(stmt)
    return res.scalars().all()


async def organizations_in_bbox(
    db: AsyncSession, lat1: float, lon1: float, lat2: float, lon2: float
) -> list[Organization]:
    """
    Возвращает все организации, которые находятся в прямоугольной области (bbox)
    """
    bbox = ST_MakeEnvelope(lon1, lat1, lon2, lat2, 4326)
    stmt = (
        select(Organization)
        .join(Organization.building)
        .where(ST_Contains(bbox, Building.geom))
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities),
        )
    )
    res = await db.execute(stmt)
    return res.scalars().all()
