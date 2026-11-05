# Main file for a battling monster game like pokemon
import json
from pathlib import Path
from mon_generator import MonInfo

# Constants
SAVE_FILE = Path(__file__).parent / "player_info.json"
MONS_FILE = Path(__file__).parent / "mons.json"

with SAVE_FILE.open(encoding="utf-8") as file:
    player = json.load(file)

with MONS_FILE.open(encoding="utf-8") as file:
    mons_data = json.load(file)

BADGE_LIST = ["badge_1", "badge_2", "badge_3", "badge_4",
              "badge_5", "badge_6", "badge_7", "badge_8"
              ]

# Highest level funcs
def save_change():
    with SAVE_FILE.open("w", encoding="utf-8") as file:
        json.dump(player, file, indent=4)

def save_mons():
    with MONS_FILE.open("w", encoding="utf-8") as file:
        json.dump(mons_data, file, indent=4)

def perform_action(action, *args):
    result = action(*args)
    save_change()
    return result

# Checks
def has_room_for_mon():
    return len(player["mons"]) < 6

def visit_area(area):
    if area not in player["areas_visited"]:
        raise ValueError(f"Unknown area: {area}")

    if player ["areas_visited"][area]:
        return False

    player["areas_visited"][area] = True
    return True

def get_mon_info(mon_name, level=1, xp=0, hp=10, moves=()):
    if mon_name not in mons_data or not mons_data[mon_name]:
        raise ValueError(f"Unknown mon: {mon_name}")

    data = mons_data[mon_name][0]
    mon = MonInfo(
        mon_name,
        data["type_main"],
        data["type_second"],
        level,
        xp,
        hp,
    )

    for move in moves:
        if not mon.learn_move(move):
            raise ValueError(f"Invalid or duplicate move {move!r} for {mon_name}")

    return mon

# Default add funcs
def add_money(amount):
    player["money"] += amount

def add_badge(badge):
    if badge not in player["badges"]:
        player["badges"].append(badge)

def add_mon(mon):
    if not has_room_for_mon():
        return False

    if mon.name not in mons_data or not mons_data[mon.name]:
        raise ValueError(f"Unknown mon: {mon.name}")

    mon_record = mons_data[mon.name][0]
    if mon_record.get("player_viewed") != "caught":
        mon_record["player_viewed"] = "caught"
        save_mons()
    
    player["mons"].append({
        "name": mon.name,
        "type_main": mon.type_main,
        "type_second": mon.type_second,
        "moves": mon.moves.copy(),
        "level": mon.level,
        "xp": mon.xp,
        "hp": mon.hp
    })

    return True

# User choices
def change_name(name):
    player["name"] = name
    return True


if __name__ == "__main__":
    new_mon = MonInfo("Pica", "normal", "water", 1, 100)
    perform_action(add_mon, new_mon)