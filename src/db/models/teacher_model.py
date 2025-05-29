from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDOrmModel

# Forward declaration for type hinting Subject
if TYPE_CHECKING:
    from .subject_model import Subject


class Teacher(IDOrmModel):
    __tablename__ = "teachers"

    fullname: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    subjects: Mapped[List["Subject"]] = relationship(
        back_populates="teacher", lazy="selectin"
    )

    def __repr__(self):
        return f"<Teacher(id={self.id}, fullname='{self.fullname}')>"
