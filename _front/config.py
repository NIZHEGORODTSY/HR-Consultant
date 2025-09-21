# config.py

DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '1234',
    'host': 'zpjoo-5-227-24-17.a.free.pinggy.link',
    'port': '42219'
}

CONNECTION_STRING = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
