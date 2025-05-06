# Alien Invasion
# Name: Rebecca Baca
# 4/23/2025

import sys  
import pygame, random
from game import Game

pygame.init()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Game Screen Height/Width/Border
Capital letters = CONSTANTS
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
BORDER = 50

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Game RGB Colors
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
COLOR = (29, 29, 29)
BLUE = (120, 211, 239, 1)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Fonts, Border, Width & Height
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
font = pygame.font.Font("Font/monogram.ttf", 40)
level_display = font.render("LEVEL O1", False, BLUE)
game_over_display = font.render("GAME OVER", False, BLUE)
score_display = font.render("SCORE", False, BLUE)
highscore_display = font.render("HIGHEST SCORE", False, BLUE)

screen = pygame.display.set_mode((SCREEN_WIDTH + BORDER, SCREEN_HEIGHT + 2*BORDER))
pygame.display.set_caption("Alien Invaders")

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, BORDER)
clock = pygame.time.Clock()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
User event - shoot bullet, set time
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
SHOOT_BULLET = pygame.USEREVENT
pygame.time.set_timer(SHOOT_BULLET, 300)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
User event - create mystery ship at random times
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
While loop - while game is NOT quit
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
while True:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # shoot bullets
        if event.type == SHOOT_BULLET and game.run:
            game.alien_shoot_bullet()

        # create mystery ship, appear at random times
        if event.type == MYSTERYSHIP and game.run:
            game.create_mystery_ship()
            pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

        # use the space bar to shoot at spaceships
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game.run == False:
            game.reset()
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Updating 
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    if game.run:
        game.spaceship_group.update()
        game.move_aliens()
        game.alien_bullets_group.update()
        game.mystery_ship_group.update()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Drawing 
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    '''Draw a blue, curved box around game and line at the bottom of the screen
    simulates actual arcade game'''
    screen.fill(COLOR)
    pygame.draw.rect(screen, BLUE, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60) #60 corner radius for rounded corners
    pygame.draw.line(screen, BLUE, (25, 700),(775, 700), 3) #line at bottom of screen to define where score and lives will display
    
    ''' Add display game level or game over'''
    if game.run:
        screen.blit(level_display, (570, 740, 50, 50))
    else:
        screen.blit(game_over_display, (570, 740, 50, 50))
    
    ''' Display lives left as ships'''
    x = 50 # 50 pixels
    for life in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (x, 745)) 
        x += 50
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Drawing on Display Continued
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.bullets_group.draw(screen)
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)
    game.aliens_group.draw(screen)
    game.alien_bullets_group.draw(screen)
    game.mystery_ship_group.draw(screen)
    game.check_for_collisions()
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Adding score to game screen, keeping score
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    screen.blit(score_display, (50, 15, 50, 50))
    score_area = font.render(str(game.score), False, BLUE)
    screen.blit(score_area, (50, 40, 50, 50))   
    
    screen.blit(highscore_display, (550, 15, 50, 50))
    highscore_area = font.render(str(game.highscore), False, BLUE)
    screen.blit(highscore_area, (550, 40, 50, 50)) 

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Game Frames updating for continuity when playing
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    pygame.display.update()
    clock.tick(60)