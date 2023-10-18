import argparse
import random
import mysql.connector
from dbconfig import db_config

MAX_ATTEMPTS = 10  # Максимальное количество попыток выбора времени


def is_teacher_available(cursor, teacher_id, day_of_week, lesson_time):
    """
    Check if a teacher is available at the specified day and time.

    Args:
        cursor (mysql.connector.cursor): Database cursor.
        teacher_id (int): The ID of the teacher to check.
        day_of_week (str): The day of the week.
        lesson_time (str): The time of the lesson.

    Returns:
        bool: True if the teacher is available, False otherwise.
    """
    sql = """
        SELECT COUNT(*) FROM lessons
        WHERE teacher_id = %s
        AND day_of_week = %s
        AND lesson_time = %s
    """
    values = (teacher_id, day_of_week, lesson_time)
    cursor.execute(sql, values)
    count = cursor.fetchone()[0]
    return count == 0


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

    # Get the list of teacher IDs and their corresponding subject IDs
    cursor.execute("SELECT teacher_id, subject_id FROM teachers")
    teacher_subject_pairs = cursor.fetchall()

    lesson_ids = []

    # Generate and insert lessons
    for _ in range(total_lessons):
        student_id = random.choice(student_ids)

        # Choose a random teacher-subject pair
        teacher_subject_pair = random.choice(teacher_subject_pairs)
        teacher_id, subject_id = teacher_subject_pair

        day_of_week = random.choice(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])

        attempts = 0

        while attempts < MAX_ATTEMPTS:
            # Generate a random lesson time
            lesson_time = f"{random.randint(8, 16):02d}:00"

            # Check if the teacher is available at this time
            if is_teacher_available(cursor, teacher_id, day_of_week, lesson_time):
                break
            attempts += 1

        if attempts == MAX_ATTEMPTS:
            # Если не удалось найти свободное время, переходим к следующему учителю
            continue

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
