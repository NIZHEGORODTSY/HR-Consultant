from flask import Flask, request as flask_request, jsonify, make_response, render_template, g
import requests
import jwt

app = Flask(__name__)


@app.before_request
def check_cookies():
    if flask_request.path not in ['/login', '/reguster']:
        if flask_request.path not in ['/login', '/reguster']:
            try:
                token = flask_request.cookies['access_token']
                decoded = jwt.decode(token, 'ashjashjsahjsfbsduifvbifbdhidiufdbsibfiubuidb', algorithms=["HS256"])
                g.uid = decoded['uid']
            except:
                return app.redirect('/')


@app.route('/authreq_resource', methods=['GET'])
def f():
    req_cookies = {
        'access_token': flask_request.cookies['access_token']
    }
    response = requests.get('http://127.0.0.1:5000/id', cookies=req_cookies)
    if response.status_code == 401:
        return app.redirect(f'/login')
    return app.redirect(f'/profile')


@app.route('/', methods=['GET'])
def login_view():
    return render_template('login.html', gnev_message='')


@app.route('/profile', methods=['GET'])
def profile_view():
    token = flask_request.cookies.get('acess_token')
    fullname = '0'
    shortname = '1'
    position = 'god'
    department = 'Yandex'
    return render_template('profile.html', fullname=fullname, shortname=shortname, position=position, department=department)


@app.route('/login', methods=['POST'])
def login_post():
    name = flask_request.form['name']
    pwd = flask_request.form['pwd']

    response = requests.post(
        'http://127.0.0.1:5000/login',
        json={
            'name': name,
            'pwd': pwd
        }
    )

    if response.status_code == 401:
        return render_template('login.html', gnev_message='Неверное имя пользователя или пароль!')
    else:
        token = response.cookies['access_token']
        resp = make_response(app.redirect('/authreq_resource'))
        resp.set_cookie(key='access_token', value=token, max_age=None)
        return resp


app.run(debug=True, port=5001, host='0.0.0.0')
