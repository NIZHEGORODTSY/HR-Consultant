import psycopg2
from functools import wraps
from config import reader

reader.read_config()

class DBContext:
    
    def __init__(self):
        pass

    def __call__(self, dbfunc):
        @wraps(dbfunc)
        def wrapper(*args, **kwargs):
            conn = psycopg2.connect(
                #dbname=reader.get_param_value('dbname'),
                user=reader.get_param_value('dbuser'),
                password=reader.get_param_value('dbpwd'),
                host=reader.get_param_value('dbhost'),
                port=reader.get_param_value('dbport')
            )
            cursor = conn.cursor()
            kwargs['cursor'] = cursor
            res = dbfunc(*args, **kwargs)
            conn.commit()
            conn.close()
            return res
        return wrapper
