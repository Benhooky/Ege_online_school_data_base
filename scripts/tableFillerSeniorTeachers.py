import argparse
import random
import mysql.connector
from dbconfig import db_config, male_names, last_names_male, female_names
from transliterate import translit


def generate_and_insert_data(total_students):
    """
    Generate and insert data for senior teachers into the database.

    Args:
        total_students (int): The number of senior teachers to generate.

    """
    # Dictionary for male names
    first_names = {name: "male" for name in male_names}
    # Add female names
    first_names.update({name: "female" for name in female_names})

    # Establish connection to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Get the maximum senior teacher ID from the database
    sql_query = "SELECT MAX(senior_teacher_id) FROM seniorteachers"
    cursor.execute(sql_query)
    start_id = cursor.fetchone()[0]
    start_id = start_id + 1 if start_id is not None else 1

    # Get the maximum subject ID from the database
    sql_query = "SELECT MAX(subject_id) FROM subjects"
    cursor.execute(sql_query)
    subject_max_id = cursor.fetchone()[0]

    # Generate and insert data for each teacher
    for teacher_id in range(start_id, start_id + total_students):
        first_name = random.choice(list(first_names.keys()))
        gender = first_names.get(first_name, "unknown")
        last_name = random.choice(
            last_names_male) if gender == "male" else random.choice(last_names_male) + "а"
        email = f"{translit(first_name.lower(), 'ru', reversed=True)}.{translit(last_name.lower(), 'ru', reversed=True)}{random.randint(1, 100)}@{random.choice(['gmail.com','yandex.ru','mail.ru','outlook.com'])}"
        phone = f"+7{random.randint(100, 999):03d}{random.randint(100, 999):03d}{random.randint(10, 99):02d}{random.randint(10, 99):02d}"
        subject_id = f"{random.randint(1, subject_max_id)}"
        salary = f"{random.randint(150000, 250000)//1000*1000}"

        # SQL query to insert data into the table
        sql = "INSERT INTO seniorteachers (senior_teacher_id, senior_teacher_name, email, phone, subject_id, salary) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (teacher_id, f"{first_name} {last_name}",
                  email.replace("'", ""), phone, subject_id, salary)
        cursor.execute(sql, values)

        # Commit the changes every N records (e.g. every 1000)
        if teacher_id % 1000 == 0:
            conn.commit()

    # Commit and close the connection
    conn.commit()
    cursor.close()
    conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Generate and insert senior teachers into the database.")
    parser.add_argument("total_students", type=int,
                        help="Total number of senior teachers to add")
    args = parser.parse_args()

    total_students_to_add = args.total_students
    generate_and_insert_data(total_students_to_add)


if __name__ == "__main__":
    main()
