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
        values = (f"{first_name} {last_name}",
                  birthdate, email, phone)
        cursor.execute(sql, values)

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
