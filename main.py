import pygame
import sys
import random


pygame.init()

FPS = 60  # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
pygame.display.set_caption('The Invasion')

######################################################################################

HEIGHT = 400
WIDTH = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (166, 8, 35)
BACK = (184, 223, 245)

FONT = pygame.font.Font('freesansbold.ttf', 16)
BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

######################################################################################

# load sprites
boss = pygame.image.load()
hero = pygame.image.load('hero.jpg')
bullet = pygame.image.load()
enemy = pygame.image.load()

ground = pygame.image.load()
clouds = pygame.image.load()

# text
gameOverSurf = FONT.render('Game Over!', True, RED)
gameOverRect = gameOverSurf.get_rect()
gameOverRect.center = (WIDTH / 2, HEIGHT / 2 - 10)

gameWinSurf = FONT.render('WELL DONE!', True, RED)
gameWinRect = gameWinSurf.get_rect()
gameWinRect.center = (WIDTH / 2, HEIGHT / 2 - 10)


######################################################################################

def mouse_x():
    x, y = pygame.mouse.get_pos()

    return x


def mouse_y():
    x, y = pygame.mouse.get_pos()

    return y


######################################################################################


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss, self).__init__()
        pass

    def update(self):
        pass


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super(Hero, self).__init__()
        pass

    def update(self):
        pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        pass

    def update(self):
        pass


class Boss_bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss_bullet, self).__init__()
        pass

    def update(self):
        pass


class Hero_bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Hero_bullet, self).__init__()
        pass

    def update(self):
        pass


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        pass

    def update(self):
        pass

######################################################################################

def startGame():
