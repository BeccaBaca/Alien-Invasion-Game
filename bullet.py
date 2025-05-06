# Bullet Object
# Name: Rebecca Baca
# 4/30/2025

import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, speed, screen_height):
        super().__init__()
        
        # create a bullet rectangle
        self.image = pygame.Surface((4, 15))
        
        # fill bullet image with color
        self.image.fill((120, 211, 239, 1)) 
        
        # starting position of the bullet
        self.rect = self.image.get_rect(center = position)
        self.speed = speed 
        self.screen_height = screen_height

# speed of bullets
    def update(self):
        # move up (positive value) move down (negative value)
        self.rect.y -= self.speed
        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            self.kill() #kill the bullets object, removes bullets from all the groups it belongs to