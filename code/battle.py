import json
from pathlib import Path

with (Path(__file__).parent / "data" / "moves.json").open(encoding="utf-8") as file:
    MOVES = {move["name"]: move for move in json.load(file)["moves"]}

with (Path(__file__).parent / "data" / "type_chart.json").open(encoding="utf-8") as file:
    TYPE_CHART = json.load(file)

class BattleSystem:
    def __init__(self, player_mon, enemy_mon):
        self.player_mon = player_mon
        self.enemy_mon = enemy_mon
        self.turn_log = []

    def get_type_multiplier(self, move_type, defender):
        multipler = 1.0

        if move_type in TYPE_CHART and defender["type_main"] in TYPE_CHART[move_type]:
            multipler *= TYPE_CHART[move_type][defender["type_main"]]

        if defender.get("type_second"):
            if move_type in TYPE_CHART and defender["type_second"] in TYPE_CHART[move_type]:
                multiplier *= TYPE_CHART[move_type][defender["type_second"]]

        return multipler

    def attack(self, attacker, defender, move_name):
        if move_name not in MOVES:
            self.turn_log.append(f"{move_name} failed!")
            return

        move_data = MOVES[move_name]

        multiplier = self.get_type_multiplier(move_data["type"], defender)
        if multiplier == 0:
            self.turn_log.append(f"{attacker.get('nickname', attacker['name'])} used {move_name}!")
            self.turn_log.append("It had no effect!")
            return

        level_factor = (2 * attacker["level"] / 5) + 2
        stat_ratio = attacker["attack"] / defender["defense"]
        base_damage = ((level_factor * move_data["power"] * stat_ratio) / 50 + 2) * multiplier

        damage = max(1, int(base_damage))

        defender["hp"] -= damage
        if defender["hp"] < 0:
            defender["hp"] = 0

        name = attacker.get("nickname", attacker["name"])
        self.turn_log.append(f"{attacker['name']} used {move_name} for {damage} damage!")

        if multiplier > 1.0:
            self.turn_log.append("It's super effective!")
        elif multiplier < 1.0:
            self.turn_log.append("It's not very effective...")

    def check_winner(self):
        if self.player_mon["hp"] <= 0:
            return "enemy"
        if self.enemy_mon["hp"] <= 0:
            return "player"
        return None