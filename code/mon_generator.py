# Generates mons based on given info
import json
from pathlib import Path

with (Path(__file__).parent / "moves.json").open(encoding="utf-8") as file:
    MOVES = json.load(file)["moves"]

class MonInfo:
    def __init__(self, name, type_main, type_second, level, xp, hp):
        self.name = name
        self.type_main = type_main
        self.type_second = type_second
        self.moves = []
        self.level = level
        self.xp = xp
        self.hp = hp

    def valid_moves(self):
        self.valid_move_list = [
            move for move in MOVES
            if move["type"] in (self.type_main, self.type_second)
        ]

        return self.valid_move_list

    def learn_move(self, move_name):
        if move_name in self.moves or len(self.moves) >= 4:
            return False

        valid_names = {move["name"] for move in self.valid_moves()}
        if move_name not in valid_names:
            return False

        self.moves.append(move_name)
        return True


if __name__ == "__main__":
    mon_info = MonInfo("Pica", "normal", "water", 1, 100, 4)

    print(mon_info.valid_moves())

    moves_by_name = {move["name"]: move for move in mon_info.valid_move_list}

    print(moves_by_name["Headbutt"])