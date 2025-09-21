from flask import Flask, request, make_response, g, jsonify
from config import reader
from core import verify_user, generate_jwt, create_recording, get_all_info, data_queue, results, results_lock, infinite_loop
import jwt
from concurrent.futures import Future
import threading
import uuid

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
    id, fullname, is_hr = verify_user(login, pwd)
    if id == -1:
        return make_response({}, 401)
    resp = make_response({}, 200)
    resp.set_cookie(key='access_token', value=generate_jwt(id, fullname, is_hr), max_age=None)
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


@app.route('/get_answer', methods=['GET'])
def generate_prompt():
    data = request.json
    message = data.get('message')
    task_id = str(uuid.uuid4())
    
    future = Future()
    with results_lock:
        results[task_id] = future
    try:
        # Помещаем задачу в очередь
        data_queue.put((task_id, message, future))
        
        # Ждем результат с таймаутом
        result = future.result(timeout=30.0)  # 30 секунд таймаут
        
        # Удаляем Future из словаря
        with results_lock:
            results.pop(task_id, None)
        
        return make_response({
            "answer": result
        }, 200)

    except TimeoutError:
        with results_lock:
            results.pop(task_id, None)
        return {"status": "error", "message": "Processing timeout"}
    
    except Exception as e:
        with results_lock:
            results.pop(task_id, None)
        return {"status": "error", "message": str(e)}


loop_thread = threading.Thread(target=infinite_loop, daemon=True)
loop_thread.start()
app.run(debug=True, port=5000, host='0.0.0.0')
