#------------------------------------------------------------------------------------------------------
#Imports everything

import pygame
import random
import time
from sys import exit

#------------------------------------------------------------------------------------------------------
# Variables Section

framerate = 60
screen_width = 960
screen_height = 540
program_state = "Placeholder"
fullscreen = False

#------------------------------------------------------------------------------------------------------
# Functions section

def normalize_for_x(input):
    return(input + screen_width / 2)

def normalize_for_y(input):
    return((input * -1) - (screen_height / 2))

def display_variables(names, values):
    if False:
        text = ""
        
        for i in range(len(names)):
            text += names[i] + ": "
            text += str(values[i])
            text += "\n"
        
        screen.blit(lexend_font.render(text, True, "#000000"), (10, 10))

#------------------------------------------------------------------------------------------------------
# Initialization section

pygame.init()

#Sets up screen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE, 0, 0, 1)
pygame.display.set_caption("Placeholder")

#Sets up mixer
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.8)
pygame.mixer.set_num_channels(32)

#Sets up fonts
lexend_font = pygame.font.Font('Fonts/Lexend-Light.ttf', 20)

#Sets up other things
clock = pygame.time.Clock()

#------------------------------------------------------------------------------------------------------
#Main Loop

while True: 
    
    start_time = time.time()
    
    #Screen width and screen height update
    screen_width, screen_height = pygame.display.get_surface().get_size()
    
    #Quitting Program and Fullscreen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                if fullscreen == False:
                    fullscreen = True
                    print("hi")
                    pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN, 0, 0, 1)
                else:
                    fullscreen = False
                    pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE, 0, 0, 1)
    
    #------------------------------------------------------------------------------------------------------
    #Main Code
    
    
    
    #------------------------------------------------------------------------------------------------------
    #Sets fps variable
    fps = (1 / (time.time() - start_time))
    
    pygame.display.update() #Updates the screen
    clock.tick(framerate) #Makes the game run at 60 fps

#------------------------------------------------------------------------------------------------------