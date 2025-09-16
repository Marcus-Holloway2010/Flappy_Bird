"""
Target: flappy game

Date:
    xx.xx.xx
    --------
    16.9.2025

Auther:
    Marc


Github       : https://github.com/Marcus-Holloway2010/Flappy_Bird


****
Python Version: 3.13.7
Pygame Version: 2.6.1

"""

import random
import time
import pygame

# pylint: disable=no-member

# START PYGAME MODULES
pygame.init()

# FUNCTIONS


def generate_pipe_rect():
    "Generate pipes"
    random_pipes = random.randrange(400, 800)
    pipe_rect_bottom = pipe_image.get_rect(midtop=(577, random_pipes))
    pipe_rect_top = pipe_image.get_rect(midbottom=(577, random_pipes - 300))
    return pipe_rect_bottom, pipe_rect_top


def move_pipe_rect(pipes):
    "Move pipes rect"
    for pipe in pipes:
        pipe.centerx -= 2
    inside_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return inside_pipes


def display_pips(pipes):
    "Show pipes"
    for pipe in pipes:
        if pipe.bottom >= 1024:
            main_screen.blit(pipe_image, pipe)

        else:
            reversed_pipes = pygame.transform.flip(pipe_image, False, True)
            main_screen.blit(reversed_pipes, pipe)


def check_collision(pipes):
    "Checks collisions"
    global ACTIVE_SCORE
    for pipe in pipes:
        if bird_image_rect.colliderect(pipe) or bird_image_rect.top <= 50 or bird_image_rect.bottom >= 900:
            game_over_sound.play()
            time.sleep(3)
            ACTIVE_SCORE = True
            return False

    return True


def bird_animation():
    "Animationing bird move"
    new_bird = bird_list[BIRD_LIST_INDEX]
    new_bird_rect = new_bird.get_rect(center=(100, bird_image_rect.centery))
    return new_bird, new_bird_rect


def display_score(status):
    "Show score"
    if status == "active":
        text1 = game_font.render(f"Score: {SCORE}", False, (255, 255, 255))
        text1_rect = text1.get_rect(center=(288, 100))
        main_screen.blit(text1, text1_rect)
    if status == "game_over":
        # SCORE
        text1 = game_font.render(f"Score: {SCORE}", False, (255, 255, 255))
        text1_rect = text1.get_rect(center=(288, 100))
        main_screen.blit(text1, text1_rect)

        # HIGH SCORE
        text2 = game_font.render(
            f"High Score: {HIGH_SCORE}", False, (255, 255, 255))
        text2_rect = text2.get_rect(center=(288, 850))
        main_screen.blit(text2, text2_rect)


def update_score():
    "Updates the score"
    global SCORE, HIGH_SCORE, ACTIVE_SCORE
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and ACTIVE_SCORE:
                SCORE += 1
                win_sound.play()
                ACTIVE_SCORE = False
            if pipe.centerx < 0:
                ACTIVE_SCORE = True

    if SCORE > HIGH_SCORE:
        HIGH_SCORE = SCORE
    return HIGH_SCORE


# ALL VARIABLE
DISPLAY_WIDTH = 576
DISPLAY_HEIGHT = 1024
FLOOR_X = 0
GRAVITY = 0.25
BIRD_MOVEMENT = 0
pipe_list = []
GAME_STATUS = True
BIRD_LIST_INDEX = 0
game_font = pygame.font.Font('assets/font/Flappy.TTF', 40)
SCORE = 0
HIGH_SCORE = 0
ACTIVE_SCORE = True

# ------------ #

create_pipe = pygame.USEREVENT
create_flap = pygame.USEREVENT + 1
pygame.time.set_timer(create_pipe, 1200)
pygame.time.set_timer(create_flap, 200)

# ------------- #
win_sound = pygame.mixer.Sound("assets/sound/smb_stomp.wav")
game_over_sound = pygame.mixer.Sound("assets/sound/smb_mariodie.wav")
# ------------- #

background_image = pygame.transform.scale2x(
    pygame.image.load("assets/img/bg2.png"))
floor_image = pygame.transform.scale2x(
    pygame.image.load("assets/img/floor.png"))

pipe_image = pygame.transform.scale2x(
    pygame.image.load("assets/img/pipe_green.png"))

bird_image_down = pygame.transform.scale2x(
    pygame.image.load("assets/img/red_bird_down_flap.png"))
bird_image_mid = pygame.transform.scale2x(
    pygame.image.load("assets/img/red_bird_mid_flap.png"))
bird_image_up = pygame.transform.scale2x(
    pygame.image.load("assets/img/red_bird_up_flap.png"))

game_over_image = pygame.transform.scale2x(
    pygame.image.load("assets/img/message.png"))
game_over_image_rect = game_over_image.get_rect(center=(288, 512))

bird_list = [bird_image_down, bird_image_up]
bird_image = bird_list[BIRD_LIST_INDEX]

# ------------- #

bird_image_rect = bird_image.get_rect(center=(100, 520))

# ------------- #
test_speed = 90
# GAME DISPLAY
main_screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))


pygame.time.set_timer(create_pipe, 1200)

# GAME TIMER
clock = pygame.time.Clock()


# GAME LOGIC
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # END PYGAME MODULES
            pygame.quit()
            # END PROGRAM (TERMINATE PROGRAM)
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                BIRD_MOVEMENT = 0
                BIRD_MOVEMENT -= 8

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                BIRD_MOVEMENT = 0
                BIRD_MOVEMENT -= 8

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                BIRD_MOVEMENT = 0
                BIRD_MOVEMENT += 8
            if event.key == pygame.K_r and GAME_STATUS == False:
                GAME_STATUS = True
                pipe_list.clear()
                bird_image_rect.center = (100, 512)
                BIRD_MOVEMENT = 0
                SCORE = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                test_speed += 10
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                test_speed -= 10

        if event.type == create_pipe:
            pipe_list.extend(generate_pipe_rect())

        if event.type == create_flap:
            if BIRD_LIST_INDEX == 1:
                BIRD_LIST_INDEX = 0
            else:
                BIRD_LIST_INDEX += 1
            bird_image, bird_image_rect = bird_animation()

    pipe_list = move_pipe_rect(pipe_list)
    # DISPLAY bg.png
    main_screen.blit(background_image, (0, 0))  # type: ignore.
    if GAME_STATUS:

        # DISPLAY red_bird_mid_flap.png
        main_screen.blit(bird_image, bird_image_rect)

        # CHECK FOR COLLISIONs
        GAME_STATUS = check_collision(pipe_list)

        # MOVE PIPES
        pipe_list = move_pipe_rect(pipe_list)
        display_pips(pipe_list)
        # FLOOR GRAVITY AND bird MOVEMENT
        BIRD_MOVEMENT += GRAVITY
        bird_image_rect.centery += BIRD_MOVEMENT

        # SHOW SCORE
        update_score()
        display_score("active")
    else:
        display_score("game_over")
        main_screen.blit(game_over_image, game_over_image_rect)

    # DISPLAY floor.png
    main_screen.blit(floor_image, (FLOOR_X, 900))
    main_screen.blit(floor_image, (FLOOR_X + 576, 900))
    if FLOOR_X <= -576:
        FLOOR_X = 0
    FLOOR_X -= 2

    pygame.display.update()
    # SET GAME SPEED
    clock.tick(test_speed)
