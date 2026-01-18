#Possible cool thing
framerate = 60

#------------------------------------------------------------------------------------------------------
#Imports everything

import pygame
import time
from sys import exit

#------------------------------------------------------------------------------------------------------
#Functions

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
    for i in range(len(rectangles)):
        bottom_left_x = normalize_for_x(rectangles[i].bottom_left_x - camera_x, 0)
        bottom_left_y = normalize_for_y(rectangles[i].bottom_left_y - camera_y, 0)
        top_right_x = normalize_for_x(rectangles[i].top_right_x - camera_x, 0)
        top_right_y = normalize_for_y(rectangles[i].top_right_y - camera_y, 0)
        width = top_right_x - bottom_left_x
        height = (top_right_y - bottom_left_y) * -1
        pygame.draw.rect(screen, "#ff00ff", pygame.Rect(bottom_left_x, top_right_y, width, height))
    
    for i in range(len(triangles)):
        x_1 = normalize_for_x(triangles[i].x1 - camera_x, 0)
        x_2 = normalize_for_x(triangles[i].x2 - camera_x, 0)
        x_3 = normalize_for_x(triangles[i].x3 - camera_x, 0)
        y_1 = normalize_for_y(triangles[i].y1 - camera_y, 0)
        y_2 = normalize_for_y(triangles[i].y2 - camera_y, 0)
        y_3 = normalize_for_y(triangles[i].y3 - camera_y, 0)
        pygame.draw.polygon(screen, "#0000ff", [(x_1, y_1), (x_2, y_2), (x_3, y_3)])

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
    for i in range(len(rectangles)):
        if (x + (width / 2) > rectangles[i].bottom_left_x and x - (width / 2) < rectangles[i].top_right_x and y + (height / 3.1) > rectangles[i].bottom_left_y and y - (height / 2) < rectangles[i].top_right_y):
            collision_detected = True
    
    return collision_detected
            
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

def display_variables():
    text = ""
    
    text += "x: "
    text += str(player.x // 1)
    
    text += "\n"
    text += "y: "
    text += str(player.y // 1)
    
    text += "\n"
    text += "grid_offset_x: "
    text += str(editor.grid_offset_x)
    
    text += "\n"
    text += "grid_offset_y: "
    text += str(editor.grid_offset_y)
    
    screen.blit(font.render(text, True, "#000000"), (10, 10))
#------------------------------------------------------------------------------------------------------
# Sets up variables

screen_width = 960
screen_height = 540
gravity = -0.60

camera_x_addition = 0
camera_y_addition = 0
smooth_camera_strength = 4
smooth_camera_smoothness = 0.125

program_state = 0

drawing_collision = True

#------------------------------------------------------------------------------------------------------
# Initializes pygame and sets up a few other things

#Pygame
pygame.init()

#Screen/Clock
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE, 0, 0, 1) #vsync is on and screen is resizable. Very cool!
pygame.display.set_caption("Did it work?")
clock = pygame.time.Clock()

#Font
font = pygame.font.Font('Sprites/font/Lexend-Light.ttf', 20)

#Backgrounds
background_1 = pygame.transform.scale(pygame.image.load('Sprites/Backgrounds/Sky.png'), (screen_height * 2, screen_height)).convert_alpha()

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

        self.width = 40
        self.height = 98

        self.acceleration = 0.4
        self.air_resistance = 0.2
        self.speed_cap = 20
        self.jump_force = 15
        self.coyote_time = 6
        self.angle = 0

        #Sets image
        self.direction_prefix = "Right"
        self.sprite_index = 0
        self.sprite = pygame.transform.scale(pygame.image.load('Sprites/Players/Sonic/sonicRight00.png'), (100, 100)).convert_alpha()

    #------------------------------------------------------------------------------------------------------
    
    def move_in_steps(self, steps):
        self.fall_counter += 1
        for i in range(steps * 1):
            
            last_value = self.x
            self.x += self.dx / (steps * 1)
            
            # TODO fix hitbox when character sprite changes from placeholder sprites to be accurate
            if colliding(self.x, self.y, self.width * 0.95, self.height) == True:
                self.collide_x_slope_or_wall(last_value, steps)

            #-----
            
            last_value = self.y
            self.y += self.dy / (steps * 1)
            
            if colliding(self.x, self.y, self.width * 0.95, self.height) == True:
                self.collide_y_ceiling_or_floor(last_value, steps)

    def collide_x_slope_or_wall(self, last_value, steps):
        if colliding(self.x, self.y + abs((self.dx) / steps), self.width * 0.95, self.height) == True:
            self.x = last_value
            self.dx = 0
        else:
            self.y += abs((self.dx) / steps)
            self.dx -= 0.03 * abs(self.dx) / self.dx
        
    def collide_y_ceiling_or_floor(self, last_value, steps):
        self.y = last_value
        if self.dy > 0:
            self.dy = 0
        else:
            if self.fall_counter > 0:
                self.fall_counter = 0
                self.slip()
            self.fall_counter = 0
            self.dy *= 0.85
        
    def slip(self):
        if colliding(self.x + 1.75, self.y - 2, self.width * 0.95, self.height) == False:
            self.fall_counter = self.coyote_time
            self.dx += 1
            self.x += 1.75
            self.y -= 2
        if colliding(self.x - 1.75, self.y - 2, self.width * 0.95, self.height) == False:
            self.fall_counter = self.coyote_time
            self.dx -= 1
            self.x -= 1.75
            self.y -= 2
            
    def movement_up_and_down(self):
        self.dy += gravity

        if keys[pygame.K_SPACE]:
            if self.fall_counter <= self.coyote_time:
                self.dy = self.jump_force
                self.fall_counter = self.coyote_time
        
        if keys[pygame.K_v]:
            self.dy += self.jump_force / 15
    
    def movement_left_and_right(self):
        if keys[pygame.K_a] and self.dx > self.speed_cap * -1:
            self.dx -= self.acceleration
        
        if keys[pygame.K_d] and self.dx < self.speed_cap:
            self.dx += self.acceleration
        
        if abs(self.dx) > self.air_resistance:
            self.dx -= self.air_resistance * (self.dx / abs(self.dx))
        else:
            self.dx = 0

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
        sprite_index_additor = 0.1 + (abs(self.dx) * 0.015)
        
        # Set Direction Prefix
        if keys[pygame.K_d]:
            self.direction_prefix = "Right"
        elif keys[pygame.K_a]:
            self.direction_prefix = "Left"
        
        #-----
        
        # In air
        if self.fall_counter > self.coyote_time:
            self.sprite_index += sprite_index_additor + 0.1
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
            # Grounded and moving, not at speed cap
            else:
                self.sprite_index += sprite_index_additor
                if self.sprite_index < 1 or self.sprite_index >= 9:
                    self.sprite_index = 1
        
        #-----
        
        # Fixes naming bug
        # TODO Fix Naming bug without these lines of code (just rename the images lmao)
        if self.sprite_index < 10:
            fixed_sprite_index = "0" + str(int(self.sprite_index))
        else:
            fixed_sprite_index = str(int(self.sprite_index))
        
        # Final Sprite
        self.sprite = pygame.transform.scale(pygame.image.load('Sprites/Players/Sonic/sonic' + self.direction_prefix + fixed_sprite_index + '.png'), (100, 100)).convert_alpha()
    
    def draw_hitbox(self):
        bl_x = normalize_for_x((self.x - self.width / 2) - camera_x, 0)
        bl_y = normalize_for_y((self.y - self.height / 2) - camera_y, 0)
        tr_x = normalize_for_x((self.x + self.width / 2) - camera_x, 0)
        tr_y = normalize_for_y((self.y + self.height / 3.1) - camera_y, 0)
        pygame.draw.polygon(screen, "#000000", [(bl_x, bl_y), (bl_x, tr_y), (tr_x, tr_y), (tr_x, bl_y)])

    #------------------------------------------------------------------------------------------------------
        
    def update(self):
        
        self.movement_up_and_down()
        self.movement_left_and_right()

        self.move_in_steps(int((abs(self.dy) + abs(self.dx) + 1)))
        self.set_sprite()

        self.calculate_camera_coordinates()
        
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
        
        self.toggle_grid()

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
#Assign Classes

player = Player()
rectangles = [Level_Rect_Collision(-15000, -270, 15000, -220), Level_Rect_Collision(100, -220, 400, -160), Level_Rect_Collision(160, -160, 400, -100), Level_Rect_Collision(220, -100, 400, -40), Level_Rect_Collision(-400, -100, -100, -40), Level_Rect_Collision(400.0, -250.0, 950.0, -200.0)]
triangles = [Level_Tri_Collision(0, 100, 300, 100, 150, 200), Level_Tri_Collision(500, 100, 900, 100, 900, 300), Level_Tri_Collision(900.0, -200.0, 1300.0, -200.0, 1300.0, 0.0), Level_Tri_Collision(1250.0, -50.0, 1650.0, -50.0, 1650.0, 350.0), Level_Tri_Collision(1600.0, 300.0, 1950.0, 300.0, 1950.0, 750.0)]
editor = Editor()

#------------------------------------------------------------------------------------------------------
#Main game loop

while True:
    
    screen_width, screen_height = pygame.display.get_surface().get_size()
    if screen_width / 2 >= screen_height:
        background_1 = pygame.transform.scale(pygame.image.load('Sprites/Backgrounds/Sky.png'), (screen_width, screen_width * 2)).convert_alpha()
    else:
        background_1 = pygame.transform.scale(pygame.image.load('Sprites/Backgrounds/Sky.png'), (screen_height * 2, screen_height)).convert_alpha()
    
    if program_state == 0:
        # Sets the input variables
        keys = pygame.key.get_pressed()
        

        # Handles miscellaneous events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    editor.x = player.x
                    editor.y = player.y
                    
                    program_state = 1
        
        # Updates the player class
        player.update()

        # Draws objects
        screen.blit(background_1, (0, 0))
        screen.blit(player.sprite, (normalize_for_x(player.x - camera_x, 100), normalize_for_y(player.y - camera_y, 100)))
        player.draw_hitbox()
        draw_collision()
    
    #----------------------------------------------------------------------------------------------------
    
    elif program_state == 1:
        
        # Sets the input variables
        keys = pygame.key.get_pressed()
        keys_pressed = pygame.key.get_just_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_just_pressed()
        mouse = pygame.mouse.get_pressed()
        
        # Handles miscellaneous events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    player.x = editor.x
                    player.y = editor.y
                    program_state = 0
        
        #Updates the editor
        editor.update()
        
        #Draws objects
        screen.blit(background_1, (0, 0))
        draw_collision()
        
        #Draws grid lines
        if editor.grid_enabled == True:
            editor.draw_grid_lines()
        
        if keys[pygame.K_0]:
            print_rectangles_and_triangles()
    
    
    
    # Updates the screen and completes the tick
    display_variables()
    pygame.display.update()
    clock.tick(framerate)

#------------------------------------------------------------------------------------------------------