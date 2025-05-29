from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

from .base import IDOrmModel

# Forward declarations for type hinting
if TYPE_CHECKING:
    from .student_model import Student
    from .subject_model import Subject


class Grade(IDOrmModel):
    __tablename__ = "grades"

    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    date_received: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False  # pylint: disable=not-callable
    )

    student: Mapped["Student"] = relationship(back_populates="grades", lazy="selectin")
    subject: Mapped["Subject"] = relationship(back_populates="grades", lazy="selectin")

    def __repr__(self):
        return f"<Grade(id={self.id}, student_id={self.student_id}, subject_id={self.subject_id}, grade={self.grade}, date_received='{self.date_received.isoformat() if self.date_received else None}')>"
