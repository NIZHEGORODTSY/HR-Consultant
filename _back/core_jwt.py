import json
import jwt
import datetime

KEY = 'sgbkslgbhfskjlgbhjk'


def verify_user(uname: str, pwd: str) -> int:
    """
    Проверяет наличие пользователя в базе данных и возвращает его id  
    Если пользователь не найден, возвращает -1
    """
    with open('JWT-Auth/_back/data.json', 'r') as f:
        data = json.load(f)
    res = -1
    for user in data['users']:
        if user['name'] == uname and user['pwd'] == pwd:
            res = user['id']
            break
    return res


def add_user(uname: str, pwd: str) -> int:
    with open('JWT-Auth/_back/data.json', 'r') as f:
        data = json.load(f)

    max_id = 0
    for user in data['users']:
        if user['name'] == uname:
            return -1
        if user['id'] > max_id:
            max_id = user['id']
    data['users'].append({
        'id': max_id + 1,
        'name': uname,
        'pwd': pwd
    })

    with open('JWT-Auth/_back/data.json', 'w') as f:
        json.dump(data, f)
    return max_id + 1


def generate_jwt(id: int) -> str:
    payload = {
        'uid': id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
    }

    token = jwt.encode(payload, KEY, algorithm='HS256')
    return token
