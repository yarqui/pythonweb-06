from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDOrmModel

# Forward declaration for type hinting Student
if TYPE_CHECKING:
    from .student_model import Student


class Group(IDOrmModel):
    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )

    students: Mapped[List["Student"]] = relationship(
        back_populates="group", lazy="selectin"
    )

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"
