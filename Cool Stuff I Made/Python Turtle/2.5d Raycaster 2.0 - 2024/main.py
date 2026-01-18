#---------------------------------------------------------------
"""
Complete Documentation: 
https://docs.python.org/3/library/turtle.html#turtle-methods
"""
#---------------------------------------------------------------
# distance = sqrt((ray_x - player_x) ** 2 + (ray_y - player_y) ** 2)
from turtle import *
import time
from math import *

hideturtle()

screen = Screen()
t = Turtle()
t.penup()
t.hideturtle()
t.home()
t.pendown()
t.speed(0)
screen.colormode(255)

game_running = True
w_pressed = False
a_pressed = False
d_pressed = False

player_angle = 0
player_acceleration = 3
player_rotation_speed = 4
player_x = 0
player_y = 0
player_width = 10
player_height = 10

ray_x = 0
ray_y = 0
ray_angle = 0
ray_distance = 0

fov = 60
resolution = 2
back_out_amount = 0.1
render_distance = 100
scene_x = 0
scan_lines = 0

#back_out_amount *= resolution
render_distance *= resolution
#---------------------------------------------------------------
"Ghost tapping is off! Good Luck"
#---------------------------------------------------------------

class Level_Rect_Collision:
    def __init__(self, bottom_left_x, bottom_left_y, top_right_x, top_right_y):
        self.bottom_left_x = bottom_left_x
        self.bottom_left_y = bottom_left_y
        self.top_right_x = top_right_x
        self.top_right_y = top_right_y

def check_for_collision(x, y, width, height, col_x_left_modifier, col_x_right_modifier, col_y_bottom_modifier, col_y_top_modifier):
    is_colliding = False
    for i in range(len(rectangles)):
        if (x + (width / 2) >= rectangles[i].bottom_left_x + col_x_left_modifier) and (x - (width / 2) <= rectangles[i].top_right_x + col_x_right_modifier) and (y + (height / 2) >= rectangles[i].bottom_left_y + col_y_bottom_modifier) and (y - (height / 2) <= rectangles[i].top_right_y + col_y_top_modifier):
            is_colliding = True
    return(is_colliding)


rectangles = [Level_Rect_Collision(-75.0000000000004, -81.87626262627907, 65.99999999999955, -46.876262626279015), Level_Rect_Collision(46.999999999999545, -9.876262626279072, 59.999999999999545, 62.12373737372096), Level_Rect_Collision(-45.0000000000004, 32.12373737372096, 8.999999999999602, 56.12373737372096), Level_Rect_Collision(-145.0000000000004, -9.876262626279072, -105.0000000000004, 92.12373737372096), Level_Rect_Collision(-61.0000000000004, 101.12373737372096, 125.99999999999955, 130.12373737372096), Level_Rect_Collision(96.99999999999955, -59.87626262627907, 154.99999999999955, 55.12373737372096), Level_Rect_Collision(-193.0000000000004, -152.87626262627907, 42.999999999999545, -109.87626262627907), Level_Rect_Collision(93.99999999999955, -122.87626262627907, 166.99999999999955, -92.87626262627907), Level_Rect_Collision(211.99999999999955, -66.87626262627907, 255.99999999999955, 161.12373737372096), Level_Rect_Collision(-250.00000000000043, -56.87626262627907, -200.0000000000004, 212.12373737372096), Level_Rect_Collision(-150.0000000000004, 176.12373737372096, -42.0000000000004, 220.12373737372096), Level_Rect_Collision(-271.00000000000045, 260.1237373737209, 320.99999999999955, 310.1237373737209), Level_Rect_Collision(69.99999999999955, 183.12373737372096, 117.99999999999955, 211.12373737372096), Level_Rect_Collision(140.99999999999955, 186.12373737372096, 188.99999999999955, 214.12373737372096), Level_Rect_Collision(288.99999999999955, -146.87626262627907, 340.99999999999955, 284.1237373737209), Level_Rect_Collision(-355.00000000000045, -144.87626262627907, -265.00000000000045, 283.1237373737209), Level_Rect_Collision(-368.00000000000045, -215.87626262627896, 346.99999999999955, -191.87626262627896), Level_Rect_Collision(-347.00000000000045, -201.87626262627896, -265.00000000000045, -121.87626262627896), Level_Rect_Collision(288.99999999999955, -195.87626262627896, 324.99999999999955, -97.87626262627896)]


#---------------------------------------------------------------

def draw_rect(bl_x, bl_y, tr_x, tr_y, color): #BL means bottom left, TR means top right
    t.color(color)
    t.setpos(bl_x, bl_y)
    t.pendown()
    t.begin_fill()
    t.setpos(bl_x, tr_y)
    t.setpos(tr_x, tr_y)
    t.setpos(tr_x, bl_y)
    t.setpos(bl_x, bl_y)
    t.end_fill()
    t.penup()

def draw_2d_player():
    global player_x, player_y, player_angle

    t.showturtle()
    t.setpos(player_x, player_y)
    t.setheading(player_angle)

#---------------------------------------------------------------

def quit():
    global game_running
    game_running = False

def process_w():
    global w_pressed
    global a_pressed
    global d_pressed
    w_pressed = True
    a_pressed = False
    d_pressed = False
def process_a():
    global a_pressed
    global d_pressed
    global w_pressed
    a_pressed = True
    d_pressed = False
    w_pressed = False
def process_d():
    global d_pressed
    global a_pressed
    global w_pressed
    d_pressed = True
    a_pressed = False
    w_pressed = False
def clear_inputs():
    global w_pressed
    global a_pressed
    global d_pressed
    w_pressed = False
    a_pressed = False
    d_pressed = False

#---------------------------------------------------------------

def process_movement():
    global a_pressed, w_pressed, d_pressed
    global player_angle, player_acceleration, player_rotation_speed

    if d_pressed == True:
        player_angle += player_rotation_speed
    elif a_pressed == True:
        player_angle -= player_rotation_speed
    if w_pressed == True:
        move(player_acceleration)

def move(steps):
    global player_x, player_angle, player_y
    player_x += cos(player_angle / 57.2958) * steps
    if check_for_collision(player_x, player_y, player_width, player_height, 0, 0, 0, 0) == True:
        player_x -= cos(player_angle / 57.2958) * steps
    player_y += sin(player_angle / 57.2958) * steps
    if check_for_collision(player_x, player_y, player_width, player_height, 0, 0, 0, 0) == True:
        player_y -= sin(player_angle / 57.2958) * steps

#---------------------------------------------------------------

def fast_proximity_ray():
    global ray_x
    global ray_y
    global ray_angle
    global player_x
    global player_y
    global scene_x
    global resolution
    global back_out_amount
    global render_distance
    global ray_distance
    break_meter = False
    
    while True:
        if check_for_collision(ray_x, ray_y, 0, 0, -5, 5, -5, 5) == False:
            ray_x += cos(ray_angle / 57.2958) * 10
            ray_y += sin(ray_angle / 57.2958) * 10
            
            while check_for_collision(ray_x, ray_y, 0, 0, -5, 5, -5, 5) == False:
                ray_x += cos(ray_angle / 57.2958) * 10
                ray_y += sin(ray_angle / 57.2958) * 10
            
            ray_x += cos(ray_angle / 57.2958) * -6
            ray_y += sin(ray_angle / 57.2958) * -6
        
        for y in range(8):
            ray_x += cos(ray_angle / 57.2958) * 1
            ray_y += sin(ray_angle / 57.2958) * 1
            if check_for_collision(ray_x, ray_y, 0, 0, 0, 0, 0, 0) == True:
                break_meter = True
                break
        
        if break_meter == True:
            break
    
    """
    #Makes ray move until it hits a wall or reaches render distance limit
    while check_for_collision(ray_x, ray_y, 0, 0, 0, 0, 0, 0) == False and ray_distance <= render_distance:
        ray_x += cos(ray_angle / 57.2958) * 2
        ray_y += sin(ray_angle / 57.2958) * 2
        ray_distance += resolution
    """
    #Slowly moves the ray back until it is no longer in the wall
    while check_for_collision(ray_x, ray_y, 0, 0, 0, 0, 0, 0) == True:
        ray_x += cos(ray_angle / 57.2958) * (back_out_amount * -1)
        ray_y += sin(ray_angle / 57.2958) * (back_out_amount * -1)
    

def process_single_ray():
    global ray_x
    global ray_y
    global ray_angle
    global player_x
    global player_y
    global scene_x
    global resolution
    global back_out_amount
    global render_distance
    global ray_distance

    ray_x = player_x
    ray_y = player_y

    ray_distance = 0
    
    #Handles what happens to the ray
    fast_proximity_ray()
    
    #Draws the rectangle if it is in render distance
    if ray_distance <= render_distance:
        distance = dist((ray_x, ray_y), (player_x, player_y))
        distance = distance * cos((ray_angle - player_angle) / 57.2958)
        height = 4000 / distance
        t.pensize(resolution)
        rect_color_modifier = int(distance * 130 / render_distance * resolution)
        if rect_color_modifier > 255:
            rect_color_modifier = 255
        if check_for_collision(ray_x, ray_y, 0, 0, back_out_amount, back_out_amount, 0, 0) == True or check_for_collision(ray_x, ray_y, 0, 0, back_out_amount * -1, back_out_amount * -1, 0, 0) == True:
            t.color(0, int((255 - rect_color_modifier) * 0.7), 255 - rect_color_modifier)
        else:
            t.color(0, 255 - rect_color_modifier, 255 - rect_color_modifier)
        t.setpos(scene_x, height * 1)
        t.pendown()
        t.setpos(scene_x, height * -1)
        t.penup()
        t.pensize(0)

def raycast():
    global ray_x
    global player_x
    global ray_y
    global player_y
    global ray_angle
    global player_angle
    global fov
    global scene_x
    global resolution

    ray_angle = player_angle - (fov / 2)
    scene_x = -200
    scan_lines = (400 / resolution) + 1

    for i in range(int(scan_lines)):
        process_single_ray()
        ray_angle += (fov / scan_lines)
        scene_x += resolution

#---------------------------------------------------------------

def stabilize_fps():
    global start_time
    while time.time() - start_time < 0.0333:
        time.sleep(0)

def show_fps():
    t.color("red")
    t.setpos(-200, 200)
    t.write(str(1.0 / (time.time() - start_time)), align="left", font=("Arial", 20))
#---------------------------------------------------------------

screen.onkey(quit, "q")
screen.onkey(process_w, "w")
screen.onkey(process_a, "a")
screen.onkey(clear_inputs, "s")
screen.onkey(process_d, "d")
screen.listen()
screen.tracer(0, 0)
#---------------------------------------------------------------

while game_running == True:
    start_time = time.time()
    
    draw_rect(-200, -200, 200, 200, "#000000")
    # for item in rectangles:
    #    draw_rect(item.bottom_left_x, item.bottom_left_y, item.top_right_x, item.top_right_y, "red")
    process_movement()
    raycast()
    #draw_2d_player()
    
    stabilize_fps()
    show_fps()
    
    screen.update()
    t.clear()

screen.bye()