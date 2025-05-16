from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import uuid
import secrets

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = str(uuid.uuid4())[:8]
        secret_code = secrets.token_hex(4)

        conn = get_db_connection()
        conn.execute('INSERT INTO users (user_id, secret_code) VALUES (?, ?)',
                     (user_id, secret_code))
        conn.commit()
        conn.close()

        return render_template('registration_success.html', user_id=user_id, secret_code=secret_code)
    return render_template('register.html')

@app.route('/leaderboard')
def leaderboard():
    conn = get_db_connection()
    users = conn.execute('SELECT user_id, score FROM users ORDER BY score DESC').fetchall()
    conn.close()
    return render_template('leaderboard.html', users=users)

@app.route('/intro/<int:step>')
def intro(step):
    try:
        return render_template(f'intro_pages/step{step}.html', step=step)
    except:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
