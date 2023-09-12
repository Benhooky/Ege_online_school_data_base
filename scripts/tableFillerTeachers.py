import argparse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from transliterate import translit
import random
import itertools
import mysql.connector


def generate_and_insert_data(total_students):
    # Параметры подключения к базе данных
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "egor21412SFAW",
        "database": "ege_online_school"
    }

    # Ваши данные
    male_names = [
        "Александр", "Андрей", "Артем", "Вадим", "Валентин", "Валерий", "Василий", "Виктор", "Владимир", "Вячеслав",
        "Георгий", "Глеб", "Даниил", "Денис", "Дмитрий", "Евгений", "Иван", "Игорь", "Илья", "Кирилл",
        "Константин", "Леонид", "Максим", "Матвей", "Михаил", "Никита", "Олег", "Павел", "Петр", "Роман",
        "Руслан", "Сергей", "Станислав", "Тимофей", "Фёдор", "Эдуард", "Юрий", "Ярослав", "Анатолий",
        "Антон", "Арсений", "Борис", "Викентий", "Владислав", "Григорий", "Давид", "Егор", "Ефим",
        "Марк", "Роберт", "Савелий", "Степан", "Яков", "Аркадий", "Виталий"
    ]

    female_names = [
        "Александра", "Алиса", "Анастасия", "Ангелина", "Анна", "Валентина", "Валерия", "Варвара", "Василиса", "Вера",
        "Вероника", "Виктория", "Галина", "Дарина", "Дарья", "Евгения", "Екатерина", "Елена", "Елизавета", "Жанна",
        "Злата", "Инна", "Ирина", "Карина", "Кира", "Ксения", "Лариса", "Лидия", "Любовь", "Маргарита", "Марина",
        "Мария", "Мирослава", "Надежда", "Наталья", "Нина", "Оксана", "Ольга", "Полина", "Раиса", "Светлана",
        "София", "Таисия", "Тамара", "Татьяна", "Ульяна", "Фёкла", "Фёдора", "Юлия", "Яна", "Агата", "Агнесса",
        "Алевтина", "Алина", "Алла", "Альбина", "Амелия", "Анжела", "Антонина", "Арина", "Ева", "Лилия", "Милана"
    ]

    last_names_male = [
        "Иванов", "Смирнов", "Кузнецов", "Попов", "Соколов", "Лебедев", "Козлов", "Новиков", "Морозов", "Петров",
        "Волков", "Соловьев", "Васильев", "Зайцев", "Павлов", "Семенов", "Голубев", "Виноградов", "Богданов", "Воробьев",
        "Фёдоров", "Михайлов", "Беляев", "Тарасов", "Белов", "Комаров", "Орлов", "Киселёв", "Макаров", "Андреев",
        "Ковалёв", "Ильин", "Гусев", "Титов", "Кузьмин", "Кудрявцев", "Баранов", "Куликов", "Алексеев", "Степанов",
        "Яковлев", "Сорокин", "Сергеев", "Романов", "Захаров", "Борисов", "Королёв", "Герасимов", "Пономарёв", "Григорьев",
        "Лазарев", "Медведев", "Ершов", "Никитин", "Соболев", "Рябов", "Поляков", "Цветков", "Данилов", "Жуков",
        "Фролов", "Журавлёв", "Николаев", "Крылов", "Максимов", "Сидоров", "Осипов", "Белоусов", "Федотов", "Дорофеев",
        "Егоров", "Матвеев", "Бобров", "Дмитриев", "Калинин", "Анисимов", "Петухов", "Антонов", "Тимофеев", "Никифоров",
        "Веселов", "Филиппов", "Марков", "Большаков", "Суханов", "Миронов", "Ширяев", "Александров", "Коновалов", "Шестаков",
        "Казаков", "Ефимов", "Денисов", "Громов", "Фомин", "Давыдов", "Мельников", "Щербаков", "Блинов", "Колесников",
        "Карпов", "Афанасьев", "Власов", "Маслов", "Савельев", "Тимофеев", "Фокин"
    ]

    # Словарь для мужских имен
    first_names = {name: "male" for name in male_names}
    # Добавляем женские имена
    first_names.update({name: "female" for name in female_names})

    # Установка соединения с базой данных
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
        start_id = start_id + 1 if start_id else 1
        subject_max_id = subject_max_id if type(
            subject_max_id) is not None else 1

        # Prepare the INSERT statements
        insert_teachers_query = "INSERT INTO teachers (teacher_id, teacher_name, email, phone, subject_id, salary) VALUES (%s, %s, %s, %s, %s, %s)"
        insert_teacherrelationship_query = "INSERT INTO teacherrelationship (junior_teacher_id) VALUES (%s)"
        teachers_data = []
        teacherrelationship_data = []

        for teacher_id in range(start_id, start_id + total_students):
            first_name = random.choice(list(first_names.keys()))
            gender = first_names.get(first_name, "unknown")
            last_name = random.choice(
                last_names_male) if gender == "male" else random.choice(last_names_male)+"а"
            email = f"{translit(first_name.lower(), 'ru', reversed=True)}.{translit(last_name.lower(), 'ru', reversed=True)}{random.randint(1, 100)}@{random.choice(['gmail.com','yandex.ru','mail.ru','outlook.com'])}"
            phone = f"+7{random.randint(100, 999):03d}{random.randint(100, 999):03d}{random.randint(10, 99):02d}{random.randint(10, 99):02d}"
            subject_id = f"{random.randint(1, subject_max_id)}"
            salary = f"{random.randint(20000, 150000)//1000*1000}"

            # Append the data for batch insert
            teachers_data.append((teacher_id, f"{first_name} {last_name}",
                                  email.replace("'", ""), phone, subject_id, salary))
            teacherrelationship_data.append((teacher_id,))

            # Выполнение коммита каждые N записей (например, каждые 1000)
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
