
import random
import mysql.connector


def generate_and_insert_data():
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

    # SQL query to select all webinar IDs
    sql = "SELECT webinar_id FROM webinars;"
    cursor.execute(sql)
    webinar_ids = cursor.fetchall()

    # SQL query to select all senior teacher IDs
    sql = "SELECT senior_teacher_id FROM seniorteachers;"
    cursor.execute(sql)
    senior_teacher_ids = cursor.fetchall()

    # Update each webinar row with a randomly selected senior teacher
    for webinar_id in webinar_ids:
        random_senior_teacher_id = random.choice(senior_teacher_ids)[0]
        sql = "UPDATE webinars SET senior_teacher_id = %s WHERE webinar_id = %s"
        values = (random_senior_teacher_id, webinar_id[0])
        cursor.execute(sql, values)

    # Commit the changes to the database
    conn.commit()


def main():
    generate_and_insert_data()


if __name__ == "__main__":
    main()
