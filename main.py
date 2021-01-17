import pygame
import random

def draw_floor():
    screen.blit(floor, (floor_x_pos, 610))
    screen.blit(floor, (floor_x_pos + 576, 610))

# Pipes

def create_pipe():
    random_pipe = random.choice(pipe_height)
    bottom_new_pipe = pipe_surface.get_rect(midtop=(620, random_pipe))
    top_pipe = pipe_surface.get_rect(midbottom=(620, random_pipe - 230))
    return top_pipe, bottom_new_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 1
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom > 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= 0 or bird_rect.bottom >= 610:
        death_sound.play()
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        # Could turn the text into a rectangle around it but not needed if no collison
        # score_rect = score_surface.get_rect(center=(285, 100))
        screen.blit(score_surface, (285, 100))
    if game_state == "game_over":
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(285, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(245, 400))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return score, high_score

pygame.init()

size = width, height = 576, 710

screen = pygame.display.set_mode(size)

color = 0, 200, 0

clock = pygame.time.Clock()

# Scores Fonts
game_font = pygame.font.Font('04B_19.TTF', 40)

#Press Space to play again font
space_font = pygame.font.Font('04B_19.TTF', 20)
press_space = space_font.render('Press Space to Play Again', True, (255, 255, 255))

# Game Variables

gravity = 0.10
bird_movement = 0
game_active = True
score = 0
high_score = 0

image_1 = pygame.image.load('sprites/background-day.png').convert()
image_1 = pygame.transform.scale(image_1, (576, 775))

floor = pygame.image.load('sprites/base.png')
floor = pygame.transform.scale(floor, (576, 100))
floor_x_pos = 0

pipe_surface = pygame.image.load('sprites/pipe-green.png')
pipe_surface = pygame.transform.scale(pipe_surface, (100, 270))
pipe_list = []
pipe_height = [500, 350, 400]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

bird_downflap = pygame.image.load('sprites/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('sprites/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('sprites/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 412))

BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP, 200)

# Look up what the convert method is and convert alpha
# bird_surface = pygame.image.load('sprites/bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
#
# # Takes new surface puts rectangle around it - first thing u have to do is grab one point from the rectangle - center
# bird_rect = bird_surface.get_rect(center=(100, 412))

game_over_surface = pygame.transform.scale2x(pygame.image.load('sprites/message.png').convert_alpha())

flap_sound = pygame.mixer.Sound('audio/wing.wav')
death_sound = pygame.mixer.Sound('audio/die.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')
score_sound_countdown = 100

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                """TypeError: unsupported operand type(s) for -=: 'pygame.Surface' and 'int' - means u are trying 
                to change the actual picture instead of variables around it"""
                """BIRD MOVEMENT IMPORTANT TO RESET IT HERE """
                bird_movement = 0
                bird_movement -= 2
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 412)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRD_FLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.fill(color)
    screen.blit(image_1, (0, 0))


    if game_active:
        # Could use some help on center y and rect methods
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        # Checking for collision
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, (100, 475))
        score, high_score = update_score(score, high_score)
        score_display('game_over')
        screen.blit(press_space, (160, 280))


    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)



"""WAS TRYING TO MAKE IT SMOOTHER WITH ARROW KEYS A WAY U CAN DO THIS IS SETTING A FLAG HAS ALL KEYS TO FALSE
 AND THEN FLAG THEM TRUE WHEN ITS A KEY DOWN SO UNTIL ANOTHER KEY IS PRESSED IT WILL STAY TRUE AND MOVE
iN FLAPPY BIRD U ONLY MOVE RIGHT HOWEVER THO """
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_RIGHT:
        #         right = True
        #


