from flask import Flask, render_template, request, redirect, url_for, session
from db_func import get_db_connection, create_table_users
from game.game import Game
import uuid
import secrets

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def load_game():
    if 'game_data' not in session:
        session['game_data'] = {
            "selected_cells": [],
            "current_weight": 0,
            "current_value": 0,
            "has_played": False
        }
    data = session['game_data']
    game = Game(GLOBAL_MATRIX)
    game.selected_cells = data["selected_cells"]
    game.current_weight = data["current_weight"]
    game.current_value = data["current_value"]
    game.has_played = data["has_played"]
    return game


# Добавить возврат на фронт id пользователя и кодового слова. Убрать возврат страниц
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = str(uuid.uuid4())[:8]
        secret_code = secrets.token_hex(4)

        create_table_users()
        conn = get_db_connection()
        conn.execute('INSERT INTO users (user_id, secret_code) VALUES (?, ?)',
                     (user_id, secret_code))
        conn.commit()
        conn.close()

        return render_template('registration_success.html', user_id=user_id, secret_code=secret_code)
    return render_template('register.html')


@app.route('/api/select-cell', methods=['POST'])
def select_cell():
    public_id = session.get('public_id')
    if not public_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    cell_index = data.get('index')
    weight = data.get('weight')
    value = data.get('value')

    selected_cells = session.get('selected_cells', [])
    current_weight = session.get('current_weight', 0)
    current_value = session.get('current_value', 0)

    if cell_index in selected_cells:
        return jsonify({
            "selected_cells": selected_cells,
            "current_weight": current_weight,
            "current_value": current_value
        })

    new_weight = current_weight + weight
    if new_weight > GLOBAL_MAX_WEIGHT:
        return jsonify({"error": "Превышен максимальный вес"}), 400

    selected_cells.append(cell_index)
    current_weight += weight
    current_value += value

    session['selected_cells'] = selected_cells
    session['current_weight'] = current_weight
    session['current_value'] = current_value

    return jsonify({
        "selected_cells": selected_cells,
        "current_weight": current_weight,
        "current_value": current_value
    })


@app.route('/api/finish', methods=['POST'])
def finish():
    public_id = session.get('public_id')
    if not public_id:
        return jsonify({"error": "Unauthorized"}), 401

    final_value = session.get('current_value', 0)

    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE users SET score = ?, has_played = 1 WHERE public_id = ?",
                (final_value, public_id))
    db.commit()
    db.close()

    return jsonify({"success": True})


@app.route('/game-data')
def game_data():
    if 'public_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    public_id = session['public_id']
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT selected_cells, current_weight, current_value
        FROM users
        WHERE public_id = ?
    """, (public_id,))
    result = cur.fetchone()
    db.close()

    if not result:
        return jsonify({"error": "Data not found"}), 404

    return jsonify({
        "matrix": GLOBAL_MATRIX,
        "max_weight": GLOBAL_MAX_WEIGHT,
        "selected_cells": json.loads(result[0]),
        "current_weight": result[1],
        "current_value": result[2]
    })


@app.route('/game')
def game():
    if 'public_id' not in session:
        return redirect(url_for('index'))

    if session.get('has_played', False):
        return "Вы уже прошли игру."

    if 'selected_cells' not in session:
        session['selected_cells'] = []
        session['current_weight'] = 0
        session['current_value'] = 0

    selected_cells = session['selected_cells']
    current_weight = session['current_weight']
    current_value = session['current_value']

    return render_template('game_vue.html',
                           matrix=GLOBAL_MATRIX,
                           max_weight=GLOBAL_MAX_WEIGHT,
                           selected_cells=json.dumps(selected_cells),
                           current_weight=current_weight,
                           current_value=current_value)


if __name__ == '__main__':
    app.run(debug=True)
