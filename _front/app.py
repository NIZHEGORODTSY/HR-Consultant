from flask import Flask, request as flask_request, make_response, render_template, g
import requests
import jwt
import core
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dashboard_app import create_dash_app

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


@app.route('/profile/dashboard')
def show_dash():
    return 'дашборд'


@app.route('/profile/progress')
def show_progress():
    token = flask_request.cookies['access_token']
    uid, name, is_hr = core.decode_jwt(token)
    lst = str(name).split()
    shortname = ''
    for word in lst:
        shortname += word[0].capitalize()
    return render_template('progress.html', fullname=name, shortname=shortname)


@app.route('/exit')
def exit():
    return app.redirect('/login')


@app.route('/profile/edit_profile')
def edit_profile():
    return 'here you can edit your profile'


@app.route('/profile/chat')
def show_chat():
    userinfo = core.get_user_info(flask_request.cookies.get('access_token'))
    token = flask_request.cookies['access_token']
    uid, name, is_hr = core.decode_jwt(token)
    shortname = ''
    lst = str(name).split()
    for word in lst:
        shortname += word[0].capitalize()
    return render_template('chat.html', fullname=name, shortname=shortname[:2])


@app.route('/profile', methods=['GET'])
def profile_view():
    token = flask_request.cookies['access_token']
    uid, name, is_hr = core.decode_jwt(token)
    lst = str(name).split()
    shortname = ''
    for word in lst:
        shortname += word[0].capitalize()
    # _data = core.get_user_info(flask_request.cookies.get('access_token'))
    return render_template('profile.html', fullname=name, shortname=shortname[:2])


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
        uid, fullname, is_hr = core.decode_jwt(token)
        g.uid = uid
        g.name = fullname
        g.is_hr = is_hr
        if is_hr == 0:
            resp = make_response(app.redirect('/profile'))
        else:
            resp = make_response(app.redirect('/admin'))
        resp.set_cookie(key='access_token', value=token, max_age=None)
        return resp


@app.route('/admin')
def show_hr_panel():
    token = flask_request.cookies['access_token']
    uid, name, is_hr = core.decode_jwt(token)
    lst = str(name).split()
    shortname = ''
    for word in lst:
        shortname += word[0].capitalize()

    return render_template('admin.html', fullname=name, shortname=shortname[:2])


@app.route('/admin/dashboard')
def show_hr_dashboard():
    token = flask_request.cookies['access_token']
    uid, name, is_hr = core.decode_jwt(token)
    shortname = ''
    lst = str(name).split()
    for word in lst:
        shortname += word[0].capitalize()
    return render_template('dashboard_hr.html', fullname=name)


@app.route('/admin/search')
def show_hr_search():
    return 'поиск'


@app.route('/admin/employee')
def show_hr_employee():
    return 'employee'


dash_app = create_dash_app(app)

# Настраиваем middleware для обработки Dash маршрутов
application = DispatcherMiddleware(app, {
    '/dash': dash_app.server
})

app.run(debug=True, port=5001, host='0.0.0.0')
