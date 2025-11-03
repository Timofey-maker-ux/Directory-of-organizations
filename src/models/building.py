from sqlalchemy import Column, Integer, String, Float, CheckConstraint, event
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry, WKTElement
from src.core.db.database import Base


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True)
    address = Column(String(500), nullable=False, unique=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    geom = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)

    organizations = relationship(
        "Organization",
        back_populates="building",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        CheckConstraint(
            "latitude >= -90 AND latitude <= 90", name="chk_latitude"
        ),
        CheckConstraint(
            "longitude >= -180 AND longitude <= 180", name="chk_longitude"
        ),
    )


@event.listens_for(Building, "before_insert")
@event.listens_for(Building, "before_update")
def update_geom(mapper, connection, target):
    target.geom = WKTElement(
        f"POINT({target.longitude} {target.latitude})", srid=4326
    )
