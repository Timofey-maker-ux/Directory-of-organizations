from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
    Security,
)
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.database import db_helper
from src.crud import base, filters, geo
from src.schemas import OrganizationRead
from src.core.config import settings


api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_key


router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    dependencies=[Depends(get_api_key)],
)


@router.get(
    "/by-building/{building_id}",
    summary="Получить организации по зданию",
    description="Возвращает все организации, находящиеся в указанном здании.",
    response_model=List[OrganizationRead],
)
async def get_by_building(
    building_id: int, db: AsyncSession = Depends(db_helper.get_session)
):
    orgs = await filters.list_by_building(db, building_id)
    if not orgs:
        raise HTTPException(status_code=404, detail="Organizations not found")
    return orgs


@router.get(
    "/search/by-activity",
    summary="Поиск организаций по виду деятельности",
    description="Возвращает организации, связанные с указанным видом деятельности или его подвидом.",
    response_model=list[OrganizationRead],
)
async def search_by_activity_name(
    activity_name: str, db: AsyncSession = Depends(db_helper.get_session)
):

    ids = await filters.get_activity_ids_by_name(db, activity_name)
    if not ids:
        raise HTTPException(status_code=404, detail="Activities not found")
    orgs = await filters.get_organizations_by_activity_ids(db, ids)
    if not orgs:
        raise HTTPException(status_code=404, detail="Organizations not found")
    return orgs


@router.get(
    "/geo/radius",
    summary="Поиск организаций в радиусе",
    description="Возвращает организации, находящиеся в радиусе от указанной точки (lat/lon) в метрах.",
    response_model=List[OrganizationRead],
)
async def get_by_radius(
    lat: float = Query(...),
    lon: float = Query(...),
    radius_meters: float = Query(...),
    db: AsyncSession = Depends(db_helper.get_session),
):
    orgs = await geo.organizations_within_radius(db, lat, lon, radius_meters)
    if not orgs:
        raise HTTPException(status_code=404, detail="Organizations not found")
    return orgs


@router.get(
    "/geo/bbox",
    summary="Поиск организаций по bounding box",
    description="Возвращает организации, находящиеся внутри заданного прямоугольника.",
    response_model=List[OrganizationRead],
)
async def get_by_bbox(
    lat1: float = Query(...),
    lon1: float = Query(...),
    lat2: float = Query(...),
    lon2: float = Query(...),
    db: AsyncSession = Depends(db_helper.get_session),
):
    orgs = await geo.organizations_in_bbox(db, lat1, lon1, lat2, lon2)
    if not orgs:
        raise HTTPException(status_code=404, detail="Organizations not found")
    return orgs


@router.get(
    "/{org_id}",
    summary="Получить организацию по ID",
    description="Возвращает организацию с её building и верхним уровнем активностей.",
    response_model=OrganizationRead,
)
async def get_org(
    org_id: int, db: AsyncSession = Depends(db_helper.get_session)
):
    org = await base.get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.get(
    "/search/by-name",
    summary="Поиск организаций по названию",
    description="Возвращает список организаций, чьи названия соответствуют поисковому запросу.",
    response_model=List[OrganizationRead],
)
async def search_by_name(
    query: str = Query(..., min_length=2),
    db: AsyncSession = Depends(db_helper.get_session),
):
    orgs = await filters.search_organizations_by_name(db, query)
    if not orgs:
        raise HTTPException(status_code=404, detail="Organizations not found")
    return orgs
