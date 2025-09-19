from flask import Flask, request, make_response, g
import jwt
import core_jwt

app = Flask(__name__)


@app.before_request
def jwt_required():
    if request.path not in ['/login', '/reguster']:
        try:
            token = request.cookies['access_token']
            decoded = jwt.decode(token, core_jwt.KEY, algorithms=["HS256"])
            g.uid = decoded['uid']
        except:
            return make_response({}, 401)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data.get('name')
    pwd = data.get('pwd')
    id = core_jwt.verify_user(name, pwd)
    if id != -1:
        resp = make_response({}, 200)
        resp.set_cookie(key='access_token', value=core_jwt.generate_jwt(id), max_age=None)
        return resp
    else:
        return make_response({}, 401)


@app.route('/id', methods=['GET'])
def get_id():
    return make_response(
        {'id': g.uid},
        200
    )


app.run(debug=True, port=5000, host='0.0.0.0')
