#----------------------------------------------------------------------------------------

extends CharacterBody2D

var acceleration_x = 10
var acceleration_x_skidding_multiplier = 2
var max_speed_x = 300
var jump_velocity = -400.0

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")
var input_direction = 0
var moving_direction = 0

@onready var animated_sprite = $AnimatedSprite2D

#----------------------------------------------------------------------------------------
#Functions

func move_up_and_down(delta):
	if is_on_wall() and not is_on_floor():
		pass
	else:
		# Add the gravity.d
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
	else:
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

func get_input_direction():
	# Get the input direction: -1, 0, 1
	input_direction = Input.get_axis("move_left", "move_right")

func get_other_directions():
	if velocity.x > 0:
		moving_direction = 1
	elif velocity.x < 0:
		moving_direction = -1

#----------------------------------------------------------------------------------------
#Main physics process

func _physics_process(delta):
	
	get_input_direction()
	
	move_up_and_down(delta)
	
	move_left_and_right(delta)

	move_and_slide()
	
	handle_sprite_animation()

#----------------------------------------------------------------------------------------
#Access/Modifier Methods
