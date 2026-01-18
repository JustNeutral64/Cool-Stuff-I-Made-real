#Possible cool thing
framerate = 60

#------------------------------------------------------------------------------------------------------
#Imports everything

import pygame
import time
import sys
from PIL import Image
import numpy as np
from math import floor

#------------------------------------------------------------------------------------------------------
#Functions
def get_tile(x, y):
    return [floor((x) / 200) + 5, floor((y) / 200) + 10]

def make_level_grid_indexes():
    global level_grid_indexes
    
    #TODO THIS IS THE WORST CODE I'VE WRITTEN. PLEASE REFORMAT THIS
    scanner_x = -900
    scanner_y = -1900
    scanner_width = 350
    scanner_height = 350
    level_grid_indexes = []
    for x in range(130):
        level_grid_indexes.append([])
        
        for i in range(70):
            level_grid_indexes[x].append([])
            
            level_grid_indexes[x][i].append([])
            level_grid_indexes[x][i].append([])
                    
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
                
            #Rectangles
            for a in range(len(rectangles)):
                if (scanner_x + (scanner_width / 2) > rectangles[a].bottom_left_x and scanner_x - (scanner_width / 2) < rectangles[a].top_right_x and scanner_y + (scanner_height / 3.1) > rectangles[a].bottom_left_y and scanner_y - (scanner_height / 2) < rectangles[a].top_right_y):
                    level_grid_indexes[x][i][0].append(a)
            scanner_y += 200
        scanner_x += 200
        scanner_y = -1900
    
def convert_for_x(old_value, width):
    return((old_value - (screen_width / 2)) + (width / 2))

def convert_for_y(old_value, height):
    return(((old_value * -1) + (screen_height / 2)) + (height / 2)) #Interchangeable with normalize for y if height = 0
    
def normalize_for_x(old_value, width):
    return((old_value + (screen_width / 2)) - (width / 2)) # x = 0 is at the center of the screen

def normalize_for_y(old_value, height):
    return(((old_value * -1) + (screen_height / 2)) - (height / 2)) #0, 0 is at the center of the screen, +y goes up and vice versa

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
    #TODO Change this back
    if do_draw_collision == False:
        #Draws rectangles
        for i in range(len(rectangles)):
            bottom_left_x = normalize_for_x(rectangles[i].bottom_left_x - camera_x, 0) // 1
            bottom_left_y = normalize_for_y(rectangles[i].bottom_left_y - camera_y, 0) // 1
            top_right_x = normalize_for_x(rectangles[i].top_right_x - camera_x, 0) // 1
            top_right_y = normalize_for_y(rectangles[i].top_right_y - camera_y, 0) // 1
            width = (top_right_x - bottom_left_x) // 1
            height = (top_right_y - bottom_left_y) // -1
            pygame.draw.rect(screen, "#ff00ff", pygame.Rect(bottom_left_x, top_right_y, width, height))
        
        #Draws Triangles
        for i in range(len(triangles)):
            x_1 = normalize_for_x(triangles[i].x1 - camera_x, 0) // 1
            x_2 = normalize_for_x(triangles[i].x2 - camera_x, 0) // 1
            x_3 = normalize_for_x(triangles[i].x3 - camera_x, 0) // 1
            y_1 = normalize_for_y(triangles[i].y1 - camera_y, 0) // 1
            y_2 = normalize_for_y(triangles[i].y2 - camera_y, 0) // 1
            y_3 = normalize_for_y(triangles[i].y3 - camera_y, 0) // 1
            pygame.draw.polygon(screen, "#0000ff", [(x_1, y_1), (x_2, y_2), (x_3, y_3)])
        
        #Draws Text Box Hitboxes
        for i in range(len(text_boxes)):
            bottom_left_x = normalize_for_x(text_boxes[i].bottom_left_x - camera_x, 0) // 1
            bottom_left_y = normalize_for_y(text_boxes[i].bottom_left_y - camera_y, 0) // 1
            top_right_x = normalize_for_x(text_boxes[i].top_right_x - camera_x, 0) // 1
            top_right_y = normalize_for_y(text_boxes[i].top_right_y - camera_y, 0) // 1
            width = (top_right_x - bottom_left_x) // 1
            height = (top_right_y - bottom_left_y) // -1
            pygame.draw.rect(screen, "#00FF00", pygame.Rect(bottom_left_x, top_right_y, width, height))

def point_collision_with_tri(x, y, x1, x2, x3, y1, y2, y3):
    original_area = abs( ((x2-x1) * (y3-y1)) - ((x3-x1) * (y2-y1)) )
    area_1 = abs( ((x1-x) * (y2-y)) - ((x2-x) * (y1-y)) )
    area_2 = abs( ((x2-x) * (y3-y)) - ((x3-x) * (y2-y)) )
    area_3 = abs( ((x3-x) * (y1-y)) - ((x1-x) * (y3-y)) )
    if area_1 + area_2 + area_3 <= original_area + 0.001:
        return True
    else:
        return False

def point_collision_with_rect(x, y, bl_x, bl_y, tr_x, tr_y):
    if (x > bl_x and x < tr_x and y > bl_y and y < tr_y):
        return True
    else:
        return False

def colliding(x, y, width, height):
    collision_detected = False
    
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
            collision_detected = True
        #Bottom Right rectangle
        elif point_collision_with_tri(x + (width / 2), y - (height / 2), x1, x2, x3, y1, y2, y3) == True:
            collision_detected = True
        #Top Left rectangle
        elif point_collision_with_tri(x - (width / 2), y + (height / 3.1), x1, x2, x3, y1, y2, y3) == True:
            collision_detected = True
        #Top Right rectangle
        elif point_collision_with_tri(x + (width / 2), y + (height / 3.1), x1, x2, x3, y1, y2, y3) == True:
            collision_detected = True
        #First vertice
        elif point_collision_with_rect(x1, y1, (x - width / 2), (y - height / 2), (x + width / 2), (y + height / 3.1)) == True:
            collision_detected = True
        #Second vertice
        elif point_collision_with_rect(x2, y2, (x - width / 2), (y - height / 2), (x + width / 2), (y + height / 3.1)) == True:
            collision_detected = True
        #Third vertice
        elif point_collision_with_rect(x3, y3, (x - width / 2), (y - height / 2), (x + width / 2), (y + height / 3.1)) == True:
            collision_detected = True
        
    #Rectangles
    for i in range(len(level_grid_indexes[get_tile(player.x, player.y)[0]][get_tile(player.x, player.y)[1]][0])):
        index = level_grid_indexes[get_tile(player.x, player.y)[0]] [get_tile(player.x, player.y)[1]] [0] [i]
        if (x + (width / 2) > rectangles[index].bottom_left_x and x - (width / 2) < rectangles[index].top_right_x and y + (height / 3.1) > rectangles[index].bottom_left_y and y - (height / 2) < rectangles[index].top_right_y):
            collision_detected = True
    
    return collision_detected
            
def colliding_with_text_boxes(x, y, width, height):
    
    collision_detected = False

    for i in range(len(text_boxes)):
        if (x + (width / 2) > text_boxes[i].bottom_left_x and x - (width / 2) < text_boxes[i].top_right_x and y + (height / 3.1) > text_boxes[i].bottom_left_y and y - (height / 2) < text_boxes[i].top_right_y):
            collision_detected = i
    
    return collision_detected

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
        elif point_collision_with_tri(x - (width / 2), y + (height / 3.1), x1, x2, x3, y1, y2, y3) == True:
            shape_type = "Triangle"
            shape_index = i
        #Top Right rectangle
        elif point_collision_with_tri(x + (width / 2), y + (height / 3.1), x1, x2, x3, y1, y2, y3) == True:
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
        if (x + (width / 2) > rectangles[i].bottom_left_x and x - (width / 2) < rectangles[i].top_right_x and y + (height / 3.1) > rectangles[i].bottom_left_y and y - (height / 2) < rectangles[i].top_right_y):
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
    
    #Text Boxes
    output = "text_boxes = "
    output += "["
    i = 0
    class_name = "Level_Rect_Collision"
    
    for rect in text_boxes:
        if i > 0:
            output += "), "
        output += class_name
        output += "("
        output += str(rect.bottom_left_x) + ", " + str(rect.bottom_left_y) + ", " + str(rect.top_right_x) + ", " + str(rect.top_right_y)
        i += 1
        
    output += ")]"
    print(output)

def display_variables(names, values):
    text = ""
    
    for i in range(len(names)):
        text += names[i] + ": "
        text += str(values[i])
        text += "\n"
    
    screen.blit(lexend_font.render(text, True, "#000000"), (10, 10))

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
            elif colliding_with_text_boxes(scanner_x, scanner_y, 0.5, 0.5) == True:
                pixels[i].append((0, 255, 0))
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
    
#------------------------------------------------------------------------------------------------------
# Sets up variables

screen_width = 1500
screen_height = 800
gravity = -0.60

camera_x_addition = 0
camera_y_addition = 0
smooth_camera_strength = 4
smooth_camera_smoothness = 0.125
#Why are there two!?!?
do_draw_collision = True
drawing_collision = True

parallax_x = 0
parallax_y = 0

program_state = "Main_Menu"


#------------------------------------------------------------------------------------------------------
# Initializes pygame and sets up a few other things

#Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Sounds/title_music.mp3")
pygame.mixer.music.play(-1, 0, 0)
pygame.mixer.music.set_volume(0.8)
pygame.mixer.set_num_channels(32)
footstep = pygame.mixer.Sound('Sounds/footstep.mp3')
jumpSonic = pygame.mixer.Sound('Sounds/jump.mp3')
air_dash = pygame.mixer.Sound('Sounds/air_dash.mp3')
whoosh = pygame.mixer.Sound('Sounds/whoosh.mp3')
menu_open = pygame.mixer.Sound('Sounds/menu_open.mp3')
menu_close = pygame.mixer.Sound('Sounds/menu_close.mp3')
button_click = pygame.mixer.Sound('Sounds/button_click.mp3')


#Screen/Clock
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE, 0, 0, 1) #vsync is on and screen is resizable. Very cool!
pygame.display.set_caption("Did it work?")
clock = pygame.time.Clock()

#Font
lexend_font = pygame.font.Font('Sprites/font/Lexend-Light.ttf', 20)
title_font = pygame.font.Font('Sprites/font/Ticketing.ttf', 125)
regular_font = pygame.font.Font("Sprites/font/MedodicaRegular[1].ttf", 30)
button_font = pygame.font.Font("Sprites/font/MedodicaRegular[1].ttf", 50)

#Backgrounds
background_1 = pygame.transform.scale(pygame.image.load('Sprites/Backgrounds/background.png'), (4000, 4000)).convert_alpha()
level = pygame.transform.scale(pygame.image.load('Sprites/Backgrounds/cancerlevel.png'), (23500, 10000)).convert_alpha()

#------------------------------------------------------------------------------------------------------
#Classes

class Player():
    
    def __init__(self):
        
        #Sets variables
        self.player_index = 0
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.fall_counter = 0
        self.action_used = 0
        self.wallrunning = 0

        self.width = 80
        self.height = 135

        self.acceleration = 0.4
        self.deceleration = 1.5
        self.air_resistance = 0.2
        self.speed_cap = 25
        self.jump_force = 15
        self.stomp_force = -15
        self.coyote_time = 6
        self.dash_speed = 40
        self.dash_multiplier = 0.45
        self.dx_modifier = 0
        self.current_text_box = False
        self.text_box_progress = 0
        self.text_box_size = 0
        

        #Sets image
        self.direction_prefix = "Right"
        self.sprite_index = 0
        self.sprite = pygame.transform.scale(pygame.image.load('Sprites/Players/Sonic/sonicRight00.png'), (100, 100)).convert_alpha()

    #------------------------------------------------------------------------------------------------------
    
    def move_in_steps(self, steps):
        self.fall_counter += 1
        self.wallrunning = False
        for i in range(steps * 1):
            
            last_value = self.x
            self.x += self.dx / (steps * 1)
            
            #Colliding x
            self.collide_x_slope_or_wall(last_value, steps)

            #-----
            
            #Colliding y (Check is to stop calculations if dy is equal to 0)
            if self.dy != 0:
                last_value = self.y
                self.y += self.dy / (steps * 1)
                if colliding(self.x, self.y, self.width * 0.95, self.height) == True:
                    self.collide_y_ceiling_or_floor(last_value)
        
        self.dx += self.dx_modifier
        
        #Colliding with text box
        self.current_text_box = colliding_with_text_boxes(self.x, self.y, 0, 0)

    def collide_x_slope_or_wall(self, last_value, steps):                                                                      
        self.dx_modifier = 0
        
        #Going up/Clipping up a slope OR running into a wall
        #Primary check is to see if you are on an upwards facing slope and not a wall
        if (colliding(self.x, self.y, self.width * 0.95, self.height) == True):
            
            #Going up a slope
            if (colliding(self.x, self.y + (abs((self.dx) / steps) * 1), self.width * 0.95, self.height) == False):
                self.y += abs((self.dx) / steps)
                self.dx -= 0.05 * abs(self.dx) / self.dx
            #Clipping up a slope
            elif (colliding(self.x, self.y + 5, self.width * 0.95, self.height) == False):
                self.y += 5
                self.dx -= 0.1 * abs(self.dx) / self.dx
            #Going into a wall
            else:
                self.x = last_value
                #Wallrunning
                #Checks are to see: if you are in the air for longer than coyote time, if you are not falling really fast, if you are moving fast enough, if you don't have a ceiling above you
                if self.fall_counter >= self.coyote_time and abs(self.dy) < abs(self.dx) and abs(self.dx) >= 8 and colliding(self.x, self.y + 1, self.width * 0.95, self.height) == False:
                    self.wallrun()
                #Ramming into a wall gobi style
                else:
                    self.dx = 0
        
        #Going down/Clipping down a slope
        #Primary checks are to see if you are not jumping and if you are actually on a slope
        elif (self.fall_counter < self.coyote_time) and (colliding(self.x, self.y - 5, self.width * 0.95, self.height) == True):
            #Clipping Down a slope
            if (colliding(self.x, self.y - 1, self.width * 0.95, self.height) == False):
                    self.y -= 1
                    #TODO FIX THIS THIS IS ALSO HORRIBLE
                    self.dx += 0.05 * ((abs(self.dx) + 0.001) / (self.dx + 0.001))
            #Going down a slope
            elif (colliding(self.x, self.y + (abs((self.dx) / steps) * -1), self.width * 0.95, self.height) == False) and (colliding(self.x, self.y + (abs((self.dx) / steps) * -2), self.width * 0.95, self.height) == True):
                    self.y += abs((self.dx) / steps) * -1
                    #TODO FIX THIS THIS IS ALSO HORRIBLE
                    self.dx += 0.05 * ((abs(self.dx) + 0.001) / (self.dx + 0.001))
        
    def wallrun(self):
        #Prevents thokking while wallrunning
        self.wallrunning = True
        self.action_used = 1
        self.y += 1
        self.dy = 0
        self.fall_counter = self.coyote_time
        self.dx_modifier = -0.75 * ((abs(self.dx) + 0.001) / (self.dx + 0.001))

    def collide_y_ceiling_or_floor(self, last_value):
        self.y = last_value
        if self.dy > 0:
            self.dy = 0
        else:
            if self.fall_counter > 0:
                self.fall_counter = 0
                self.action_used = 0
            self.fall_counter = 0
            self.dy = 0
            
    def movement_up_and_down(self):
        self.dy += gravity

        #Jumping
        if keys_pressed[pygame.K_SPACE]:
            #Regular Jump
            if self.wallrunning == False and self.fall_counter < self.coyote_time:
                self.dy = self.jump_force
                self.fall_counter = self.coyote_time
                jumpSonic.play()
            #Walljump
            elif self.wallrunning == True:
                self.dx = (self.dx * -1) + (-5 * (self.dx)) / ((abs(self.dx) + 0.005))
                self.dy = abs(self.dx) / 2
                self.fall_counter = self.coyote_time
                jumpSonic.play()
        
        if keys_released[pygame.K_SPACE] and self.fall_counter >= self.coyote_time and self.action_used == 0 and self.dy > 0 and keys[pygame.K_w] == False:
            self.dy = self.dy / 2
    
    def movement_left_and_right(self):
        #moving left
        if keys[pygame.K_a] and self.dx > 0:
            self.dx -= self.deceleration
        #skidding left
        elif keys[pygame.K_a] and self.dx > self.speed_cap * -1:
            self.dx -= self.acceleration
        
        #moving right
        if keys[pygame.K_d] and self.dx < 0:
            self.dx += self.deceleration
        #skidding right
        elif keys[pygame.K_d] and self.dx < self.speed_cap:
            self.dx += self.acceleration
        
        #air resistance when moving (resistance is not there)
        if abs(self.dx) > self.air_resistance and (keys[pygame.K_d] or keys[pygame.K_a]):
            #self.dx -= self.air_resistance * (self.dx / abs(self.dx)) * 0.4 #Universal for left or right, half air resistance
            pass
        #air resistance when not moving
        elif abs(self.dx) > self.air_resistance:
            self.dx -= self.air_resistance * (self.dx / abs(self.dx)) #Universal for left or right
        #Prevent glitch of being in movement limbo
        else:
            self.dx = 0

    def movement_special(self):
        #thokking
        if keys_pressed[pygame.K_SPACE] and self.fall_counter != self.coyote_time and self.action_used == 0:
            self.action_used = 1
            air_dash.play()
            if keys[pygame.K_d]:
                self.dx += (self.dash_speed - self.dx) * self.dash_multiplier
            elif keys[pygame.K_a]:
                self.dx -= (self.dash_speed + self.dx) * self.dash_multiplier
            
            if self.dy < 0:
                self.dy = 0
        
        #Stomping    
        if keys_pressed[pygame.K_s] and self.fall_counter >= 1:
            air_dash.play()
            self.action_used = 2
            self.fall_counter += self.coyote_time
            self.dy += self.stomp_force
    
    #------------------------------------------------------------------------------------------------------

    def calculate_camera_coordinates(self):
        global camera_x_addition
        global camera_y_addition
        global camera_x
        global camera_y

        camera_x_addition = camera_x_addition + (((self.dx * smooth_camera_strength) - camera_x_addition) * smooth_camera_smoothness)
        camera_y_addition = camera_y_addition + (((self.dy * smooth_camera_strength) - camera_y_addition) * smooth_camera_smoothness)

        camera_x = self.x + camera_x_addition
        camera_y = self.y + camera_y_addition

    def set_sprite(self):
        # Set Sprite index additor
        last_sprite_index = self.sprite_index
        sprite_index_additor = 0.1 + (abs(self.dx) * 0.013)
        
        # Set Direction Prefix
        if keys[pygame.K_d]:
            self.direction_prefix = "Right"
        elif keys[pygame.K_a]:
            self.direction_prefix = "Left"
        
        #-----
        #In air
        if self.fall_counter > self.coyote_time:
            if self.dy > 0:
                self.sprite_index = 11
            else:
                self.sprite_index = 12
        
        #Wallrunning
        elif self.wallrunning == True:
            self.sprite_index += sprite_index_additor
            
            if self.sprite_index < 0 or self.sprite_index >= 10:
                self.sprite_index = 0
            if self.sprite_index >= 1 and last_sprite_index < 1:
                footstep.play()
            if self.sprite_index >= 6 and last_sprite_index < 6:
                footstep.play()
            
            if keys[pygame.K_d]:
                self.direction_prefix = "wallRight"
            elif keys[pygame.K_a]:
                self.direction_prefix = "wallLeft"
        
        #On ground 
        else:
            self.sprite_index += sprite_index_additor
            if self.dx == 0 and not keys[pygame.K_a] and not keys[pygame.K_d]:
                self.sprite_index = 0
            elif self.sprite_index < 1 or self.sprite_index >= 11:
                self.sprite_index = 1
            
            if self.sprite_index >= 2 and last_sprite_index < 2:
                footstep.play()
            if self.sprite_index >= 7 and last_sprite_index < 7:
                footstep.play()
                
        """
        # In air
        if self.fall_counter > self.coyote_time:
            self.sprite_index += sprite_index_additor + 0.23
            # Start of jump
            if self.fall_counter < 18 and (self.sprite_index < 36 or self.sprite_index >= 37):
                self.sprite_index = 36
            # Transitioning into mid
            elif self.fall_counter >= 18 and self.fall_counter < 22 and (self.sprite_index < 37 or self.sprite_index >= 38):
                self.sprite_index = 37
            # Middle of jump
            elif self.fall_counter >= 22 and self.dy <= -10 and (self.sprite_index < 38 or self.sprite_index >= 40):
                self.sprite_index = 38
            # Falling down
            elif self.fall_counter >= 22 and self.dy > -10 and (self.sprite_index < 19 or self.sprite_index >= 27):
                self.sprite_index = 19
        
        # On Ground
        else:
            # Grounded and standing
            if self.dx == 0 and not keys[pygame.K_a] and not keys[pygame.K_d]:
                self.sprite_index = 0
            # Grounded and moving, skidding in other direction
            elif ((self.dx <= self.speed_cap / -3.5 and keys[pygame.K_d]) or (self.dx >= self.speed_cap / 3.5 and keys[pygame.K_a])):
                self.sprite_index += 0.2
                if self.sprite_index < 17 or self.sprite_index >= 19:
                    self.sprite_index = 17
                if self.direction_prefix == "Right":
                    self.direction_prefix = "Left"
                else:
                    self.direction_prefix = "Right"
            # Grounded and moving, at speed cap
            elif abs(self.dx) >= self.speed_cap * 0.9:
                self.sprite_index += sprite_index_additor
                if self.sprite_index < 9 or self.sprite_index >= 17:
                    self.sprite_index = 9
                
                if self.sprite_index >= 11 and last_sprite_index < 11:
                    footstepMC.play()
                elif self.sprite_index >= 15 and last_sprite_index < 15:
                    footstepMC.play()
            # Grounded and moving, not at speed cap
            else:
                self.sprite_index += sprite_index_additor
                if self.sprite_index < 1 or self.sprite_index >= 9:
                    self.sprite_index = 1
                if self.sprite_index >= 4 and last_sprite_index < 4:
                    footstepMC.play()
                elif self.sprite_index >= 8 and last_sprite_index < 8:
                    footstepMC.play()
        
        #-----
        """
        # Fixes naming bug
        # TODO Fix Naming bug without these lines of code (just rename the images lmao)
        if self.sprite_index < 10:
            fixed_sprite_index = "0" + str(int(self.sprite_index))
        else:
            fixed_sprite_index = str(int(self.sprite_index))
        
        # Final Sprite
        self.sprite = pygame.transform.scale(pygame.image.load('Sprites/Players/Ninja/ninja' + self.direction_prefix + fixed_sprite_index + '.png'), (120, 120)).convert_alpha()
    
    #------------------------------------------------------------------------------------------------------
        
    def update(self):
        #Regular playing
        if type(self.current_text_box) == type(True):
            self.movement_up_and_down()
            self.movement_left_and_right()
            self.movement_special()

            self.move_in_steps(int((abs(self.dy) + abs(self.dx) + 1)))
            self.set_sprite()

            self.calculate_camera_coordinates()
        else:
            if keys_pressed[pygame.K_SPACE]:
                button_click.play()
                self.text_box_progress += 1
                #TODO later change this into a close animation
                if self.text_box_progress > len(text[self.current_text_box]) - 1:
                    self.current_text_box = False
                    self.text_box_progress = 0
                    text_boxes.remove(text_boxes[self.current_text_box])
                    text.remove(text[self.current_text_box])
                    self.text_box_size = 0
        
    #------------------------------------------------------------------------------------------------------

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
        
        #Shape Restoring
        elif keys_pressed[pygame.K_z]:
            index = len(self.last_shapes_type) - 1
            
            #Prevents crash if there is no objects
            print(index)
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

class Main_Menu():
    
    def __init__(self):
        screen = "Title Screen"

    #------------------------------------------------------------------------------------------------------
    
    def draw_background(self):
        screen.blit(background_1, (parallax_x - 128, parallax_y - 128))
    
    def draw_title(self):
        
        title_text = title_font.render("Cancer Ninja", False, "#FFFFFF")
        
        screen.blit(title_text, title_text.get_rect(center=(screen_width/2, 125)))

    def draw_button(self):
        global screen_height
        
        tl_x = normalize_for_x(-180, 0)
        tl_y = screen_height - 180
        br_x = normalize_for_x(180, 0)
        br_y = screen_height - 40
        width = br_x - tl_x
        height = abs(br_y - tl_y)
        
        #Draws Main Text Box
        pygame.draw.rect(screen, "#222244", pygame.Rect(tl_x, tl_y, width, height))
        
        #Draws Text Box Outline
        pygame.draw.rect(screen, "#555599", pygame.Rect(tl_x, tl_y, width, 10)) #Top
        pygame.draw.rect(screen, "#555599", pygame.Rect(tl_x, br_y - 10, width, 10)) #Bottom
        pygame.draw.rect(screen, "#555599", pygame.Rect(tl_x, tl_y, 10, height)) #Left
        pygame.draw.rect(screen, "#555599", pygame.Rect(br_x - 10, tl_y, 10, height)) #Right
        
        text = button_font.render("Tutorial", False, "#FFFFFF")
        
        screen.blit(text, text.get_rect(center=(screen_width/2, screen_height - 110)))
        
    def handle_button(self):
        global program_state
        if (mouse_pos[0] >= 570 and mouse_pos[0] <= 920) and (mouse_pos[1] >= 618 and mouse_pos[1] <= 756) and (mouse_pressed[0] == True):
            program_state = "Gaming"
            
            pygame.mixer.music.load("Sounds/demo_music.mp3")
            pygame.mixer.music.play(-1, 0, 0)
            pygame.mixer.music.set_volume(0.8)
            
    #------------------------------------------------------------------------------------------------------
    
    def update(self):
        self.draw_background()
        self.draw_title()
        self.draw_button()
        self.handle_button()
    
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
        self.x1 = x_1
        self.x2 = x_2
        self.x3 = x_3
        self.y1 = y_1
        self.y2 = y_2
        self.y3 = y_3
    
    def update(self, x_1, y_1, x_2, y_2, x_3, y_3):
        self.x1 = x_1
        self.x2 = x_2
        self.x3 = x_3
        self.y1 = y_1
        self.y2 = y_2
        self.y3 = y_3

#------------------------------------------------------------------------------------------------------
#Assign Classes/Lists

player = Player()
editor = Editor()
menu = Main_Menu()
#rectangles = [Level_Rect_Collision(-1000000, -270, 1000000, -220), Level_Rect_Collision(-50.0, -320.0, 50.0, -220.0), Level_Rect_Collision(300.0, -220.0, 450.0, -70.0), Level_Rect_Collision(600.0, -220.0, 750.0, 130.0), Level_Rect_Collision(750.0, -220.0, 900.0, 180.0), Level_Rect_Collision(900.0, -220.0, 1050.0, 130.0), Level_Rect_Collision(2550.0, -220.0, 2700.0, 480.0), Level_Rect_Collision(-50.0, 230.0, 450.0, 280.0), Level_Rect_Collision(300.0, -100.0, 450.0, -50.0), Level_Rect_Collision(-457.0, -76.0, -380.0, 30.0), Level_Rect_Collision(2550.0, 450.0, 2700.0, 17400.0), Level_Rect_Collision(2100.0, 2400.0, 2250.0, 17400.0)]
#text_boxes = [Level_Rect_Collision(2000, -130, 2300, 170)]
#text = [["Text 1", "Text 2", "Text 3"]]
#triangles = [Level_Tri_Collision(1050.0, 130.0, 1050.0, -220.0, 1400.0, -220.0), Level_Tri_Collision(1300.0, -120.0, 1300.0, -220.0, 1500.0, -220.0), Level_Tri_Collision(-50.0, 280.0, -400.0, 280.0, -400.0, 430.0), Level_Tri_Collision(-300.0, 380.0, -650.0, 380.0, -650.0, 630.0), Level_Tri_Collision(-550.0, 530.0, -950.0, 580.0, -950.0, 1030.0), Level_Tri_Collision(0.0, 580.0, 550.0, 580.0, 750.0, 880.0), Level_Tri_Collision(-550.0, 780.0, -150.0, 780.0, -350.0, 980.0), Level_Tri_Collision(700.0, 130.0, 750.0, 130.0, 750.0, 180.0), Level_Tri_Collision(950.0, 130.0, 900.0, 130.0, 900.0, 180.0), Level_Tri_Collision(-208.0, -71.0, -381.0, -72.0, -384.0, 29.0), Level_Tri_Collision(-597.0, -71.0, -452.0, -70.0, -453.0, 25.0), Level_Tri_Collision(-608.0, -74.0, -456.0, -73.0, -455.0, 34.0)]
rectangles = [Level_Rect_Collision(-300.0, -200.0, -200.0, 2050.0), Level_Rect_Collision(-200.0, -200.0, 900.0, -100.0), Level_Rect_Collision(900.0, -200.0, 1000.0, 0.0), Level_Rect_Collision(1000.0, -200.0, 1100.0, 100.0), Level_Rect_Collision(1100.0, -200.0, 1200.0, 200.0), Level_Rect_Collision(1200.0, -200.0, 1300.0, 0.0), Level_Rect_Collision(1200.0, -300.0, 2450.0, -200.0), Level_Rect_Collision(1450.0, 200.0, 1700.0, 300.0), Level_Rect_Collision(1950.0, 300.0, 2200.0, 400.0), Level_Rect_Collision(2450.0, 400.0, 3550.0, 500.0), Level_Rect_Collision(2450.0, -300.0, 2550.0, 400.0), Level_Rect_Collision(-200.0, 1950.0, 2600.0, 2050.0), Level_Rect_Collision(2450.0, 750.0, 2550.0, 2000.0), Level_Rect_Collision(2550.0, 750.0, 3700.0, 850.0), Level_Rect_Collision(3650.0, 400.0, 3750.0, 850.0), Level_Rect_Collision(3450.0, 100.0, 3550.0, 400.0), Level_Rect_Collision(3450.0, 50.0, 3850.0, 150.0), Level_Rect_Collision(5350.0, -300.0, 5450.0, 50.0), Level_Rect_Collision(3800.0, -400.0, 5450.0, -300.0), Level_Rect_Collision(3800.0, -300.0, 3950.0, -150.0), Level_Rect_Collision(3750.0, -250.0, 3900.0, 0.0), Level_Rect_Collision(3700.0, -50.0, 3850.0, 50.0), Level_Rect_Collision(5350.0, 50.0, 6200.0, 150.0), Level_Rect_Collision(3750.0, 550.0, 6550.0, 650.0), Level_Rect_Collision(6450.0, -1100.0, 6550.0, 600.0), Level_Rect_Collision(6100.0, -1600.0, 6200.0, 100.0), Level_Rect_Collision(6100.0, -1600.0, 7250.0, -1500.0), Level_Rect_Collision(7250.0, -1600.0, 7350.0, -1100.0), Level_Rect_Collision(7250.0, -1200.0, 8000.0, -1100.0), Level_Rect_Collision(6550.0, -750.0, 7800.0, -650.0), Level_Rect_Collision(8000.0, -1200.0, 8100.0, -350.0), Level_Rect_Collision(6900.0, -650.0, 7000.0, 150.0), Level_Rect_Collision(7000.0, 50.0, 8100.0, 150.0), Level_Rect_Collision(7200.0, -350.0, 8450.0, -250.0), Level_Rect_Collision(10650.0, -1800.0, 12000.0, -1700.0), Level_Rect_Collision(16150.0, -1850.0, 16250.0, 3800.0), Level_Rect_Collision(11900.0, -1950.0, 16250.0, -1800.0), Level_Rect_Collision(16950.0, 3800.0, 17050.0, 3950.0), Level_Rect_Collision(16250.0, 3700.0, 17050.0, 3800.0), Level_Rect_Collision(17050.0, 3850.0, 18750.0, 3950.0), Level_Rect_Collision(16150.0, 4450.0, 18850.0, 4550.0), Level_Rect_Collision(18750.0, 3850.0, 18850.0, 4500.0)]
triangles = [Level_Tri_Collision(5250.0, 150.0, 5350.0, 150.0, 5350.0, 50.0), Level_Tri_Collision(8450.0, -250.0, 8450.0, -1700.0, 10900.0, -1700.0)]
text_boxes = [Level_Rect_Collision(-50.0, -100.0, 50.0, 250.0), Level_Rect_Collision(750.0, -100.0, 850.0, 250.0), Level_Rect_Collision(3050.0, 500.0, 3150.0, 750.0), Level_Rect_Collision(5850.0, 150.0, 5950.0, 550.0), Level_Rect_Collision(6650.0, -1500.0, 6750.0, -750.0), Level_Rect_Collision(7800.0, -250.0, 7900.0, 50.0), Level_Rect_Collision(17100.0, 3950.0, 17200.0, 4450.0)]
text = []
text.append(["Welcome to cancer ninja! Here, you will rid the bodies of cancer while learning more about it.", "Use the A and D keys to move left and right."])
text.append(["Use the space key to jump."])
text.append(["Use the space key while in the air to perform an air dash. The air dash you from falling down and increases your \nhorizontal speed in the direction you are going."])
text.append(["Press the S key to dash downwards. you can press this multiple times to go downwards very quickly.", "By now, you may be wondering why there aren't any enemies. This is because you are in a benign tumor.\n\nThere are two different types of tumors, benign and malignant. In a benign tumor, the cells are not too damaging yet \nand cannot leave the tumor site. \n \n This means that there are currently no cancer cells outside the tumor site."])
text.append(["You can run up walls by jumping next to them with enough speed.", "If you lose too much speed while wallrunning, you will lose grip and fall off the wall.", "You can also walljump by pressing space during a wallrun."])
text.append(["Running down slopes will greatly increase your speed, allowing you to cross much longer gaps and run up large walls!"])
text.append(["We are now reaching where the tumor site would be.", "If you were in a real body, you would place one of our vessels in the tumor site.", "These vessels contain small organelles called enzymes that make the cancer cells die.", "However, since you are in an example body, and not the real thing, you can just reach the end of this hallway and we \nwill teleport you back to the start of the level."])

level_grid_indexes = 0
make_level_grid_indexes()

#------------------------------------------------------------------------------------------------------
#Main game loop

while True:
    #Set start time, screen width, screen height
    start_time = time.time()
    last_screen_width, last_screen_height = screen_width, screen_height
    screen_width, screen_height = pygame.display.get_surface().get_size()
    
    if program_state == "Main_Menu":
        
        #Sets the input variables
        keys = pygame.key.get_pressed()
        keys_pressed = pygame.key.get_just_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_just_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        
        menu.update()
        
        parallax_x -= 1
        while abs(parallax_x) > 128:
            if parallax_x < -128:
                parallax_x += 128
            elif parallax_x > 128:
                parallax_x -= 128
        parallax_y -= 0.5
        while abs(parallax_y) > 128:
            if parallax_y < -128:
                parallax_y += 128
            elif parallax_y > 128:
                parallax_y -= 128
    
    #----------------------------------------------------------------------------------------------------    
    
    elif program_state == "Gaming":
        # Sets the input variables
        keys = pygame.key.get_pressed()
        keys_pressed = pygame.key.get_just_pressed()
        keys_released = pygame.key.get_just_released()

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
        
        # Updates the player class
        player.update()
        
        #Ends game
        if player.x > 18500:
            program_state = "Main_Menu"
            
            text_boxes = [Level_Rect_Collision(-50.0, -100.0, 50.0, 250.0), Level_Rect_Collision(750.0, -100.0, 850.0, 250.0), Level_Rect_Collision(3050.0, 500.0, 3150.0, 750.0), Level_Rect_Collision(5850.0, 150.0, 5950.0, 550.0), Level_Rect_Collision(6650.0, -1500.0, 6750.0, -750.0), Level_Rect_Collision(7800.0, -250.0, 7900.0, 50.0), Level_Rect_Collision(17100.0, 3950.0, 17200.0, 4450.0)]
            text = []
            text.append(["Welcome to cancer ninja! Here, you will rid the bodies of cancer while learning more about it.", "Use the A and D keys to move left and right."])
            text.append(["Use the space key to jump."])
            text.append(["Use the space key while in the air to perform an air dash. The air dash you from falling down and increases your \nhorizontal speed in the direction you are going."])
            text.append(["Press the S key to dash downwards. you can press this multiple times to go downwards very quickly.", "By now, you may be wondering why there aren't any enemies. This is because you are in a benign tumor.\n\nThere are two different types of tumors, benign and malignant. In a benign tumor, the cells are not too damaging yet \nand cannot leave the tumor site. \n \n This means that there are currently no cancer cells outside the tumor site."])
            text.append(["You can run up walls by jumping next to them with enough speed.", "If you lose too much speed while wallrunning, you will lose grip and fall off the wall.", "You can also walljump by pressing space during a wallrun."])
            text.append(["Running down slopes will greatly increase your speed, allowing you to cross much longer gaps and run up large walls!"])
            text.append(["We are now reaching where the tumor site would be", "If you were in a real body, you would place one of our vessels in the tumor site.", "These vessels contain small organelles called enzymes that make the cancer cells die.", "However, since you are in an example body, and not the real thing, you can just reach the end of this hallway and we will teleport you back outside."])
            
            
            player.x = 0
            player.y = 0
            player.dx = 0
            player.dy = 0
            
            pygame.mixer.music.load("Sounds/title_music.mp3")
            pygame.mixer.music.play(-1, 0, 0)
            pygame.mixer.music.set_volume(0.8)

        # Draws objects
        parallax_x = camera_x / -6
        while abs(parallax_x) > 128:
            if parallax_x < -128:
                parallax_x += 128
            elif parallax_x > 128:
                parallax_x -= 128
        parallax_y = camera_y / 6
        while abs(parallax_y) > 128:
            if parallax_y < -128:
                parallax_y += 128
            elif parallax_y > 128:
                parallax_y -= 128
                
        
        screen.blit(background_1, (parallax_x - 128, parallax_y - 128))
        screen.blit(level, (normalize_for_x(-3000 - camera_x, 0), normalize_for_y(6500 - camera_y, 0)))
        screen.blit(player.sprite, (normalize_for_x(player.x - camera_x, 100), normalize_for_y(player.y - camera_y, 100)))
        draw_collision()
        
        #Growing Textbox
        if type(player.current_text_box) == type(3):
            #Growing Text Box
            if player.text_box_size == 0:
                menu_open.play()
            if player.text_box_size < 100:
                player.text_box_size += 5
                actual_text_box_size = player.text_box_size / 100
                #Draws Main Text Box
                pygame.draw.rect(screen, "#222244", pygame.Rect(40, 40, (screen_width - 80) * actual_text_box_size, (screen_height - 80) * actual_text_box_size))
                
                #Draws Text Box Outline
                pygame.draw.rect(screen, "#555599", pygame.Rect(40, 40, (screen_width - 80) * actual_text_box_size, 12)) #Top
                pygame.draw.rect(screen, "#555599", pygame.Rect(40, (screen_height - 80) * actual_text_box_size + 28, (screen_width - 80) * actual_text_box_size, 12)) #Bottom
                pygame.draw.rect(screen, "#555599", pygame.Rect(40, 40, 12, (screen_height - 80) * actual_text_box_size)) #Left
                pygame.draw.rect(screen, "#555599", pygame.Rect((screen_width - 80) * actual_text_box_size + 28, 40, 12, (screen_height - 80) * actual_text_box_size)) #Right
                
            elif player.text_box_progress < len(text[player.current_text_box]):
                #Draws Main Text Box
                pygame.draw.rect(screen, "#222244", pygame.Rect(40, 40, screen_width - 80, screen_height - 80))
                
                #Draws Text Box Outline
                pygame.draw.rect(screen, "#555599", pygame.Rect(40, 40, screen_width - 80, 12)) #Top
                pygame.draw.rect(screen, "#555599", pygame.Rect(40, screen_height - (40 + 12), screen_width - 80, 12)) #Bottom
                pygame.draw.rect(screen, "#555599", pygame.Rect(40, 40, 12, screen_height - 80)) #Left
                pygame.draw.rect(screen, "#555599", pygame.Rect(screen_width - (40 + 12), 40, 12, screen_height - 80)) #Right
                
                #Draws Text
                text_box_text = regular_font.render(text[player.current_text_box][player.text_box_progress], True, "#FFFFFF")
                screen.blit(text_box_text, (60, 60))
                
                #Draws bottom text to press space to continue
                text_box_text = regular_font.render("Press [Space] to continue.", True, "#FFFFFF")
                screen.blit(text_box_text, text_box_text.get_rect(center=(screen_width/2, screen_height - 86)))
        
        fps = (1 / (time.time() - start_time))
        
        #display_variables(["x", "dx", "y", "dy", "wallrunning?", "fps", "Text_Box_size", "grid_x", "grid_y"], [player.x // 1, player.dx - (player.dx % 0.1), player.y // 1, player.dy - (player.dx // 0.1), player.wallrunning, fps // 1, player.text_box_size, get_tile(player.x, player.y)[0], get_tile(player.x, player.y)[1]])

        
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
        screen.blit(background_1, (0, 0))
        draw_collision()
        
        #Draws grid lines
        if editor.grid_enabled == True:
            editor.draw_grid_lines()
        
        display_variables(["x", "dx", "y", "dy", "wallrunning?", "fps", "Text_Box_size", "grid_x", "grid_y"], [player.x // 1, player.dx - (player.dx % 0.1), player.y // 1, player.dy - (player.dx // 0.1), player.wallrunning, fps // 1, player.text_box_size, get_tile(player.x, player.y)[0], get_tile(player.x, player.y)[1]])
    
    
    #prints the rectangles and triangles if 0 is pressed
    if keys[pygame.K_0]:
        print_rectangles_and_triangles()
    elif keys[pygame.K_9]:
        export_level(-3000, -3500, 20500, 6500)
    
    print(level_grid_indexes[get_tile(player.x, player.y)[0]][get_tile(player.x, player.y)[1]])
    
    # Updates the screen and completes the tick
    pygame.display.update()
    clock.tick(60)

#------------------------------------------------------------------------------------------------------1