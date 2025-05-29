from typing import List, TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDOrmModel

# Forward declarations for type hinting
if TYPE_CHECKING:
    from .group_model import Group
    from .grade_model import Grade


class Student(IDOrmModel):
    __tablename__ = "students"

    fullname: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("groups.id", ondelete="SET NULL"), nullable=True
    )

    group: Mapped["Group"] = relationship(back_populates="students", lazy="selectin")

    grades: Mapped[List["Grade"]] = relationship(
        back_populates="student", lazy="selectin", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Student(id={self.id}, fullname='{self.fullname}', group_id={self.group_id})>"
