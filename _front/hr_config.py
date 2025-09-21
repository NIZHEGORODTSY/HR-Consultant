# config.py

DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '1234',
    'host': '192.168.0.101',
    'port': '5432'
}

CONNECTION_STRING = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
