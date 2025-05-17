import psycopg2


def get_db_connection():
    conn = psycopg2.connect(
        host="",
        database="",
        user="",
        password="",
        port="",
        sslmode=""
    )
    return conn


def update_user_score(user_id, user_score):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT score FROM users WHERE user_id = %s', (user_id,))
    result = cursor.fetchone()

    if result:
        current_score = result[0] if result[0] is not None else 0
    else:
        return

    if user_score > current_score:
        cursor.execute(
            '''
            UPDATE users
            SET score = %s
            WHERE user_id = %s
            ''',
            (user_score, user_id)
        )
        conn.commit()
    cursor.close()
    conn.close()


def create_table_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT NOT NULL UNIQUE,
            secret_code TEXT NOT NULL UNIQUE,
            score INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    conn.commit()
    cursor.close()
    conn.close()


def add_user(user_id, secret_code):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT 1 FROM users WHERE user_id = %s', (user_id,))
    if cursor.fetchone():
        print(f"Пользователь {user_id} уже существует")
        return

    cursor.execute(
        'INSERT INTO users (user_id, secret_code, score) VALUES (%s, %s, %s)',
        (user_id, secret_code, 0)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_top_leaders():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT user_id, score
        FROM users
        ORDER BY score DESC
        LIMIT 10
        '''
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    leaders = [{"user_id": row[0], "score": row[1]} for row in rows]
    return leaders


def check_user_exist(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
    user_exists = cursor.fetchone()
    cursor.close()
    conn.close()

    return user_exists


if __name__ == '__main__':
    get_top_leaders()
