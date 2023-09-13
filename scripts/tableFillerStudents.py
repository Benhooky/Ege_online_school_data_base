import argparse
from transliterate import translit
import random
import mysql.connector
from dbconfig import db_config, male_names, last_names_male, female_names


def generate_and_insert_data(total_students):
    """
    Generate and insert random student data into the database.

    Parameters:
        total_students (int): The total number of students to generate data for.
    """

    # Dictionary for male and female names
    first_names = {name: "male" for name in male_names}
    first_names.update({name: "female" for name in female_names})

    # Establish a connection to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Generate random first names
    random_first_names = random.choices(
        list(first_names.keys()), k=total_students)

    # Generate random last names
    random_last_names = [random.choice(last_names_male) if first_names.get(
        first_name) == "male" else random.choice(last_names_male)+"а" for first_name in random_first_names]

    # Generate random birthdates, emails, and phone numbers
    birthdates = [
        f"{random.randint(2006, 2009)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}" for _ in range(total_students)]
    emails = [f"{translit(first_name.lower(), 'ru', reversed=True)}.{translit(last_name.lower(), 'ru', reversed=True)}{random.randint(1, 100)}@gmail.com" for first_name,
              last_name in zip(random_first_names, random_last_names)]
    phones = [
        f"+7{random.randint(100, 999):03d}{random.randint(100, 999):03d}{random.randint(10, 99):02d}{random.randint(10, 99):02d}" for _ in range(total_students)]

    # Iterate over the lists and insert data into the table
    for first_name, last_name, birthdate, email, phone in zip(random_first_names, random_last_names, birthdates, emails, phones):
        sql = "INSERT INTO students (student_name, birthdate, email, phone) VALUES (%s, %s, %s, %s)"
        values = (f"{first_name} {last_name}", birthdate, email, phone)
        cursor.execute(sql, values)

    # Commit and close the cursor and connection
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
