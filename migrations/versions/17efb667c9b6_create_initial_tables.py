"""create_initial_tables

Revision ID: 17efb667c9b6
Revises:
Create Date: 2025-05-29 02:53:23.057805

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "17efb667c9b6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "groups",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_groups_id"), "groups", ["id"], unique=False)
    op.create_index(op.f("ix_groups_name"), "groups", ["name"], unique=True)

    op.create_table(
        "teachers",
        sa.Column("fullname", sa.String(length=100), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_teachers_fullname"), "teachers", ["fullname"], unique=False
    )
    op.create_index(op.f("ix_teachers_id"), "teachers", ["id"], unique=False)
    op.create_table(
        "students",
        sa.Column("fullname", sa.String(length=100), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["group_id"], ["groups.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_students_fullname"), "students", ["fullname"], unique=False
    )
    op.create_index(op.f("ix_students_id"), "students", ["id"], unique=False)
    op.create_table(
        "subjects",
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("teacher_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["teacher_id"], ["teachers.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_subjects_id"), "subjects", ["id"], unique=False)
    op.create_index(op.f("ix_subjects_name"), "subjects", ["name"], unique=False)
    op.create_table(
        "grades",
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("grade", sa.Integer(), nullable=False),
        sa.Column("date_received", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["subject_id"], ["subjects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_grades_id"), "grades", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_grades_id"), table_name="grades")
    op.drop_table("grades")
    op.drop_index(op.f("ix_subjects_name"), table_name="subjects")
    op.drop_index(op.f("ix_subjects_id"), table_name="subjects")
    op.drop_table("subjects")
    op.drop_index(op.f("ix_students_id"), table_name="students")
    op.drop_index(op.f("ix_students_fullname"), table_name="students")
    op.drop_table("students")
    op.drop_index(op.f("ix_teachers_id"), table_name="teachers")
    op.drop_index(op.f("ix_teachers_fullname"), table_name="teachers")
    op.drop_table("teachers")
    op.drop_index(op.f("ix_groups_name"), table_name="groups")
    op.drop_index(op.f("ix_groups_id"), table_name="groups")
    op.drop_table("groups")
    # ### end Alembic commands ###
