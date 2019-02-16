import pygame
import random
import os
import sys

pygame.init()

FPS = 60  # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
pygame.display.set_caption('The Invasion')

######################################################################################

HEIGHT = 400
WIDTH = 300

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (166, 8, 35)
BACK = (184, 223, 245)

FONT = pygame.font.Font('freesansbold.ttf', 16)
BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

######################################################################################

# load sprites
bosssurf = [pygame.image.load(os.path.join('boss', '%d%s' % (x, '.png'))) for x in range(1, 5)]
blastsurf = [pygame.image.load(os.path.join('blast', '%d%s' % (x, '.png'))) for x in range(1, 6)]
boss = pygame.image.load()
hero = pygame.image.load('data_sprites/hero.jpg')
bullet = pygame.image.load()
enemy = pygame.image.load()

firep = pygame.image.load()
firer = pygame.image.load()
ammo = pygame.image.load()
life = pygame.image.load()
bonus = (firep, firer, ammo, life)

background = pygame.image.load()

# text
gameOverSurf = FONT.render('Game Over!', True, RED)
gameOverRect = gameOverSurf.get_rect()
gameOverRect.center = (WIDTH / 2, HEIGHT / 2 - 10)

gameWinSurf = FONT.render('WELL DONE!', True, RED)
gameWinRect = gameWinSurf.get_rect()
gameWinRect.center = (WIDTH / 2, HEIGHT / 2 - 10)

InvasionSurf = BIGFONT.render('The Invasion', True, RED)
InvasionRect = InvasionSurf.get_rect()
InvasionRect.center = (WIDTH / 2, HEIGHT / 2 - 10)

show_rect = False


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
        self.cooldown = 100
        self.cooldownt = 0
        self.bornt = 0
        self.timer = 0
        self.blastst = 0
        self.loop = 0
        self.width = 80
        self.height = 38
        self.direction = 1
        self.health = 10000
        self.x = WIDTH + self.width
        self.y = 0

    def update(self):

        global endgame

        if self.x > 250 and self.health > 0:
            self.x -= self.direction

            if self.x < 260:
                self.direction = -1

            if self.x > 320:
                self.direction = 1
        else:
            self.x -= 1

            if self.x < -90:
                endgame = 'win'

        if self.y > mouse_y() and self.health > 0 and hero.health > 0:
            self.y -= 1

        elif self.y < mouse_y() and self.health > 0 and hero.health > 0:
            self.y += 1

        elif self.y == mouse_y() and self.health > 0 and hero.health > 0:
            bossfire()

        if self.health <= 0 and pygame.time.get_ticks() - self.blastst >= 200:
            self.blastst = pygame.time.get_ticks()
            a = random.randrange(1, 70) - 20
            b = random.randrange(1, 30) - 20
            blastgroup.add(Blast(self.x + a, self.y + b, 1))

        self.image = bosssurf[self.loop]
        self.rect = pygame.draw.Rect(self.x, self.y, self.width, self.height)
        # self.rect = pygame.Rect(200, 150, self.width, self.height)
        if show_rect:
            pygame.draw.rect(SCREEN, RED, self.rect, 1)


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super(Hero, self).__init__()
        self.cooldown = 100
        self.enmkiled = 0
        self.cooldownt = 0
        self.blastst = 0
        self.fallt = 0
        self.falls = 1
        self.fire = 0
        self.firepower = 7
        self.timer = 0
        self.loop = 0
        self.rotate = 0
        self.health = 3
        self.width = 40
        self.height = 40
        self.ammobox = 1000
        self.collided = False
        self.image = hero
        self.x, self.y = -30, -30

    def update(self):
        pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        pass

    def update(self):
        pass


class BossBullet(pygame.sprite.Sprite):
    def __init__(self):
        super(BossBullet, self).__init__()
        pass

    def update(self):
        pass


class HeroBullet(pygame.sprite.Sprite):
    def __init__(self):
        super(HeroBullet, self).__init__()
        pass

    def update(self):
        pass


class Blast(pygame.sprite.Sprite):
    def __init__(self):
        super(Blast, self).__init__()
        pass

    def update(self):
        pass


class Button:
    def __init__(self, text, color, yshift, func):
        self.image = FONT.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2 + yshift)
        self.func = func
        self.enabled = False

    def update(self):
        # on press
        SCREEN.blit(self.image, self.rect)

        if self.enabled:

            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    self.func()


class Bonus(pygame.sprite.Sprite):
    def __init__(self, X, Y, num):
        super(Bonus, self).__init__()
        self.width = 40
        self.height = 40
        self.x, self.y = X, Y
        self.image = bonus[num]

    def update(self):
        # movement
        self.x -= 1

        if self.x < -40:
            bonusgroup.remove(self)

        self.rect = pygame.draw.Rect(self.x, self.y, self.width, self.height)
        if show_rect:
            pygame.draw.rect(SCREEN, RED, self.rect, 1)


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        pass

    def update(self):
        pass


######################################################################################


def bossfire():
    if pygame.time.get_ticks() - boss.cooldownt >= boss.cooldown:
        boss.cooldownt = pygame.time.get_ticks()
        bossbgroup.add(BossBullet())


def herofire():
    hero.fire = pygame.mouse.get_pressed()[0]

    if pygame.mouse.get_pressed()[0] and hero.ammobox > 0 and hero.health > 0:

        if pygame.time.get_ticks() - hero.cooldownt >= hero.cooldown:
            hero.cooldownt = pygame.time.get_ticks()
            herobgroup.add(HeroBullet(hero.x, hero.y, True))
            hero.ammobox -= 1


def bosscollide():
    if boss.health > 0:

        hit = pygame.sprite.spritecollideany(boss, herogroup, collided=None)

        if hit:

            if pygame.sprite.collide_mask(hit, boss):

                if not hit.collided:
                    boss.health -= 100
                    hit.collided = True

                    hit.health -= 1

    hit = pygame.sprite.spritecollideany(boss, herobgroup, collided=None)

    if hit:

        if pygame.sprite.collide_mask(hit, boss):

            herobgroup.remove(hit)

            if hit.local:

                boss.health -= hero.firepower

            else:

                boss.health -= remotehero.firepower


def herocollide():
    hit = pygame.sprite.groupcollide(herogroup, bossbgroup, False, False, collided=None)

    if hit:

        for hero, bullets in hit.items():

            for bul in bullets:

                if pygame.sprite.collide_mask(hero, bul):
                    hero.health -= 1

                    bossbgroup.remove(bul)

    hit = pygame.sprite.groupcollide(herogroup, bonusgroup, False, False, collided=None)

    if hit:

        for hero, bonus in hit.items():

            for spr in bonus:

                if pygame.sprite.collide_mask(hero, spr):

                    if spr.image == life:
                        hero.health += 1

                    elif spr.image == ammo:
                        hero.ammobox += 200

                    elif spr.image == firep:
                        hero.firepower += 1

                    elif spr.image == firer:
                        hero.cooldown -= 1

                    bonusgroup.remove(spr)


def enemycollide():
    # hit = pygame.sprite.spritecollideany(hero, enemygroup, collided = None)
    hit = pygame.sprite.groupcollide(herogroup, enemygroup, False, False, collided=None)

    if hit:

        for hero, enemies in hit.items():

            for en in enemies:

                if pygame.sprite.collide_mask(hero, en):
                    hero.collided = True

                    hero.health -= 1

                    hero.enmkiled += 1
                    en.health = 0

    hit = pygame.sprite.groupcollide(enemygroup, herobgroup, False, False, collided=None)

    if hit:

        for enemy, bullets in hit.items():

            for bul in bullets:

                if pygame.sprite.collide_mask(enemy, bul):

                    if not client:

                        enemy.health -= localhero.firepower

                        if enemy.health < 0:

                            if bul.local:

                                localhero.enmkiled += 1

                            else:

                                remotehero.enmkiled += 1

                    herobgroup.remove(bul)


def boss_health_meter():
    bossurf = FONT.render('BOSS: ', True, RED)
    bossrect = bossurf.get_rect()

    hm = WIDTH - bossrect[2] - 5 * 2
    health = boss.health / 100

    if health < 0:
        health = 0

    hp = float(hm) / 100 * health
    boshm = pygame.Surface((hp, 16))
    boshm.fill(RED)
    boshm.set_alpha(150)

    SCREEN.blit(bossurf, (5, 280))
    SCREEN.blit(boshm, (bossrect[2] + 5, 281))


def make_enemy():
    global enmid

    if len(enemygroup) < maxenemy:

        if not bosshow:
            enemygroup.add(Enemy(enmid[0]))
            del enmid[0]

        if bosshow and boss.health > 0 and pygame.time.get_ticks() - boss.bornt >= 1000:
            boss.bornt = pygame.time.get_ticks()
            enemygroup.add(Enemy(enmid[0]))
            del enmid[0]


def cake_make():
    global enmyhealth

    for en in enemygroup:

        if en.health <= 0:

            if en.bonus[1] == 0:
                bonusgroup.add(Bonus(en.x, en.y, en.bonus[0]))

            blastgroup.add(Blast(en.x, en.y, 0))
            enemygroup.remove(en)
            enmid.append(en.id)
            enmyhealth += 1


def gameinfo():
    info = [''.join(map(str,
                        ["Hero Life: ", hero.health, " Ammo: ", hero.ammobox, "  Enemy Killed: ",
                         hero.enmkiled]))]
    gameInfoSurf = FONT.render("".join(info), True, WHITE)
    SCREEN.blit(gameInfoSurf, (5, 5))


######################################################################################

def start_game():
    global server, client, enmid, maxenemy, tillboss, enmyhealth, endgame, bosshow, enmyhealth, localhero, \
        remotehero, boss, enemygroup, herogroup, herobgroup, bossbgroup, blastgroup, bonusgroup

    bosshow = False
    endgame = 'game'
    maxenemy = 5
    tillboss = 100
    enmyhealth = 100

    boss = Boss()
    hero = Hero()

    herogroup = pygame.sprite.Group(hero)

    boss_group = pygame.sprite.Group(boss)
    hero_b_group = pygame.sprite.Group()
    boss_b_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    blast_group = pygame.sprite.Group()

    pygame.mouse.set_visible(0)

    enmid = []

    for i in range(maxenemy):
        enmid.append(i)

    ######################################################################################
    # -----------------------------------main game loop-----------------------------------

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        make_enemy()
        herofire()

        # fill screen
        SCREEN.fill(BACK)

        # update & draw sprites
        bgroundgroup.update()
        bgroundgroup.draw(SCREEN)

        enemygroup.update()
        enemygroup.draw(SCREEN)

        herobgroup.update()
        herobgroup.draw(SCREEN)
        herogroup.update()
        herogroup.draw(SCREEN)

        if bosshow:
            boss_group.update()
            bossbgroup.update()
            boss_group.draw(SCREEN)
            bossbgroup.draw(SCREEN)

            boss_health_meter()
            bosscollide()

        blastgroup.update()
        blastgroup.draw(SCREEN)

        gameinfo()

        enemycollide()
        herocollide()

        if localhero.enmkiled > tillboss:
            bosshow = True

        if endgame == 'win':
            gameover(True)

        elif endgame == 'loose':
            gameover(False)

        cake_make()

        pygame.display.update()
        fpsClock.tick(FPS)


######################################################################################

def gameover(win):
    A = 0
    darktimer = 0
    buttontimer = pygame.time.get_ticks()
    darkness = pygame.Surface((WIDTH, HEIGHT))

    darkness.fill((BLACK))
    darkness.set_alpha(A)

    pygame.mouse.set_visible(1)

    again = Button("again", WHITE, 30, start_game)
    back = Button("menu", WHITE, 60, menu)
    exit = Button("exit", WHITE, 90, sys.exit)

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pygame.time.get_ticks() - darktimer >= 500:

            darktimer = pygame.time.get_ticks()

            if A != 255:
                A += 1
            darkness.set_alpha(A)
            SCREEN.blit(darkness, (0, 0))

        if win == False:

            SCREEN.blit(gameOverSurf, gameOverRect)

        else:

            SCREEN.blit(gameWinSurf, gameWinRect)

        again.update()
        back.update()
        exit.update()

        if pygame.time.get_ticks() - buttontimer >= 500:
            buttontimer = pygame.time.get_ticks()
            again.enabled = True
            back.enabled = True
            exit.enabled = True

        pygame.display.update()
        fpsClock.tick(FPS)


def menu():
    buttontimer = pygame.time.get_ticks()
    pygame.mouse.set_visible(1)

    singlplay = Button("Start Game", WHITE, 30, start_game)
    exit = Button("exit", WHITE, 120, sys.exit)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill(BLACK)
        SCREEN.blit(InvasionSurf, InvasionRect)

        singlplay.update()
        server.update()
        client.update()
        exit.update()

        if pygame.time.get_ticks() - buttontimer >= 1000:
            buttontimer = pygame.time.get_ticks()
            singlplay.enabled = True
            server.enabled = True
            client.enabled = True
            exit.enabled = True

        pygame.display.update()
        fpsClock.tick(FPS)


bgroundgroup = pygame.sprite.OrderedUpdates()

menu()
