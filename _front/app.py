from flask import Flask, request as flask_request, make_response, render_template, g
import requests
import jwt
import core

app = Flask(__name__)


@app.before_request
def check_cookies():
    if flask_request.path != '/' and flask_request.path != '/login' and '/static' not in flask_request.path:
        try:
            token = flask_request.cookies['access_token']
            decoded = jwt.decode(token, 'ashjashjsahjsfbsduifvbifbdhidiufdbsibfiubuidb', algorithms=["HS256"])
            g.uid = decoded['uid']
        except:
            return app.redirect('/login')


@app.route('/')
def dum():
    return app.redirect('/profile')


@app.route('/projects')
def show_projects():
    return render_template('projects.html')


@app.route('/tasks')
def show_tasks():
    return render_template('tasks.html')


@app.route('/calendar')
def show_calendar():
    return render_template('calendar.html')


@app.route('/exit')
def exit():
    return app.redirect('/login')


@app.route('/edit_profile')
def edit_profile():
    return 'here you can edit your profile'


@app.route('/chat')
def show_chat():
    userinfo = core.get_user_info(flask_request.cookies.get('access_token'))
    token = flask_request.cookies['access_token']
    uid, name = core.decode_jwt(token)
    return render_template('chat.html')


@app.route('/profile', methods=['GET'])
def profile_view():
    token = flask_request.cookies['access_token']
    uid, name = core.decode_jwt(token)
    lst = str(name).split()
    shortname = ''
    for word in lst:
        shortname += word[0].capitalize()
    position = 'god'
    department = 'Yandex'
    _data = core.get_user_info(flask_request.cookies.get('access_token'))
    return render_template('profile.html', data=_data, fullname=name, shortname=shortname[:2], position=_data,
                           department=department)


@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    name = flask_request.form['name']
    pwd = flask_request.form['pwd']

    response = requests.post(
        'http://127.0.0.1:5000/login',
        json={
            'login': name,
            'pwd': pwd
        }
    )
    if response.status_code == 401:
        return render_template('login.html', gnev_message='Неверное имя пользователя или пароль!')
    else:
        token = response.cookies['access_token']
        resp = make_response(app.redirect('/profile'))
        resp.set_cookie(key='access_token', value=token, max_age=None)

        uid, fullname = core.decode_jwt(token)
        g.uid = uid
        g.name = fullname

        return resp


app.run(debug=True, port=5001, host='0.0.0.0')
