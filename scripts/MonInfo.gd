class_name MonInfo
extends RefCounted

var name: String
var nickname: String
var type_main: String
var type_second: String # Can be empty string "" instead of null
var moves: Array = []
var level: int
var xp: int
var max_hp: int
var hp: int
var attack: int
var defense: int

var _moves_database: Array

func _init(_name: String, _type_main: String, _type_second: String = "", _level: int = 1, _xp: int = 0, _hp: int = 10, _attack: int = 10, _defense: int = 10, _nickname: String = ""):
    name = _name
    nickname = _nickname if _nickname != "" else name
    type_main = _type_main
    type_second = _type_second
    level = _level
    xp = _xp
    max_hp = _hp
    hp = _hp
    attack = _attack
    defense = _defense
    
    _load_moves_db()

func _load_moves_db():
    var file = FileAccess.open("res://data/moves.json", FileAccess.READ)
    if file:
        var json = JSON.new()
        if json.parse(file.get_as_text()) == OK:
            _moves_database = json.data["moves"]

func valid_moves() -> Array:
    var valid_list = []
    var active_types = [type_main]
    if type_second != "":
        active_types.append(type_second)
        
    for move in _moves_database:
        if move["type"] in active_types:
            valid_list.append(move)
            
    return valid_list

func learn_move(move_name: String) -> bool:
    if moves.has(move_name) or moves.size() >= 4:
        return false
        
    var is_valid = false
    for valid_move in valid_moves():
        if valid_move["name"] == move_name:
            is_valid = true
            break
            
    if not is_valid:
        return false
        
    moves.append(move_name)
    return true

func to_dict() -> Dictionary:
    return {
        "name": name,
        "nickname": nickname,
        "type_main": type_main,
        "type_second": type_second,
        "moves": moves.duplicate(),
        "level": level,
        "xp": xp,
        "hp": hp,
        "max_hp": max_hp,
        "attack": attack,
        "defense": defense
    }