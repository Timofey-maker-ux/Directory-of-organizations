from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    CheckConstraint,
    event,
)
from sqlalchemy.orm import relationship
from src.core.db.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    parent_id = Column(
        Integer,
        ForeignKey("activities.id", ondelete="SET NULL"),
        nullable=True,
    )
    depth = Column(Integer, nullable=False, default=1)
    path = Column(
        String(200), nullable=False, index=True
    )

    parent = relationship("Activity", remote_side=[id], backref="children")

    organizations = relationship(
        "Organization",
        secondary="organization_activities",
        back_populates="activities",
    )

    __table_args__ = (
        CheckConstraint(
            "depth >= 1 AND depth <= 3", name="chk_activity_depth"
        ),
    )


@event.listens_for(Activity, "before_insert")
@event.listens_for(Activity, "before_update")
def set_depth_and_path(mapper, connection, target):
    if target.parent_id:
        parent = connection.execute(
            Activity.__table__.select().where(Activity.id == target.parent_id)
        ).first()
        if parent:
            target.depth = parent.depth + 1
            if target.depth > 3:
                raise ValueError("Activity depth cannot exceed 3")
            target.path = f"{parent.path}.{target.id or 'new'}"
    else:
        target.depth = 1
        target.path = str(target.id or "new")
