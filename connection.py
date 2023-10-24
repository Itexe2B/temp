import sqlite3
DATABASE_NAME = 'database'
def connect():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    return conn, cursor

def close(conn):
    conn.close()

def request(request):
    conn, cursor = connect()
    cursor.execute(request)
    conn.commit()
    return_val = cursor.fetchall()
    conn.close()
    return return_val

def request_with_params(request, params):
    conn, cursor = connect()
    cursor.execute(request, params)
    conn.commit()
    return_val = cursor.fetchall()
    conn.close()
    return return_val
