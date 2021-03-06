#!/usr/bin/env python3

import pygame

class Window(object):
    def __init__(self, width, height):
        pygame.init()
        self.surf = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self._image = None

    def set_title(self, title):
        pygame.display.set_caption(title)

    def set_background(self, image_path):
        self._image = pygame.image.load(image_path)

    def draw(self):
        if self._image:
            self.surf.blit(self._image, (0, 0))
        else:
            self.surf.fill((0, 0, 0))
