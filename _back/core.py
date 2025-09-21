from dbapi.main import *
import datetime
from config import reader
import jwt
from queue import Queue
import threading
import time
from _MODELS.get_ai_answer import get_ai_answer

reader.read_config()

CATEGORIES = ['educations', 'additional_educations', 'roles', 'skills', 'additional_info', 'career_preferences']


def verify_user(login: str, pwd: str):
    res = get_user(login, pwd)
    if len(res) == 0:
        return -1, None
    return res[0][0], res[0][1], res[0][2]


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


def add(uid: int, data: dict[str, dict]):
    for category, category_data in data.items():
        has_multiple_records = False
        for key in category_data.keys():
            if isinstance(key, int):
                has_multiple_records = True
                break
        if has_multiple_records:
            for record_id, record_data in category_data.items():
                update_recording(uid, category, record_id, record_data)
        else:
            update_recording(category=category, record_id=None, values=category_data)
    # for category in CATEGORIES:
    #     items = data.get(category)
    #     update_recording(category, items)


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
            "grad_year": educ[5]
        }

    data = get_category_info('additional_educations', uid)
    res['additional_educations'] = {}
    for educ in data:
        res['additional_educations'][str(educ[0])] = {
            "user_id": educ[1],
            "name": educ[2],
            "company": educ[3],
            "issued": educ[4],
            "hours_amount": educ[5]
        }

    data = get_category_info('roles', uid)
    res['roles'] = {}
    for educ in data:
        res['roles'][str(educ[0])] = {
            "user_id": educ[1],
            "role": educ[2],
            "start_date": educ[3],
            "end_date": educ[4]
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
            "description": [lang for lang in educ[2]]
        }

    data = get_category_info('career_preferences', uid)
    res['career_preferences'] = {}
    for educ in data:
        res['career_preferences'][str(educ[0])] = {
            "user_id": educ[1],
            "description": [tech for tech in educ[2]]
        }

    return res


def generate_jwt(id: int, name: int, is_hr: int) -> str:
    payload = {
        'uid': id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5),
        'name': name,
        'is_hr': is_hr
    }

    token = jwt.encode(payload, reader.get_param_value('jwt-key'), algorithm='HS256')
    return token


data_queue = Queue()

results = {}
results_lock = threading.Lock()


def infinite_loop():
    while True:
        try:
            if not data_queue.empty():
                # Получаем данные из очереди
                task_id, data, future = data_queue.get_nowait()

                print(f"Обрабатываю данные для task {task_id}: {data}")

                # Выполняем обработку
                result = get_ai_answer(data)

                # Устанавливаем результат в Future
                future.set_result(result)

                # Помечаем задачу как выполненную
                data_queue.task_done()

            else:
                time.sleep(0.1)

        except Exception as e:
            print(f"Ошибка в цикле: {e}")
            # Если произошла ошибка, устанавливаем исключение
            with results_lock:
                if task_id in results:
                    results[task_id].set_exception(e)
            time.sleep(1)
