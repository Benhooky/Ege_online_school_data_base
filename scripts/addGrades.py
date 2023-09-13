import argparse
import random
import mysql.connector
from dbconfig import db_config


def generate_and_insert_data(total_students):
    """
    Generate and insert random data into the grades table.

    Args:
        total_students (int): The total number of students.

    Returns:
        None
    """

    # Establish database connection
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Loop through total_students
    for i in range(total_students):
        # Generate random student ID
        cursor.execute(
            "SELECT student_id FROM students ORDER BY RAND() LIMIT 1;")
        student_id = cursor.fetchone()[0]

        # Generate random webinar ID
        cursor.execute(
            "SELECT webinar_id FROM webinars ORDER BY RAND() LIMIT 1;")
        webinar_id = cursor.fetchone()[0]

        # Generate random grade value
        grade_value = random.randint(1, 5)

        # Insert data into grades table
        sql = "INSERT INTO grades (student_id, webinar_id, grade_value) VALUES (%s, %s, %s)"
        values = (student_id, webinar_id, grade_value)
        cursor.execute(sql, values)

        # Commit every 1000 records
        if i % 1000 == 0:
            conn.commit()

    # Commit and close connection
    conn.commit()
    cursor.close()
    conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Generate and insert student data into the database.")
    parser.add_argument("total_students", type=int,
                        help="Total number of students to add")
    args = parser.parse_args()

    total_students_to_add = args.total_students
    generate_and_insert_data(total_students_to_add)


if __name__ == "__main__":
    main()
