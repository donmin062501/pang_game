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

# Character moving direction
character_to_x = 0

# Character moving speed
character_speed = 5

# Weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# Many weapons at a time (NOT ONLY ONE)
weapons = []

# Weapon speed
weapon_speed = 10

# Event Loop
running = True
while running:
    delta = clock.tick(30)

    # 2. events in pygame (keyboard, mouse, etc) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # closing the window
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key  == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. define game characters' locations
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # weapons location change
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons] # weapon going up

    # weapon disappearing after it hits the top
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 4. collision check

    # 5. screen.blit (drawing on the screen)
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(character, (character_x_pos, character_y_pos))

    pygame.display.update() # have to update the screen in every single while loop

pygame.quit() # end pygame