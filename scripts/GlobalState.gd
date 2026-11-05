extends Node

const SAVE_FILE_PATH = "user://player_info.json"
const MONS_FILE_PATH = "res://data/mons.json"

var player_data: Dictionary
var mons_data: Dictionary
var badge_list: Array = [
    "badge_1", "badge_2", "badge_3", "badge_4",
    "badge_5", "badge_6", "badge_7", "badge_8"
]

func _ready():
    _load_mons_data()
    _load_player_data()

func _load_mons_data():
    var file = FileAccess.open(MONS_FILE_PATH, FileAccess.READ)
    if file:
        var json_string = file.get_as_text()
        var json = JSON.new()
        if json.parse(json_string) == OK:
            mons_data = json.data
        file.close()

func _load_player_data():
    # Attempt to load from user:// first (saved games), fallback to res:// (defaults)
    if FileAccess.file_exists(SAVE_FILE_PATH):
        var file = FileAccess.open(SAVE_FILE_PATH, FileAccess.READ)
        var json = JSON.new()
        if json.parse(file.get_as_text()) == OK:
            player_data = json.data
        file.close()
    else:
        var default_file = FileAccess.open("res://data/player_info.json", FileAccess.READ)
        var json = JSON.new()
        if json.parse(default_file.get_as_text()) == OK:
            player_data = json.data
        default_file.close()

func save_change():
    var file = FileAccess.open(SAVE_FILE_PATH, FileAccess.WRITE)
    file.store_string(JSON.stringify(player_data, "\t"))
    file.close()

func has_room_for_mon() -> bool:
    return player_data["mons"].size() < 6

func visit_area(area: String) -> bool:
    if not player_data["areas_visited"].has(area):
        push_error("Unknown area: " + area)
        return false

    if player_data["areas_visited"][area]:
        return false

    player_data["areas_visited"][area] = true
    save_change()
    return true

func add_mon(mon: Dictionary) -> bool:
    if not has_room_for_mon():
        return false
        
    player_data["mons"].append(mon)
    save_change()
    return true
    
# ... translate item and money functions similarly ...