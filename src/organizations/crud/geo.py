from typing import List
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.organizations.models import Organization
from src.buildings.models import Building


async def organizations_within_radius(
    db: AsyncSession,
    lat: float,
    lon: float,
    radius_meters: float,
    limit: int = 100,
    offset: int = 0,
) -> List[Organization]:
    """
    Возвращает организации, чьи buildings находятся в радиусе radius_meters от точки (lat, lon).
    Использует PostGIS ST_DWithin с приведением к geography (чтобы расстояние было в метрах).
    """
    point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
    stmt = (
        select(Organization)
        .join(Building, Organization.building_id == Building.id)
        .where(
            func.ST_DWithin(
                func.cast(Building.geom, text("geography")),
                func.cast(point, text("geography")),
                radius_meters,
            )
        )
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities),
        )
        .limit(limit)
        .offset(offset)
    )
    res = await db.execute(stmt)
    return res.scalars().all()


async def organizations_in_bbox(
    db: AsyncSession,
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    limit: int = 100,
    offset: int = 0,
) -> List[Organization]:
    """
    Возвращает организации, чьи здания находятся внутри bbox (lat1, lon1) - (lat2, lon2).
    Работает через простую проверку latitude/longitude, потому что у нас есть эти колонки.
    """
    min_lat, max_lat = sorted([lat1, lat2])
    min_lon, max_lon = sorted([lon1, lon2])
    stmt = (
        select(Organization)
        .join(Building, Organization.building_id == Building.id)
        .where(
            (Building.latitude >= min_lat)
            & (Building.latitude <= max_lat)
            & (Building.longitude >= min_lon)
            & (Building.longitude <= max_lon)
        )
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities),
        )
        .limit(limit)
        .offset(offset)
    )
    res = await db.execute(stmt)
    return res.scalars().all()
