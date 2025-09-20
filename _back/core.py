from dbapi.main import *
import datetime
from config import reader
import jwt

reader.read_config()

CATEGORIES = ['educations', 'additional_educations', 'roles', 'skills', 'additional_info', 'career_preferences']

def verify_user(login: str, pwd: str) -> int:
    res = get_user(login, pwd)
    if len(res) == 0:
        return -1
    return res[0][0]

def create_recording(category: str, id: int):
    if category == 'educations':
        create_education_recording(id)
    elif category == 'additional_educations':
        create_additional_education_recording(id)
    elif category == 'roles':
        create_role_recording(id)
    elif category == 'skills':
        create_skill_recording(id)
    elif category == 'additional_info':
        create_additional_info_recording(id)
    elif category == 'career_preferences':
        create_career_preference_recording(id)

def add(data, id: int):
    for category in CATEGORIES:
        items = data.get(category)
        update_recording(category, items)



def generate_jwt(id: int, name : int) -> str:
    payload = {
        'uid': id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5),
        'name': name
    }

    token = jwt.encode(payload, reader.get_param_value('jwt-key'), algorithm='HS256')
    return token

create_recording(0, 1)
