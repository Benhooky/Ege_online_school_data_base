import mysql.connector
from itertools import cycle


def update_relations():
    # Establish a connection to the database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="egor21412SFAW",
        database="ege_online_school"
    )

    # Create a cursor object to execute SQL queries
    cursor = db_connection.cursor()

    # Count the total number of distinct subjects
    cursor.execute(
        "SELECT COUNT(DISTINCT subject_id) AS total_subjects FROM subjects"
    )
    amount_subjects = cursor.fetchone()[0]

    # Iterate over each subject
    for subject_id in range(1, amount_subjects+1):
        # Retrieve junior teacher IDs for a specific subject
        sql = """
            SELECT t.teacher_id
            FROM teachers t
            LEFT JOIN teacherrelationship tr ON t.teacher_id = tr.junior_teacher_id
            WHERE t.subject_id = %s
            AND tr.senior_teacher_id IS NULL
            AND tr.relationship_id IS NOT NULL;
        """
        cursor.execute(sql, (subject_id,))
        junior_teacher_ids = cursor.fetchall()

        # Retrieve senior teacher IDs for the same subject
        cursor.execute(
            "SELECT senior_teacher_id FROM seniorteachers WHERE subject_id = %s",
            (subject_id,)
        )
        senior_teacher_ids = cursor.fetchall()

        # Create a cyclic iterator over senior teacher IDs
        senior_cycle = cycle(senior_teacher_ids)

        # Assign senior teacher IDs to junior teacher IDs
        for row in junior_teacher_ids:
            senior_teacher_id = next(senior_cycle)
            sql = "UPDATE teacherrelationship SET senior_teacher_id = %s WHERE junior_teacher_id = %s"
            values = (senior_teacher_id[0], row[0])
            cursor.execute(sql, values)

        # Commit the changes to the database
        db_connection.commit()

    # Close the cursor and database connection
    cursor.close()
    db_connection.close()


def main():
    update_relations()


if __name__ == "__main__":
    main()
