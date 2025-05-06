# Game Class
# Name: Rebecca Baca
#5/2/2025


#class created to contain all the game elements: spaceships, aliens, and obstacles
#and to hold various methods: updating position, checking for collisions, and updating score
import pygame, random
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien
from bullet import Bullet
from alien import MysteryShip


class Game:
    def __init__(self, screen_width, screen_height, border):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.border = border
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height, self.border))
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_bullets_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        self.lives = 3
        self.run = True
        self.score = 0
        self.highscore = 0
        self.display_highscore()
        self.spaceship_hit = pygame.mixer.Sound("SoundEffects/spaceship_hit.ogg")
        pygame.mixer.music.load("SoundEffects/background_music.ogg")
        pygame.mixer.music.play(-1) #-1 plays the music in a forever loop 

#method to add obstacles and space them evenly on the screen
    def create_obstacles(self):
        obstacle_width = len(grid[0]) * 3
        gap = (self.screen_width + self.border - (4 * obstacle_width))/5
        obstacles = []
        for i in range(4):
            border_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(border_x, self.screen_height - 100)
            obstacles.append(obstacle)
        return obstacles

#method to create rows of aliens
    def create_aliens(self):
        for row in range(5):
            for column in range(11):
                x = 75 + column * 55 #adding spacer to the column and the cell size
                y = 110 + row * 55 #dding spacer to the column and the cell size

                if row == 0:
                    alien_type = 3
                elif row in (1, 2):
                    alien_type = 2
                else:
                    alien_type = 1

                alien = Alien(alien_type, x + self.border/2, y)
                self.aliens_group.add(alien)

    def move_aliens(self):
        self.aliens_group.update(self.aliens_direction)

        #check that the alien is in screen window
        alien_sprites = self.aliens_group.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width + self.border/2:
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= self.border/2:
                self.aliens_direction = 1
                self.alien_move_down(2)
    
    def alien_move_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_bullet(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites()) #picks a random alien
            bullet_sprite = Bullet(random_alien.rect.center, -6, self.screen_height)
            self.alien_bullets_group.add(bullet_sprite)

    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.screen_width, self.border))

    def check_for_collisions(self):
        if self.spaceship_group.sprite.bullets_group:
            for bullet_sprite in self.spaceship_group.sprite.bullets_group:
                aliens_hit = pygame.sprite.spritecollide(bullet_sprite, self.aliens_group, True)
                if aliens_hit:
                    #add sound effect
                    self.spaceship_hit.play() 
                    for alien in aliens_hit:
                        self.score += alien.type * 100
                        self.highscore_tracker()
                        bullet_sprite.kill()

                if pygame.sprite.spritecollide(bullet_sprite, self.mystery_ship_group, True):
                    #add sound effect
                    self.score += 500
                    self.spaceship_hit.play() 
                    self.highscore_tracker()
                    bullet_sprite.kill()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(bullet_sprite, obstacle.blocks_group, True):
                        bullet_sprite.kill()

        #alien bullets
        if self.alien_bullets_group:
            for bullet_sprite in self.alien_bullets_group:
                
                if pygame.sprite.spritecollide(bullet_sprite, self.spaceship_group, False):
                    bullet_sprite.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over()
                
                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(bullet_sprite, obstacle.blocks_group, True):
                        bullet_sprite.kill()

        if self.aliens_group:
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

                if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                    self.game_over()
    
    def highscore_tracker(self):
        if self.score > self.highscore:
            self.highscore = self.score
            
            # add writing high score to a file
            with open("highscore.txt", "w") as file:
                file.write(str(self.highscore))

    def display_highscore(self):
        # open and read highscore file, set higscore to saved highscore
        try:
            with open("highscore.tx", "r") as file:
                self.highscore = int(file.read())
        # when file not found, set high score to 0
        except FileNotFoundError:
            self.highscore = 0

    def game_over(self):
        self.run = False

    def reset(self):
        self.run = True
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_bullets_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.obstacles = self.create_obstacles()
        self.score = 0
