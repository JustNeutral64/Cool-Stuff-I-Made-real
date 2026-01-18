#--------------------------------------------------------------------------------------------------------
"""
"""
#--------------------------------------------------------------------------------------------------------
from turtle import *
import time
screen = Screen()
canvas = getscreen()
t = Turtle()
t.shape("turtle")
screen.tracer(False)
t.speed(0)
speed(0)
penup()
forward(1000)
#--------------------------------------------------------------------------------------------------------
frame = 0

start_time = time.time()
time_limit = 0.1
counter = 0

actions_limit=5500
actions = 0

#----------

left = 0
right = 0
up = 0
down = 0

dx = 0
dy = 0
player_x = 0
player_y = 0
camera_x = 0
camera_y = 0

last_value = 0
falling = 10

camera_x_addition = 0
camera_y_addition = 0
camera_smoothing = 0

in_editor = False
editor_x = ""
editor_y = ""
editor_color = "#000000"
editor_filled = True
placement_confirmed = True
grid_enabled = True
settings_menu_opened = False

#----------

screen_width = 900
screen_height = 750


level = "test"

x = 0
y = 0

gravity = -0.35
jump_height = 10
coyote_frames = 5
acceleration = 0.2
resistance = 0.1
max_speed = 7.5

camera_smoothing = 0.1
camera_addition_multiplier = 3

rect_bl_x_coords = [-150]
rect_bl_y_coords = [-400]
rect_tr_x_coords = [400]
rect_tr_y_coords = [-100]
rect_color = ["#51f0ff"]
rect_filled = [True]
rect_col_bl_x_coords = [-150]
rect_col_bl_y_coords = [-300]
rect_col_tr_x_coords = [400]
rect_col_tr_y_coords = [-100]
rect_col_color = "red"

drawing_col = False

editor_speed = 2
grid_width = 25
#--------------------------------------------------------------------------------------------------------
def jump():
    global dy
    global falling
    if falling <= coyote_frames:
        dy = jump_height
        falling += coyote_frames * 2

def rocket_jump():
    global dy
    global falling
    dy = jump_height * 0.7
    falling += coyote_frames * 2

def move_left():
    global left
    global right
    left = 1
    right = 0

def move_right():
    global left
    global right
    left = 0
    right = 1

def move_up():
    global up
    global down
    up = 1
    down = 0

def move_down():
    global up
    global down
    up = 0
    down = 1

def stop_moving():
    global left
    global right
    global up
    global down
    left = 0
    right = 0
    up = 0
    down = 0

def move():
    global left
    global right
    global dx
    global acceleration
    global resistance
    global max_speed
    global dy
    global gravity
    
    if left == 1:
        dx -= acceleration
    elif right == 1:
        dx += acceleration
    else:
        if abs(dx) <= resistance:
            dx = 0
    
    if dx > 0:
        dx -= resistance
    elif dx < 0:
        dx += resistance
    
    if dx > max_speed:
        dx = max_speed
    elif dx < -1 * max_speed:
        dx = -1 * max_speed
    
    dy += gravity
#
#--------------------------------------------------------------------------------------------------------
def move_in_editor():
    global left
    global right
    global up
    global down
    global x
    global y
    global editor_speed
    if left == 1:
        x -= editor_speed
    if right == 1:
        x += editor_speed
    if up == 1:
        y += editor_speed
    if down == 1:
        y -= editor_speed

def confirm_placement():
    global placement_confirmed
    placement_confirmed = True

def enable_grid():
    global grid_enabled
    if grid_enabled == True:
        grid_enabled = False
    else:
        grid_enabled = True

def change_placement_type():
    global in_editor
    global drawing_col
    if in_editor == True:
        if drawing_col == True:
            drawing_col = False
        else:
            drawing_col = True

def change_placement_color():
    global rect_col_color
    rect_col_color = input("Choose a color for rectangle placement (Hex codes work). \n")

def change_collision_color():
    global editor_color
    editor_color = input("Choose a color for collision (Hex codes work). \n")

def toggle_placement_fill():
    global editor_filled
    if editor_filled == True:
        editor_filled = False
    else:
        editor_filled = True

def change_editor_movement_speed():
    global editor_speed
    editor_speed = int(input("What do you want your speed to be in the editor? \n"))
#
#--------------------------------------------------------------------------------------------------------
def collision_detection():

    move_in_steps(int( ((abs(dx) + abs(dy)) // 1) + 1))

def move_in_steps(steps):
    global last_value
    global y
    global dy
    global x
    global dx
    global falling
    global rect_col_bl_x_coords
    global rect_col_bl_y_coords
    global rect_col_tr_x_coords
    global rect_col_tr_y_coords
    global dx
    global dy

    falling += 1

    for i in range(steps):
        last_value = x
        x += dx/steps
        for i in range((len(rect_col_bl_x_coords) + len(rect_col_tr_x_coords)) // 2):
            if x >= rect_col_bl_x_coords[i] and x <= rect_col_tr_x_coords[i] and y >= rect_col_bl_y_coords[i] and y <= rect_col_tr_y_coords[i]:
                x = last_value
                dx = 0

        last_value = y
        y += dy/steps
        for i in range((len(rect_col_bl_x_coords) + len(rect_col_tr_x_coords)) // 2):
            if x >= rect_col_bl_x_coords[i] and x <= rect_col_tr_x_coords[i] and y >= rect_col_bl_y_coords[i] and y <= rect_col_tr_y_coords[i]:
                y = last_value
                if dy < 0:
                    falling = 0
                dy = 0
#
#--------------------------------------------------------------------------------------------------------
def draw_rect(lb_x, lb_y, tr_x, tr_y, color, filled):
    global camera_x
    global camera_y
    global actions

    t.color(color)
    if filled == True:
        t.begin_fill()
        t.penup()
        t.setpos(camera_x + lb_x, camera_y + lb_y)
        t.pendown()
        t.setpos(camera_x + tr_x, camera_y + lb_y)
        t.setpos(camera_x + tr_x, camera_y + tr_y)
        t.setpos(camera_x + lb_x, camera_y + tr_y)
        t.setpos(camera_x + lb_x, camera_y + lb_y)
        t.end_fill()
    else:
        t.penup()
        t.setpos(camera_x + lb_x, camera_y + lb_y)
        t.pendown()
        t.setpos(camera_x + tr_x, camera_y + lb_y)
        t.setpos(camera_x + tr_x, camera_y + tr_y)
        t.setpos(camera_x + lb_x, camera_y + tr_y)   
        t.setpos(camera_x + lb_x, camera_y + lb_y)  

    actions += 5

def draw_level():
    global camera_x
    global x
    global camera_y
    global y
    global actions
    global dx
    global dy
    global camera_x_addition
    global camera_y_addition
    global camera_smoothing
    global camera_addition_multiplier
    global frame

    camera_x_addition = camera_x_addition + (((dx * camera_addition_multiplier) - camera_x_addition) * camera_smoothing)
    camera_y_addition = camera_y_addition + (((dy * camera_addition_multiplier) - camera_y_addition) * camera_smoothing)

    camera_x = x * -1 - camera_x_addition
    camera_y = y * -1 - camera_y_addition
    if drawing_col == False:
        for i in range((len(rect_bl_x_coords) + len(rect_tr_x_coords)) // 2):
            draw_rect(rect_bl_x_coords[i], rect_bl_y_coords[i], rect_tr_x_coords[i], rect_tr_y_coords[i], rect_color[i], rect_filled[i])
    else:
        for i in range((len(rect_col_bl_x_coords) + len(rect_col_tr_x_coords)) // 2):
            draw_rect(rect_col_bl_x_coords[i], rect_col_bl_y_coords[i], rect_col_tr_x_coords[i], rect_col_tr_y_coords[i], rect_col_color, True)

def draw_character():
    global x
    global y
    global player_x
    global player_y
    global camera_x
    global camera_y
    global actions
    global dx
    global dy

    player_x = x + camera_x
    player_y = y + camera_y
    
    t.penup()
    t.color("Black")
    t.showturtle()
    if dx > 0:
        t.setheading(0)
    elif dx < 0:
        t.setheading(180)
        
    t.setpos(player_x, player_y)
    actions += 2

def draw_editor_grid():
    global grid_width
    global screen_height
    global screen_width
    global camera_x
    global camera_y
    global actions
    global grid_enabled

    if grid_enabled == True:

        temp_x = 0
        temp_y = 0

        t.penup()
        t.color("black")
        temp_x = (-1 * screen_width * 0.5) + (camera_x % grid_width)
        temp_y = -1 * screen_height / 2
        t.setposition(temp_x, temp_y)
        actions += 1
        t.pendown()
        for i in range(int((screen_width / grid_width) // 1)):
            t.setposition(temp_x, screen_height / 2)
            t.penup()
            temp_x += grid_width
            t.setposition(temp_x, -1 * screen_height / 2)
            t.pendown()
            actions += 15
        
        t.penup()
        temp_x = -1 * screen_width / 2
        temp_y = (-1 * screen_height / 2) + (camera_y % grid_width)
        t.setposition(temp_x, temp_y)
        actions += 1
        t.pendown()
        for i in range(int((screen_height / grid_width) // 1)):
            t.setposition(screen_width / 2, temp_y)
            t.penup()
            temp_y += grid_width
            t.setposition(-1 * screen_width / 2, temp_y)
            t.pendown()
            actions += 15
        
        t.penup()

def expand_grid():
    global grid_width
    grid_width += 1

def contract_grid():
    global grid_width
    grid_width -= 1

#
#--------------------------------------------------------------------------------------------------------
def set_editor_variables(x, y):
    global editor_x
    global editor_y
    global camera_x
    global camera_y
    editor_x = x - camera_x
    editor_y = y - camera_y

def add_rect():
    global rect_bl_x_coords
    global rect_bl_y_coords
    global rect_tr_x_coords
    global rect_tr_y_coords
    global rect_color
    global rect_filled
    global rect_col_bl_x_coords
    global rect_col_bl_y_coords
    global rect_col_tr_x_coords
    global rect_col_tr_y_coords
    global rect_col_color
    global editor_x
    global editor_y
    global editor_color
    global editor_filled
    global placement_confirmed
    global drawing_col
    if editor_x != "" or editor_y != "":
        if drawing_col == True:
            if placement_confirmed == True:
                rect_col_bl_x_coords.append(editor_x)
                rect_col_bl_y_coords.append(editor_y)
                editor_x = ""
                editor_y = ""
                placement_confirmed = False
            elif len(rect_col_bl_x_coords) > len(rect_col_tr_y_coords):
                rect_col_tr_x_coords.append(editor_x)
                rect_col_tr_y_coords.append(editor_y)
                editor_x = ""
                editor_y = ""
            else:
                rect_col_tr_x_coords[len(rect_col_tr_x_coords) - 1] = editor_x
                rect_col_tr_y_coords[len(rect_col_tr_y_coords) - 1] = editor_y
                editor_x = ""
                editor_y = ""
        else:
            if placement_confirmed == True:
                rect_bl_x_coords.append(editor_x)
                rect_bl_y_coords.append(editor_y)
                editor_x = ""
                editor_y = ""
                placement_confirmed = False
            elif len(rect_bl_x_coords) > len(rect_tr_y_coords):
                rect_tr_x_coords.append(editor_x)
                rect_tr_y_coords.append(editor_y)
                rect_color.append(editor_color)
                rect_filled.append(editor_filled)
                editor_x = ""
                editor_y = ""
            else:
                rect_tr_x_coords[len(rect_tr_x_coords) - 1] = editor_x
                rect_tr_y_coords[len(rect_tr_y_coords) - 1] = editor_y
                editor_x = ""
                editor_y = ""
               
def mode_switch():
    global dx
    global dy
    global in_editor
    if in_editor == True:
        in_editor = False
    else:
        in_editor = True
    
    stop_moving()
    dx = 0
    dy = 0
#
#--------------------------------------------------------------------------------------------------------
def stabilize_fps():
    global actions
    global actions_limit
    global time_limit
    global frame_start_time
    temporary_time = time.time()
    if (temporary_time - frame_start_time) >= 0.015:
        print("LAG!!!!")
    actions = 0

    while (temporary_time - frame_start_time) < 0.015:
        temporary_time = time.time()

def count_fps():
    global counter
    global start_time
    global time_limit
    
    counter+=1
    if (time.time() - start_time) > time_limit :
        print("FPS: ", counter / (time.time() - start_time))
        counter = 0
        start_time = time.time()
#
#--------------------------------------------------------------------------------------------------------
def quit():
    screen.bye()
#
#--------------------------------------------------------------------------------------------------------
screen.onkeypress(jump, "space") #Jump Button
screen.onkeypress(rocket_jump, "v") #Infinite jump/Jump while in the air (For debugging)
screen.onkeypress(move_left, "a") #Move left
screen.onkeypress(move_right, "d") #Move Right
screen.onkeypress(move_up, "w") #Move Up (For Editor Only)
screen.onkeypress(move_down, "s") #Move Down (For Editor Only)
screen.onkeypress(stop_moving, "Shift_L") #Stop moving (the move left/right/up/down keys are toggles)
screen.onkeypress(quit, "Escape") #Close ths window
screen.onkeypress(mode_switch, "e") #Switch between editor mode and platformer mode
screen.onkeypress(change_editor_movement_speed, "i") #Changes the speed you move in the editor
screen.onkeypress(expand_grid, "equal") #Expands the grid size while in the editor
screen.onkeypress(contract_grid, "minus") #Contracts the grid size while in the editor
screen.onkeypress(confirm_placement, "c") #Confirms placement of a block
screen.onkeypress(enable_grid, "g") #Enables or disables the grid
screen.onkeypress(change_placement_type, "n") #Changes if you are placing a collision block or a visual block
screen.onkeypress(change_placement_color, "p") #Changes the color of the next visual blocks you place
screen.onkeypress(toggle_placement_fill, "f") #Toggles if the next visual blocks will be filled or not
screen.onkeypress(change_collision_color, "o") #Changes the color of all collision blocks
canvas.onclick(set_editor_variables) #Used for placing a block (In the editor, click once to set the first point, click again to set the second point, click more times to edit the position of the second point, press C to confirm placement of a block)

screen.listen()

showturtle()
while True:

    frame_start_time = time.time()

    if in_editor == False:
        #----------
        t.clear()
        #----------
        
        move()

        collision_detection()

        draw_level()

        #----------
        stabilize_fps()
        #----------

        draw_character()

        #----------
        count_fps()
        #----------

        screen.update()

    else:
        
        #----------
        t.clear()
        #----------

        move_in_editor()

        add_rect()

        #---

        print(len(rect_col_bl_x_coords), len(rect_col_bl_y_coords), len(rect_col_tr_x_coords), len(rect_col_tr_y_coords))
        
        draw_level()

        draw_editor_grid()

        #----------
        stabilize_fps()
        #----------

        #----------
        count_fps()
        #----------

        screen.update()
    
    t.hideturtle()
    frame += 1
    