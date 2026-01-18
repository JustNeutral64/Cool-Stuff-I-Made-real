#------------------------------------------------------------------------------------------------------
#Imports everything

import pygame
import time
from sys import exit
#------------------------------------------------------------------------------------------------------
#Variables

screen_width = 960
screen_height = 540
camera_zoom = 1
camera_zoom_addition_amount = 0.025

polygon_bottom_left_x = [-50]
polygon_bottom_left_y = [-23]
polygon_bottom_right_x = [20]
polygon_bottom_right_y = [-50]
polygon_top_left_x = [-30]
polygon_top_left_y = [42]
polygon_top_right_x = [51]
polygon_top_right_y = [61]
#------------------------------------------------------------------------------------------------------
#Functions

def normalize_for_x(old_value):
    return((old_value + (screen_width / 2))) #0, 0 is at the center of the screen

def normalize_for_y(old_value):
    return(((old_value * -1) + (screen_height / 2))) #0, 0 is at the center of the screen, +y goes up and vice versa

def camera_zoom_in():
    global camera_zoom
    camera_zoom += camera_zoom_addition_amount

def camera_zoom_out():
    global camera_zoom
    camera_zoom -= camera_zoom_addition_amount

def draw_polygons():
    for i in range(len(polygon_bottom_left_x)):
        
        #Bottom
        pygame.draw.line(screen, "red", (normalize_for_x(polygon_bottom_left_x[i] * camera_zoom), normalize_for_y(polygon_bottom_left_y[i] * camera_zoom)), (normalize_for_x(polygon_bottom_right_x[i] * camera_zoom), normalize_for_y(polygon_bottom_right_y[i] * camera_zoom)), 3)

        #Left
        pygame.draw.line(screen, "red", (normalize_for_x(polygon_bottom_left_x[i] * camera_zoom), normalize_for_y(polygon_bottom_left_y[i] * camera_zoom)), (normalize_for_x(polygon_top_left_x[i] * camera_zoom), normalize_for_y(polygon_top_left_y[i] * camera_zoom)), 3)

        #Right
        pygame.draw.line(screen, "red", (normalize_for_x(polygon_bottom_right_x[i] * camera_zoom), normalize_for_y(polygon_bottom_right_y[i] * camera_zoom)), (normalize_for_x(polygon_top_right_x[i] * camera_zoom), normalize_for_y(polygon_top_right_y[i] * camera_zoom)), 3)
        
        #Top
        pygame.draw.line(screen, "red", (normalize_for_x(polygon_top_left_x[i] * camera_zoom), normalize_for_y(polygon_top_left_y[i] * camera_zoom)), (normalize_for_x(polygon_top_right_x[i] * camera_zoom), normalize_for_y(polygon_top_right_y[i] * camera_zoom)), 3)

def create_new_polygon():
    length = len(polygon_bottom_left_x) - 1
    midpoint_bottom_x = polygon_bottom_left_x + (polygon_bottom_right_x - polygon_bottom_left_x) / 2
    midpoint_bottom_y = polygon_bottom_left_y + (polygon_bottom_right_y - polygon_bottom_left_y) / 2
    midpoint_left_x = polygon_bottom_left_x + (polygon_top_left_x - polygon_bottom_left_x) / 2
    midpoint_left_y = polygon_bottom_right_y + (polygon_top_right_y - polygon_bottom_right_y) / 2
    midpoint_right_x
    midpoint_right_y
    midpoint_top_x
    midpoint_top_y
#------------------------------------------------------------------------------------------------------
# Initializes pygame and sets up a few other things

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height)) #Sets the screen dimensions
pygame.display.set_caption("Did it work?")

clock = pygame.time.Clock()

#Font
#game_font = pygame.font.Font('Sprites/font/Pixeltype.ttf', 50)

#Background
background = pygame.Surface((960, 540)).convert_alpha() #Sets up the background sky as a large square
background.fill('#99ffff') #Fills the sky to be a solid color of light blue

#------------------------------------------------------------------------------------------------------
while True:

    #Sets some variables
    keys = pygame.key.get_pressed()

    # Handles miscellaneous events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if keys[pygame.K_SPACE]:
        camera_zoom_in()
    if keys[pygame.K_LSHIFT]:
        camera_zoom_out()
    

    if camera_zoom < 1:
        camera_zoom = 1
    
    if camera_zoom < len(polygon_bottom_left_x):
        create_new_polygon()
    
    screen.blit(background, (0, 0))

    draw_polygons()
    
    print(camera_zoom)

    pygame.display.update()
    clock.tick(60)
