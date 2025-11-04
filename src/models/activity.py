from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
    Table,
    select,
    text,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload
from src.core.db.database import Base


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        UniqueConstraint("name", "parent_id", name="uq_activity_name_parent"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    parent_id = Column(
        Integer,
        ForeignKey("activities.id", ondelete="CASCADE"),
        nullable=True,
    )
    parent = relationship(
        "Activity",
        back_populates="children",
        remote_side=[id],
    )
    children = relationship(
        "Activity",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    organizations = relationship(
        "Organization",
        secondary="organization_activities",
        back_populates="activities",
    )

    def __repr__(self):
        return f"Activity(id={self.id!r}, name={self.name!r}, parent_id={self.parent_id!r})"
