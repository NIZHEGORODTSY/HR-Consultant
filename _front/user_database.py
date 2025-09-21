# database.py
# Функции для работы с базой данных
import pandas as pd
from sqlalchemy import create_engine, inspect
from user_config import DB_CONFIG

def connect_to_db():
    """Подключение к базе данных"""
    try:
        connection_string = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

def get_table_columns(engine, table_name):
    """Получить список колонок таблицы"""
    try:
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        return columns
    except Exception as e:
        print(f"Ошибка получения колонок таблицы {table_name}: {e}")
        return []

def find_join_key(columns1, columns2):
    """Найти общий ключ для соединения таблиц"""
    common_columns = set(columns1) & set(columns2)
    
    # Приоритетные ключи для соединения
    preferred_keys = ['user_id', 'id', 'userid', 'user', 'user_key']
    
    for key in preferred_keys:
        if key in common_columns:
            return key
    
    # Если нет приоритетных ключей, вернуть первый общий
    if common_columns:
        return list(common_columns)[0]
    
    return None

def load_data_from_db():
    """Загрузка данных из PostgreSQL"""
    engine = connect_to_db()
    if engine:
        try:
            # Загружаем данные из таблиц
            users = pd.read_sql('SELECT * FROM users', engine)
            skills = pd.read_sql('SELECT * FROM skills', engine)
            roles = pd.read_sql('SELECT * FROM roles', engine)
            educations = pd.read_sql('SELECT * FROM educations', engine)
            career_preferences = pd.read_sql('SELECT * FROM career_preferences', engine)
            
            # Получаем колонки каждой таблицы для определения ключей соединения
            users_cols = get_table_columns(engine, 'users')
            skills_cols = get_table_columns(engine, 'skills')
            roles_cols = get_table_columns(engine, 'roles')
            educations_cols = get_table_columns(engine, 'educations')
            career_preferences_cols = get_table_columns(engine, 'career_preferences')
            
            # Объединяем все данные с автоматическим определением ключей
            merged_data = users.copy()
            
            # Определяем ключи для соединения
            users_roles_key = find_join_key(users_cols, roles_cols) or 'id'
            users_edu_key = find_join_key(users_cols, educations_cols) or 'id'
            users_career_key = find_join_key(users_cols, career_preferences_cols) or 'id'
            
            print(f"Ключи соединения: users-roles: {users_roles_key}, users-edu: {users_edu_key}, users-career: {users_career_key}")
            
            # Объединяем таблицы
            if not roles.empty and users_roles_key in users.columns and users_roles_key in roles.columns:
                merged_data = merged_data.merge(roles, on=users_roles_key, how='left')
            
            if not educations.empty and users_edu_key in merged_data.columns and users_edu_key in educations.columns:
                merged_data = merged_data.merge(educations, on=users_edu_key, how='left')
            
            if not career_preferences.empty and users_career_key in merged_data.columns and users_career_key in career_preferences.columns:
                merged_data = merged_data.merge(career_preferences, on=users_career_key, how='left')
            
            # Анализ данных
            if not skills.empty:
                # Определяем, какая колонка содержит описание навыков
                skill_column = 'description' if 'description' in skills.columns else (
                    'skill' if 'skill' in skills.columns else skills.columns[0] if not skills.empty else None
                )
                if skill_column:
                    skill_counts = skills[skill_column].value_counts().reset_index()
                    skill_counts.columns = ['skill', 'count']
                else:
                    skill_counts = pd.DataFrame(columns=['skill', 'count'])
            else:
                skill_counts = pd.DataFrame(columns=['skill', 'count'])
            
            if not roles.empty:
                # Определяем, какая колонка содержит роль
                role_column = 'role' if 'role' in roles.columns else (
                    'position' if 'position' in roles.columns else roles.columns[0] if not roles.empty else None
                )
                if role_column:
                    role_stats = roles[role_column].value_counts().reset_index()
                    role_stats.columns = ['role', 'count']
                else:
                    role_stats = pd.DataFrame(columns=['role', 'count'])
            else:
                role_stats = pd.DataFrame(columns=['role', 'count'])
            
            return users, skills, roles, educations, career_preferences, merged_data, skill_counts, role_stats
            
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            return None, None, None, None, None, None, None, None
    return None, None, None, None, None, None, None, None

def explore_database_structure():
    """Функция для исследования структуры базы данных"""
    engine = connect_to_db()
    if engine:
        try:
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print("Таблицы в базе данных:", tables)
            
            for table in tables:
                columns = inspector.get_columns(table)
                print(f"\nТаблица: {table}")
                for column in columns:
                    print(f"  Колонка: {column['name']} ({column['type']})")
            
        except Exception as e:
            print(f"Ошибка исследования структуры БД: {e}")

def get_empty_dataframes():
    """Создание пустых DataFrame для обработки ошибок"""
    users = pd.DataFrame()
    skills = pd.DataFrame()
    roles = pd.DataFrame()
    educations = pd.DataFrame()
    career_preferences = pd.DataFrame()
    merged_data = pd.DataFrame()
    skill_counts = pd.DataFrame(columns=['skill', 'count'])
    role_stats = pd.DataFrame(columns=['role', 'count'])
    
    return users, skills, roles, educations, career_preferences, merged_data, skill_counts, role_stats