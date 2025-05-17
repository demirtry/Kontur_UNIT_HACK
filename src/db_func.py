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

    cursor.execute(
        '''
            UPDATE users
            SET score = ?
            WHERE user_id = ?
        ''', (user_score, user_id))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table_users()
