import json
from pathlib import Path

ITEMS_FILE = Path('src/game/items.json')


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
    def __init__(self, cell_id, treasure, weight):
        self.cell_id = cell_id
        self.treasure = treasure
        self.weight = weight
        self.status = False

    def change_status(self):
        self.status = not self.status


class Matrix:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.weight_sum = 0
        self.treasure_sum = 0
        self.selected_cells = set()
        self.cells = []

        items = load_items()

        for i in range(size_x * size_y):
            cur_item = items.get(str(i))
            self.cells.append(Cell(i, cur_item['treasure'], cur_item['weight']))

    def get_cell_by_id(self, cell_id):
        return self.cells[cell_id]

    def get_selected_ids(self):
        return tuple(self.selected_cells)


class Game:
    def __init__(self, size_x=5, size_y=5, backpack_size=100):
        self.weight_sum = 0
        self.treasure_sum = 0
        self.matrix = Matrix(size_x, size_y)
        self.best_treasure = 0
        self.backpack_size = backpack_size

    def compare_scores(self):
        self.best_treasure = max(self.best_treasure, self.treasure_sum)

    def process_click(self, cell_id):
        cell = self.matrix.get_cell_by_id(cell_id)

        if cell.status:
            self.weight_sum -= cell.weight
            self.treasure_sum -= cell.treasure
            self.matrix.selected_cells.remove(cell.cell_id)
        else:
            if self.weight_sum + cell.weight > self.backpack_size:
                return False
            self.weight_sum += cell.weight
            self.treasure_sum += cell.treasure
            self.matrix.selected_cells.add(cell.cell_id)

        cell.change_status()
        self.compare_scores()
        return True

    def get_values(self):
        return {
            "backpack_size": self.backpack_size,
            "weight_sum": self.weight_sum,
            "treasure_sum": self.treasure_sum,
            "best_treasure": self.best_treasure,
            "selected_ids": list(self.matrix.get_selected_ids())
        }


if __name__ == "__main__":
    items = load_items()
    print(items)
