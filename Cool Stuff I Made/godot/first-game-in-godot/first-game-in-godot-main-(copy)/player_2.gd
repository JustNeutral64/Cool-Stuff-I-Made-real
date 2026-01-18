#----------------------------------------------------------------------------------------

extends CharacterBody2D

var acceleration_x = 10
var acceleration_x_skidding_multiplier = 2
var max_speed_x = 250
var jump_velocity = -365.0
var walljump_velocity_y = -300
var walljump_velocity_x = 200
var accepting_input = true
var is_stomping = false
var stomp_gravity_multiplier = 2
var stomp_gravity_initial_speed = 60
var stompjump_velocity = -445

var grappling = false
var grapple_pull_angle = 0
var grapple_pull_velocity = 20000
var hook_position = 0

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")
var walljump_gravity_multipler = 0.4
var walljump_fast_gravity_multiplier = 0.85
var input_direction = 0
var moving_direction = 0

@onready var walljumpActionTimer = $WalljumpActionTimer
@onready var camera = $Camera2D
@onready var animated_sprite = $AnimatedSprite2D
@onready var transmitter = get_node("/root/TestLevel/TransmitterNode")

#----------------------------------------------------------------------------------------
#Functions

func handle_grappling_hook(delta):
	if Input.is_action_just_pressed("grapple"):
		var mouse_position = position
		var true_camera_position = camera.get_screen_center_position()
		var mouse_pos = get_viewport().get_mouse_position()
		var viewport_size = get_viewport().get_visible_rect().size
		mouse_position.x = mouse_pos[0] - viewport_size[0] / 2
		mouse_position.y = mouse_pos[1] - viewport_size[1] / 2
		mouse_position.x += true_camera_position[0]
		mouse_position.y += true_camera_position[1]
		var actual_angle = rad_to_deg(position.angle_to_point(mouse_position))
		transmitter.grapplingHook_grapple.emit(actual_angle)
	if grappling:
		velocity.x = grapple_pull_velocity * delta * cos(grapple_pull_angle)
		velocity.y = grapple_pull_velocity * delta * sin(grapple_pull_angle)
		if (position.x > hook_position.x - (grapple_pull_velocity * delta) / 10) and (position.x < hook_position.x + (grapple_pull_velocity * delta) / 10) and (position.y > hook_position.y - (grapple_pull_velocity * delta) / 10) and (position.y < hook_position.y + (grapple_pull_velocity * delta) / 10):
			grappling = false
			transmitter.grapplingHook_reset.emit()
		

func move_up_and_down(delta):
	"""
	#Stomping
	if is_stomping:
		if velocity.y < stomp_gravity_initial_speed:
			velocity.y = stomp_gravity_initial_speed
		velocity.y += gravity * delta * stomp_gravity_multiplier
		
		#stopping stomp
		if is_on_floor():
			is_stomping = false
			if Input.is_action_pressed("jump"):
				velocity.y = stompjump_velocity
				
	
	#wallride/jump
	elif is_on_wall() and not is_on_floor():
		if velocity.y < 0:
			velocity.y += gravity * delta * walljump_fast_gravity_multiplier
		else:
			velocity.y += gravity * delta * walljump_gravity_multipler
		if Input.is_action_just_pressed("jump"):
			velocity.y = walljump_velocity_y
			velocity.x = walljump_velocity_x * moving_direction * -1
			accepting_input = false
			input_direction = 0
			walljumpActionTimer.start()
	"""
	#regular jumping/gravity
	# Add the gravity.
	if not is_on_floor():
		velocity.y += gravity * delta
	# Handle jump.
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = jump_velocity

func move_left_and_right(_delta):
	# Apply movement
	if input_direction > 0:
		if velocity.x >= 0 and velocity.x < max_speed_x:
			velocity.x += acceleration_x
		elif velocity.x < 0:
			velocity.x += acceleration_x * acceleration_x_skidding_multiplier
	elif input_direction < 0:
		if velocity.x <= 0 and velocity.x > max_speed_x * -1:
			velocity.x -= acceleration_x
		elif velocity.x > 0:
			velocity.x -= acceleration_x * acceleration_x_skidding_multiplier
	elif accepting_input:
		if abs(velocity.x) > acceleration_x:
			velocity.x -= acceleration_x * (velocity.x / abs(velocity.x))
		else:
			velocity.x = 0

func handle_sprite_animation():
	# Flip the Sprite
	if input_direction > 0:
		animated_sprite.flip_h = false
	elif input_direction < 0:
		animated_sprite.flip_h = true
	
	# Play animations
	if is_on_floor():
		if input_direction == 0:
			animated_sprite.play("idle")
		else:
			animated_sprite.play("run")
	else:
		animated_sprite.play("jump")

func get_misc_input():
	
	#Stomp
	if Input.is_action_just_pressed("stomp"):
		accepting_input = true
		is_stomping = true
	
	# Get the input direction: -1, 0, 1
	if accepting_input:
		input_direction = Input.get_axis("move_left", "move_right")

func get_other_directions():
	if velocity.x > 0:
		moving_direction = 1
	elif velocity.x < 0:
		moving_direction = -1

#----------------------------------------------------------------------------------------
#Main physics process

func _physics_process(delta):
	
	#get_misc_input()
	
	#get_other_directions()
	
	#handle_grappling_hook(delta)
	
	if not grappling:
		
		move_up_and_down(delta)
	
		move_left_and_right(delta)

	move_and_slide()
	
	#handle_sprite_animation()

#----------------------------------------------------------------------------------------
#Timer methods

func _on_walljump_action_timer_timeout() -> void:
	accepting_input = true

#----------------------------------------------------------------------------------------
#Access/Modifier Methods

func _on_transmitter_node_grappling_hook_pull(pos_x: Variant, pos_y: Variant) -> void:
	var position_copy = position
	position_copy.x = pos_x
	position_copy.y = pos_y
	grapple_pull_angle = position.angle_to_point(position_copy)
	hook_position = position_copy
	grappling = true
