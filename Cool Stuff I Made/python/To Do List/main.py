
"""
TO-DO:
fix the time in the time box being a bit jittery
make animations and other things work correctly on different framerates (primarily 30, 60, 120, 240) 
"""

#------------------------------------------------------------------------------------------------------
#Imports everything

import pygame
import time
import datetime
from random import randrange
import sys
from math import *
import ctypes

#Sine & Cosine Number is 57.295779513

#------------------------------------------------------------------------------------------------------
# Initializes pygame and sets up a few other things

#Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(1)
pygame.mixer.set_num_channels(32)

#Screen/Clock
screen_width = 800
screen_height = 450
window = pygame.Window(size = (800, 450), allow_high_dpi = True, resizable = True)
screen_width *= 2
screen_height *= 2
screen = window.get_surface()
clock = pygame.time.Clock()

#Font
lexend_light_40 = pygame.font.Font('Fonts/Lexend-Light.ttf', 40)
lexend_light_35 = pygame.font.Font('Fonts/Lexend-Light.ttf', 35)
lexend_regular_30 = pygame.font.Font('Fonts/Lexend-Regular.ttf', 30)
lexend_bold_70 = pygame.font.Font('Fonts/Lexend-Bold.ttf', 70)

#Sprites
settings_button = pygame.transform.scale(pygame.image.load('Sprites/ClassicTheme/SettingsButton.png'), (36, 36)).convert_alpha()
trash_button = pygame.transform.scale(pygame.image.load('Sprites/ClassicTheme/TrashIcon.png'), (90, 90)).convert_alpha()
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

def display_variables(names, values, x, y):
    text = ""
    
    for i in range(len(names)):
        text += names[i] + ": "
        text += str(values[i])
        text += "\n"
    
    screen.blit(lexend_light_40.render(text, True, "#000000"), (x, y))

def get_time(): #Gets the time and stores it in variables
    global day, month, month_number, time_hours, time_minutes, time_seconds, time_decaseconds, year_number, current_year
    full_time = time.asctime()
    exact_time = time.time()
    #Sun Apr  6 14:57:05 20251743965825.5590801
    day = full_time[0:3]
    month = full_time[4:7]
    month_number = full_time[8:10]
    year_number = int(month_number)
    time_hours = full_time[11:13]
    if time_hours[0] == "0": #Remove that 0 (ex: 09:15 turns to 9:15)
        time_hours = time_hours[1]
    time_minutes = full_time[14:16]
    time_seconds = full_time[17:19]
    time_decaseconds = (exact_time % 1 - exact_time % 0.1)
    time_decaseconds = ((time_decaseconds * 10) // 1) / 10 #Fix rounding errors because they are horrible
    now = datetime.datetime.now()
    current_year = int(now.year)
    
    match day: #Removes the shortening
        case "Sun":
            day = "Sunday"
        case "Mon":
            day = "Monday"
        case "Tue":
            day = "Tuesday"
        case "Wed":
            day = "Wednesday"
        case "Thu":
            day = "Thursday"
        case "Fri":
            day = "Friday"
        case "Sat":
            day = "Saturday"
        case _:
            day = "THE WORLD HAS ENDED WHAT HAVE YOU DONE!?!?"
    
    match month: #Removes the shortening and also gets the year number (excluding leap years)
        case "Jan":
            month = "January"
        case "Feb":
            month = "February"
            year_number += 31
        case "Mar":
            month = "March"
            year_number += 59
        case "Apr":
            month = "April"
            year_number += 90
        case "May":
            month = "May"
            year_number += 120
        case "Jun":
            month = "June"
            year_number += 151
        case "Jul":
            month = "July"
            year_number += 181
        case "Aug":
            month = "August"
            year_number += 212
        case "Sep":
            month = "September"
            year_number += 243
        case "Oct":
            month = "October"
            year_number += 273
        case "Nov":
            month = "November"
            year_number += 304
        case "Dec":
            month = "December"
            year_number += 334
        
    #Leap Year
    if month != "January":
        if year % 100 == 0 and year % 400 != 0 and year % 4 == 0:
            year_number += 1

def draw_screen(): #Draws everything to the screen (Except the degugging variables)
    global frame
    global fps
    
    # Draws background
    pygame.draw.rect(screen, "#FFFFFF", pygame.Rect(0, 0, screen_width, screen_height))
    
    #Draws trash can icon
    screen.blit(trash_button, (10, 10))
    
    #Draws title
    text_surface = lexend_bold_70.render("To-Do List:", True, "#000000")
    rect = text_surface.get_rect(midtop = (normalize_for_x(0, 0), 10))
    screen.blit(text_surface, rect)
    
    #Draws the time and date box at the top right
    #Date and Box Outline
    text = day + ", " + month + " " + month_number + ", " + str(year)
    text_surface = lexend_light_40.render(text, True, "#000000")
    rect = text_surface.get_rect(topright = (screen_width - 10, 5))
    pygame.draw.rect(screen, "#000000", pygame.Rect(normalize_for_x(screen_width / 2 - rect.width - 17, 0), -10, rect.width + 50, rect.height * 2 + 15), 4)
    screen.blit(text_surface, rect)
    
    draw_time()
    
    #Draws to-do list
    to_do_list.draw()
    #Draws the rect separating the ToDoIst and the input
    if to_do_list.selected_index == False and type(to_do_list.selected_index) == bool:
        pygame.draw.rect(screen, "#EEEEEE", pygame.rect.Rect(0, screen_height - 150, screen_width, 150))
        pygame.draw.line(screen, "#000000", (0, screen_height - 150), (screen_width, screen_height - 150), 3) #Outline
    else:
        pygame.draw.rect(screen, "#EEEEEE", pygame.rect.Rect(0, screen_height - 300, screen_width, 300))
        pygame.draw.line(screen, "#000000", (0, screen_height - 300), (screen_width, screen_height - 300), 3) #Outline
    #Draws all text boxes
    for box in text_input_boxes:
        box.draw()
    #Draws all buttons
    for button in buttons:
        button.draw()

#This is complicated enough to be it's own separate function
def draw_time():
    text = [str(time_hours), ": ", str(time_minutes), ": ", str(time_seconds)]
    positions = [176, 126, 116, 66, 56]
    
    for i in range(len(text)):
        text_surface = lexend_light_40.render(text[i][0], True, "#000000")
        rect = text_surface.get_rect(topleft = (screen_width - positions[i], 50))
        screen.blit(text_surface, rect)
        
        text_surface = lexend_light_40.render(text[i][1], True, "#000000")
        rect = text_surface.get_rect(topleft = (screen_width - positions[i] + 23, 50))
        screen.blit(text_surface, rect)
    
#------------------------------------------------------------------------------------------------------
#Variables (Screen width/height are set up above)

framerate = 60 #Actual Framerate
frame = 0 #The frame the program is in
fps = [] #What the max fps could be
avg_fps = 0 #Will be used to calculate the average fps when the program is running.

day = "" #The Current Day (Sunday through Saturday)
month = "" #The Current Month (January through December)
month_number = "" #The day of the Month (Ex: if it's april 15 then month_number would be set to 15)
time_hours = 0 #The current time in hours
time_minutes = 0 #The current time in minutes
time_seconds = 0 #The current time in seconds
time_decaseconds = 0 #The current time in decaseconds
year = 2025 #The current year
get_time()
to_do_list_file_path = "Data/to_do_list.txt"
last_day_file_path = "Data/last_day.txt"

#Gets data from list
data = open(to_do_list_file_path).readlines()
formatted_data = []
line = 0
for i in range(int(len(data) / 5)):
    formatted_data.append([])
    for x in range(5):
        item = data[line]
        item = item[0:len(item) - 1]
        try:
            item = int(item)
        except:
            if item == "False":
                item = False
            elif item == "True":
                item = True
        formatted_data[i].append(item)
        line += 1
del(data)
del(line)

#Saves month number
last_year_number = int(open(last_day_file_path).readlines()[0])
with open(last_day_file_path, "w") as file:
    file.write(str(year_number))
#------------------------------------------------------------------------------------------------------
#Classes
class Button:
    
    def __init__(self, left_x, right_x, bottom_y, top_y, visible, inactive_fill_color, hover_fill_color, active_fill_color, outline_color, outline_width, text):
        self.left_x = left_x
        self.right_x = right_x
        self.bottom_y = bottom_y
        self.top_y = top_y
        self.inactive_fill_color = inactive_fill_color
        self.hover_fill_color = hover_fill_color
        self.active_fill_color = active_fill_color
        self.fill_color = inactive_fill_color
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.text = text
        self.active = False
        self.visible = visible
        self.width = right_x - left_x
        self.height = top_y - bottom_y
        
        self.text_surface = lexend_light_40.render(self.text, True, "#000000")

    def handle_event(self, event):
        mouse_colliding = (mouse_pos[0] >= self.left_x and mouse_pos[0] <= self.right_x) and (mouse_pos[1] >= self.bottom_y and mouse_pos[1] <= self.top_y)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_colliding:
                self.active = True
                self.fill_color = self.active_fill_color
            else:
                self.active = False
                self.fill_color = self.inactive_fill_color
        elif event.type == pygame.MOUSEBUTTONUP:
            if mouse_colliding:
                self.active = False
                self.fill_color = self.hover_fill_color
            else:
                self.fill_color = self.inactive_fill_color
        elif self.active == False:
            if mouse_colliding:
                self.fill_color = self.hover_fill_color
            else:
                self.active = False
                self.fill_color = self.inactive_fill_color
    
    def update_position(self, left_x, right_x, bottom_y, top_y):
        self.left_x = left_x
        self.right_x = right_x
        self.bottom_y = bottom_y
        self.top_y = top_y
        self.width = right_x - left_x
        self.height = top_y - bottom_y
    
    def draw(self):
        pygame.draw.rect(screen, self.fill_color, pygame.Rect(normalize_for_x(self.left_x, 0), normalize_for_y(self.top_y, 0), self.width, self.height))
        pygame.draw.rect(screen, self.outline_color, pygame.Rect(normalize_for_x(self.left_x, 0), normalize_for_y(self.top_y, 0), self.width, self.height), 3)
        screen.blit(self.text_surface, (normalize_for_x(self.left_x, -5), normalize_for_y(self.top_y, 0))) #The negative width and height move the text a bit more inside the box
    
class textInput:
    
    def __init__(self, left_x, right_x, bottom_y, top_y, title, inactive_fill_color, hover_fill_color, active_fill_color, outline_color, outline_width, number_input_only):
        self.left_x = left_x
        self.right_x = right_x
        self.bottom_y = bottom_y
        self.top_y = top_y
        self.title = title
        self.inactive_fill_color = inactive_fill_color
        self.hover_fill_color = hover_fill_color
        self.active_fill_color = active_fill_color
        self.fill_color = inactive_fill_color
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.number_input_only = number_input_only
        self.text = ""
        self.active = False
        self.width = right_x - left_x
        self.height = top_y - bottom_y
        
        self.text_surface = lexend_light_40.render(self.text, True, "#000000")
        self.title_surface = lexend_regular_30.render(self.title, True, "#000000")
    
    def handle_event(self, event):
        mouse_colliding = (mouse_pos[0] >= self.left_x and mouse_pos[0] <= self.right_x) and (mouse_pos[1] >= self.bottom_y and mouse_pos[1] <= self.top_y)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_colliding:
                self.active = True
                self.fill_color = self.active_fill_color
            else:
                self.active = False
                self.fill_color = self.inactive_fill_color
        elif self.active == False:
            if mouse_colliding:
                self.fill_color = self.hover_fill_color
            else:
                self.active = False
                self.fill_color = self.inactive_fill_color

        if event.type == pygame.KEYDOWN and self.active:
            if self.active == True:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.fill_color = self.inactive_fill_color
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif self.number_input_only == True:
                    if event.unicode.isdigit():
                        self.text += event.unicode
                else:
                    self.text += event.unicode
                    
            self.text_surface = lexend_light_35.render(self.text, True, "#000000")  
    
    def update_position(self, left_x, right_x, bottom_y, top_y):
        self.left_x = left_x
        self.right_x = right_x
        self.bottom_y = bottom_y
        self.top_y = top_y
        self.width = right_x - left_x
        self.height = top_y - bottom_y
    
    def draw(self):
        #Draws the title
        screen.blit(self.title_surface, self.title_surface.get_rect(midbottom = (normalize_for_x(self.left_x + (self.width / 2), 0), normalize_for_y(self.top_y, 0) - 2)))
        #Draws the fill-in
        pygame.draw.rect(screen, self.fill_color, pygame.Rect(normalize_for_x(self.left_x, 0), normalize_for_y(self.top_y, 0), self.width, self.height))
        #Draws the outline
        pygame.draw.rect(screen, self.outline_color, pygame.Rect(normalize_for_x(self.left_x, 0), normalize_for_y(self.top_y, 0), self.width, self.height), 3)
        #Draws the text
        screen.blit(self.text_surface, (normalize_for_x(self.left_x, -15), normalize_for_y(self.top_y, -10))) #The negative width and height move the text a bit more inside the box

#Making this a class for when I make it so that you can have more than one to-do list and possibly have multiple on screen at once
class toDoList:
    
    def __init__(self, items):
        self.items = items #Name, days_left, is_important, time_interval, is_finished
        self.selected_index = False
        
    def add_item(self, name, days_left, is_important, time_interval):
        self.items.append([name, days_left, is_important, time_interval, False])
        self.sort()
    
    def handle_event(self):
        global buttons
        global text_input_boxes
        
        y = 140
        i = 0
        while i < len(self.items):
            
            #Sets Finished Tasks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if original_mouse_pos[0] >= 9 and original_mouse_pos[0] <= 45 and original_mouse_pos[1] >= y + 8 and original_mouse_pos[1] <= y + 45:
                    #Uncheck and check tasks
                    self.items[i][4] = not self.items[i][4]
                    self.sort()
                if original_mouse_pos[1] < screen_height - 300: #Click off settings
                    self.selected_index = False
                    buttons = [Button(screen_width / 2 - 50, screen_width / 2, 50 - screen_height / 2, 100 - screen_height / 2, True, "#00FF00", "#00DD00", "#00BB00", "#000000", 4, "ADD ITEM")]
                    buttons[0].update_position(screen_width / 2 - 250, screen_width / 2 - 50, 50 - screen_height / 2, 100 - screen_height / 2)
                    text_input_boxes = [textInput(50 - screen_width / 2, 0 - screen_width * 0.15, 50 - screen_height / 2, 100 - screen_height / 2, "Item Name", "#FFFFFF", "#E9E9E9", "#CCCCCC", "#000000", 4, False)]
                    text_input_boxes.append(textInput(20 - screen_width * 0.15, screen_width * 0.3, 50 - screen_height / 2, 100 - screen_height / 2, "Days until due", "#FFFFFF", "#E9E9E9", "#CCCCCC", "#000000", 4, False))
                    text_input_boxes[0].update_position(50 - screen_width / 2, screen_width / 2 - 650, 50 - screen_height / 2, 100 - screen_height / 2)
                    text_input_boxes[1].update_position(screen_width / 2 - 600, screen_width / 2 - 300, 50 - screen_height / 2, 100 - screen_height / 2)
                if original_mouse_pos[0] >= screen_width - 300 and original_mouse_pos[0] <= screen_width - 264 and original_mouse_pos[1] >= y + 8 and original_mouse_pos[1] <= y + 45: #Click on settings
                    self.selected_index = i
                    buttons = []
                    text_input_boxes = [textInput(50, screen_width / 2 - 50, 200 - screen_height / 2, 250 - screen_height / 2, "Item Name", "#FFFFFF", "#E9E9E9", "#CCCCCC", "#000000", 4, False)]
                    text_input_boxes.append(textInput(50, screen_width / 2 - 50, 50 - screen_height / 2, 100 - screen_height / 2, "Days until due", "#FFFFFF", "#E9E9E9", "#CCCCCC", "#000000", 4, False))
                    text_input_boxes[0].text = str(to_do_list.items[to_do_list.selected_index][0])
                    text_input_boxes[0].text_surface = lexend_light_35.render(text_input_boxes[0].text, True, "#000000")
                    text_input_boxes[1].text = str(to_do_list.items[to_do_list.selected_index][1])
                    text_input_boxes[1].text_surface = lexend_light_35.render(text_input_boxes[1].text, True, "#000000")
                    
                    i += 1000 #Breaks loop
                
            i += 1
            y += 50
            
    def sort(self): 
        
        #Sorts for due date
        self.items = sorted(self.items, key=lambda index: index[1])
        
        #Sorts for finished
        unfinished_index = 0 #This is the point to add unfinished items
        output_list = []
        for item in self.items:
            if item[4] == False:
                output_list.insert(unfinished_index, item)
                unfinished_index += 1
            else:
                output_list.append(item)
        self.items = output_list
        
    def delete_finished_items(self):
        finished_indexes = []
        
        #Gets Finished Indexes
        for i in range(len(self.items)):
            if self.items[i][4] == True:
                finished_indexes.append(i)
        
        #Gets deletes all finished items using finished indexes list
        finished_indexes = reversed(finished_indexes) #Prevent Crash from having more than 1 finished task (go through it when you have more than one finished task and you will see what I mean)
        for index in finished_indexes:
            self.items.remove(self.items[index])
    
    def day_pass_actions(self): #This is now 2 functions. May split up more if needed
        
        self.delete_finished_items()
        
        #Increments all days left by one for each item (unless it's at 0!)
        for item in self.items:
            if item[1] > 0:
                item[1] -= 1
    
    def save_list(self):
        text_data = ""
        for item in self.items:
            for segment in item:
                text_data += str(segment)
                text_data += "\n"
        with open(to_do_list_file_path, "w") as file:
            file.write(text_data)
        
    def draw(self):
        
        #There is no x because it stays the same throughout drawing
        y = 140
        
        for i in range(len(self.items)):
            
            #Gets text color
            text_color = (0, 0, 0)
            if self.items[i][4] == True: #Finished task
                text_color = (125, 125, 125)
            elif self.items[i][1] <= 3:
                text_color = (255, 0, 0)
            elif self.items[i][1] <= 7:
                text_color = (128, 0, 0)
                
            
            #When you hover over an item
            if normalize_for_y(mouse_pos[1], 0) >= y and normalize_for_y(mouse_pos[1], 0) < y + 50:
                #Set active index
                pygame.draw.rect(screen, "#DDDDDD", pygame.Rect(0, y + 1, screen_width, 50)) #Backround
                pygame.draw.rect(screen, "#000000", pygame.Rect(9, y + 8, 36, 36)) #Checkbox
                screen.blit(settings_button, settings_button.get_rect(topleft=(screen_width - 300, y + 8)))#Settings Menu
            
            #Text on left
            text = "    "
            text += self.items[i][0]
            text += "\n"
            text_surface = lexend_light_40.render(text, True, text_color)
            #Item Text Shaking
            if self.items[i][1] == 0 and self.items[i][4] == False:
                rect = text_surface.get_rect(topleft = (randrange(8, 12), randrange(y - 3, y + 3)))
            else:
                rect = text_surface.get_rect(topleft = (10, y))
            screen.blit(text_surface, rect)
            
            #Text on right
            text = str(self.items[i][1])
            if self.items[i][4] == True:
                text = "Finished!"
            elif text == "0":
                text += " days left"
            elif text == "1":
                text += " day left"
            else:
                text += " days left"
            
            text_surface = lexend_light_40.render(text, True, text_color)
            
            #Due date text shaking
            if self.items[i][1] == 0 and self.items[i][4] == False:
                rect = text_surface.get_rect(topright = (randrange(screen_width - 12, screen_width - 8), randrange(y - 2, y + 2)))
            else:
                rect = text_surface.get_rect(topright = (screen_width - 10, y))
            
            #Cross Out Text
            if self.items[i][4] == True:
                pygame.draw.line(screen, text_color, (50, y + 28), (screen_width - 10, y + 28), 3)
            
            screen.blit(text_surface, rect)
            
            
            y += 50 #Add a bit of a space between items

#------------------------------------------------------------------------------------------------------
#Assign Classes
#left_x, right_x, bottom_y, top_y, blank_text, inactive_fill_color, active_fill_color, outline_color, outline_width, number_input_only, bottom_anchored
#Note that these positions do not accurately reflect the actual positions of the text boxes, but the update_position functions do.
text_input_boxes = [textInput(50 - screen_width / 2, 0 - screen_width * 0.15, 50 - screen_height / 2, 100 - screen_height / 2, "Item Name", "#FFFFFF", "#E9E9E9", "#CCCCCC", "#000000", 4, False)]
text_input_boxes.append(textInput(20 - screen_width * 0.15, screen_width * 0.3, 50 - screen_height / 2, 100 - screen_height / 2, "Days until due", "#FFFFFF", "#E9E9E9", "#CCCCCC", "#000000", 4, True))

#self, left_x, right_x, bottom_y, top_y, visible, inactive_fill_color, hover_fill_color, active_fill_color, outline_color, outline_width, text
buttons = [Button(screen_width / 2 - 50, screen_width / 2, 50 - screen_height / 2, 100 - screen_height / 2, True, "#00FF00", "#00DD00", "#00BB00", "#000000", 4, "ADD ITEM")]

#Does day pass actions
to_do_list = toDoList(formatted_data)
#Preset
if True:
    to_do_list = toDoList(
                        [['Item 1', 1, True, False, False], 
                        ['Item 2', 2, True, False, False], 
                        ['Item 3', 3, True, False, False], 
                        ['Item 4', 4, True, False, False], 
                        ['Item 5', 5, True, False, False], 
                        ['Item 6', 6, True, False, False], 
                        ['Item 7', 7, True, False, False],
                        ['Item 8', 8, True, False, False], 
                        ['Item 9', 9, True, False, False], 
                        ['Item 10', 10, True, False, True]])
to_do_list.sort()
if last_year_number > year_number:
    last_year_number -= 365
    if month != "January":
        if (year - 1) % 100 == 0 and (year - 1) % 400 != 0 and (year - 1) % 4 == 0:
            last_year_number -= 1
for i in range(year_number - last_year_number):
    to_do_list.day_pass_actions()
#------------------------------------------------------------------------------------------------------
#Main Loop

while True:
    
    #Set start time, screen width, screen height, gets mouse coordinates
    start_time = time.time()
    screen_width, screen_height = window.size
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = (convert_for_x(mouse_pos[0], 0), (convert_for_y(mouse_pos[1], 0))) #what why does this work anyways im not gonna care that much about it
    original_mouse_pos = ((mouse_pos[0] + screen_width / 2), (mouse_pos[1] - screen_height / 2) * -1) #I'm gonna hope this still works
    #Gets the time and stores it in the variables
    get_time()
    
    #Updates position of multiple elements
    if str(to_do_list.selected_index) == "False":
        text_input_boxes[0].update_position(50 - screen_width / 2, screen_width / 2 - 650, 50 - screen_height / 2, 100 - screen_height / 2)
        text_input_boxes[1].update_position(screen_width / 2 - 600, screen_width / 2 - 300, 50 - screen_height / 2, 100 - screen_height / 2)
        buttons[0].update_position(screen_width / 2 - 250, screen_width / 2 - 50, 50 - screen_height / 2, 100 - screen_height / 2)
    else:
        text_input_boxes[0].update_position(50, screen_width / 2 - 50, 200 - screen_height / 2, 250 - screen_height / 2)
        text_input_boxes[1].update_position(50, screen_width / 2 - 50, 50 - screen_height / 2, 100 - screen_height / 2)
    
    #Handles Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            to_do_list.save_list()
            pygame.quit()
            sys.exit()
        
        for box in text_input_boxes:
            box.handle_event(event)
        for button in buttons:
            button.handle_event(event)
        
        to_do_list.handle_event()
        
        #Handles Misc Events (Trashcan):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if original_mouse_pos[0] >= 10 and original_mouse_pos[0] <= 100 and original_mouse_pos[1] >= 10 and original_mouse_pos[1] <= 100:
                to_do_list.delete_finished_items()
    
    #Handles the button that adds stuff to the to-do list
    if str(to_do_list.selected_index) == "False":
        if buttons[0].active == True and (text_input_boxes[0].text != "" and text_input_boxes[1].text != ""):
            try:
                check_if_second_text_box_contains_number_and_is_more_than_zero = int(text_input_boxes[1].text)
                if check_if_second_text_box_contains_number_and_is_more_than_zero < 0:
                    print(int(text_input_boxes[0].text)) #Cause error on purpose, this can be improved
                to_do_list.add_item(text_input_boxes[0].text, int(text_input_boxes[1].text), False, False)
                text_input_boxes[0].text = ""
                text_input_boxes[0].text_surface = lexend_light_35.render("", True, "#000000") 
                text_input_boxes[1].text = ""
                text_input_boxes[1].text_surface = lexend_light_35.render("", True, "#000000") 
                buttons[0].active == False
            except:
                print("Input is incorrect")
    else: #Handles editor
        pass
    
    
    #Draws everything to the screen
    draw_screen()
    
    
    #Handles FPS tracker
    frame += 1
    
    #Fix crash in case someone actually manages to keep the app open for 59 days.
    if frame >= 2147483000:
        frame = 10
        fps = [14, 14, 14, 14, 14, 14, 14, 14, 14, 14]
        print("how")
    
    fps.append((1 / (time.time() - start_time)))
    if frame % 10 == 0:
        avg_fps = (fps[0] + fps[1] + fps[2] + fps[3] + fps[4] + fps[5] + fps[6] + fps[7] + fps[8] + fps[9]) / 10
        fps = []
    elif frame > 2147483000: #Fix some things breaking with fps going above the limit
        frame = 0
    
    display_variables(["Fps"], [avg_fps // 1], -1000, 50)
    # Updates the screen completes the tick
    window.flip()
    clock.tick(60)

#------------------------------------------------------------------------------------------------------




