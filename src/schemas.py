from pydantic import BaseModel
from typing import List


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

    model_config = {"from_attributes": True}


class OrganizationRead(BaseModel):
    name: str
    phones: List[str] | None = None
    id: int
    building: BuildingRead
    activities: List[ActivityRead] | None = None

    model_config = {"from_attributes": True}
