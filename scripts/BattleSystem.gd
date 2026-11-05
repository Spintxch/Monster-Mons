class_name BattleSystem
extends RefCounted

var player_mon: Dictionary
var enemy_mon: Dictionary
var turn_log: Array = []
var _moves_db: Dictionary = {}
var _type_chart: Dictionary = {}

func _init(_player_mon: Dictionary, _enemy_mon: Dictionary):
    player_mon = _player_mon
    enemy_mon = _enemy_mon
    _load_data()

func _load_data():
    # Load moves and convert array to dictionary mapping names to data
    var m_file = FileAccess.open("res://data/moves.json", FileAccess.READ)
    var m_json = JSON.new()
    m_json.parse(m_file.get_as_text())
    for move in m_json.data["moves"]:
        _moves_db[move["name"]] = move
        
    var t_file = FileAccess.open("res://data/type_chart.json", FileAccess.READ)
    var t_json = JSON.new()
    t_json.parse(t_file.get_as_text())
    _type_chart = t_json.data

func get_type_multiplier(move_type: String, defender: Dictionary) -> float:
    var multiplier = 1.0
    
    if _type_chart.has(move_type) and _type_chart[move_type].has(defender["type_main"]):
        multiplier *= _type_chart[move_type][defender["type_main"]]
        
    if defender.has("type_second") and defender["type_second"] != "":
        if _type_chart.has(move_type) and _type_chart[move_type].has(defender["type_second"]):
            multiplier *= _type_chart[move_type][defender["type_second"]]
            
    return multiplier

func attack(attacker: Dictionary, defender: Dictionary, move_name: String):
    if not _moves_db.has(move_name):
        turn_log.append(move_name + " failed!")
        return
        
    var move_data = _moves_db[move_name]
    var multiplier = get_type_multiplier(move_data["type"], defender)
    
    var attacker_name = attacker.get("nickname", attacker["name"])
    
    if multiplier == 0:
        turn_log.append(attacker_name + " used " + move_name + "!")
        turn_log.append("It had no effect!")
        return
        
    var level_factor = (2.0 * attacker["level"] / 5.0) + 2.0
    var stat_ratio = float(attacker["attack"]) / float(defender["defense"])
    var base_damage = ((level_factor * move_data["power"] * stat_ratio) / 50.0 + 2.0) * multiplier
    
    var damage = max(1, int(base_damage))
    defender["hp"] -= damage
    if defender["hp"] < 0:
        defender["hp"] = 0
        
    turn_log.append(attacker_name + " used " + move_name + " for " + str(damage) + " damage!")
    
    if multiplier > 1.0:
        turn_log.append("It's super effective!")
    elif multiplier < 1.0:
        turn_log.append("It's not very effective...")