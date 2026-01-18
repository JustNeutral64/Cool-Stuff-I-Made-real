#Possible cool thing
framerate = 60
#------------------------------------------------------------------------------------------------------
#Imports everything

import pygame
import time
import sys
from PIL import Image
import numpy as np
from math import *
from collections import deque

#57.295779513
#Convert radians to degrees
oldpixels = []
#------------------------------------------------------------------------------------------------------
#Functions

def get_tile(x, y):
    return [floor((x) / 200) + 5, floor((y) / 200) + 10]

def convert_for_x(old_value, width):
    return((old_value - (screen_width / 2)) + (width / 2))

def convert_for_y(old_value, height):
    return(((old_value * -1) + (screen_height / 2)) + (height / 2)) #Interchangeable with normalize for y if height = 0
    
def normalize_for_x(old_value, width):
    return((old_value + (screen_width / 2)) - (width / 2)) # x = 0 is at the center of the screen

def normalize_for_y(old_value, height):
    return(((old_value * -1) + (screen_height / 2)) - (height / 2)) #0, 0 is at the center of the screen, +y goes up and vice versa

def make_level_grid_indexes():
    global level_grid_indexes
    
    #TODO THIS IS THE WORST CODE I'VE WRITTEN. PLEASE REFORMAT THIS
    scanner_width = 700
    scanner_height = 700
    
    scanner_x = -900
    scanner_y = -1900
    level_grid_indexes = []
    for x in range(130):
        level_grid_indexes.append([])
        
        for i in range(70):
            level_grid_indexes[x].append([])
            
            #Lists for each shape
            level_grid_indexes[x][i].append([])
            level_grid_indexes[x][i].append([])
            level_grid_indexes[x][i].append([])
            
            #Rectangles
            for a in range(len(rectangles)):
                if (scanner_x + (scanner_width / 2) > rectangles[a].bottom_left_x and scanner_x - (scanner_width / 2) < rectangles[a].top_right_x and scanner_y + (scanner_height / 3.1) > rectangles[a].bottom_left_y and scanner_y - (scanner_height / 2) < rectangles[a].top_right_y):
                    level_grid_indexes[x][i][0].append(a)
            
            #Triangles
            for a in range(len(triangles)):
                # Why did i create a 4d list
                #TODO You could probably remove these 6 lines
                x1 = triangles[a].x1
                x2 = triangles[a].x2
                x3 = triangles[a].x3
                y1 = triangles[a].y1
                y2 = triangles[a].y2
                y3 = triangles[a].y3
                #Bottom left rectangle
                if point_collision_with_tri(scanner_x - (scanner_width / 2), scanner_y - (scanner_height / 2), x1, x2, x3, y1, y2, y3) == True:
                    level_grid_indexes[x][i][1].append(a)
                #Bottom Right rectangle
                elif point_collision_with_tri(scanner_x + (scanner_width / 2), scanner_y - (scanner_height / 2), x1, x2, x3, y1, y2, y3) == True:
                    level_grid_indexes[x][i][1].append(a)
                #Top Left rectangle
                elif point_collision_with_tri(scanner_x - (scanner_width / 2), scanner_y + (scanner_height / 3.1), x1, x2, x3, y1, y2, y3) == True:
                    level_grid_indexes[x][i][1].append(a)
                #Top Right rectangle
                elif point_collision_with_tri(scanner_x + (scanner_width / 2), scanner_y + (scanner_height / 3.1), x1, x2, x3, y1, y2, y3) == True:
                    level_grid_indexes[x][i][1].append(a)
                #First vertice
                elif point_collision_with_rect(x1, y1, (scanner_x - scanner_width / 2), (scanner_y - scanner_height / 2), (scanner_x + scanner_width / 2), (scanner_y + scanner_height / 3.1)) == True:
                    level_grid_indexes[x][i][1].append(a)
                #Second vertice
                elif point_collision_with_rect(x2, y2, (scanner_x - scanner_width / 2), (scanner_y - scanner_height / 2), (scanner_x + scanner_width / 2), (scanner_y + scanner_height / 3.1)) == True:
                    level_grid_indexes[x][i][1].append(a)
                #Third vertice
                elif point_collision_with_rect(x3, y3, (scanner_x - scanner_width / 2), (scanner_y - scanner_height / 2), (scanner_x + scanner_width / 2), (scanner_y + scanner_height / 3.1)) == True:
                    level_grid_indexes[x][i][1].append(a)
            
            #Circles
            for a in range(len(circles)):
                center_x = circles[a].center_x
                center_y = circles[a].center_y
                radius = circles[a].radius
                if ((scanner_x - center_x) ** 2) + ((scanner_y - center_y) ** 2) <= radius ** 2:
                    level_grid_indexes[x][i][2].append(a)
                
            scanner_y += 200
        scanner_x += 200
        scanner_y = -1900

def draw_collision():
    global rectangles
    global triangles
    global text_boxes
    global do_draw_collision
    
    #Toggles drawing collision
    if keys_pressed[pygame.K_c]:
        if do_draw_collision == True:
            do_draw_collision = False
        elif do_draw_collision == False:
            do_draw_collision = True

    if do_draw_collision == True:
        
        #Draws Rectangles
        for i in range(len(rectangles)):
            bottom_left_x = normalize_for_x((rectangles[i].bottom_left_x - camera_x) * scale_factor, 0) // 1
            bottom_left_y = normalize_for_y((rectangles[i].bottom_left_y - camera_y) * scale_factor, 0) // 1
            top_right_x = normalize_for_x((rectangles[i].top_right_x - camera_x) * scale_factor, 0) // 1
            top_right_y = normalize_for_y((rectangles[i].top_right_y - camera_y) * scale_factor, 0) // 1
            width = (top_right_x - bottom_left_x) // 1
            height = (top_right_y - bottom_left_y) // -1
            
            pygame.draw.rect(screen, "#ff00ff", pygame.Rect(bottom_left_x, top_right_y, width, height))
        
        #Draws Triangles
        for i in range(len(triangles)):
            x_1 = normalize_for_x((triangles[i].x1 - camera_x) * scale_factor, 0) // 1
            x_2 = normalize_for_x((triangles[i].x2 - camera_x) * scale_factor, 0) // 1
            x_3 = normalize_for_x((triangles[i].x3 - camera_x) * scale_factor, 0) // 1
            y_1 = normalize_for_y((triangles[i].y1 - camera_y) * scale_factor, 0) // 1
            y_2 = normalize_for_y((triangles[i].y2 - camera_y) * scale_factor, 0) // 1
            y_3 = normalize_for_y((triangles[i].y3 - camera_y) * scale_factor, 0) // 1
            pygame.draw.polygon(screen, "#0000ff", [(x_1, y_1), (x_2, y_2), (x_3, y_3)])
        
        #Draws Circles
        for i in range(len(circles)):
            x = normalize_for_x((circles[i].center_x - camera_x) * scale_factor, 0)
            y = normalize_for_y((circles[i].center_y - camera_y) * scale_factor, 0)
            radius = circles[i].radius * scale_factor
            pygame.draw.circle(screen, "#ff9000", (x, y), radius)
        
def point_collision_with_tri(x, y, x1, x2, x3, y1, y2, y3):
    original_area = abs( ((x2-x1) * (y3-y1)) - ((x3-x1) * (y2-y1)) )
    area_1 = abs( ((x1-x) * (y2-y)) - ((x2-x) * (y1-y)) )
    area_2 = abs( ((x2-x) * (y3-y)) - ((x3-x) * (y2-y)) )
    area_3 = abs( ((x3-x) * (y1-y)) - ((x1-x) * (y3-y)) )
    if area_1 + area_2 + area_3 <= original_area + 0.0001:
        return True
    else:
        return False

def rect_collision_with_rect(bl_x_1, bl_y_1, tr_x_1, tr_y_1, bl_x_2, bl_y_2, tr_x_2, tr_y_2):
    if (tr_x_1 > bl_x_2 and bl_x_1 < tr_x_2 and tr_y_1 > bl_y_2 and bl_y_1 < tr_y_2):
        return True
    else:
        return False

def point_collision_with_rect(x, y, bl_x, bl_y, tr_x, tr_y):
    if (x > bl_x and x < tr_x and y > bl_y and y < tr_y):
        return True
    else:
        return False

def find_angle(x, y, shape, index):
    if shape == "triangle":
        
        x1 = triangles[index].x1
        x2 = triangles[index].x2
        x3 = triangles[index].x3
        y1 = triangles[index].y1
        y2 = triangles[index].y2
        y3 = triangles[index].y3
        
        for i in range(3):
            #If you are colliding with the vertex of I
            
            #Note that the x used here isn't the player x. It is the x position of the corner of the rectangle that collided with the triangle.
            #TODO Try to get this lower than 20 * value
            if point_collision_with_tri(x + (50 * cos(triangles[index].rotation_angles[i] / 57.2957795)), y + (50 * sin(triangles[index].rotation_angles[i] / 57.2957795)), x1, x2, x3, y1, y2, y3) == True and point_collision_with_tri(x - (50 * cos(triangles[index].rotation_angles[i] / 57.2957795)), y - (50 * sin(triangles[index].rotation_angles[i] / 57.2957795)), x1, x2, x3, y1, y2, y3) == True:
                return [triangles[index].rotation_angles[i], triangles[index].angles[i]]
            
    elif shape == "rectangle":
        if rect_collision_with_rect((x - player.width / 2), (y - 10 - player.height / 2), (x + player.width / 2), (y - 10 + player.height / 3.1), rectangles[index].bottom_left_x, rectangles[index].bottom_left_y, rectangles[index].top_right_x, rectangles[index].top_right_y) == True and rect_collision_with_rect((x - player.width / 2), (y + 10 - player.height / 2), (x + player.width / 2), (y + 10 + player.height / 3.1), rectangles[index].bottom_left_x, rectangles[index].bottom_left_y, rectangles[index].top_right_x, rectangles[index].top_right_y) == True:
            return [90, 90]
        else:
            return [0, 1]
    
    elif shape == "circle":
        center_point = (circles[index].center_x, circles[index].center_y)
        radius = circles[index].radius
        lengths = [radius, radius, dist((center_point[0] + radius, center_point[1]), (x, y))]
        #acos((side_3 ** 2 - side_1 ** 2 - side_2 ** 2) / (-2 * side_1 * side_2)) * 180 / pi
        angle = acos((lengths[2] ** 2 - lengths[0] ** 2 - lengths[1] ** 2) / (-2 * lengths[0] * lengths[1])) * 57.295779513
        if y < center_point[1]:
            angle = 360 - angle
        angle -= 90
        if angle < 0:
            angle += 360
        return [angle, angle]
        
    return player.rotation

def colliding(x, y, width, height):
    
    #Triangles
    for i in range(len(level_grid_indexes[get_tile(x, y)[0]][get_tile(x, y)[1]][1])):

        #TODO You could probably remove these 6 lines
        index = level_grid_indexes[get_tile(x, y)[0]] [get_tile(x, y)[1]] [1] [i]
        x1 = triangles[index].x1
        x2 = triangles[index].x2
        x3 = triangles[index].x3
        y1 = triangles[index].y1
        y2 = triangles[index].y2
        y3 = triangles[index].y3
        
        #Bottom left rectangle
        if point_collision_with_tri(x - (width / 2), y - (height / 2), x1, x2, x3, y1, y2, y3) == True:
            return True
        #Bottom Right rectangle
        elif point_collision_with_tri(x + (width / 2), y - (height / 2), x1, x2, x3, y1, y2, y3) == True:
            return True
        #Top Left rectangle
        elif point_collision_with_tri(x - (width / 2), y + ((height / 3.1)), x1, x2, x3, y1, y2, y3) == True:
            return True
        #Top Right rectangle
        elif point_collision_with_tri(x + (width / 2), y + ((height / 3.1)), x1, x2, x3, y1, y2, y3) == True:
            return True
        #First vertice
        elif point_collision_with_rect(x1, y1, (x - width / 2), (y - height / 2), (x + width / 2), (y + height / 2)) == True:
            return True
        #Second vertice
        elif point_collision_with_rect(x2, y2, (x - width / 2), (y - height / 2), (x + width / 2), (y + height / 2)) == True:
            return True
        #Third vertice
        elif point_collision_with_rect(x3, y3, (x - width / 2), (y - height / 2), (x + width / 2), (y + height / 2)) == True:
            return True
        
    #Rectangles
    for i in range(len(level_grid_indexes[get_tile(x, y)[0]][get_tile(x, y)[1]][0])):
        index = level_grid_indexes[get_tile(x, y)[0]] [get_tile(x, y)[1]] [0] [i]
        if (x + (width / 2) > rectangles[index].bottom_left_x and x - (width / 2) < rectangles[index].top_right_x and y + ((height / 2)) > rectangles[index].bottom_left_y and y - (height / 2) < rectangles[index].top_right_y):
            return True
    
    #Circles
    for i in range(len(circles)):
        
        #Center of circle and radius
        center_x = circles[i].center_x
        center_y = circles[i].center_y
        radius = circles[i].radius
        
        #Move the x and y to top left to make stuff easier
        rectangle_x = x - width / 2
        rectangle_y = y - height / 3.1
        rectangle_width = width
        rectangle_height = height / 3.1 + height / 2

        #Test x and test y
        test_x = center_x
        test_y = center_y
        
        if center_x < rectangle_x:
            test_x = rectangle_x
        elif center_x > rectangle_x + rectangle_width:
            test_x = rectangle_x + rectangle_width
        if center_y < rectangle_y:
            test_y = rectangle_y
        elif center_y > rectangle_y + rectangle_height:
            test_y = rectangle_y + rectangle_height
        
        if ((center_x - test_x) ** 2) + ((center_y - test_y) ** 2) <= (radius ** 2):
            return True
            
    return False

def find_shape_at_point(x, y, width, height):
    shape_type = ""
    shape_index = -1
    
    #Triangles
    for i in range(len(triangles)):
        #TODO You could probably remove these 6 lines
        x1 = triangles[i].x1
        x2 = triangles[i].x2
        x3 = triangles[i].x3
        y1 = triangles[i].y1
        y2 = triangles[i].y2
        y3 = triangles[i].y3
        
        #Bottom left rectangle
        if point_collision_with_tri(x - (width / 2), y - (height / 2), x1, x2, x3, y1, y2, y3) == True:
            shape_type = "Triangle"
            shape_index = i
        #Bottom Right rectangle
        elif point_collision_with_tri(x + (width / 2), y - (height / 2), x1, x2, x3, y1, y2, y3) == True:
            shape_type = "Triangle"
            shape_index = i
        #Top Left rectangle
        elif point_collision_with_tri(x - (width / 2), y + ((height / 3.1)), x1, x2, x3, y1, y2, y3) == True:
            shape_type = "Triangle"
            shape_index = i
        #Top Right rectangle
        elif point_collision_with_tri(x + (width / 2), y + ((height / 3.1)), x1, x2, x3, y1, y2, y3) == True:
            shape_type = "Triangle"
            shape_index = i
        #First vertice
        elif point_collision_with_rect(x1, y1, (x - width / 2), (y - height / 2), (x + width / 2), (y + height / 3.1)) == True:
            shape_type = "Triangle"
            shape_index = i
        #Second vertice
        elif point_collision_with_rect(x2, y2, (x - width / 2), (y - height / 2), (x + width / 2), (y + height / 3.1)) == True:
            shape_type = "Triangle"
            shape_index = i
        #Third vertice
        elif point_collision_with_rect(x3, y3, (x - width / 2), (y - height / 2), (x + width / 2), (y + height / 3.1)) == True:
            shape_type = "Triangle"
            shape_index = i
    
    #Rectangles
    for i in range(len(rectangles)):
        if (x + (width / 2) > rectangles[i].bottom_left_x and x - (width / 2) < rectangles[i].top_right_x and y + ((height / 3.1)) > rectangles[i].bottom_left_y and y - (height / 2) < rectangles[i].top_right_y):
            shape_type = "Rectangle"
            shape_index = i
    
    return [shape_type, shape_index]

def print_rectangles_and_triangles():
    #New paragraph
    for i in range(10):
        print("")
        
    #Rectangles
    output = "rectangles = "
    output += "["
    i = 0
    class_name = "Level_Rect_Collision"
    
    for rect in rectangles:
        if i > 0:
            output += "), "
        output += class_name
        output += "("
        output += str(rect.bottom_left_x) + ", " + str(rect.bottom_left_y) + ", " + str(rect.top_right_x) + ", " + str(rect.top_right_y)
        i += 1
        
    output += ")]"
    print(output)
    
    #Triangles
    output = "triangles = "
    output += "["
    i = 0
    class_name = "Level_Tri_Collision"
    for tri in triangles:
        if i > 0:
            output += "), "
        output += class_name
        output += "("
        output += str(tri.x1) + ", " + str(tri.y1) + ", " + str(tri.x2) + ", " + str(tri.y2) + ", " + str(tri.x3) + ", " + str(tri.y3)
        i += 1
    output += ")]"
    print(output)
    
def display_variables(names, values):
    text = ""
    
    for i in range(len(names)):
        text += names[i] + ": "
        text += str(values[i])
        text += "\n"
    
    screen.blit(lexend_font.render(text, True, "#00FF00"), (10, 10))

def export_level(bl_x, bl_y, tr_x, tr_y):
    image_length = tr_x - bl_x
    image_height = tr_y - bl_y
    scanner_x = bl_x
    scanner_y = tr_y
    
    #Seperate from rest of printed stuff
    for i in range(100):
        print("")
    pixels = []
    
    for i in range(image_height):
        pixels.append([])
        for x in range(image_length):
            if colliding(scanner_x, scanner_y, 0.5, 0.5) == True:
                pixels[i].append((255, 0, 255))
            else:
                pixels[i].append((0, 0, 0))
            scanner_x += 1
        scanner_y -= 1
        print(scanner_y - bl_y)
        scanner_x = bl_x
    
    # Convert the pixels into an array using numpy
    array = np.array(pixels, dtype=np.uint8)

    # Use PIL to create an image from the new array of pixels
    new_image = Image.fromarray(array)
    new_image.save('new.png')

def process_tick():
    player.last_x = player.x
    player.last_y = player.y
    
    player.movement_up_and_down()
    player.movement_left_and_right()

    for grapple in grapples:
        if player.grappling == True:
            player.dg = 0
            player.dy = 0
        grapple.move()
        
        if grapple.finished == True:
            grapples.remove(grapple)
    if len(grapples) == 0:
        player.grappling = False
    
    player.move_in_steps(int((abs(player.dy) + abs(player.dg) + 1)))
    player.set_sprite()

    player.calculate_camera_coordinates()

#------------------------------------------------------------------------------------------------------
# Sets up variables

screen_width = 1500
screen_height = 800
gravity = -0.5

camera_x_addition = 0
camera_y_addition = 0
smooth_camera_strength = 6
smooth_camera_smoothness = 0.125

scale_factor = 1

camera_x = 0
camera_y = 0

do_draw_collision = True

program_state = "Gaming"


#------------------------------------------------------------------------------------------------------
# Initializes pygame and sets up a few other things

#Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0)
pygame.mixer.set_num_channels(32)
footstep = pygame.mixer.Sound('Sounds/jump.mp3')
jumpSonic = pygame.mixer.Sound('Sounds/jump.mp3')
air_dash = pygame.mixer.Sound('Sounds/jump.mp3')
whoosh = pygame.mixer.Sound('Sounds/whoosh.mp3')
menu_open = pygame.mixer.Sound('Sounds/menu_open.mp3')
menu_close = pygame.mixer.Sound('Sounds/menu_close.mp3')
button_click = pygame.mixer.Sound('Sounds/button_click.mp3')


#Screen/Clock
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE, 0, 0, 1) #vsync is on and screen is resizable. Very cool!
pygame.display.set_caption("Did it work?")
clock = pygame.time.Clock()
if sys.platform == 'win32':
    # On Windows, the monitor scaling can be set to something besides normal 100%.
    # PyScreeze and Pillow needs to account for this to make accurate screenshots.
    # TODO - How does macOS and Linux handle monitor scaling?
    import ctypes
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass # Windows XP doesn't support monitor scaling, so just do nothing.
#Font
lexend_font = pygame.font.Font('Sprites/font/Lexend-Light.ttf', 20)
title_font = pygame.font.Font('Sprites/font/Ticketing.ttf', 125)
regular_font = pygame.font.Font("Sprites/font/MedodicaRegular[1].ttf", 30)
button_font = pygame.font.Font("Sprites/font/MedodicaRegular[1].ttf", 50)


#------------------------------------------------------------------------------------------------------
#Classes

class Player():
    
    def __init__(self):
        
        #Sets variables
        self.player_index = 0
        self.x = 5000
        self.y = 500
        self.dg = 0
        self.dx = 0
        self.dy = 0
        self.falling = 0
        self.action_used = 0
        self.rotation = [0, 0]

        self.width = 30
        self.height = 75

        self.regular_movement_friction = 0.03
        self.top_speed = 20
        self.jump_force = 14
        self.stomp_force = -15
        self.coyote_time = 6
        self.dash_speed = 40
        self.dash_multiplier = 0.45
        self.dx_modifier = 0
        self.current_text_box = False
        self.text_box_progress = 0
        self.text_box_size = 0
        self.jump_delay = 8
        
        self.grappling = False
        

        #Sets image
        self.direction_prefix = "Right"
        self.direction = 1
        self.sprite_index = 0
        self.height_factor = 1
        self.width_factor = 1

    #------------------------------------------------------------------------------------------------------
    
    def move_in_steps(self, steps):
        
        #Setup
        self.falling += 1
        self.wallrunning = False
        if self.dg < 0:
            dg_modifier = -1
        else:
            dg_modifier = 1
        starting_x = self.x
        starting_y = self.y
        
        iteration = 0
        
        #Ground movement
        while sqrt((self.x - starting_x) ** 2 + (self.y - starting_y) ** 2) < int(abs(self.dg)) and iteration < abs(self.dg) + 100:
            
            last_value = self.x
            
            self.x += 1 * dg_modifier
            #Colliding x
            self.collide_x_slope_or_wall_bottom(last_value)
                
            iteration += 1
            
        
        #Colliding y (Check is to stop calculations if dy is equal to 0)
        for i in range(steps * 1):
            if self.dy != 0:
                last_x = self.x
                #In this case, last value is y
                last_value = self.y
                
                self.y += self.dy / (steps * 1)
                
                if self.colliding(self.x, self.y, self.width * 0.95, self.height) == True:
                    self.collide_y_ceiling_or_floor(last_x, last_value)
                
                #Grapple Fix
        self.dg += self.dx_modifier

    #Bottom
    def collide_x_slope_or_wall_bottom(self, last_value):                                                                      
        self.dx_modifier = 0
        
        #Going up/Clipping up a slope OR running into a wall
        #Primary check is to see if you are on an upwards facing slope and not a wall
        if (self.colliding(self.x, self.y, self.width * 0.95, self.height) == True):
            #Going up a slope
            if (self.colliding(self.x, self.y + 1, self.width * 0.95, self.height) == False):
                self.y += 1
            #Clipping up a slope
            elif (self.colliding(self.x, self.y + 1.2, self.width * 0.95, self.height) == False):
                self.y += 1.2
            #Going into a wall
            else:
                self.x = last_value
                self.dg = 0
            
        #Going down a slope
        #Primary checks are to see if you are not jumping and if you are actually on a slope
        elif (self.falling < self.coyote_time) and (self.colliding(self.x, self.y - 3, self.width * 0.95, self.height) == True):
            #Going Down a slope
            if (self.colliding(self.x, self.y - 2, self.width * 0.95, self.height) == False):
                self.y -= 2
            elif (self.colliding(self.x, self.y - 1, self.width * 0.95, self.height) == False):
                self.y -= 1
    
    """
    #Left
    def collide_x_slope_or_wall_left(self, last_value):                                                                      
        self.dx_modifier = 0
        
        #Going up/Clipping up a slope OR running into a wall
        #Primary check is to see if you are on an upwards facing slope and not a wall
        if (self.colliding(self.x, self.y, self.width * 0.95, self.height) == True):
            #Going up a slope
            if (self.colliding(self.x + 1, self.y, self.width * 0.95, self.height) == False):
                self.x += 1
            #Clipping up a slope
            elif (self.colliding(self.x + 2, self.y, self.width * 0.95, self.height) == False):
                self.x += 2
            elif (self.colliding(self.x + 5, self.y, self.width * 0.95, self.height) == False):
                self.x += 5
            #Going into a wall
            else:
                self.x = last_value
                self.dg = 0
            
        #Going down a slope
        #Primary checks are to see if you are not jumping and if you are actually on a slope
        elif (self.falling < self.coyote_time) and (self.colliding(self.x - 3, self.y, self.width * 0.95, self.height) == True):
            #Going Down a slope
            if (self.colliding(self.x - 2, self.y, self.width * 0.95, self.height) == False):
                self.x -= 2
            elif (self.colliding(self.x - 1, self.y, self.width * 0.95, self.height) == False):
                self.x -= 1
    
    #Right
    def collide_x_slope_or_wall_right(self, last_value):                                                                      
        self.dx_modifier = 0
        
        #Going up/Clipping up a slope OR running into a wall
        #Primary check is to see if you are on an upwards facing slope and not a wall
        if (self.colliding(self.x, self.y, self.width * 0.95, self.height) == True):
            #Going up a slope
            if (self.colliding(self.x - 1, self.y, self.width * 0.95, self.height) == False):
                self.x -= 1
            #Clipping up a slope
            elif (self.colliding(self.x - 2, self.y, self.width * 0.95, self.height) == False):
                self.x -= 2
            elif (self.colliding(self.x - 5, self.y, self.width * 0.95, self.height) == False):
                self.x -= 5
            #Going into a wall
            else:
                self.x = last_value
                self.dg = 0
            
        #Going down a slope
        #Primary checks are to see if you are not jumping and if you are actually on a slope
        elif (self.falling < self.coyote_time) and (self.colliding(self.x + 3, self.y, self.width * 0.95, self.height) == True):
            #Going Down a slope
            if (self.colliding(self.x + 2, self.y, self.width * 0.95, self.height) == False):
                self.x += 2
            elif (self.colliding(self.x + 1, self.y, self.width * 0.95, self.height) == False):
                self.x += 1
    
    #Top
    def collide_x_slope_or_wall_top(self, last_value):                                                                      
        self.dx_modifier = 0
        
        #Going up/Clipping up a slope OR running into a wall
        #Primary check is to see if you are on an upwards facing slope and not a wall
        if (self.colliding(self.x, self.y, self.width * 0.95, self.height) == True):
            #Going up a slope
            if (self.colliding(self.x, self.y - 1, self.width * 0.95, self.height) == False):
                self.y -= 1
            #Clipping up a slope
            elif (self.colliding(self.x, self.y - 2, self.width * 0.95, self.height) == False):
                self.y -= 2
            elif (self.colliding(self.x, self.y - 5, self.width * 0.95, self.height) == False):
                self.y -= 5
            #Going into a wall
            else:
                self.x = last_value
                self.dg = 0
            
        #Going down a slope
        #Primary checks are to see if you are not jumping and if you are actually on a slope
        elif (self.falling < self.coyote_time) and (self.colliding(self.x, self.y + 3, self.width * 0.95, self.height) == True):
            #Going Down a slope
            if (self.colliding(self.x, self.y + 2, self.width * 0.95, self.height) == False):
                self.y += 2
            elif (self.colliding(self.x, self.y + 1, self.width * 0.95, self.height) == False):
                self.y += 1
    """
    
    def collide_y_ceiling_or_floor(self, last_x, last_value):
        self.x = last_x
        self.y = last_value
        if self.dy > 0:
            self.dy = 0
        else:
            if self.falling > 0:
                self.falling = 0
                self.action_used = 0
            self.falling = 0
            self.dy = 0
            
    def movement_up_and_down(self):
        self.dy += gravity
        
        #Starting Jump
        if keys_pressed[pygame.K_SPACE] and self.falling < self.coyote_time:
            self.dy = self.jump_force
            self.falling = self.coyote_time
        
        if keys_released[pygame.K_SPACE] and self.falling >= self.coyote_time and self.action_used == 0 and self.dy > 0 and keys[pygame.K_w] == False:
            self.dy = self.dy / 2
        
        if keys[pygame.K_v]:
            self.dy += self.jump_force / 15
    
    def movement_left_and_right(self):
        
        #Moving Left or Right
        if keys[pygame.K_d] or keys[pygame.K_a]:
            self.dg += (self.top_speed * self.direction - self.dg) * self.regular_movement_friction
        #Moving without input
        else:
            self.dg += (0 - self.dg) * self.regular_movement_friction * 2
    
    #------------------------------------------------------------------------------------------------------

    def calculate_camera_coordinates(self):
        global camera_x_addition
        global camera_y_addition
        global camera_x
        global camera_y
        
        #true_dx = self.x - self.last_x
        #true_dy = self.y - self.last_y
        
        true_dx = self.dg
        true_dy = self.dy

        camera_x_addition = camera_x_addition + (((true_dx * smooth_camera_strength) - camera_x_addition) * smooth_camera_smoothness)
        camera_y_addition = camera_y_addition + (((true_dy / 2 * smooth_camera_strength) - camera_y_addition) * smooth_camera_smoothness)
        
        camera_x = self.x + camera_x_addition
        camera_y = self.y + camera_y_addition

    def set_sprite(self):
        # Set Sprite index additor and factors
        self.width_factor = 1
        self.height_factor = 1
        last_sprite_index = self.sprite_index
        
        # Set Direction Prefix
        if True:
            if keys[pygame.K_d]:
                self.direction_prefix = "Right"
                self.direction = 1
            elif keys[pygame.K_a]:
                self.direction_prefix = "Left"
                self.direction = -1
        
        #Jumping/Falling
        if self.falling > self.coyote_time:
            self.sprite_index += 0.3
            if self.sprite_index < 17 or self.sprite_index >= 20:
                self.sprite_index = 17

        #On Ground, Pressing a movement key
        elif keys[pygame.K_d] or keys[pygame.K_a]:
            #Normal Running
            if abs(self.dg) > 1:
                self.sprite_index += 0.1 + abs(self.dg) * 0.012
                if self.sprite_index < 1 or self.sprite_index >= 9:
                    self.sprite_index = 1
        else:
            #TODO Make Sure this is correct
            #Running without input
            if abs(self.dg) > 1:
                self.sprite_index += 0.05 + (abs(self.dg) * 0.0125)
                if self.sprite_index < 1 or self.sprite_index >= 9:
                    self.sprite_index = 1
            #Standing
            else:
                self.sprite_index = 0
        
        
        # Fixes naming bug with piskel's exporting (yes, I am using piskel to export these images)
        # TODO Fix Naming bug without these lines of code (just rename the images lmao)
        if self.sprite_index < 10:
            fixed_sprite_index = "0" + str(int(floor(self.sprite_index)))
        else:
            fixed_sprite_index = str(int(floor(self.sprite_index)))
        
        
        # Final Sprite
        self.sprite = pygame.transform.scale(pygame.image.load('Sprites/Sonic/Xsonic' + self.direction_prefix + fixed_sprite_index + '.png'), (146 * self.width_factor * scale_factor, 115 * self.height_factor * scale_factor)).convert_alpha()
        
    #------------------------------------------------------------------------------------------------------
    
    def colliding(self, x, y, width, height):
    
        #Triangles
        for i in range(len(level_grid_indexes[get_tile(player.x, player.y)[0]][get_tile(player.x, player.y)[1]][1])):

            #TODO You could probably remove these 6 lines
            index = level_grid_indexes[get_tile(player.x, player.y)[0]] [get_tile(player.x, player.y)[1]] [1] [i]
            x1 = triangles[index].x1
            x2 = triangles[index].x2
            x3 = triangles[index].x3
            y1 = triangles[index].y1
            y2 = triangles[index].y2
            y3 = triangles[index].y3
            
            #Bottom left rectangle
            if point_collision_with_tri(x - (width / 2), y - (height / 2), x1, x2, x3, y1, y2, y3) == True:
                player.rotation = find_angle(x - (width / 2), y - (height / 2), "triangle", index)
                return True
            #Bottom Right rectangle
            elif point_collision_with_tri(x + (width / 2), y - (height / 2), x1, x2, x3, y1, y2, y3) == True:
                player.rotation = find_angle(x + (width / 2), y - (height / 2), "triangle", index)
                return True
            #Top Left rectangle
            elif point_collision_with_tri(x - (width / 2), y + ((height / 3.1)), x1, x2, x3, y1, y2, y3) == True:
                player.rotation = find_angle(x - (width / 2), y + (height / 2), "triangle", index)
                return True
            #Top Right rectangle
            elif point_collision_with_tri(x + (width / 2), y + ((height / 3.1)), x1, x2, x3, y1, y2, y3) == True:
                player.rotation = find_angle(x + (width / 2), y + (height / 2), "triangle", index)
                return True
            #First vertice
            elif point_collision_with_rect(x1, y1, (x - width / 2), (y - height / 2), (x + width / 2), (y + height / 3.1)) == True:
                return True
            #Second vertice
            elif point_collision_with_rect(x2, y2, (x - width / 2), (y - height / 2), (x + width / 2), (y + height / 3.1)) == True:
                return True
            #Third vertice
            elif point_collision_with_rect(x3, y3, (x - width / 2), (y - height / 2), (x + width / 2), (y + height / 3.1)) == True:
                return True
            
        #Rectangles
        for i in range(len(level_grid_indexes[get_tile(player.x, player.y)[0]][get_tile(player.x, player.y)[1]][0])):
            index = level_grid_indexes[get_tile(player.x, player.y)[0]] [get_tile(player.x, player.y)[1]] [0] [i]
            if (x + (width / 2) > rectangles[index].bottom_left_x and x - (width / 2) < rectangles[index].top_right_x and y + ((height / 3.1)) > rectangles[index].bottom_left_y and y - (height / 2) < rectangles[index].top_right_y):
                player.rotation = find_angle(x, y, "rectangle", index)
                return True
        
        #Circles
        for i in range(len(circles)):
            
            #Center of circle and radius
            center_x = circles[i].center_x
            center_y = circles[i].center_y
            radius = circles[i].radius
            
            #Move the x and y to top left to make stuff easier
            rectangle_x = x - width / 2
            rectangle_y = y - height / 3.1
            rectangle_width = width
            rectangle_height = height / 3.1 + height / 2

            #Test x and test y
            test_x = center_x
            test_y = center_y
            
            if center_x < rectangle_x:
                test_x = rectangle_x
            elif center_x > rectangle_x + rectangle_width:
                test_x = rectangle_x + rectangle_width
            if center_y < rectangle_y:
                test_y = rectangle_y
            elif center_y > rectangle_y + rectangle_height:
                test_y = rectangle_y + rectangle_height
            
            if ((center_x - test_x) ** 2) + ((center_y - test_y) ** 2) <= (radius ** 2):
                player.rotation = find_angle(test_x, test_y, "circle", i)
                return True
        
        #This is here so it can happen before the other rotation scripts
        if player.falling > player.coyote_time:
            player.rotation = [0, 0]
                
        return False
    
    #------------------------------------------------------------------------------------------------------
    
class Grapple():
    
    def __init__(self, start_x, start_y, direction, type):
        self.x = start_x
        self.y = start_y
        self.direction = direction
        self.type = type
        self.collided = False
        self.speed = 40
        self.finished = False
    
    def move(self):
        if self.collided == False:
            self.x += cos(self.direction / (57.295779513)) * self.speed
            self.y += sin(self.direction / (57.295779513)) * self.speed
            if colliding(self.x, self.y, 5, 5):
                self.collided = True
                self.speed = 20
        else:
            player.grappling = True
            try:
                self.direction = (self.y - player.y) / (self.x - player.x)
                if self.x > player.x:
                    self.direction = atan(self.direction) * 57.29577
                else:
                    self.direction = (atan(self.direction) * 57.29577) + 180
            except:
                if self.x < player.x:
                    self.direction = 270
                else:
                    self.direction = 90
            player.dg += cos(self.direction / (57.295779513)) * self.speed
            player.dy += sin(self.direction / (57.295779513)) * self.speed
            self.speed += 0.5
            if self.speed > 75:
                self.speed = 75
            
            #Grapple check to delete itself
            if rect_collision_with_rect(self.x - self.speed, self.y - self.speed, self.x + self.speed, self.y + self.speed, (player.x - player.width / 2), (player.y - player.height / 2), (player.x + player.width / 2), (player.y + player.height / 3.1)):
                self.finished = True
    
    def draw(self):
        pygame.draw.line(screen, "#000000", (normalize_for_x(player.x - camera_x, 0), normalize_for_y(player.y - camera_y, 0)), (normalize_for_x(self.x - camera_x, 0), normalize_for_y(self.y - camera_y, 0)), 4)

class Editor():
    
    def __init__(self):
        
        #Sets variables
        self.x = 0
        self.y = 0
        
        self.base_movement_speed = 8
        self.movement_speed = 8
        self.camera_smoothing = 0.25
        self.rect_placing_state = 0
        self.tri_placing_state = 0
        
        self.last_shapes_type = []
        self.last_shapes_information = []
        
        self.grid_size = 50
        self.grid_offset_x = 0
        self.grid_offset_y = 0
        self.grid_enabled = True
    
    #------------------------------------------------------------------------------------------------------
    
    def move(self):
        
        #Doubles the movement speed if the shift key is pressed
        if keys[pygame.K_LSHIFT]:
            self.movement_speed = self.base_movement_speed * 2
        else:
            self.movement_speed = self.base_movement_speed
        
        # Moves around the screen
        if keys[pygame.K_d]:
            self.x += self.movement_speed
        if keys[pygame.K_a]:
            self.x -= self.movement_speed
        if keys[pygame.K_w]:
            self.y += self.movement_speed
        if keys[pygame.K_s]:
            self.y -= self.movement_speed
    
    def calculate_camera_coordinates(self):
        global camera_x
        global camera_y
        camera_x += (self.x - camera_x) * self.camera_smoothing
        camera_y += (self.y - camera_y) * self.camera_smoothing
    
    #------------------------------------------------------------------------------------------------------
    
    def process_rect_placing(self):
        #Bottom left of rect
        if mouse[0]:
            #Creating vertex
            if self.rect_placing_state == 0:
                mouse_x = convert_for_x(mouse_pos[0] + camera_x, 0)
                mouse_x -= (mouse_x - self.grid_offset_x) % self.grid_size
                mouse_y = normalize_for_y(mouse_pos[1] - camera_y, 0)
                mouse_y -= (mouse_y - self.grid_offset_y) % self.grid_size
                rectangles.append(Level_Rect_Collision(mouse_x, mouse_y, mouse_x, mouse_y))
                
                self.rect_placing_state = 1
            
            #Modifying vertex
            elif self.rect_placing_state == 1:
                mouse_x = convert_for_x(mouse_pos[0] + camera_x, 0)
                mouse_x -= (mouse_x - self.grid_offset_x) % self.grid_size
                mouse_y = normalize_for_y(mouse_pos[1] - camera_y, 0)
                mouse_y -= (mouse_y - self.grid_offset_y) % self.grid_size
                rectangles[len(rectangles) - 1].update(mouse_x, mouse_y, rectangles[len(rectangles) - 1].top_right_x, rectangles[len(rectangles) - 1].top_right_y)

        #Top right of rect
        if mouse[2]:
            
            #Creating Vertex
            if self.rect_placing_state == 0:
                mouse_x = convert_for_x(mouse_pos[0] + camera_x, 0)
                mouse_x -= (mouse_x - self.grid_offset_x) % self.grid_size
                mouse_y = normalize_for_y(mouse_pos[1] - camera_y, 0)
                mouse_y -= (mouse_y - self.grid_offset_y) % self.grid_size
                rectangles.append(Level_Rect_Collision(mouse_x, mouse_y, mouse_x, mouse_y))
                
                self.rect_placing_state = 1
            #Modifying Vertex
            elif self.rect_placing_state == 1:
                mouse_x = convert_for_x(mouse_pos[0] + camera_x, 0)
                mouse_x -= (mouse_x - self.grid_offset_x) % self.grid_size
                mouse_y = normalize_for_y(mouse_pos[1] - camera_y, 0)
                mouse_y -= (mouse_y - self.grid_offset_y) % self.grid_size
                rectangles[len(rectangles) - 1].update(rectangles[len(rectangles) - 1].bottom_left_x, rectangles[len(rectangles) - 1].bottom_left_y, mouse_x, mouse_y)

        #Finishing
        if keys_pressed[pygame.K_RETURN]:
            self.rect_placing_state = 0
            make_level_grid_indexes()
        
        
        #Bottom left of rect
        if keys[pygame.K_u]:
            #Creating vertex
            if self.rect_placing_state == 0:
                mouse_x = convert_for_x(mouse_pos[0] + camera_x, 0)
                mouse_x -= (mouse_x - self.grid_offset_x) % self.grid_size
                mouse_y = normalize_for_y(mouse_pos[1] - camera_y, 0)
                mouse_y -= (mouse_y - self.grid_offset_y) % self.grid_size
                text_boxes.append(Level_Rect_Collision(mouse_x, mouse_y, mouse_x, mouse_y))
                
                self.rect_placing_state = 1
            
            #Modifying vertex
            elif self.rect_placing_state == 1:
                mouse_x = convert_for_x(mouse_pos[0] + camera_x, 0)
                mouse_x -= (mouse_x - self.grid_offset_x) % self.grid_size
                mouse_y = normalize_for_y(mouse_pos[1] - camera_y, 0)
                mouse_y -= (mouse_y - self.grid_offset_y) % self.grid_size
                text_boxes[len(text_boxes) - 1].update(mouse_x, mouse_y, text_boxes[len(text_boxes) - 1].top_right_x, text_boxes[len(text_boxes) - 1].top_right_y)

        #Top right of rect
        if keys[pygame.K_i]:
            
            #Creating Vertex
            if self.rect_placing_state == 0:
                mouse_x = convert_for_x(mouse_pos[0] + camera_x, 0)
                mouse_x -= (mouse_x - self.grid_offset_x) % self.grid_size
                mouse_y = normalize_for_y(mouse_pos[1] - camera_y, 0)
                mouse_y -= (mouse_y - self.grid_offset_y) % self.grid_size
                text_boxes.append(Level_Rect_Collision(mouse_x, mouse_y, mouse_x, mouse_y))
                
                self.rect_placing_state = 1
            #Modifying Vertex
            elif self.rect_placing_state == 1:
                mouse_x = convert_for_x(mouse_pos[0] + camera_x, 0)
                mouse_x -= (mouse_x - self.grid_offset_x) % self.grid_size
                mouse_y = normalize_for_y(mouse_pos[1] - camera_y, 0)
                mouse_y -= (mouse_y - self.grid_offset_y) % self.grid_size
                text_boxes[len(text_boxes) - 1].update(text_boxes[len(text_boxes) - 1].bottom_left_x, text_boxes[len(text_boxes) - 1].bottom_left_y, mouse_x, mouse_y)

        #Finishing
        if keys_pressed[pygame.K_RETURN]:
            self.rect_placing_state = 0
            make_level_grid_indexes()
            
    def process_tri_placing(self):
        #Placing/Editing first vertex
        if keys[pygame.K_1]:
            #Placing
            if self.tri_placing_state == 0:
                mouse_x = convert_for_x(mouse_pos[0] + camera_x, 0)
                mouse_x -= (mouse_x - self.grid_offset_x) % self.grid_size
                mouse_y = normalize_for_y(mouse_pos[1] - camera_y, 0)
                mouse_y -= (mouse_y - self.grid_offset_y) % self.grid_size
                triangles.append(Level_Tri_Collision(mouse_x, mouse_y, mouse_x, mouse_y, mouse_x, mouse_y))
                self.tri_placing_state = 1
            #Editing
            elif self.tri_placing_state == 1:
                mouse_x = convert_for_x(mouse_pos[0] + camera_x, 0)
                mouse_x -= (mouse_x - self.grid_offset_x) % self.grid_size
                mouse_y = normalize_for_y(mouse_pos[1] - camera_y, 0)
                mouse_y -= (mouse_y - self.grid_offset_y) % self.grid_size
                current_x2 = triangles[len(triangles) - 1].x2
                current_y2 = triangles[len(triangles) - 1].y2
                current_x3 = triangles[len(triangles) - 1].x3
                current_y3 = triangles[len(triangles) - 1].y3
                triangles[len(triangles) - 1].update(mouse_x, mouse_y, current_x2, current_y2, current_x3, current_y3)
        
        #Editing second vertex
        elif keys[pygame.K_2]:
            if self.tri_placing_state == 1:
                mouse_x = convert_for_x(mouse_pos[0] + camera_x, 0)
                mouse_x -= (mouse_x - self.grid_offset_x) % self.grid_size
                mouse_y = normalize_for_y(mouse_pos[1] - camera_y, 0)
                mouse_y -= (mouse_y - self.grid_offset_y) % self.grid_size
                current_x1 = triangles[len(triangles) - 1].x1
                current_y1 = triangles[len(triangles) - 1].y1
                current_x3 = triangles[len(triangles) - 1].x3
                current_y3 = triangles[len(triangles) - 1].y3
                triangles[len(triangles) - 1].update(current_x1, current_y1, mouse_x, mouse_y, current_x3, current_y3)
        
        #Editing third vertex
        elif keys[pygame.K_3]:
            if self.tri_placing_state == 1:
                mouse_x = convert_for_x(mouse_pos[0] + camera_x, 0)
                mouse_x -= (mouse_x - self.grid_offset_x) % self.grid_size
                mouse_y = normalize_for_y(mouse_pos[1] - camera_y, 0)
                mouse_y -= (mouse_y - self.grid_offset_y) % self.grid_size
                current_x1 = triangles[len(triangles) - 1].x1
                current_y1 = triangles[len(triangles) - 1].y1
                current_x2 = triangles[len(triangles) - 1].x2
                current_y2 = triangles[len(triangles) - 1].y2
                triangles[len(triangles) - 1].update(current_x1, current_y1, current_x2, current_y2, mouse_x, mouse_y)
        
        #Finishing
        if keys_pressed[pygame.K_RSHIFT]:
            self.tri_placing_state = 0
            make_level_grid_indexes()
    
    def process_shape_deleting_or_restoring(self):
        #Shape Deleting
        if keys_pressed[pygame.K_SPACE]:
            mouse_x = convert_for_x(mouse_pos[0] + camera_x, 0)
            mouse_y = normalize_for_y(mouse_pos[1] - camera_y, 0)
            shape, index = find_shape_at_point(mouse_x, mouse_y, 0, 0)
            
            if shape == "Rectangle":
                self.last_shapes_type.append("Rectangle")
                self.last_shapes_information.append(rectangles[index])

                rectangles.remove(rectangles[index])
            
            elif shape == "Triangle":
                self.last_shapes_type.append("Triangle")
                self.last_shapes_information.append(triangles[index])

                triangles.remove(triangles[index])
            
            make_level_grid_indexes()
        
        #Shape Restoring
        elif keys_pressed[pygame.K_z]:
            index = len(self.last_shapes_type) - 1
            
            #Prevents crash if there is no objects
            if index == -1:
                pass

            elif self.last_shapes_type[index] == "Rectangle":
                rectangles.append(self.last_shapes_information[index])
                self.last_shapes_type.remove(self.last_shapes_type[index])
                self.last_shapes_information.remove(self.last_shapes_information[index])
            
            elif self.last_shapes_type[index] == "Triangle":
                triangles.append(self.last_shapes_information[index])
                self.last_shapes_type.remove(self.last_shapes_type[index])
                self.last_shapes_information.remove(self.last_shapes_information[index])
            
            make_level_grid_indexes()
    
    #------------------------------------------------------------------------------------------------------
    
    def draw_grid_lines(self):
        
        #Expand/Contract grid
        if keys_pressed[pygame.K_EQUALS]:
            if keys[pygame.K_LSHIFT]:
                self.grid_size += 4 #4 + 1 = 5
            self.grid_size += 1
        if keys_pressed[pygame.K_MINUS]:
            if keys[pygame.K_LSHIFT]:
                self.grid_size -= 4
            self.grid_size -= 1
        
        #Offset Grid
        if keys_pressed[pygame.K_LEFT]:
            if keys[pygame.K_LSHIFT]:
                self.grid_offset_x -= 4
            self.grid_offset_x -= 1
        if keys_pressed[pygame.K_RIGHT]:
            if keys[pygame.K_LSHIFT]:
                self.grid_offset_x += 4
            self.grid_offset_x += 1
        if keys_pressed[pygame.K_DOWN]:
            if keys[pygame.K_LSHIFT]:
                self.grid_offset_y -= 4
            self.grid_offset_y -= 1
        if keys_pressed[pygame.K_UP]:
            if keys[pygame.K_LSHIFT]:
                self.grid_offset_y += 4
            self.grid_offset_y += 1
        
        #Prevent fatal crash
        if self.grid_size < 1:
            self.grid_size = 1
        
        #TODO Add code to prevent numbers from getting too high (if offset is more than grid size remove grid size from offset etc.)
        
        #Draws for x
        x = -1 + normalize_for_x((-1 * camera_x) + self.grid_offset_x, 0) % self.grid_size
        for i in range(int(screen_width / self.grid_size) + 1):
            pygame.draw.line(screen, "#000000", (x, screen_height), (x, 0), 1)
            x += self.grid_size
        #Slightly different bc +x moves normally but +y doesn't
        #The -1 is there because width of 1 moves in a way I don't want it to and you have to fix that
        #Draws for y
        y = -1 + normalize_for_y((-1 * camera_y) + self.grid_offset_y, 0) % self.grid_size
        for i in range(int(screen_width / self.grid_size) + 1):
            pygame.draw.line(screen, "#000000", (0, y), (screen_width, y), 1)
            y += self.grid_size
    
    def toggle_grid(self):
        if keys_pressed[pygame.K_g]:
            if self.grid_enabled == True:
                self.grid_enabled = False
                self.grid_size = 1
            else:
                self.grid_enabled = True
                self.grid_size = 50
    
    #------------------------------------------------------------------------------------------------------
    
    def update(self):
        
        self.move()
        self.calculate_camera_coordinates()
        
        self.process_rect_placing()
        self.process_tri_placing()
        self.process_shape_deleting_or_restoring()
        
        self.toggle_grid()

        screen = "Title Screen"
    
#------------------------------------------------------------------------------------------------------
#Level Objects

class Level_Rect_Collision:
    
    def __init__(self, bottom_left_x, bottom_left_y, top_right_x, top_right_y):
        self.bottom_left_x = bottom_left_x
        self.bottom_left_y = bottom_left_y
        self.top_right_x = top_right_x
        self.top_right_y = top_right_y
    
    def update(self, bottom_left_x, bottom_left_y, top_right_x, top_right_y):
        self.bottom_left_x = bottom_left_x
        self.bottom_left_y = bottom_left_y
        self.top_right_x = top_right_x
        self.top_right_y = top_right_y

class Level_Tri_Collision:
    
    def __init__(self, x_1, y_1, x_2, y_2, x_3, y_3):
        angle = 0
        rotation_angle = 0
        self.x1 = x_1
        self.x2 = x_2
        self.x3 = x_3
        self.y1 = y_1
        self.y2 = y_2
        self.y3 = y_3
        #Angles follows the 0 to 180 degree system i made
        self.angles = []
        #Rotation angles follows the standard 0 to 360 rotation, used for putting accurate rotations on the player.
        self.rotation_angles = []
        midpoint_x = (self.x2 + self.x1) / 2
        midpoint_y = (self.y2 + self.y1) / 2
        if (self.x2 - self.x1 != 0):
            angle = (atan((self.y2 - self.y1) / (self.x2 - self.x1)) * 57.2958)
            rotation_angle = 0
            
            #Base : if point_collision_with_tri(midpoint_x, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
            if angle == 0:
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180
                rotation_angle = angle
                
            elif angle > 0 and angle <= 45:
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = 360 - angle
                else:
                    rotation_angle = angle
                
            elif angle > 45 and angle < 90:
                if point_collision_with_tri(midpoint_x + 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = 360 - angle
                else:
                    rotation_angle = angle
                
            elif angle >= -45 and angle < 0:
                rotation_angle = 360 + angle
                angle *= -1
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = rotation_angle - 180
                else: 
                    angle = -1 * angle
                    
            elif angle < 0:
                rotation_angle = 360 + angle
                angle *= -1
                if point_collision_with_tri(midpoint_x - 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = rotation_angle - 180
                else:
                    angle = -1 * angle
                    
            self.angles.append(angle)
            self.rotation_angles.append(rotation_angle)
        else:
            if point_collision_with_tri(midpoint_x - 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == True:
                self.angles.append(270)
                self.rotation_angles.append(270)
            else:
                self.angles.append(90)
                self.rotation_angles.append(90)
            
        midpoint_x = (self.x3 + self.x2) / 2
        midpoint_y = (self.y3 + self.y2) / 2
        if (self.x3 - self.x2 != 0):
            angle = (atan((self.y3 - self.y2) / (self.x3 - self.x2)) * 57.2958)
            
            #Base : if point_collision_with_tri(midpoint_x, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
            if angle == 0:
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180
                rotation_angle = angle
                
            elif angle > 0 and angle <= 45:
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = 360 - angle
                else:
                    rotation_angle = angle
                
            elif angle > 45 and angle < 90:
                if point_collision_with_tri(midpoint_x + 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = 360 - angle
                else:
                    rotation_angle = angle
                
            elif angle >= -45 and angle < 0:
                rotation_angle = 360 + angle
                angle *= -1
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = rotation_angle - 180
                else: 
                    angle = -1 * angle
                    
            elif angle < 0:
                rotation_angle = 360 + angle
                angle *= -1
                if point_collision_with_tri(midpoint_x - 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = rotation_angle - 180
                else:
                    angle = -1 * angle
                    
            self.angles.append(angle)
            self.rotation_angles.append(rotation_angle)
        else:
            if point_collision_with_tri(midpoint_x - 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == True:
                self.angles.append(270)
                self.rotation_angles.append(270)
            else:
                self.angles.append(90)
                self.rotation_angles.append(90)
        
        midpoint_x = (self.x3 + self.x1) / 2
        midpoint_y = (self.y3 + self.y1) / 2
        if (self.x3 - self.x1 != 0):
            angle = (atan((self.y3 - self.y1) / (self.x3 - self.x1)) * 57.2958)
            
            #Base : if point_collision_with_tri(midpoint_x, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
            if angle == 0:
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180
                rotation_angle = angle
                
            elif angle > 0 and angle <= 45:
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = 360 - angle
                else:
                    rotation_angle = angle
                
            elif angle > 45 and angle < 90:
                if point_collision_with_tri(midpoint_x + 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = 360 - angle
                else:
                    rotation_angle = angle
                
            elif angle >= -45 and angle < 0:
                rotation_angle = 360 + angle
                angle *= -1
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = rotation_angle - 180
                else: 
                    angle = -1 * angle
                    
            elif angle < 0:
                rotation_angle = 360 + angle
                angle *= -1
                if point_collision_with_tri(midpoint_x - 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = rotation_angle - 180
                else:
                    angle = -1 * angle
            
            self.angles.append(angle)
            self.rotation_angles.append(rotation_angle)
        else:
            if point_collision_with_tri(midpoint_x - 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == True:
                self.angles.append(270)
                self.rotation_angles.append(270)
            else:
                self.angles.append(90)
                self.rotation_angles.append(90)
    
    def update(self, x_1, y_1, x_2, y_2, x_3, y_3):
        angle = 0
        rotation_angle = 0
        self.x1 = x_1
        self.x2 = x_2
        self.x3 = x_3
        self.y1 = y_1
        self.y2 = y_2
        self.y3 = y_3
        #Angles follows the 0 to 180 degree system i made
        self.angles = []
        #Rotation angles follows the standard 0 to 360 rotation, used for putting accurate rotations on the player.
        self.rotation_angles = []
        midpoint_x = (self.x2 + self.x1) / 2
        midpoint_y = (self.y2 + self.y1) / 2
        if (self.x2 - self.x1 != 0):
            angle = (atan((self.y2 - self.y1) / (self.x2 - self.x1)) * 57.2958)
            rotation_angle = 0
            
            #Base : if point_collision_with_tri(midpoint_x, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
            if angle == 0:
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180
                rotation_angle = angle
                
            elif angle > 0 and angle <= 45:
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = 360 - angle
                else:
                    rotation_angle = angle
                
            elif angle > 45 and angle < 90:
                if point_collision_with_tri(midpoint_x + 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = 360 - angle
                else:
                    rotation_angle = angle
                
            elif angle >= -45 and angle < 0:
                rotation_angle = 360 + angle
                angle *= -1
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = rotation_angle - 180
                else: 
                    angle = -1 * angle
                    
            elif angle < 0:
                rotation_angle = 360 + angle
                angle *= -1
                if point_collision_with_tri(midpoint_x - 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = rotation_angle - 180
                else:
                    angle = -1 * angle
                    
            self.angles.append(angle)
            self.rotation_angles.append(rotation_angle)
        else:
            if point_collision_with_tri(midpoint_x - 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == True:
                self.angles.append(270)
                self.rotation_angles.append(270)
            else:
                self.angles.append(90)
                self.rotation_angles.append(90)
            
        midpoint_x = (self.x3 + self.x2) / 2
        midpoint_y = (self.y3 + self.y2) / 2
        if (self.x3 - self.x2 != 0):
            angle = (atan((self.y3 - self.y2) / (self.x3 - self.x2)) * 57.2958)
            
            #Base : if point_collision_with_tri(midpoint_x, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
            if angle == 0:
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180
                rotation_angle = angle
                
            elif angle > 0 and angle <= 45:
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = 360 - angle
                else:
                    rotation_angle = angle
                
            elif angle > 45 and angle < 90:
                if point_collision_with_tri(midpoint_x + 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = 360 - angle
                else:
                    rotation_angle = angle
                
            elif angle >= -45 and angle < 0:
                rotation_angle = 360 + angle
                angle *= -1
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = rotation_angle - 180
                else: 
                    angle = -1 * angle
                    
            elif angle < 0:
                rotation_angle = 360 + angle
                angle *= -1
                if point_collision_with_tri(midpoint_x - 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = rotation_angle - 180
                else:
                    angle = -1 * angle
                    
            self.angles.append(angle)
            self.rotation_angles.append(rotation_angle)
        else:
            if point_collision_with_tri(midpoint_x - 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == True:
                self.angles.append(270)
                self.rotation_angles.append(270)
            else:
                self.angles.append(90)
                self.rotation_angles.append(90)
        
        midpoint_x = (self.x3 + self.x1) / 2
        midpoint_y = (self.y3 + self.y1) / 2
        if (self.x3 - self.x1 != 0):
            angle = (atan((self.y3 - self.y1) / (self.x3 - self.x1)) * 57.2958)
            
            #Base : if point_collision_with_tri(midpoint_x, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
            if angle == 0:
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180
                rotation_angle = angle
                
            elif angle > 0 and angle <= 45:
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = 360 - angle
                else:
                    rotation_angle = angle
                
            elif angle > 45 and angle < 90:
                if point_collision_with_tri(midpoint_x + 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = 360 - angle
                else:
                    rotation_angle = angle
                
            elif angle >= -45 and angle < 0:
                rotation_angle = 360 + angle
                angle *= -1
                if point_collision_with_tri(midpoint_x, midpoint_y - 5, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = rotation_angle - 180
                else: 
                    angle = -1 * angle
                    
            elif angle < 0:
                rotation_angle = 360 + angle
                angle *= -1
                if point_collision_with_tri(midpoint_x - 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == False:
                    angle = 180 - angle
                    rotation_angle = rotation_angle - 180
                else:
                    angle = -1 * angle
            
            self.angles.append(angle)
            self.rotation_angles.append(rotation_angle)
        else:
            if point_collision_with_tri(midpoint_x - 5, midpoint_y, self.x1, self.x2, self.x3, self.y1, self.y2, self.y3) == True:
                self.angles.append(270)
                self.rotation_angles.append(270)
            else:
                self.angles.append(90)
                self.rotation_angles.append(90)

class Level_Circle_Collision:
    
    def __init__(self, x, y, radius):
        self.center_x = x
        self.center_y = y
        self.radius = radius
    
    def update(self, x, y, radius):
        self.center_x = x
        self.center_y = y
        self.radius = radius

#------------------------------------------------------------------------------------------------------
#Assign Classes/Lists

player = Player()
editor = Editor()

#rectangles = [Level_Rect_Collision(-15000, -270, 15000, -220), Level_Rect_Collision(100, -220, 400, -160), Level_Rect_Collision(160, -160, 400, -100), Level_Rect_Collision(220, -100, 400, -40), Level_Rect_Collision(-400, -100, -100, -40), Level_Rect_Collision(400.0, -250.0, 950.0, -200.0), Level_Rect_Collision(1950.0, 700.0, 2200.0, 1250.0)]
#triangles = [Level_Tri_Collision(0, 100, 300, 100, 150, 200), Level_Tri_Collision(500, 100, 900, 100, 900, 300), Level_Tri_Collision(900.0, -200.0, 1300.0, -200.0, 1300.0, 0.0), Level_Tri_Collision(1250.0, -50.0, 1650.0, -50.0, 1650.0, 350.0), Level_Tri_Collision(1600.0, 300.0, 1950.0, 300.0, 1950.0, 750.0), Level_Tri_Collision(1950.0, 1250.0, 1800.0, 1550.0, 1950.0, 1550.0), Level_Tri_Collision(1850.0, 1450.0, 1850.0, 1750.0, 1550.0, 1750.0), Level_Tri_Collision(900.0, -200.0, 1250.0, -200.0, 1300.0, 0.0), Level_Tri_Collision(1050.0, 1900.0, 1650.0, 1900.0, 1650.0, 1700.0), Level_Tri_Collision(2300.0, 0.0, 3150.0, 0.0, 3150.0, -200.0), Level_Tri_Collision(1050.0, 1900.0, 1650.0, 1900.0, 1650.0, 1700.0), Level_Tri_Collision(1050.0, 1900.0, 1350.0, 1900.0, 1350.0, 1800.0), Level_Tri_Collision(1200.0, 1900.0, 600.0, 1900.0, 600.0, 2050.0), Level_Tri_Collision(200.0, 1750.0, -250.0, 1750.0, -250.0, 1450.0), Level_Tri_Collision(-200.0, 1500.0, -450.0, 1500.0, -450.0, 1250.0), Level_Tri_Collision(-650.0, 1300.0, -450.0, 1300.0, -450.0, 950.0), Level_Tri_Collision(-450.0, 1000.0, -450.0, 650.0, -150.0, 650.0), Level_Tri_Collision(350.0, 350.0, -200.0, 350.0, -200.0, 700.0), Level_Tri_Collision(0.0, 1650.0, 0.0, 1950.0, 750.0, 1950.0), Level_Tri_Collision(650.0, 1900.0, 250.0, 1900.0, 250.0, 1750.0)]

rectangles = [Level_Rect_Collision(100, 100, 30000, 200), Level_Rect_Collision(6750.0, 200.0, 7150.0, 1200.0), Level_Rect_Collision(7150.0, 200.0, 7500.0, 2050.0), Level_Rect_Collision(7500.0, 200.0, 7800.0, 900.0)]
triangles = [Level_Tri_Collision(5950.0, 200.0, 6450.0, 200.0, 6450.0, 400.0), Level_Tri_Collision(6350.0, 350.0, 6750.0, 350.0, 6750.0, 750.0), Level_Tri_Collision(7650.0, 900.0, 7500.0, 900.0, 7500.0, 1050.0), Level_Tri_Collision(7000.0, 1200.0, 7150.0, 1200.0, 7150.0, 1350.0), Level_Tri_Collision(7800.0, 900.0, 7800.0, 450.0, 8250.0, 450.0), Level_Tri_Collision(8150.0, 500.0, 8150.0, 200.0, 8750.0, 200.0), Level_Tri_Collision(8600.0, 250.0, 8450.0, 250.0, 8450.0, 350.0), Level_Tri_Collision(8450.0, 350.0, 8250.0, 350.0, 8250.0, 450.0)]
grapples = []
circles = [] #Unused For now

level_grid_indexes = 0
make_level_grid_indexes()

#------------------------------------------------------------------------------------------------------
#Main game loop
frame = 0
background = pygame.image.load('Sprites/Backgrounds/bob.png').convert_alpha()

while True:
    frame += 1
    #Set start time, screen width, screen height
    start_time = time.time()
    last_screen_width, last_screen_height = screen_width, screen_height
    screen_width, screen_height = pygame.display.get_surface().get_size()
    
    #----------------------------------------------------------------------------------------------------    
    
    if program_state == "Gaming":
        # Sets the input variables
        keys = pygame.key.get_pressed()
        keys_pressed = pygame.key.get_just_pressed()
        keys_released = pygame.key.get_just_released()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_just_pressed()

        #When you left click summons grapple
        if mouse_pressed[0]:
            mouse_x = mouse_pos[0] + camera_x - (screen_width / 2)
            mouse_y = (mouse_pos[1] * -1) + camera_y + (screen_height / 2)
            #Angle (tysm geogebra)
            try:
                angle = (mouse_y - player.y) / (mouse_x - player.x)
                if mouse_x > player.x:
                    angle = atan(angle) * 57.29577
                else:
                    angle = (atan(angle) * 57.29577) + 180
            except:
                if mouse_x < player.x:
                    angle = 270
                else:
                    angle = 90
                
            grapples.append(Grapple(player.x, player.y, angle, "Straight"))
        
        #Removes grapple
        if keys_pressed[pygame.K_LSHIFT]:
            grapples.remove(grapples[len(grapples) - 1])
        
        # Handles miscellaneous events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    editor.x = player.x
                    editor.y = player.y
                    
                    program_state = "Editor"
        
        # Updates the game logic (also known as a tick)
        process_tick()
        
        # Draws objects
        pygame.draw.rect(screen, "#99FFFF", pygame.Rect(0, 0, screen_width, screen_height))
        
        if frame % 4 == 0:
            background = pygame.image.load('Sprites/Backgrounds/bob.png').convert_alpha()
            background = pygame.transform.rotate(background, 90)
            background_array = pygame.PixelArray(background)
            
            oldpixels = []
            for i in range(len(background_array)):
                current_list = deque(background_array[i])
                if i % 2 == 0:
                    current_list.rotate(int(sin(((frame / 4) + i) / 5) * 4))
                else:
                    current_list.rotate(int(sin(((frame / 4) + i) / 5) * -4))
                
                background_array[i] = list(current_list)
                oldpixels.append(background_array[i])
                
            
            
            background_array.close()
            
            background = pygame.transform.rotate(background, 270)
            #background = pygame.transform.scale(background, (screen_width, int(screen_width * 1.14285714286))).convert_alpha()
            
            # Convert the pixels into an array using numpy
            pixels = []
            for i in range(len(oldpixels)):
                pixels.append([])
                for x in range(len(oldpixels[i])):
                    if oldpixels[i][x] == -1:
                        pixels[i].append((0, 0, 0))
                    elif oldpixels[i][x] == -65794:
                        pixels[i].append((255, 255, 255))
                    else:
                        pixels[i].append((255, 0, 0))
            array = np.array(pixels, dtype=np.uint8)
            
            # Use PIL to create an image from the new array of pixels
            new_image = Image.fromarray(array)
            new_image.save('new.png')
            
        screen.blit(background, (200, 200))

        screen.blit(player.sprite, (normalize_for_x((player.x - camera_x) * scale_factor, player.sprite.get_width()), normalize_for_y((player.y - camera_y - 7) * scale_factor, player.sprite.get_height()) + ((35 - (35 * player.height_factor))* scale_factor)))
        draw_collision()
        for grapple in grapples:
            grapple.draw()
        
        
        if keys_pressed[pygame.K_u]:
            scale_factor -= 0.1
        elif keys_pressed[pygame.K_i]:
            scale_factor += 0.1
        
        fps = (1 / (time.time() - start_time))
        
    
    #----------------------------------------------------------------------------------------------------
    
    elif program_state == "Editor":
        
        # Sets the input variables
        keys = pygame.key.get_pressed()
        keys_pressed = pygame.key.get_just_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_just_pressed()
        mouse = pygame.mouse.get_pressed()
        
        # Handles miscellaneous events
        player.x = editor.x
        player.y = editor.y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    program_state = "Gaming"
        
        #Updates the editor
        editor.update()
        
        #Draws objects
        pygame.draw.rect(screen, "#99FFFF", pygame.Rect(0, 0, screen_width, screen_height))
        draw_collision()
        
        #Draws grid lines
        if editor.grid_enabled == True:
            editor.draw_grid_lines()
        
    
    display_variables(["x", "y", "dg", "dx", "dy", "scale_factor", "fps", "Rotation"], [player.x // 1, player.y // 1, player.dg - (player.dg % 0.1), player.dx - (player.dx % 0.1), player.dy, scale_factor, fps // 1, player.rotation])
    
    #prints the rectangles and triangles if 0 is pressed
    if keys[pygame.K_0]:
        print_rectangles_and_triangles()
    elif keys[pygame.K_9]:
        export_level(-3000, -3500, 20500, 6500)
    
    # Updates the screen and completes the tick
    pygame.display.update()
    clock.tick(60)

#------------------------------------------------------------------------------------------------------1