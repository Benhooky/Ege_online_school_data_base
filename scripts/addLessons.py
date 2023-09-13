import argparse
import random
import mysql.connector
from dbconfig import db_config


def generate_and_insert_lessons(total_lessons):
    """
    Generate and insert lessons into the database.

    Args:
        total_lessons (int): The total number of lessons to generate and insert.

    Returns:
        None
    """
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Get the list of student IDs
    cursor.execute("SELECT student_id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]

    # Get the list of teacher IDs
    cursor.execute("SELECT teacher_id FROM teachers")
    teacher_ids = [row[0] for row in cursor.fetchall()]

    # Get the list of subject IDs
    cursor.execute("SELECT subject_id FROM subjects")
    subject_ids = [row[0] for row in cursor.fetchall()]

    lesson_ids = []

    # Generate and insert lessons
    for _ in range(total_lessons):
        student_id = random.choice(student_ids)
        teacher_id = random.choice(teacher_ids)
        subject_id = random.choice(subject_ids)
        day_of_week = random.choice(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
        lesson_time = f"{random.randint(8, 16):02d}:00"

        # Insert lesson into the database
        sql = """
            INSERT INTO lessons (teacher_id, student_id, subject_id, day_of_week, lesson_time)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (teacher_id, student_id, subject_id, day_of_week, lesson_time)

        cursor.execute(sql, values)
        conn.commit()
        lesson_ids.append(cursor.lastrowid)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate and insert lesson data into the database.")
    parser.add_argument("total_lessons", type=int,
                        help="Total number of lessons to add")
    args = parser.parse_args()

    total_lessons_to_add = args.total_lessons
    generate_and_insert_lessons(total_lessons_to_add)
