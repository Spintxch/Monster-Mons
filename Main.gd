extends Control

# Grab references to the UI nodes you built in the editor
@onready var dialogue_box = $DialogueBox
@onready var dialogue_text = $DialogueBox/DialogueText
@onready var starter_menu = $StarterMenu
@onready var overworld = $Overworld
@onready var player = $Overworld/Player

var state = "DIALOGUE" # States: DIALOGUE, STARTER_SELECT, OVERWORLD, BATTLE
var current_event = []
var dialogue_index = 0
var starters = ["Pica", "Grassy", "Flamer"]

func _ready():
    print("1. Game starting...")
    
    var file = FileAccess.open("res://data/events.json", FileAccess.READ)
    if file == null:
        print("ERROR: Could not find events.json! Check your FileSystem tab.")
        return
        
    print("2. Found events.json...")
    var json = JSON.new()
    var error = json.parse(file.get_as_text())
    
    if error != OK:
        print("ERROR: events.json is not formatted correctly.")
        return
        
    print("3. Parsed JSON successfully...")
    current_event = json.data["town_1_intro"]
    
    print("4. Updating UI...")
    _update_ui()

func _input(event):
    # Check if a key was physically pressed down (and ignore holding the key down)
    if event is InputEventKey and event.pressed and not event.echo:
        
        # Explicitly check for the Spacebar
        if event.keycode == KEY_SPACE:
            if state == "DIALOGUE":
                advance_dialogue()
                
        # Move the starter selection into this same key check
        elif state == "STARTER_SELECT":
            if event.keycode == KEY_1: select_starter(0)
            elif event.keycode == KEY_2: select_starter(1)
            elif event.keycode == KEY_3: select_starter(2)

func advance_dialogue():
    dialogue_index += 1
    if dialogue_index >= current_event.size():
        # GlobalState is your Autoload from step 1
        if GlobalState.player_data["mons"].size() == 0:
            state = "STARTER_SELECT"
        else:
            state = "OVERWORLD"
        dialogue_index = 0
    _update_ui()

func select_starter(index: int):
    var starter_name = starters[index]
    
    # Instantiate your custom MonInfo class
    var starter_mon = MonInfo.new(starter_name, "normal", "", 5, 0, 20)
    var valid_moves = starter_mon.valid_moves()
    if valid_moves.size() > 0:
        starter_mon.learn_move(valid_moves[0]["name"])
        
    GlobalState.add_mon(starter_mon.to_dict())
    state = "OVERWORLD"
    _update_ui()

func _update_ui():
    dialogue_box.hide()
    starter_menu.hide()
    overworld.hide()
    player.visible = false
    
    if state == "DIALOGUE":
        dialogue_box.show()
        dialogue_text.text = current_event[dialogue_index]
        
    elif state == "STARTER_SELECT":
        starter_menu.show()
        
    elif state == "OVERWORLD":
        overworld.show()
        player.visible = true