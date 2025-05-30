import asyncio
import random
import datetime
from faker import Faker

from src.db.session import AsyncSessionFactory, engine
from src.db.models import Student, Group, Teacher, Subject, Grade

fake = Faker()
# Config for Seeding
NUMBER_OF_STUDENTS = random.randint(30, 50)
NUMBER_OF_GROUPS = 3
NUMBER_OF_SUBJECTS = random.randint(5, 8)
NUMBER_OF_TEACHERS = random.randint(3, 5)
MAX_GRADES_PER_STUDENT = 20


async def seed_data():
    async with AsyncSessionFactory() as session:
        async with session.begin():
            # Create Groups
            groups = []
            for _ in range(1, NUMBER_OF_GROUPS + 1):
                group_name = f"{fake.word().capitalize()}{fake.word().capitalize()}-{random.randint(10,99)}"
                group = Group(name=group_name)
                groups.append(group)
            session.add_all(groups)
            await session.flush()
            print(f"Created {len(groups)} groups.")

            # Create Teachers
            teachers = []
            for _ in range(NUMBER_OF_TEACHERS):
                teacher = Teacher(fullname=fake.name())
                teachers.append(teacher)
            session.add_all(teachers)
            await session.flush()
            print(f"Created {len(teachers)} teachers.")

            # Create Subjects (and assign teachers)
            subjects = []
            if not teachers:
                print(
                    "No teachers available to assign to subjects. Skipping subject creation."
                )
            else:
                subject_names = set()
                while len(subjects) < NUMBER_OF_SUBJECTS:
                    name = fake.catch_phrase().capitalize()
                    if name not in subject_names:
                        subject_names.add(name)
                        subject = Subject(name=name, teacher=random.choice(teachers))
                        subjects.append(subject)
                session.add_all(subjects)
                await session.flush()
                print(f"Created {len(subjects)} subjects.")

            # Create Students (and assign groups)
            students = []
            if not groups:
                print(
                    "No groups available to assign to students. Skipping student creation."
                )
            else:
                for _ in range(NUMBER_OF_STUDENTS):
                    student = Student(fullname=fake.name(), group=random.choice(groups))
                    students.append(student)
                session.add_all(students)
                await session.flush()
                print(f"Created {len(students)} students.")

            # Create Grades
            all_grades_to_add = []
            if students and subjects:
                for student in students:
                    num_grades_for_this_student = random.randint(
                        1, MAX_GRADES_PER_STUDENT
                    )
                    for _ in range(num_grades_for_this_student):
                        selected_subject = random.choice(subjects)
                        grade_value = random.randint(60, 100)
                        aware_grade_date = fake.date_time_between(
                            start_date="-2y",
                            end_date="now",
                            tzinfo=datetime.timezone.utc,
                        )
                        naive_utc_grade_date = aware_grade_date.astimezone(
                            datetime.timezone.utc
                        ).replace(tzinfo=None)

                        grade_entry = Grade(
                            student_id=student.id,
                            subject_id=selected_subject.id,
                            grade=grade_value,
                            date_received=naive_utc_grade_date,
                        )

                        all_grades_to_add.append(grade_entry)
                session.add_all(all_grades_to_add)
                print(f"Added {len(all_grades_to_add)} grades.")

            else:
                print("No students or subjects available to create grades.")

        print("Seeding transaction complete (committed or rolled back).")


async def run_seeding():
    """Main function to run the seeding process and clean up engine resources."""
    # Clear existing data for future seeding
    # async with AsyncSessionFactory() as session:
    #     async with session.begin():
    #         from sqlalchemy import text
    #         print("Clearing old data (grades, students, subjects, teachers, groups)...")
    #         await session.execute(text("TRUNCATE TABLE grades RESTART IDENTITY CASCADE;"))
    #         await session.execute(text("TRUNCATE TABLE students RESTART IDENTITY CASCADE;"))
    #         await session.execute(text("TRUNCATE TABLE subjects RESTART IDENTITY CASCADE;"))
    #         await session.execute(text("TRUNCATE TABLE teachers RESTART IDENTITY CASCADE;"))
    #         await session.execute(text("TRUNCATE TABLE groups RESTART IDENTITY CASCADE;"))
    #     print("Old data cleared.")

    await seed_data()
    print("Data seeding function finished.")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run_seeding())
    print("Seeder script finished.")
