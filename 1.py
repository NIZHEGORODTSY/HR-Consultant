import psycopg2

conn = psycopg2.connect(
    dbname='main',
    user='postgres',
    password='1234',
    host='192.168.0.101',
    port='5432'
)

cursor = conn.cursor()

query = f"""SELECT * FROM users"""
cursor.execute(query)

res = cursor.fetchall()

print(res)

conn.close()
