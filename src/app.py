from flask import Flask, render_template, request, redirect, url_for, session
from db_func import get_db_connection, create_table_users, add_user
from game.game import Game
import uuid
import secrets
from flask import jsonify


app = Flask(__name__)
app.secret_key = "AAAAAAAAAA"
secret_codes = set()
user_ids = set()

games = dict()

@app.route('/')
def index():
    return render_template('index.html')


def get_user_id_this_session():
    user_id = session["user_id"]
    return user_id

def load_game(user_id):
    if games.get(user_id) is None:
        games[user_id] = Game()

    return games[user_id]

# Добавить возврат на фронт id пользователя и кодового слова. Убрать возврат страниц
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        secret_code = secrets.token_hex(4)
        while secret_code in secret_codes:
            secret_code = secrets.token_hex(4)
        secret_codes.add(secret_code)

        user_id = secrets.token_hex(4)
        while user_id in user_ids:
            user_id = secrets.token_hex(4)
        user_ids.add(user_id)

        create_table_users()
        add_user(user_id, secret_code)
        session["user_id"] = user_id
        print(session)

        return render_template('registration_success.html', user_id=user_id, secret_code=secret_code)
    return render_template('register.html')


# @app.route('/api/select-cell', methods=['POST'])
# def select_cell():
#     public_id = session.get('public_id')
#     if not public_id:
#         return jsonify({"error": "Unauthorized"}), 401
#
#     data = request.get_json()
#     cell_index = data.get('index')
#     weight = data.get('weight')
#     value = data.get('value')
#
#     selected_cells = session.get('selected_cells', [])
#     current_weight = session.get('current_weight', 0)
#     current_value = session.get('current_value', 0)
#
#     if cell_index in selected_cells:
#         return jsonify({
#             "selected_cells": selected_cells,
#             "current_weight": current_weight,
#             "current_value": current_value
#         })
#
#     new_weight = current_weight + weight
#     if new_weight > GLOBAL_MAX_WEIGHT:
#         return jsonify({"error": "Превышен максимальный вес"}), 400
#
#     selected_cells.append(cell_index)
#     current_weight += weight
#     current_value += value
#
#     session['selected_cells'] = selected_cells
#     session['current_weight'] = current_weight
#     session['current_value'] = current_value
#
#     return jsonify({
#         "selected_cells": selected_cells,
#         "current_weight": current_weight,
#         "current_value": current_value
#     })
#
#
# @app.route('/api/finish', methods=['POST'])
# def finish():
#     public_id = session.get('public_id')
#     if not public_id:
#         return jsonify({"error": "Unauthorized"}), 401
#
#     final_value = session.get('current_value', 0)
#
#     db = get_db()
#     cur = db.cursor()
#     cur.execute("UPDATE users SET score = ?, has_played = 1 WHERE public_id = ?",
#                 (final_value, public_id))
#     db.commit()
#     db.close()
#
#     return jsonify({"success": True})
#
#
# @app.route('/game-data')
# def game_data():
#     if 'public_id' not in session:
#         return jsonify({"error": "Unauthorized"}), 401
#
#     public_id = session['public_id']
#     db = get_db()
#     cur = db.cursor()
#     cur.execute("""
#         SELECT selected_cells, current_weight, current_value
#         FROM users
#         WHERE public_id = ?
#     """, (public_id,))
#     result = cur.fetchone()
#     db.close()
#
#     if not result:
#         return jsonify({"error": "Data not found"}), 404
#
#     return jsonify({
#         "matrix": GLOBAL_MATRIX,
#         "max_weight": GLOBAL_MAX_WEIGHT,
#         "selected_cells": json.loads(result[0]),
#         "current_weight": result[1],
#         "current_value": result[2]
#     })


@app.route('/start_game')
def start_game():
    user_id = get_user_id_this_session()
    game = load_game(user_id)
    """
    текущий скор, индексы ячеек которые выбраны, размер рюкзака, максимальный результат
    """

    values = {
        "backpack_size": game.backpack_size,
        "treasure_sum": game.matrix.treasure_sum,
        "best_treasure": game.best_treasure,
        "selected_ids": game.matrix.get_selected_ids()
    }
    print("отработало")
    return jsonify(values)

    # return render_template('game_vue.html',
    #                        matrix=game.matrix,
    #                        max_weight=game.backpack_size,
    #                        selected_cells=json.dumps(selected_cells),
    #                        current_weight=current_weight,
    #                        current_value=current_value)


if __name__ == '__main__':
    app.run(debug=True)
