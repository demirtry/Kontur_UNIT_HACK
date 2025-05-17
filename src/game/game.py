import json
from pathlib import Path


# ITEMS_FILE = Path('items.json')
ITEMS_FILE = Path(__file__).parent / 'items.json'

def load_items():
    if not ITEMS_FILE.exists():
        print("not exist")
        return {}

    with open(ITEMS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_items(data):
    with open(ITEMS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


class Cell:
    def __init__(self, id, treasure, weight):
        self.id = id
        self.treasure = treasure
        self.weight = weight
        self.status = False

    def change_status(self):
        if self.status:
            pass
        else:
            pass


class Matrix:
    def __init__(self, size_x, size_y):
        print("alive")
        self.size_x = size_x
        self.size_y = size_y
        self.weight_sum = 0
        self.treasure_sum = 0
        self.selected_cells = set()

        self.cells = []
        items = load_items()
        print(items, "items")
        item_id = 0
        for j in range(size_y):
            current_cell = []
            for i in range(size_x):
                current_item = items.get(str(item_id))
                print(current_item, "cur_item")
                item_treasure, item_weight = current_item["treasure"], current_item["weight"]
                current_cell.append(Cell(item_id, item_treasure, item_weight))

                item_id += 1

            self.cells.append(current_cell)

    def update_values(self, cell_id):
        current_cell = self.cells[cell_id // self.size_y][cell_id % self.size_x]
        if current_cell.status:
            self.weight_sum -= current_cell.weight
            self.treasure_sum -= current_cell.treasure
            self.selected_cells.remove(current_cell.id)
        else:
            self.weight_sum += current_cell.weight
            self.treasure_sum += current_cell.treasure
            self.selected_cells.add(current_cell.id)

        current_cell.change_status()

    def get_selected_ids(self):
        return tuple(self.selected_cells)



class Game:
    def __init__(self, size_x=5, size_y=5, backpack_size=100):
        self.matrix = Matrix(size_x, size_y)
        self.best_treasure = 0
        self.backpack_size = backpack_size

    def compare_scores(self):
        self.best_treasure = max(self.best_treasure, self.matrix.treasure_sum)

    def process_click(self, cell_id):
        self.matrix.update_values(cell_id)
        self.compare_scores()


# Подумать как обрабатывать если объект не влезает в рюкзак
# реализовать Cell.change_status



if __name__ == "__main__":
    items = load_items()
    print(items)
    # game = Game()
    # values = {
    #     "backpack_size": game.backpack_size,
    #     "treasure_sum": game.matrix.treasure_sum,
    #     "best_treasure": game.best_treasure,
    #     "selected_ids": game.matrix.get_selected_ids()
    # }
    # print(values)
