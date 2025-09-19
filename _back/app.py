from flask import Flask, request, make_response, g
from _back.config import reader
from core import verify_user, generate_jwt, create_recording
import jwt

reader.read_config()

app = Flask(__name__)

@app.before_request
def jwt_required():
    if request.path not in ['/login', '/reguster']:
        try:
            token = request.cookies['access_token']
            decoded = jwt.decode(token, reader.get_param_value("jwt-key"), algorithms=["HS256"])
            g.uid = decoded['uid']
        except:
            return make_response({}, 401)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    login = data.get('login')
    pwd = data.get('pwd')
    id = verify_user(login, pwd)
    if id == -1:
        return make_response({}, 401)
    resp = make_response({}, 200)
    resp.set_cookie(key='access_token', value=generate_jwt(id), max_age=None)
    return resp

@app.route('/create', methods=['POST'])
def create():
    # {
    #     "category": 0
    # }
    data = request.json
    category = data.get('category')
    create_recording(category, g.uid)
    return make_response({}, 200)

    