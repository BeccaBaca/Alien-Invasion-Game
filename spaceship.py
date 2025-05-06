# Spaceship Object
# Name: Rebecca Baca
# 4/25/2025

import pygame
from bullet import Bullet

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, border):
        super().__init__()
        self.border = border
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("Graphics/spaceship.png")
        self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.border)/2, self.screen_height - 25)) #sets starting position of the spaceship
        self.speed = 6 #set speed to 6 pixels movement
        self.bullets_group = pygame.sprite.Group()
        self.bullet_ready = True
        self.bullet_time = 0
        self.bullet_delay = 300 # miliseconds before bullet is ready  
        self.bullet_sound = pygame.mixer.Sound("SoundEffects/bullet.ogg")

# responding to player commands
    def get_user_input(self):
        keys = pygame.key.get_pressed()

        # if right arrow key is pressed, move obj positive on X axis
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # if left arrow key is pressed, move obj negative X axis
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # if space is pressed, position bullet at center of spaceship and move 5 pixel speed, max sreen height
        if keys[pygame.K_SPACE] and self.bullet_ready:
            self.bullet_ready = False
            bullet = Bullet(self.rect.center, 5, self.screen_height) #arguments (position, speed, screen height)
            self.bullets_group.add(bullet)
            self.bullet_time = pygame.time.get_ticks()
            self.bullet_sound.play()


# Update 
    def update(self):
        self.get_user_input()
        self.constrain_movement()
        self.bullets_group.update() #calls update method of the bullet class
        self.recharge_bullet()

# Constrain Movement
    def constrain_movement(self):
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < self.border:
            self.rect.left = self.border

# Bullet Readiness
    def recharge_bullet(self):
        if not self.bullet_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.bullet_time >= self.bullet_delay:
                self.bullet_ready = True

# Reset game after game over
    def reset(self):
        self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.border)/2, self.screen_height))
        self.bullets_group.empty()