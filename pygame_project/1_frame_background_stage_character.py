import pygame
import os
##############################################################
# basic requirements
pygame.init() # start pygame

# screen size setting
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# window caption
pygame.display.set_caption("Don's PyGame") # game caption

# FPS
clock = pygame.time.Clock()
##############################################################

# 1. user interface (background, game images, coordinates, speed, font, etc)
current_path = os.path.dirname(__file__) # return the location of the current file
image_path = os.path.join(current_path, "images") # return the location of "images" folder

# Background
background = pygame.image.load(os.path.join(image_path, "background.png"))

# Stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # to locate a character on the stage

# Character
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# Event Loop
running = True
while running:
    delta = clock.tick(30)

    # 2. events in pygame (keyboard, mouse, etc) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # closing the window
            running = False

    # 3. define game characters' locations

    # 4. collision check

    # 5. screen.blit (drawing on the screen)
    screen.blit(background, (0, 0))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    pygame.display.update() # have to update the screen in every single while loop

pygame.quit() # end pygame