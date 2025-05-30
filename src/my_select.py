import asyncio
from sqlalchemy import func, select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Student, Grade, Subject, Teacher, Group
from src.db.session import AsyncSessionFactory, engine


# Query Functions
async def select_1_top_students(session: AsyncSession, limit: int = 5):
    """Find the 5 students with the highest GPA in all subjects."""
    print(f"\n--- Query 1: Top {limit} students by average grade ---")
    stmt = (
        select(
            Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(limit)
    )
    result = await session.execute(stmt)
    students = result.all()
    for student in students:
        print(f"{student.fullname}: Average Grade = {student.avg_grade}")
    return students


async def select_2_student_top_grade_for_subject(
    session: AsyncSession, subject_name: str
):
    """Find the student with the highest GPA in a specific subject."""
    print(
        f"\n--- Query 2: Student with highest average grade for subject '{subject_name}' ---"
    )
    stmt = (
        select(
            Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(1)
    )
    result = await session.execute(stmt)
    student = result.first()
    if student:
        print(
            f"Student: {student.fullname}, Highest Avg Grade in {subject_name}: {student.avg_grade}"
        )
    else:
        print(f"No student found or no grades for subject: {subject_name}")
    return student


async def select_3_avg_grade_in_group_for_subject(
    session: AsyncSession, subject_name: str, group_name: str
):
    """Find the average score in groups for a specific subject."""
    print(
        f"\n--- Query 3: Average grade in group '{group_name}' for subject '{subject_name}' ---"
    )
    stmt = (
        select(func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(and_(Subject.name == subject_name, Group.name == group_name))
    )
    result = await session.execute(stmt)
    avg_grade = result.scalar_one_or_none()
    if avg_grade is not None:
        print(
            f"Average grade for group '{group_name}' in '{subject_name}': {avg_grade}"
        )
    else:
        print(f"No grades found for group '{group_name}' in subject '{subject_name}'.")
    return avg_grade


async def select_4_overall_avg_grade(session: AsyncSession):
    """Find the average score on the cohort (across the entire grade table)."""
    print(f"\n--- Query 4: Overall average grade across all grades ---")
    stmt = select(
        func.round(func.avg(Grade.grade), 2).label("overall_avg_grade")
    ).select_from(Grade)
    result = await session.execute(stmt)
    overall_avg = result.scalar_one_or_none()
    if overall_avg is not None:
        print(f"Overall average grade: {overall_avg}")
    else:
        print("No grades found in the database.")
    return overall_avg


async def select_5_courses_by_teacher(session: AsyncSession, teacher_fullname: str):
    """Find which courses a particular teacher teaches."""
    print(f"\n--- Query 5: Courses taught by teacher '{teacher_fullname}' ---")
    stmt = (
        select(Subject.name).join(Teacher).filter(Teacher.fullname == teacher_fullname)
    )
    result = await session.execute(stmt)
    courses = result.scalars().all()
    if courses:
        print(f"Teacher '{teacher_fullname}' teaches: {', '.join(courses)}")
    else:
        print(
            f"No courses found for teacher '{teacher_fullname}' or teacher not found."
        )
    return courses


async def select_6_students_in_group(session: AsyncSession, group_name: str):
    """Find a list of students in a specific group."""
    print(f"\n--- Query 6: Students in group '{group_name}' ---")
    stmt = (
        select(Student.fullname)
        .join(Group)
        .filter(Group.name == group_name)
        .order_by(Student.fullname)
    )
    result = await session.execute(stmt)
    students = result.scalars().all()
    if students:
        print(f"Students in group '{group_name}':")
        for s_name in students:
            print(f"- {s_name}")
    else:
        print(f"No students found in group '{group_name}' or group not found.")
    return students


async def select_7_grades_in_group_for_subject(
    session: AsyncSession, group_name: str, subject_name: str
):
    """Find student grades in a specific group for a specific subject."""
    print(
        f"\n--- Query 7: Grades of students in group '{group_name}' for subject '{subject_name}' ---"
    )
    stmt = (
        select(Student.fullname, Grade.grade, Grade.date_received)
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(and_(Group.name == group_name, Subject.name == subject_name))
        .order_by(Student.fullname, Grade.date_received)
    )
    result = await session.execute(stmt)
    grades_info = result.all()
    if grades_info:
        print(f"Grades in group '{group_name}' for subject '{subject_name}':")
        for s_name, grade, date_rec in grades_info:
            print(
                f"- Student: {s_name}, Grade: {grade}, Date: {date_rec.strftime('%Y-%m-%d') if date_rec else 'N/A'}"
            )
    else:
        print(f"No grades found for group '{group_name}' in subject '{subject_name}'.")
    return grades_info


async def select_8_avg_grade_by_teacher(session: AsyncSession, teacher_fullname: str):
    """Find the average grade given by a particular teacher in their subjects."""
    print(f"\n--- Query 8: Average grade given by teacher '{teacher_fullname}' ---")
    stmt = (
        select(func.round(func.avg(Grade.grade), 2).label("avg_teacher_grade"))
        .select_from(Grade)
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.fullname == teacher_fullname)
    )
    result = await session.execute(stmt)
    avg_grade = result.scalar_one_or_none()
    if avg_grade is not None:
        print(f"Average grade given by '{teacher_fullname}': {avg_grade}")
    else:
        print(
            f"No grades found for subjects taught by '{teacher_fullname}' or teacher not found."
        )
    return avg_grade


async def select_9_courses_for_student(session: AsyncSession, student_fullname: str):
    """Find a list of courses taken by a particular student."""
    print(f"\n--- Query 9: Courses attended by student '{student_fullname}' ---")
    stmt = (
        select(Subject.name)
        .distinct()
        .select_from(Grade)
        .join(Subject)
        .join(Student)
        .filter(Student.fullname == student_fullname)
        .order_by(Subject.name)
    )
    result = await session.execute(stmt)
    courses = result.scalars().all()
    if courses:
        print(
            f"Student '{student_fullname}' attends (has grades in): {', '.join(courses)}"
        )
    else:
        print(
            f"No courses found for student '{student_fullname}' or student not found."
        )
    return courses


async def select_10_courses_for_student_by_teacher(
    session: AsyncSession, student_fullname: str, teacher_fullname: str
):
    """List of courses taught by a certain teacher to a certain student."""
    print(
        f"\n--- Query 10: Courses taught by '{teacher_fullname}' that '{student_fullname}' attends ---"
    )
    stmt = (
        select(Subject.name)
        .distinct()
        .select_from(Grade)
        .join(Student, Grade.student_id == Student.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(
            and_(
                Student.fullname == student_fullname,
                Teacher.fullname == teacher_fullname,
            )
        )
        .order_by(Subject.name)
    )
    result = await session.execute(stmt)
    courses = result.scalars().all()
    if courses:
        print(
            f"Student '{student_fullname}' attends courses by teacher '{teacher_fullname}': {', '.join(courses)}"
        )
    else:
        print(
            f"No such courses found for student '{student_fullname}' with teacher '{teacher_fullname}'."
        )
    return courses


async def fetch_example_data(session: AsyncSession):
    """Fetches example data to use as parameters for other queries."""
    print("\n--- Fetching example data for queries ---")
    example_data = {
        "subject_name": None,
        "group_name": None,
        "teacher_fullname": None,
        "student_fullname": None,
    }

    result = await session.execute(select(Subject.name).limit(1))
    subject = result.scalar_one_or_none()
    if subject:
        example_data["subject_name"] = subject
    else:
        print("Could not fetch an example subject.")

    result = await session.execute(select(Group.name).limit(1))
    group = result.scalar_one_or_none()
    if group:
        example_data["group_name"] = group
    else:
        print("Could not fetch an example group.")

    result = await session.execute(select(Teacher.fullname).limit(1))
    teacher = result.scalar_one_or_none()
    if teacher:
        example_data["teacher_fullname"] = teacher
    else:
        print("Could not fetch an example teacher.")

    result = await session.execute(select(Student.fullname).limit(1))
    student = result.scalar_one_or_none()
    if student:
        example_data["student_fullname"] = student
    else:
        print("Could not fetch an example student.")

    return example_data


async def main():
    """Main function to demonstrate running the select queries."""
    async with AsyncSessionFactory() as session:
        examples = await fetch_example_data(session)

        await select_1_top_students(session)

        if examples["subject_name"]:
            await select_2_student_top_grade_for_subject(
                session, examples["subject_name"]
            )
        else:
            print("Skipping Query 2: No example subject name available.")

        if examples["subject_name"] and examples["group_name"]:
            await select_3_avg_grade_in_group_for_subject(
                session, examples["subject_name"], examples["group_name"]
            )
        else:
            print("Skipping Query 3: Missing example subject or group name.")

        await select_4_overall_avg_grade(session)

        if examples["teacher_fullname"]:
            await select_5_courses_by_teacher(session, examples["teacher_fullname"])
        else:
            print("Skipping Query 5: No example teacher name available.")

        if examples["group_name"]:
            await select_6_students_in_group(session, examples["group_name"])
        else:
            print("Skipping Query 6: No example group name available.")

        if examples["group_name"] and examples["subject_name"]:
            await select_7_grades_in_group_for_subject(
                session, examples["group_name"], examples["subject_name"]
            )
        else:
            print("Skipping Query 7: Missing example group or subject name.")

        if examples["teacher_fullname"]:
            await select_8_avg_grade_by_teacher(session, examples["teacher_fullname"])
        else:
            print("Skipping Query 8: No example teacher name available.")

        if examples["student_fullname"]:
            await select_9_courses_for_student(session, examples["student_fullname"])
        else:
            print("Skipping Query 9: No example student name available.")

        if examples["student_fullname"] and examples["teacher_fullname"]:
            await select_10_courses_for_student_by_teacher(
                session, examples["student_fullname"], examples["teacher_fullname"]
            )
        else:
            print("Skipping Query 10: Missing example student or teacher name.")

    await engine.dispose()
    print("\nQueries finished and database engine disposed.")


if __name__ == "__main__":
    print("Running 'select' script...")
    asyncio.run(main())
    print("'Select' script finished.")
