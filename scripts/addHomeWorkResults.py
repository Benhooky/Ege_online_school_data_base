import argparse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from transliterate import translit
import random
import itertools
import mysql.connector


def generate_and_insert_data(total_students):
    # Параметры подключения к базе данных
    # Параметры подключения к базе данных
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "egor21412SFAW",
        "database": "ege_online_school"
    }

    # Установка соединения с базой данных
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Generate random student IDs
    sql_query = "SELECT student_id FROM students ORDER BY RAND() LIMIT %s;"
    cursor.execute(sql_query, (total_students,))
    student_ids = [row[0] for row in cursor.fetchall()]

    # Prepare the INSERT statement and values
    sql = "INSERT INTO homeworkresults (student_id, homework_id, score) VALUES (%s, %s, %s)"
    values = []
    for student_id in student_ids:
        # Generate random homework ID
        sql_query = "SELECT homework_id FROM homework ORDER BY RAND() LIMIT 1;"
        cursor.execute(sql_query)
        homework_id = cursor.fetchone()[0]

        # Generate random score for the homework
        sql_query = "SELECT max_points FROM homework WHERE homework_id = %s;"
        cursor.execute(sql_query, (homework_id,))
        max_points = cursor.fetchone()[0]
        score = random.randint(0, max_points)

        values.append((student_id, homework_id, score))

    # Execute the bulk INSERT
    cursor.executemany(sql, values)

    # Commit the transaction
    conn.commit()

    # Завершение и сохранение изменений
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
