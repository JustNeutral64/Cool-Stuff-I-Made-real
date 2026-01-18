# How to Create an Endless Runner Game Using Pyglet

Hey everyone, welcome back to another exciting tutorial! Today, we're diving into the world of game development with Python and Pyglet. We'll walk you through step-by-step on how to build your very own endless runner game. By the end of this video, you'll have a game where your player can jump over obstacles and try to survive as long as possible. Let's get started!

## Introduction

So, what exactly is an endless runner game? Well, think of classics like Temple Run or Subway Surfers, where the goal is to keep running, dodging obstacles, and scoring points. We're going to create something similar using Pyglet, which is an awesome library for making games and interactive applications in Python.

## Prerequisites

Before we jump in, here's what you'll need:
- Basic knowledge of Python programming.
- Pyglet installed on your system. If you haven't already, you can easily install it with a simple pip command:
  
  ```bash
  pip install pyglet
  ```

## Setting Up Our Project

First things first, let's set up our project file (`endless_runner_game.py`). This is where all the magic happens!

## Creating the Game Elements

### 1. Player and Ground

The player and ground are essential parts of our game. The player will run on the ground and jump over obstacles. Here's how we set them up using Pyglet's shape drawing:

```python
import pyglet
from pyglet.window import key
from pyglet import shapes
import random

# Create a window
window = pyglet.window.Window(width=800, height=600, caption="Endless Runner Game")

# Define gravity, jump speed, and player speed
gravity = -900
jump_speed = 500
player_speed = 300

# Create a batch for better performance
batch = pyglet.graphics.Batch()

# Create player using shapes
player = shapes.Rectangle(50, 100, 50, 50, color=(50, 225, 30), batch=batch)

# Create ground using shapes
ground = shapes.Rectangle(0, 50, 800, 20, color=(0, 0, 255), batch=batch)
```

### 2. Handling Player Movement

Now, let's handle the player's movement. We'll track keyboard inputs to move the player left and right, as well as handle jumping:

```python
# Variables to track player movement and state
keys = key.KeyStateHandler()
window.push_handlers(keys)
player_velocity_y = 0
is_jumping = False

@window.event
def on_key_press(symbol, modifiers):
    global player_velocity_y, is_jumping

    # Handle jump
    if symbol == key.SPACE and not is_jumping:
        player_velocity_y = jump_speed
        is_jumping = True
```

## Obstacle Management

Every good endless runner needs obstacles to dodge! Let's create and manage our obstacles:

```python
# List to hold obstacles
obstacles = []

# Function to create obstacles
def create_obstacle():
    x = window.width
    y = ground.y + ground.height
    width = 20
    height = random.randint(20, 50)
    obstacle = shapes.Rectangle(x, y, width, height, color=(255, 0, 0), batch=batch)
    obstacles.append(obstacle)

# Function to update obstacles
def update_obstacles(dt):
    for obstacle in obstacles:
        obstacle.x -= player_speed * dt
    # Remove obstacles that are off-screen
    obstacles[:] = [obstacle for obstacle in obstacles if obstacle.x + obstacle.width > 0]
```

## Game Mechanics

Now, let's put everything together in our game loop and handle game mechanics like gravity, collisions, and drawing:

```python
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

    # Check for collisions with obstacles
    for obstacle in obstacles:
        if (player.x + player.width > obstacle.x and player.x < obstacle.x + obstacle.width and
                player.y < obstacle.y + obstacle.height):
            print("Game Over!")
            pyglet.app.exit()

    # Update obstacles
    update_obstacles(dt)

@window.event
def on_draw():
    window.clear()
    batch.draw()

# Schedule the update function
pyglet.clock.schedule_interval(update, 1/60.0)
# Schedule obstacle creation
pyglet.clock.schedule_interval(lambda dt: create_obstacle(), 1.5)

# Start the game
pyglet.app.run()
```

## Conclusion

And there you have it! We've just created a basic endless runner game using Pyglet. You've learned how to set up a game window, create game elements like the player and obstacles, handle player movement and collisions, and more. Feel free to expand on this game by adding features like scoring, power-ups, or even different levels.
