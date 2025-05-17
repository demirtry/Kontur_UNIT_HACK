import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    conn = psycopg2.connect(
        host="",
        database="",
        user="",
        password="",
        port='',
        cursor_factory=RealDictCursor,
        sslmode=""
    )
    return conn


def update_user_score(user_id, user_score):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Получаем текущий счёт пользователя
        cursor.execute('SELECT score FROM users WHERE user_id = %s', (user_id,))
        result = cursor.fetchone()

        # Обрабатываем результат
        if result:
            current_score = result['score'] if result['score'] is not None else 0
        else:
            print(f"⚠️ Пользователь {user_id} не найден")
            return

        # Обновляем, только если новый счёт больше текущего
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
    except Exception as e:
        print(f"❌ Ошибка при обновлении счёта: {e}")
        conn.rollback()
    finally:
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
    conn.close()


def add_user(user_id, secret_code):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Проверяем, существует ли пользователь
        cursor.execute('SELECT 1 FROM users WHERE user_id = %s', (user_id,))
        if cursor.fetchone():
            print(f"Пользователь {user_id} уже существует")
            return

        # Добавляем пользователя
        cursor.execute(
            'INSERT INTO users (user_id, secret_code, score) VALUES (%s, %s, %s)',
            (user_id, secret_code, 0)
        )
        conn.commit()
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def test_connection():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print("✅ Успешно подключено к PostgreSQL:")


if __name__ == '__main__':
    create_table_users()
    add_user('123', '123')
    add_user('456', '456')
    add_user('789', '789')
    update_user_score('123', 100)
    update_user_score('456', 200)
    update_user_score('789', 300)