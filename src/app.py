import json
import secrets

from flask import Flask, render_template, request, session, make_response, jsonify

from .db_postgres_funcs import create_table_users, add_user, update_user_score, get_top_leaders, check_user_exist
from .game.game import Game

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

create_table_users()

games = {}
secret_codes = set()
user_ids = set()


@app.route('/')
def index():
    return render_template('index.html')


def get_user_id_this_session():
    return session.get("user_id")


def load_game(user_id):
    if user_id not in games:
        games[user_id] = Game()
    return games[user_id]


@app.route('/register', methods=['GET', 'POST'])
def register():
    user_id = request.cookies.get('user_id')

    if request.method == 'POST':
        if user_id:
            secret_code = secrets.token_hex(4)
            while secret_code in secret_codes:
                secret_code = secrets.token_hex(4)
            secret_codes.add(secret_code)

            user_exists = check_user_exist(user_id)
            if not user_exists:
                add_user(user_id, secret_code)
        else:
            secret_code = secrets.token_hex(4)
            while secret_code in secret_codes:
                secret_code = secrets.token_hex(4)
            secret_codes.add(secret_code)

            user_id = secrets.token_hex(4)
            while user_id in user_ids:
                user_id = secrets.token_hex(4)
            user_ids.add(user_id)

            add_user(user_id, secret_code)

        session["user_id"] = user_id
        response = make_response(render_template('registration_success.html',
                                                 user_id=user_id,
                                                 secret_code=secret_code))
        response.set_cookie('user_id', user_id, max_age=24*60*60)
        return response

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


@app.route('/intro1')
def go_to_intro1():
    return render_template('intro_pages/intro1.html')


@app.route('/intro2')
def go_to_intro2():
    return render_template('intro_pages/intro2.html')


@app.route('/intro3')
def go_to_intro3():
    return render_template('intro_pages/intro3.html')


@app.route('/game')
def start_game():
    user_id = get_user_id_this_session()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    game = load_game(user_id)
    game_state = game.get_values()

    return render_template('game.html',
                           backpack_size=game_state['backpack_size'],
                           weight_sum=game_state['weight_sum'],
                           treasure_sum=game_state['treasure_sum'],
                           best_treasure=game_state['best_treasure'],
                           selected_ids=game_state['selected_ids'])


@app.route('/api/get_items')
def get_items():
    try:
        with open('src/game/items.json', 'r', encoding='utf-8') as f:
            items_data = json.load(f)
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


# if __name__ == '__main__':
#     create_table_users()
#     app.run(debug=True)
