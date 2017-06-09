#!/usr/bin/env python3
'''Main game loop for pygame'''

import pygame
import window
import block
import player
import time

# RGB colour definitions
WHITE = (255, 255, 255)

# Frames per second defintion
FPS = 60

# Initialise pygame window
window = window.Window(500, 600)
window.set_title('Arkanoid')

# Initialise objects
manager = block.BlockManager(6, 9, window)
player1 = player.Player(window, 'sprites/player.png', 80, 19)

# Set initial difficulty
player.Ball.SPEED = 8
player.Player.SPEED = 8

# Initialise clock
clock = pygame.time.Clock()

# Initialise fonts and logo
SMALL_FONT = pygame.font.Font('freesansbold.ttf', 15)
LARGE_FONT = pygame.font.Font('freesansbold.ttf', 70)
SCORE_FONT = pygame.font.Font('freesansbold.ttf', 20)
LOGO = pygame.image.load('sprites/logo.png')
LOGO = pygame.transform.scale(LOGO, (int(window.width * 0.6),
                                     int(window.width * 0.6 / 2.75)))

def intro():
    window.surf.blit(LOGO, (window.width * 0.2, window.height/3))

    key_text_surf, key_text_rect = make_text_obj("Press 'x' to play",
                                                 SMALL_FONT)
    key_text_rect.center = window.width / 2, window.height / 2 + 100
    window.surf.blit(key_text_surf, key_text_rect)

    pygame.display.update()
    time.sleep(0.5)

    while replay_or_quit() == None:
        clock.tick()

def game_over():
    title_text_surf, title_text_rect = make_text_obj('Game Over!', LARGE_FONT)
    title_text_rect.center = window.width / 2, window.height / 2
    window.surf.blit(title_text_surf, title_text_rect)

    key_text_surf, key_text_rect = make_text_obj("Press 'x' to continue",
                                                 SMALL_FONT)
    key_text_rect.center = window.width / 2, window.height / 2 + 100
    window.surf.blit(key_text_surf, key_text_rect)

    pygame.display.update()
    time.sleep(0.5)

    while replay_or_quit() == None:
        clock.tick()

    player1.reset()
    player.Ball.SPEED = 8
    player.Player.SPEED = 8
    main()

def next_level():
    title_text_surf, title_text_rect = make_text_obj('Next Level!', LARGE_FONT)
    title_text_rect.center = window.width / 2, window.height / 2
    window.surf.blit(title_text_surf, title_text_rect)

    key_text_surf, key_text_rect = make_text_obj("Press 'x' to continue",
                                                 SMALL_FONT)
    key_text_rect.center = window.width / 2, window.height / 2 + 100
    window.surf.blit(key_text_surf, key_text_rect)

    pygame.display.update()
    time.sleep(0.5)

    while replay_or_quit() == None:
        clock.tick()

    player1.reset()
    manager.reset(6, 9)
    player.Ball.SPEED += 2
    player.Player.SPEED += 1


def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                pygame.event.clear()
                return True
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
    return None

def make_text_obj(text, font):
    text_surf = font.render(text, True, WHITE)
    return text_surf, text_surf.get_rect()

def draw_score(score):
    text = SCORE_FONT.render('Score: {0}'.format(score), True, WHITE)
    window.surf.blit(text, [0, 0])

def draw_level(level):
    text = SCORE_FONT.render('Level: {0}'.format(level), True, WHITE)
    window.surf.blit(text, [window.width - 100, 0])

def main():
    window.draw()
    intro()
    score = 0
    level = 1
    manager.set_paddings(70, 100)
    manager.create_blocks()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT]:
            player1.move(player.LEFT)

        if keys_pressed[pygame.K_RIGHT]:
            player1.move(player.RIGHT)

        # Draw background
        window.draw()

        draw_score(score)
        draw_level(level)

        manager.draw()
        player1.draw()
        if not player1.ball.move():
            game_over()

        # Event checks
        player1.ball_bounce()
        if manager.collision(player1):
            score += 1

        if manager.win():
            level += 1
            next_level()


        pygame.display.update()
        clock.tick(FPS)

main()
pygame.quit()
quit()


# implement levels
# implement score
# implement game_over screen
