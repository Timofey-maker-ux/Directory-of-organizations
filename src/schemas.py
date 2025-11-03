from pydantic import BaseModel
from typing import List, Optional


class BuildingRead(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    model_config = {"from_attributes": True}


class ActivityRead(BaseModel):
    id: int
    name: str
    parent_id: int | None = None
    depth: int | None = 1
    path: str
    children: List["ActivityRead"] = []

    model_config = {"from_attributes": True}


class OrganizationRead(BaseModel):
    name: str
    phones: Optional[List[str]] = []
    id: int
    building: BuildingRead
    activities: List[ActivityRead] = []

    model_config = {"from_attributes": True}
