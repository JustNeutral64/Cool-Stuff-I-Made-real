extends Node2D

@onready var transmitter = get_node("/root/TestLevel/TransmitterNode")
@onready var player = get_node("/root/TestLevel/Player")
@onready var collision = $Area2D

var active = 0
var direction = 0
var speed_modifier_x = 0
var speed_modifier_y = 0
var current_speed = 600
var acceleration = 150

func reset():
	position.y = 5000000
	active = 0
	direction = 0
	speed_modifier_x = 0
	speed_modifier_y = 0
	current_speed = 600
	acceleration = 150

# Currently does nothing
func _ready() -> void:
	position.y = 5000000
	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if active == 1:
		position.x += current_speed * cos(direction) * delta
		position.x += speed_modifier_x * delta
		position.y += current_speed * sin(direction) * delta
		position.y += speed_modifier_y * delta
		current_speed += acceleration * delta
		#if is_on_floor():
		#	active = 2
		#	transmitter.grapplingHook_pull.emit(position.x, position.y)
	elif active == 2:
		pass
		


func _on_transmitter_node_grappling_hook_grapple(angle: Variant) -> void:
	if active == 0:
		reset()
		direction = deg_to_rad(angle)
		position.x = player.position.x
		position.y = player.position.y - 15
		speed_modifier_x = player.velocity.x
		speed_modifier_y = player.velocity.y
		active = 1


func _on_transmitter_node_grappling_hook_reset() -> void:
	reset()
