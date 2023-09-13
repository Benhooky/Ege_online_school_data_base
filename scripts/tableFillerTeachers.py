import argparse
from transliterate import translit
import random
import mysql.connector
from dbconfig import db_config, male_names, last_names_male, female_names


def generate_and_insert_data(total_students):
    """
    Generate and insert data into the database for a given number of students.

    Args:
        total_students (int): The total number of students.

    Raises:
        Exception: If there is an error during the transaction.

    Returns:
        None
    """

    # Dictionary for male and female names
    first_names = {name: "male" for name in male_names}
    first_names.update({name: "female" for name in female_names})

    # Establish a connection to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Begin a transaction
    conn.start_transaction()

    try:
        # Get the maximum teacher ID and subject ID
        cursor.execute("SELECT MAX(teacher_id) FROM teachers")
        start_id = cursor.fetchone()[0]
        cursor.execute("SELECT MAX(subject_id) FROM subjects")
        subject_max_id = cursor.fetchone()[0]

        # Increment the start ID if it exists
        start_id = start_id + 1 if start_id else 1
        subject_max_id = subject_max_id if subject_max_id is not None else 1

        # Prepare the INSERT statements
        insert_teachers_query = """
            INSERT INTO teachers (teacher_id, teacher_name, email, phone, subject_id, salary)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        insert_teacherrelationship_query = """
            INSERT INTO teacherrelationship (junior_teacher_id)
            VALUES (%s)
        """
        teachers_data = []
        teacherrelationship_data = []

        for teacher_id in range(start_id, start_id + total_students):
            # Generate random data for each student
            first_name = random.choice(list(first_names.keys()))
            gender = first_names.get(first_name, "unknown")
            last_name = random.choice(
                last_names_male) if gender == "male" else random.choice(last_names_male) + "а"
            email = f"{translit(first_name.lower(), 'ru', reversed=True)}.{translit(last_name.lower(), 'ru', reversed=True)}{random.randint(1, 100)}@{random.choice(['gmail.com','yandex.ru','mail.ru','outlook.com'])}"
            phone = f"+7{random.randint(100, 999):03d}{random.randint(100, 999):03d}{random.randint(10, 99):02d}{random.randint(10, 99):02d}"
            subject_id = f"{random.randint(1, subject_max_id)}"
            salary = f"{random.randint(20000, 150000)//1000*1000}"

            # Append the data for batch insert
            teachers_data.append((teacher_id, f"{first_name} {last_name}",
                                  email.replace("'", ""), phone, subject_id, salary))
            teacherrelationship_data.append((teacher_id,))

            # Commit the transaction every N records (e.g., every 1000)
            if teacher_id % 1000 == 0:
                # Batch insert the data
                cursor.executemany(insert_teachers_query, teachers_data)
                cursor.executemany(
                    insert_teacherrelationship_query, teacherrelationship_data)
                # Clear the data lists
                teachers_data.clear()
                teacherrelationship_data.clear()

        # Batch insert any remaining data
        if teachers_data:
            # Batch insert the data
            cursor.executemany(insert_teachers_query, teachers_data)
            cursor.executemany(
                insert_teacherrelationship_query, teacherrelationship_data)

        # Commit the transaction
        conn.commit()
    except Exception as e:
        # Rollback the transaction in case of any exception
        conn.rollback()
        raise e
    finally:
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
