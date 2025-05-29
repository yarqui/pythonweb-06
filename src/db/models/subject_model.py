from typing import List, TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDOrmModel

# Forward declarations for type hinting
if TYPE_CHECKING:
    from .teacher_model import Teacher
    from .student_model import Student
    from .grade_model import Grade


class Subject(IDOrmModel):
    __tablename__ = "subjects"

    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    teacher_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True
    )

    teacher: Mapped["Teacher"] = relationship(
        back_populates="subjects", lazy="selectin"
    )

    grades: Mapped[List["Grade"]] = relationship(
        back_populates="subject", lazy="selectin", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Subject(id={self.id}, name='{self.name}', teacher_id={self.teacher_id})>"
        )
