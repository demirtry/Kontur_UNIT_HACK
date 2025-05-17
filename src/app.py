import json

from flask import Flask, render_template, request, session
from db_func import create_table_users, add_user, update_user_score, get_top_leaders
from game.game import Game
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


@app.route('/api/process_click/<int:cell_id>', methods=['POST'])
def process_click(cell_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    game = load_game(user_id)

    weight_is_lower = game.process_click(cell_id)

    values = game.get_values()
    values['weight_is_lower'] = weight_is_lower

    return jsonify(values)


@app.route('/game')
def start_game():
    user_id = get_user_id_this_session()
    game = load_game(user_id)
    game_state = game.get_values()

    return render_template('game.html',
                           backpack_size=game_state['backpack_size'],
                           weight_sum=game_state['weight_sum'],  # Изменил initial_weight на weight_sum
                           treasure_sum=game_state['treasure_sum'],  # Изменил initial_treasure на treasure_sum
                           best_treasure=game_state['best_treasure'],
                           selected_ids=game_state['selected_ids'])

@app.route('/api/get_items')
def get_items():
    try:
        with open('game/items.json', 'r', encoding='utf-8') as f:
            items_data = json.load(f)

        # Преобразуем объект в массив
        items_array = [items_data[str(i)] for i in range(len(items_data))]
        return jsonify(items_array)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/game_end', methods=['POST'])
def game_end():
    user_id = request.json.get("user_id") or session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    best_from_client = request.json.get("best_treasure")
    if best_from_client is None:
        return jsonify({"error": "No score provided"}), 400

    update_user_score(user_id, best_from_client)

    return jsonify({
        "message": "Игра завершена",
        "saved_score": best_from_client
    })


@app.route("/leaderboard")
def leaderboard():
    leaders = get_top_leaders()
    return render_template("leaderboard.html",
                         title="Таблица лидеров",
                         leaders=leaders)


if __name__ == '__main__':
    app.run(debug=True)
