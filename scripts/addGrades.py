import argparse
import random
import mysql.connector


def generate_and_insert_data(total_students):
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

    for i in range(total_students):
        # Generate random student ID
        sql_query = "SELECT student_id FROM students ORDER BY RAND() LIMIT 1;"
        cursor.execute(sql_query)
        student_id = cursor.fetchone()[0]

        # Generate random webinar ID
        sql_query = "SELECT webinar_id FROM webinars ORDER BY RAND() LIMIT 1;"
        cursor.execute(sql_query)
        webinar_id = cursor.fetchone()[0]

        # Generate random grade value
        grade_value = random.randint(1, 5)

        # SQL-запрос для добавления данных в таблицу
        sql = "INSERT INTO grades (student_id, webinar_id, grade_value) VALUES (%s, %s, %s)"
        values = (student_id, webinar_id, grade_value)
        cursor.execute(sql, values)

        # Выполнение коммита каждые N записей (например, каждые 1000)
        if i % 1000 == 0:
            conn.commit()

    # Завершение и сохранение изменений
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
