from flask import Flask, request, make_response, g, jsonify
from config import reader
from core import verify_user, generate_jwt, create_recording, get_all_info
import jwt

reader.read_config()

app = Flask(__name__)


@app.before_request
def jwt_required():
    if request.path not in ['/login']:
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
    id, fullname = verify_user(login, pwd)
    if id == -1:
        return make_response({}, 401)
    resp = make_response({}, 200)
    resp.set_cookie(key='access_token', value=generate_jwt(id, fullname), max_age=None)
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


@app.route('/info', methods=['GET'])
def get_user_info():
    id = g.uid
    res = get_all_info(id)
    return make_response(jsonify(res), 200)


# @app.route('/generate_prompt', methods=['GET'])
# def generate_prompt():
#     name = 'Вася' #временно
#     prompt = get_final_prompt(name)
#     return make_response(jsonify(prompt), 200)


app.run(debug=True, port=5000, host='0.0.0.0')
