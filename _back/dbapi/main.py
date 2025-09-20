from .decorators import DBContext
from typing import Union

@DBContext()
def get_user(login: str, pwd: str, cursor=None) -> Union[list, None]:
    query = f"""select id, full_name from users where login = '{login}' and pwd = '{pwd}' """
    cursor.execute(query)
    return cursor.fetchall()

@DBContext()
def get_all_users(cursor=None) -> list:
    query = f"""select id, full_name from users"""
    cursor.execute(query)
    return cursor.fetchall()

@DBContext()
def create_education_recording(uid: int, cursor=None) -> Union[int, None]:
    query = f"""INSERT INTO educations (user_id) VALUES ('{uid}')"""
    cursor.execute(query)

@DBContext()
def create_additional_education_recording(uid: int, cursor=None) -> Union[int, None]:
    query = f"""INSERT INTO additional_educations (user_id) VALUES ('{uid}')"""
    cursor.execute(query)

@DBContext()
def create_role_recording(uid: int, cursor=None) -> Union[int, None]:
    query = f"""INSERT INTO roles (user_id) VALUES ('{uid}')"""
    cursor.execute(query)

@DBContext()
def create_skill_recording(uid: int, cursor=None) -> Union[int, None]:
    query = f"""INSERT INTO skills (user_id) VALUES ('{uid}')"""
    cursor.execute(query)

@DBContext()
def create_additional_info_recording(uid: int, cursor=None) -> Union[int, None]:
    query = f"""INSERT INTO additional_info (user_id) VALUES ('{uid}')"""
    cursor.execute(query)

@DBContext()
def create_career_preference_recording(uid: int, cursor=None) -> Union[int, None]:
    query = f"""INSERT INTO career_preferences (user_id) VALUES ('{uid}')"""
    cursor.execute(query)

@DBContext()
def get_category_info(table: str, uid: int, cursor=None):
    query = f"""select * from {table} where user_id = {uid}"""
    cursor.execute(query)
    return cursor.fetchall()

@DBContext()
def update_recording(table: str, values: dict[str, any], cursor=None) -> None:
    body = ''
    for key, value in values.items():
        if isinstance(value, str):
            body += f"{key} = '{value}',"
        else:
            body += f"{key} = {value},"
    body = body[:-1]
    query = f"""UPDATE {table} SET {body}"""
    cursor.execute(query)
