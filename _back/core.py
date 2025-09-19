from dbapi.main import *
import datetime
from _back.config import reader
import jwt

reader.read_config()


def verify_user(login: str, pwd: str) -> int:
    res = get_user(login, pwd)
    if len(res) == 0:
        return -1
    return res[0][0]


def create_recording(category: int, id: int):
    if category == 0:
        create_education_recording(id)
    elif category == 1:
        create_additional_education_recording(id)
    elif category == 2:
        create_role_recording(id)
    elif category == 3:
        create_skill_recording(id)
    elif category == 4:
        create_additional_info_recording(id)
    elif category == 5:
        create_career_preference_recording(id)


def generate_jwt(id: int) -> str:
    payload = {
        'uid': id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
    }

    token = jwt.encode(payload, reader.get_param_value('jwt-key'), algorithm='HS256')
    return token


create_recording(0, 1)
