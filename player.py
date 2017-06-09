#!/usr/bin/env python3
'''Player class'''

import pygame
import math

# RGB colour definitions
BLACK = (0, 0, 0)

# Direction constants
LEFT = 0
RIGHT = 1

class Player(object):
    SPEED = 12
    def __init__(self, window, image_path, width, height):
        self.x = int((window.width - width)/ 2)
        self.y = window.height - height - 30
        self.window = window
        self.ball = Ball(self.x + int(width / 2), self.y, window)
        self._image = pygame.image.load(image_path)
        self.width = width
        self.height = height
        # Prevents second bounce bug
        self.bounced = False

    def draw(self):
        self.window.surf.blit(self._image, (self.x, self.y))
        self.ball.draw()

    def move(self, direction):
        if direction == LEFT and self.x > 0:
            self.x -= Player.SPEED
        elif direction == RIGHT and self.x < self.window.width - self.width:
            self.x += Player.SPEED

    def ball_bounce(self):
        if self.x - 10 < self.ball.x < self.x + self.width + 10:
            if self.y < self.ball.y - 1 < self.y + Ball.SPEED:
                if not self.bounced:
                    self.ball.bounce(Ball.HORIZONTAL,
                            self.x + int(self.width/2) - self.ball.x)
                    self.bounced = True
                    return

        self.bounced = False

    def reset(self):
        self.x = int((self.window.width - self.width)/ 2)
        self.y = self.window.height - self.height - 30
        self.ball = Ball(self.x + int(self.width / 2), self.y, self.window)
        # Prevents second bounce bug
        self.bounced = False



class Ball(object):
    SPEED = 10
    HORIZONTAL = 0
    VERTICAL = 1
    def __init__(self, x, y, window):
        self.x = x
        self.y = y
        self.window = window
        self.direction = 0

    def draw(self):
        pygame.draw.circle(self.window.surf, (255, 0, 0), (self.x, self.y), 4)

    def bounce(self, axis, correction=0):
        if axis == Ball.HORIZONTAL:
            self.direction = 180 - self.direction % 360
            self.direction += correction
        elif axis == Ball.VERTICAL:
            self.direction = -self.direction
            self.direction += correction

    def move(self):
        if self.x < 0:
            self.direction = -self.direction
        elif self.x > self.window.width:
            self.direction = -self.direction

        if self.y < 0:
            self.direction = 180 - self.direction % 360
        elif self.y > self.window.height:
            return False

        self.y += int(-math.cos(math.radians(self.direction)) * Ball.SPEED)
        self.x += int(-math.sin(math.radians(self.direction)) * Ball.SPEED)

        return True

