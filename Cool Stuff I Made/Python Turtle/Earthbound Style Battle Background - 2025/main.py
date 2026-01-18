#---------------------------------------------------------------
"""
Complete Documentation: 
https://docs.python.org/3/library/turtle.html#turtle-methods
"""
#---------------------------------------------------------------8
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

def stabilize_fps():
    global start_time
    while time.time() - start_time < 0.00409:
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

turn_amount = 91
frame = 0
t_color = 0
move_amount = 0

while game_running == True:
    start_time = time.time()
    #Background
    draw_rect(-2000, -2000, 2000, 2000, "#000000")
    
    if t_color < 40:
        t_color = 255
    t_color_additor = int(t_color)
    
    
    
    turn_amount = 91 + (sin(frame * 0.001))
    move_amount = 0
    
    t.setpos(0, 0)
    t.seth(0)
    t.pd()
    
    for i in range(300):
        t.color((t_color_additor, 0, 0))
        t.forward(move_amount)
        t.left(turn_amount)
        move_amount += 3 + sin(frame * 0.001)
        t_color_additor += 1
        if t_color_additor > 255:
            t_color_additor = 40
    t.pu()
    
    
    
    turn_amount = 91 + (cos(frame * 0.001))
    move_amount = 0
    
    t.setpos(0, 0)
    t.seth(0)
    t.pd()
    
    for i in range(300):
        t.color((t_color_additor, 0, 0))
        t.forward(move_amount)
        t.left(turn_amount)
        move_amount += 3 + cos(frame * 0.001)
        t_color_additor += 1
        if t_color_additor > 255:
            t_color_additor = 40
    
    t.pu()

    
    #stabilize_fps()
    #show_fps()
    
    screen.update()
    t.clear()
    frame += 4
    t_color -= 1

screen.bye()