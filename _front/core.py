import jwt
import requests


def decode_jwt(token: str) -> tuple[int, str]:
    decoded = jwt.decode(token, 'ashjashjsahjsfbsduifvbifbdhidiufdbsibfiubuidb', algorithms='HS256')
    return decoded['uid'], decoded['name'], decoded['is_hr']


def get_user_info(token: str):
    response = requests.get(
        'http://127.0.0.1:5000/info',
        cookies={
            'access_token': token
        }
    )
    return response.json()
