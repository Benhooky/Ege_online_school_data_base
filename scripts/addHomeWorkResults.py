import argparse
import random
import mysql.connector
from dbconfig import db_config


def generate_and_insert_data(total_students):
    """
    Generate and insert homework results for a given number of students.

    Args:
        total_students (int): The number of students for whom to generate and insert homework results.
    """
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Select random student IDs from the students table
    sql_query = "SELECT student_id FROM students ORDER BY RAND() LIMIT %s;"
    cursor.execute(sql_query, (total_students,))
    student_ids = [row[0] for row in cursor.fetchall()]

    # Prepare the SQL statement for inserting homework results
    sql = "INSERT INTO homeworkresults (student_id, homework_id, score) VALUES (%s, %s, %s)"
    values = []

    # Generate and insert homework results for each student
    for student_id in student_ids:
        # Select a random homework ID
        sql_query = "SELECT homework_id FROM homework ORDER BY RAND() LIMIT 1;"
        cursor.execute(sql_query)
        homework_id = cursor.fetchone()[0]

        # Get the maximum points for the selected homework
        sql_query = "SELECT max_points FROM homework WHERE homework_id = %s;"
        cursor.execute(sql_query, (homework_id,))
        max_points = cursor.fetchone()[0]

        # Generate a random score between 0 and the maximum points
        score = random.randint(0, max_points)

        # Add the student ID, homework ID, and score to the values list
        values.append((student_id, homework_id, score))

    # Insert the generated values into the homeworkresults table
    cursor.executemany(sql, values)
    conn.commit()

    # Close the cursor and database connection
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
