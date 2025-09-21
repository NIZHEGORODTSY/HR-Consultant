# database.py
import pandas as pd
from sqlalchemy import create_engine, text
from hr_config import CONNECTION_STRING


def get_data_from_db():
    """Получение данных из PostgreSQL базы данных с использованием SQLAlchemy"""
    try:
        # Создаем engine
        engine = create_engine(CONNECTION_STRING)

        # Загрузка данных из таблиц
        with engine.connect() as conn:
            users = pd.read_sql(text("SELECT * FROM users"), conn)
            skills = pd.read_sql(text("SELECT * FROM skills"), conn)
            roles = pd.read_sql(text("SELECT * FROM roles"), conn)
            educations = pd.read_sql(text("SELECT * FROM educations"), conn)
            career_preferences = pd.read_sql(text("SELECT * FROM career_preferences"), conn)

        return users, skills, roles, educations, career_preferences

    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()


def create_test_data():
    """Создание тестовых данных для демонстрации"""
    users = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'full_name': ['Иванов Иван Иванович', 'Петров Петр Петрович', 'Сидорова Анна Сергеевна', 'Кузнецов Алексей',
                      'Смирнова Ольга'],
        'is_admin': [0, 0, 0, 0, 0],
        'login': ['ivanov', 'petrov', 'sidorova', 'kuznetsov', 'smirnova'],
        'pwd': ['pass1', 'pass2', 'pass3', 'pass4', 'pass5']
    })

    skills = pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 6, 7, 8],
        'user_id': [1, 1, 2, 2, 3, 4, 5, 5],
        'description': ['Python', 'SQL', 'JavaScript', 'React', 'Python', 'Java', 'C++', 'Data Analysis']
    })

    roles = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'user_id': [1, 2, 3, 4, 5],
        'role': ['Разработчик Python', 'Frontend разработчик', 'Data Scientist', 'Java разработчик', 'C++ разработчик'],
        'start_date': pd.to_datetime(['2020-01-01', '2019-05-15', '2021-03-10', '2018-07-20', '2022-02-01']),
        'end_date': [None, None, None, None, None]
    })

    educations = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'user_id': [1, 2, 3, 4, 5],
        'university': ['МГУ', 'СПбГУ', 'МГТУ', 'МФТИ', 'ВШЭ'],
        'level': ['Бакалавр', 'Магистр', 'Бакалавр', 'Магистр', 'Бакалавр'],
        'speciality': ['Информатика', 'Математика', 'Программирование', 'Физика', 'Экономика'],
        'graduation_year': [2020, 2019, 2021, 2018, 2022]
    })

    career_preferences = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'user_id': [1, 2, 3, 4, 5],
        'desired_position': ['Senior Developer', 'Team Lead', 'Data Scientist', 'Architect', 'Project Manager'],
        'work_format': ['Офис', 'Удаленно', 'Гибрид', 'Офис', 'Удаленно'],
        'expected_salary': [150000, 180000, 120000, 200000, 160000]
    })

    return users, skills, roles, educations, career_preferences
