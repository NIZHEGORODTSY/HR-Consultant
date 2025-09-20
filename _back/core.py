from dbapi.main import *
import datetime
from config import reader
import jwt

reader.read_config()

CATEGORIES = ['educations', 'additional_educations', 'roles', 'skills', 'additional_info', 'career_preferences']

def verify_user(login: str, pwd: str) -> tuple[int, Union[str, None]]:
    res = get_user(login, pwd)
    if len(res) == 0:
        return -1, None
    return res[0][0], res[0][1]

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


def get_all_info(uid: int) -> dict:
    res = {}
    data = get_category_info('educations', uid)
    res['educations'] = {}
    for educ in data:
        res['educations'][str(educ[0])] = {
            "user_id": educ[1],
            "university": educ[2],
            "level": educ[3],
            "spec": educ[4],
            "grad_year": educ[5],
            "diploma": educ[6]
        }
    
    data = get_category_info('additional_educations', uid)
    res['additional_educations'] = {}
    for educ in data:
        res['additional_educations'][str(educ[0])] = {
            "user_id": educ[1],
            "name": educ[2],
            "company": educ[3],
            "issued": educ[4],
            "hours_amount": educ[5],
            "diploma": educ[6]
        }
    
    data = get_category_info('roles', uid)
    res['roles'] = {}
    for educ in data:
        res['roles'][str(educ[0])] = {
            "user_id": educ[1],
            "role": educ[2],
            "experiance": educ[3],
            "func_role": educ[4],
            "team_role": educ[5],
            "functionality": educ[6]
        }
    
    data = get_category_info('skills', uid)
    res['skills'] = {}
    for educ in data:
        res['skills'][str(educ[0])] = {
            "user_id": educ[1],
            "description": educ[2]
        }
    
    data = get_category_info('additional_info', uid)
    res['additional_info'] = {}
    for educ in data:
        res['additional_info'][str(educ[0])] = {
            "user_id": educ[1],
            "description": educ[2]
        }
    
    data = get_category_info('career_preferences', uid)
    res['career_preferences'] = {}
    for educ in data:
        res['career_preferences'][str(educ[0])] = {
            "user_id": educ[1],
            "description": educ[2]
        }
    
    return res


def generate_jwt(id: int, name : int) -> str:
    payload = {
        'uid': id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5),
        'name': name
    }

    token = jwt.encode(payload, reader.get_param_value('jwt-key'), algorithm='HS256')
    return token