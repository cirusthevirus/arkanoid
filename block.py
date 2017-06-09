#!/usr/bin/env python3
'''Block class'''

import pygame
import random
import player

# RGB colour definitions
BLACK = (0, 0, 0)

class Block(object):
    def __init__(self, x, y, width, height, window, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.window = window
        self.colour = colour

    def draw(self):
        pygame.draw.rect(self.window.surf, self.colour, [self.x, self.y,
                self.width, self.height])
        pygame.draw.lines(self.window.surf, BLACK, True,
                [[self.x, self.y],
                 [self.x + self.width, self.y],
                 [self.x + self.width, self.y + self.height],
                 [self.x, self.y + self.height]], 3)

    def collides(self, pl):
        if self.x < pl.ball.x < self.x + self.width:
            if self.y <= pl.ball.y <= self.y + self.height:
                # Collision, check if vertical or horizontal
                if pl.ball.x < self.x + player.Ball.SPEED:
                    return player.Ball.VERTICAL
                elif self.x + self.width - player.Ball.SPEED < pl.ball.x:
                    return player.Ball.VERTICAL
                elif pl.ball.y < self.y + player.Ball.SPEED:
                    return player.Ball.HORIZONTAL
                elif self.y + self.height - player.Ball.SPEED < pl.ball.y:
                    return player.Ball.HORIZONTAL
        elif self.x == pl.ball.x:
            if self.y <= pl.ball.y <= self.y + self.height:
                return player.Ball.HORIZONTAL
        return None


class BlockManager(object):
    def __init__(self, rows, cols, window):
        self.rows = rows
        self.cols = cols
        self.window = window
        self._block_list = []

    def set_paddings(self, sides, top):
        self.top_pad = top
        self.side_pad = sides

    def create_blocks(self):
        self._block_list = []
        b_width = int(self.window.width - 2 * self.side_pad)
        b_height = min(int(self.window.height / 2 - self.top_pad),
                15 * self.rows)
        block_width = int(b_width / self.cols)
        block_height = min(int(b_height / self.rows), 15)

        x = self.side_pad
        y = self.top_pad

        for y in range(self.top_pad, self.top_pad + block_height * \
                self.rows, block_height):
            red = random.randrange(0, 256)
            green = random.randrange(0, 256)
            blue = random.randrange(0, 256)
            colour = (red, green, blue)
            for x in range(self.side_pad, self.side_pad + block_width * \
                    self.cols, block_width):
                self._block_list.append(Block(x, y, block_width, block_height,
                        self.window, colour))

    def draw(self):
        for block in self._block_list:
            block.draw()

    def collision(self, player):
        for block in self._block_list:
            axis = block.collides(player)
            if axis != None:
                self._block_list.remove(block)
                player.ball.bounce(axis)
                return True
        return False

    def reset(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self._block_list = []
        self.create_blocks()

    def win(self):
        if not self._block_list:
            return True
        return False


