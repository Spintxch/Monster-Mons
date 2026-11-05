# Main file for a battling monster game like pokemon
import json
from pathlib import Path
from mon_generator import MonInfo

# Constants
DATA_DIR = Path(__file__).parent / "data"
SAVE_FILE = DATA_DIR / "player_info.json"
MONS_FILE = DATA_DIR / "mons.json"

class GameState:
    def __init__(self):
        
        with SAVE_FILE.open(encoding="utf-8") as file:
            self.player = json.load(file)

        with MONS_FILE.open(encoding="utf-8") as file:
            self.mons_data = json.load(file)

        self.badge_list = [
            "badge_1", "badge_2", "badge_3", "badge_4",
            "badge_5", "badge_6", "badge_7", "badge_8"
        ]

    # Highest level funcs
    def save_change(self):
        with SAVE_FILE.open("w", encoding="utf-8") as file:
            json.dump(self.player, file, indent=4)

    def save_mons(self):
        with MONS_FILE.open("w", encoding="utf-8") as file:
            json.dump(self.mons_data, file, indent=4)

    def perform_action(self, action, *args):
        result = action(*args)
        self.save_change()
        return result

    # Checks
    def has_room_for_mon(self):
        return len(self.player["mons"]) < 6

    def visit_area(self, area):
        if area not in self.player["areas_visited"]:
            raise ValueError(f"Unknown area: {area}")

        if self.player ["areas_visited"][area]:
            return False

        self.player["areas_visited"][area] = True
        return True

    def get_mon_info(self, mon_name, level=1, xp=0, hp=10, moves=()):
        if mon_name not in self.mons_data or not self.mons_data[mon_name]:
            raise ValueError(f"Unknown mon: {mon_name}")

        data = self.mons_data[mon_name]
        mon = MonInfo(
            mon_name,
            data["type_main"],
            data.get("type_second"),
            level,
            xp,
            hp,
        )

        for move in moves:
            if not mon.learn_move(move):
                raise ValueError(f"Invalid or duplicate move {move!r} for {mon_name}")

        return mon

    # Default add funcs
    def add_item(self, item_name, amount=1):
        if item_name not in self.player["inventory"]:
            self.player["inventory"][item_name] = 0
        self.player["inventory"][item_name] += amount

    def consume_item(self, item_name):
        if self.player["inventory"].get(item_name, 0) > 0:
            self.player["inventory"][item_name] -= 1
            return True
        return False

    def use_potion(self, mon_index):
        if self.consume_item("potion"):
            mon = self.player["mons"][mon_index]
            mon["hp"] = min(mon["hp"] + 20, mon["max_hp"])
            self.save_change()
            return True
        return False

    def add_money(self, amount):
        self.player["money"] += amount

    def add_badge(self, badge):
        if badge not in self.player["badges"]:
            self.player["badges"].append(badge)

    def add_mon(self, mon):
        if not self.has_room_for_mon():
            return False

        if mon.name not in self.mons_data or not self.mons_data[mon.name]:
            raise ValueError(f"Unknown mon: {mon.name}")

        mon_record = self.mons_data[mon.name][0]
        if mon_record.get("player_viewed") != "caught":
            mon_record["player_viewed"] = "caught"
            self.save_mons()
        
        self.player["mons"].append(mon.to_dict())
        return True

    # User choices
    def change_name(self, name):
        self.player["name"] = name
        return True

game = GameState()

if __name__ == "__main__":
    new_mon = MonInfo("Pica", "normal", "water", 1, 100, 10)
    game.perform_action(game.add_mon, new_mon)