
import mysql.connector
import random
from itertools import cycle


def update_relations():
    """
    Update the student-teacher relationships in the database.
    """
    # Establish a connection to the database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="egor21412SFAW",
        database="ege_online_school"
    )
    cursor = db_connection.cursor()

    # Retrieve all student IDs from the 'students' table
    cursor.execute("SELECT student_id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]

    # Retrieve all teacher IDs and subject IDs from the 'teachers' table
    cursor.execute("SELECT teacher_id, subject_id FROM teachers")
    teacher_data = cursor.fetchall()

    # Retrieve all subject IDs from the 'subjects' table
    cursor.execute("SELECT subject_id FROM subjects")
    subject_ids = [row[0] for row in cursor.fetchall()]

    # Create a dictionary to map subject IDs to an iterator of teacher IDs
    subject_teacher_dict = {}
    for subject_id in subject_ids:
        teachers_for_subject = [teacher[0]
                                for teacher in teacher_data if teacher[1] == subject_id]
        subject_teacher_dict[subject_id] = cycle(teachers_for_subject)

    # Update the student-teacher relationships for each student
    for student_id in student_ids:
        selected_subjects = random.sample(
            subject_ids, random.randint(1, len(subject_ids)))
        for subject_id in selected_subjects:
            teacher_id = next(subject_teacher_dict[subject_id])
            sql = "INSERT INTO student_teacher_relationship (student_id, teacher_id) VALUES (%s, %s)"
            values = (student_id, teacher_id)
            cursor.execute(sql, values)

        # Commit the changes to the database
        db_connection.commit()

    # Close the cursor and the database connection
    cursor.close()
    db_connection.close()


def main():
    update_relations()


if __name__ == "__main__":
    main()
