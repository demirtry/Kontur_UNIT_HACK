from flask import Flask, request, jsonify
import sqlite3
import uuid
import secrets
from db_func import get_db_connection, create_table_users
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Создаем таблицу, если еще нет
create_table_users()

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    name = data.get('name', 'anonymous')

    user_id = str(uuid.uuid4())[:8]
    secret_code = secrets.token_hex(4)

    conn = get_db_connection()
    conn.execute('INSERT INTO users (user_id, secret_code, name, score) VALUES (?, ?, ?, ?)',
                 (user_id, secret_code, name, 0))
    conn.commit()
    conn.close()

    return jsonify({'id': user_id, 'code': secret_code})

@app.route('/api/submit', methods=['POST'])
def api_submit():
    data = request.json
    user_id = data.get('id')
    score = data.get('score', 0)

    if not user_id:
        return jsonify({'error': 'No user id provided'}), 400

    conn = get_db_connection()
    # Обновляем счет, если новый больше текущего
    cur = conn.execute('SELECT score FROM users WHERE user_id = ?', (user_id,))
    row = cur.fetchone()
    if row and score > row[0]:
        conn.execute('UPDATE users SET score = ? WHERE user_id = ?', (score, user_id))
        conn.commit()
    conn.close()

    return jsonify({'status': 'ok'})

@app.route('/api/leaderboard', methods=['GET'])
def api_leaderboard():
    conn = get_db_connection()
    users = conn.execute('SELECT user_id, secret_code, score FROM users ORDER BY score DESC LIMIT 10').fetchall()
    conn.close()
    result = [{'id': row[0], 'code': row[1], 'score': row[2]} for row in users]
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
