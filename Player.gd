extends CharacterBody2D

const TILE_SIZE = 64
var is_moving = false

func _input(event):
    # Prevent movement if already sliding or if in a menu
    if is_moving or not visible:
        return
        
    var direction = Vector2.ZERO
    if event.is_action_pressed("ui_right"): direction.x = 1
    elif event.is_action_pressed("ui_left"): direction.x = -1
    elif event.is_action_pressed("ui_down"): direction.y = 1
    elif event.is_action_pressed("ui_up"): direction.y = -1
    
    if direction != Vector2.ZERO:
        move_grid(direction)

func move_grid(direction: Vector2):
    is_moving = true
    var target_position = position + (direction * TILE_SIZE)
    
    # Simple tween for smooth sliding animation
    var tween = create_tween()
    tween.tween_property(self, "position", target_position, 0.2)
    await tween.finished
    is_moving = false