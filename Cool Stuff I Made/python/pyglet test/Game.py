#-----------------------------------------------------------------------------------------------------------------------------------------------

import pyglet
from pyglet.window import key
from pyglet import shapes
import random

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Create a window
window = pyglet.window.Window(width=800, height=600, caption="Endless Runner Game",resizable=True)

# Create a batch for better performance
batch = pyglet.graphics.Batch()

# Create player using shapes
player = shapes.Rectangle(50, 100, 50, 50, color=(50, 225, 30), batch=batch)

# Create ground using shapes
ground = shapes.Rectangle(0, 50, 800, 20, color=(0, 0, 255), batch=batch)

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Define gravity, jump speed, and player speed
gravity = -900
jump_speed = 500
player_speed = 300
player_velocity_y = 0

#-----------------------------------------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------------------------------------------------

# Update function to handle movement and gravity
def update(dt):
    global player_velocity_y, is_jumping

    # Apply gravity
    player_velocity_y += gravity * dt

    # Move player vertically
    player.y += player_velocity_y * dt

    # Check for collisions with the ground
    if player.y <= ground.y + ground.height:
        player.y = ground.y + ground.height
        player_velocity_y = 0
        is_jumping = False

@window.event
def on_key_press(symbol, modifiers):
    global player_velocity_y, is_jumping

    # Handle jump
    if symbol == key.SPACE and not is_jumping:
        player_velocity_y = jump_speed
        is_jumping = True

@window.event
def on_draw():
    window.clear()
    batch.draw()

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Schedule the update function
pyglet.clock.schedule_interval(update, 0.000000001)

# Start the game
pyglet.app.run()

# Credits to Proxlight - Subscribe for more Python game tutorials!
print("Thanks for playing! Check out Proxlight on YouTube for more tutorials.") #You keep your advertising :)

#-----------------------------------------------------------------------------------------------------------------------------------------------