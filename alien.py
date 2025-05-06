# Alien Class
# Name: Rebecca Baca
#5/2/2025

import pygame, random

class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        path = f"Graphics/alien_{type}.png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, direction):
        self.rect.x += direction

class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, border):
        super().__init__()
        self.screen_width = screen_width
        self.border = border
        self.image = pygame.image.load("Graphics/mystery.png")

        x = random.choice([self.border/2, self.screen_width + self.border - self.image.get_width()])
        if x == self.border/2:
            self.speed = 3
        else:
            self.speed = -3
        self.rect = self.image.get_rect(topleft = (x, 90))

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > self.screen_width + self.border/2:
            self.kill()
        elif self.rect.left < self.border/2:
            self.kill()
