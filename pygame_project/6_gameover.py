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

# Making balls
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))]

# Varying ball speed based on its size
ball_speed_y = [-18, -15, -12, -9]

# Balls
balls = []

# First big ball
balls.append({
    "pos_x" : 50, # x-coord
    "pos_y" : 50, # y-coord
    "img_idx" : 0, # image index ---> starting with the largest ball, then onto samller ones
    "to_x" : 3, # moving direction in x-axis
    "to_y" : -6, # moving direction in y-axis
    "init_spd_y" : ball_speed_y[0] # ball's initial speed in y-axis
})

# Disappearing weapon, ball
weapon_to_remove = -1
ball_to_remove = -1

# In-game font
game_font = pygame.font.Font(None, 40)

# Timer
total_time = 100
start_ticks = pygame.time.get_ticks() # start time

# Ending message:
'''
When the character is hit by the ball ---> Game Over
When the player runs out of time ---> Time Over
When the player successfully beats the level ---> Mission Complete
'''
game_result = "Game Over"

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

    # define ball location
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # bounce off the wall when the ball hits the wall
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        # ball's y position
        # when the ball hits the stage, set its speed to "initial speed"
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: # parabola effect
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. collision check

    # character rect info update
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # ball rect info update
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # ball and character collision
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # ball and weapon collision
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # weapon rect info update
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # collision check
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                # ball division when the weapon hits the ball
                if ball_img_idx < 3:
                    
                    # current ball size info
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # divided ball size info
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect() # current index + 1 = smaller ball
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # spliting in half: left ball
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # x-coord
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # y-coord
                        "img_idx" : ball_img_idx + 1, # image index ---> starting with the largest ball, then onto samller ones
                        "to_x" : -3, # moving direction in x-axis
                        "to_y" : -6, # moving direction in y-axis
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1] # ball's initial speed in y-axis
                    })

                    # spliting in half: right ball
                    balls.append({
                            "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # x-coord
                            "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # y-coord
                            "img_idx" : ball_img_idx + 1, # image index ---> starting with the largest ball, then onto samller ones
                            "to_x" : 3, # moving direction in x-axis
                            "to_y" : -6, # moving direction in y-axis
                            "init_spd_y" : ball_speed_y[ball_img_idx + 1] # ball's initial speed in y-axis
                    }) 
                break
        else:
            continue
        break
    
    # removing weapons as well as balls after collisions
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # when all ball are popped:
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    # 5. screen.blit (drawing on the screen)
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(character, (character_x_pos, character_y_pos))

    # Elapsed Time (Timer)
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms ---> s
    timer = game_font.render("Time: {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # Case: Time Over
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update() # have to update the screen in every single while loop

msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000) # delay 2 sec before closing the window

pygame.quit() # end pygame