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

    sql_query = "SELECT MAX(senior_teacher_id) FROM seniorteachers"
    cursor.execute(sql_query)
    start_id = cursor.fetchone()[0]
    start_id = start_id + 1 if start_id is not None else 1
    sql_query = "SELECT MAX(subject_id) FROM subjects"
    cursor.execute(sql_query)
    subject_max_id = cursor.fetchone()[0]
    for teacher_id in range(start_id, start_id + total_students):
        first_name = random.choice(list(first_names.keys()))
        gender = first_names.get(first_name, "unknown")
        last_name = random.choice(
            last_names_male) if gender == "male" else random.choice(last_names_male)+"а"
        email = f"{translit(first_name.lower(), 'ru', reversed=True)}.{translit(last_name.lower(), 'ru', reversed=True)}{random.randint(1, 100)}@{random.choice(['gmail.com','yandex.ru','mail.ru','outlook.com'])}"
        phone = f"+7{random.randint(100, 999):03d}{random.randint(100, 999):03d}{random.randint(10, 99):02d}{random.randint(10, 99):02d}"
        subject_id = f"{random.randint(1, subject_max_id)}"
        salary = f"{random.randint(150000, 250000)//1000*1000}"
        # SQL-запрос для добавления данных в таблицу
        sql = "INSERT INTO seniorteachers (senior_teacher_id, senior_teacher_name, email, phone, subject_id, salary) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (teacher_id, f"{first_name} {last_name}",
                  email.replace("'", ""), phone, subject_id, salary)
        cursor.execute(sql, values)

        # Выполнение коммита каждые N записей (например, каждые 1000)
        if teacher_id % 1000 == 0:
            conn.commit()

    # Завершение и сохранение изменений
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
