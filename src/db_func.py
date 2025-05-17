import sqlite3


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_table_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
        user_id TEXT NOT NULL UNIQUE,
        secret_code TEXT NOT NULL UNIQUE,
        score INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    conn.commit()
    conn.close()


def add_user(user_id, secret_code):
    conn = get_db_connection()
    conn.execute('INSERT INTO users (user_id, secret_code, score) VALUES (?, ?, ?)',
                 (user_id, secret_code, 0))
    conn.commit()
    conn.close()


def update_user_score(user_id, user_score):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT score FROM users WHERE user_id = ?', (user_id,))
    current_score = cursor.fetchone()[0] or 0

    if user_score > current_score:
        cursor.execute(
            '''
            UPDATE users
            SET score = ?
            WHERE user_id = ?
            ''', (user_score, user_id))

    conn.commit()
    conn.close()


# def update_user_score(user_id, user_score):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     cursor.execute(
#         '''
#         UPDATE users
#         SET score = ?
#         WHERE user_id = ?
#         ''', (user_score, user_id))
#
#     conn.commit()
#     conn.close()


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
    conn.close()
    leaders = [{"user_id": row[0], "score": row[1]} for row in rows]
    return leaders


def get_all_users_by_score():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_id, score
        FROM users
        ORDER BY score DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_place_by_user_id(user_id, all_users):
    for place, (uid, _) in enumerate(all_users, start=1):
        if uid == user_id:
            return place
    return None


def get_place_in_top(user_id, leaders):
    if user_id in leaders.keys():
        pass


if __name__ == "__main__":
    create_table_users()
