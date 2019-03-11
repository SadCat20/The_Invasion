import os
import pygame
import random
import sys

pygame.init()

HEIGHT = 400
WIDTH = 300

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('The Invasion')

DAMAGE_IMG = pygame.image.load(os.path.join('source/explosion', 'damage.png'))
DESTROY_IMG = pygame.image.load(os.path.join('source/explosion', 'destroy.png'))

class Button:
    def __init__(self, text, color, yshift, func):
        self.font = pygame.font.Font('freesansbold.ttf', 25)
        self.image = self.font.render(text, True, color)
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


class Score:
    def __init__(self):
        self.boss_destroy = 0
        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 15)

    def update(self, life):
        textsurface = self.font.render('Score: {}'.format(self.score), True, (255, 255, 255))
        SCREEN.blit(textsurface, (0, 0))
        textsurface = self.font.render('Health: {}'.format(life), True, (255, 255, 255))
        SCREEN.blit(textsurface, (0, 20))
        textsurface = self.font.render('Boss killed: {}'.format(self.boss_destroy), True, (255, 255, 255))
        SCREEN.blit(textsurface, (180, 0))


class BulletEnemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.img = pygame.image.load(os.path.join('source', 'enemy_bullet.png'))


class BulletHero(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.img = pygame.image.load(os.path.join('source', 'bullet.png'))


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.get_damage = False
        self.damage_time = 0
        self.firetime = 100
        self.cooldown = 20
        self.health = 10
        self.x = WIDTH / 2
        self.y = HEIGHT - 100
        self.del_index = []
        self.bullets = []
        self.img = pygame.image.load(os.path.join('source/hero', 'hero.png'))

    def update(self):
        for i in range(len(self.bullets)):
            self.bullets[i].y -= 1
            SCREEN.blit(self.bullets[i].img, (self.bullets[i].x, self.bullets[i].y))
        for i in range(len(self.bullets)):
            if self.bullets[i].y + 20 <= 0:
                self.del_index.append(i)
        for i in self.del_index:
            self.bullets.pop(i)
        SCREEN.blit(self.img, (self.x, self.y))
        self.del_index = []

    def interface(self):
        self.firetime += 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= 2
        if keys[pygame.K_RIGHT] and self.x + 42 < WIDTH:
            self.x += 2
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= 2
        if keys[pygame.K_DOWN] and self.y + 42 < HEIGHT:
            self.y += 2
        if keys[pygame.K_SPACE] and self.firetime >= self.cooldown:
            self.firetime = 0
            self.bullets.append(BulletHero())
            self.bullets[len(self.bullets) - 1].x = self.x + 16
            self.bullets[len(self.bullets) - 1].y = self.y

    def destroy(self):
        if self.damage_time < 10:
            self.damage_time += 1
            if self.health <= 0:
                SCREEN.blit(DESTROY_IMG, (self.x, self.y))
            else:
                SCREEN.blit(DAMAGE_IMG, (self.x, self.y))
        else:
            self.damage_time = 0
            self.get_damage = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.get_damage = False
        self.damage_time = 0
        self.health = 3
        self.firetime = 250
        self.cooldown = 250
        self.bullets = []
        self.del_index = []
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(-HEIGHT, 0)
        self.img = pygame.image.load(os.path.join('source/enemy', 'alien.png'))

    def update(self):
        for i in range(len(self.bullets)):
            self.bullets[i].y += 1
            SCREEN.blit(self.bullets[i].img, (self.bullets[i].x, self.bullets[i].y))
        for i in range(len(self.bullets)):
            if self.bullets[i].y >= HEIGHT:
                self.del_index.append(i)
        for i in self.del_index:
            self.bullets.pop(i)
        SCREEN.blit(self.img, (self.x, self.y))
        self.del_index = []

    def fire(self):
        self.firetime += 1
        if self.firetime >= self.cooldown:
            self.firetime = 0
            self.bullets.append(BulletEnemy())
            self.bullets[len(self.bullets) - 1].x = self.x + 8
            self.bullets[len(self.bullets) - 1].y = self.y

    def destroy(self):
        if self.damage_time < 10:
            self.damage_time += 1
            if self.health <= 0:
                SCREEN.blit(DESTROY_IMG, (self.x, self.y))
            else:
                SCREEN.blit(DAMAGE_IMG, (self.x, self.y))
        else:
            self.damage_time = 0
            self.get_damage = False


########################################################################################################################

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.animation_time = 0
        self.get_damage = False
        self.megabul_fire = False
        self.damage_time = 0
        self.health = 50
        self.firetime = 150
        self.cooldown = 80
        self.bullets = []
        self.del_index = []
        self.x = WIDTH / 2 - 61
        self.y = -140
        self.imgs = [pygame.image.load(os.path.join('source/boss', '{}.png'.format(x))) for x in range(1, 6)]
        self.mega_bullet_img = pygame.image.load(os.path.join('source', 'mega_bullet.png'))
        self.mega_x = 0
        self.mega_y = 0

    def update(self):
        self.animation_time += 1
        if self.megabul_fire:
            self.mega_y += 1
            SCREEN.blit(self.mega_bullet_img, (self.mega_x, self.mega_y))
        for i in range(len(self.bullets)):
            self.bullets[i].y += 1
            SCREEN.blit(self.bullets[i].img, (self.bullets[i].x, self.bullets[i].y))
        for i in range(len(self.bullets)):
            if self.bullets[i].y >= HEIGHT:
                self.del_index.append(i)
        for i in self.del_index:
            self.bullets.pop(i)
        SCREEN.blit(self.animation(), (self.x, self.y))
        self.del_index = []

    def animation(self):
        if self.animation_time <= 300:
            return self.imgs[0]
        elif self.animation_time <= 330:
            return self.imgs[1]
        elif self.animation_time <= 360:
            return self.imgs[2]
        elif self.animation_time <= 390:
            return self.imgs[3]
        elif self.animation_time <= 420:
            self.animation_time = 0
            self.megabul_fire = True
            SCREEN.blit(self.mega_bullet_img, (self.x + 61, self.y + 130))
            self.mega_x = self.x + 61
            self.mega_y = self.y + 130
            return self.imgs[4]

    def fire(self):
        self.firetime += 1
        if self.firetime >= self.cooldown:
            self.firetime = 0
            self.bullets.append(BulletEnemy())
            self.bullets[len(self.bullets) - 1].x = self.x + 61
            self.bullets[len(self.bullets) - 1].y = self.y

    def destroy(self):
        if self.damage_time < 10:
            self.damage_time += 1
            if self.health <= 0:
                SCREEN.blit(DESTROY_IMG, (self.x + 60, self.y + 60))
            else:
                SCREEN.blit(DAMAGE_IMG, (self.x + 60, self.y + 60))
        else:
            self.damage_time = 0
            self.get_damage = False


########################################################################################################################

def start_game():
    boss_go_lest = True
    endgame = False
    first_boss_appearance = True
    createenemy_time = 2000
    timeing_create = 0
    untill_boss_score = 400
    bg = pygame.image.load(os.path.join('source', 'background.jpg'))
    enemys_arr = [Enemy() for i in range(2)]
    hero = Hero()
    score = Score()
    boss = Boss()
    while not endgame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        SCREEN.blit(bg, (0, 0))
        hero.interface()
        hero.update()
        if score.score < untill_boss_score:
            first_boss_appearance = True
            hero.cooldown = 20
            for i in enemys_arr:
                i.y += 0.3
                if i.y + 50 >= 0:
                    i.fire()
                i.update()

            for i in enemys_arr:
                for j in range(len(i.bullets)):
                    if hero.x <= i.bullets[j].x + 4 <= hero.x + 42 and hero.y < i.bullets[j].y < hero.y + 20:
                        if i.del_index.count(j) == 0:
                            i.del_index.append(j)
                        hero.get_damage = True
                        hero.health -= 1
                        if hero.health == 0:
                            endgame = True

            for i in enemys_arr:
                if hero.x + 42 >= i.x and hero.x <= i.x + 23 and hero.y <= i.y + 42 and hero.y + 42 >= i.y:
                    hero.get_damage = True
                    hero.health -= 2
                    if hero.health <= 0:
                        endgame = True
                    i.get_damage = True
                    i.health = 0
                    enemys_arr[enemys_arr.index(i)] = Enemy()

            for i in range(len(hero.bullets)):
                for j in range(len(enemys_arr)):
                    if enemys_arr[j].x < hero.bullets[i].x + 4 < enemys_arr[j].x + 23 and enemys_arr[j].y + 42 >= \
                            hero.bullets[i].y >= enemys_arr[j].y:
                        if hero.del_index.count(i) == 0:
                            hero.del_index.append(i)
                        enemys_arr[j].health -= 1
                        enemys_arr[j].get_damage = True
        else:
            if first_boss_appearance:
                boss.x = WIDTH / 2 - 61
                boss.y = -140
                boss.health = 50
                boss.firetime = 150
                hero.cooldown = 60
                first_boss_appearance = False
                for i in enemys_arr:
                    i.health = 0
                    i.get_damage = True
            if boss.y <= 0:
                boss.y += 1
            else:
                if boss_go_lest:
                    if boss.x > 0:
                        boss.x -= 0.5
                    else:
                        boss_go_lest = False
                else:
                    if boss.x + 128 < WIDTH:
                        boss.x += 0.5
                    else:
                        boss_go_lest = True
            hero.interface()
            hero.update()
            boss.fire()
            boss.update()
            for i in range(len(hero.bullets)):
                if boss.x <= hero.bullets[i].x + 8 <= boss.x + 120 and boss.y + 130 > hero.bullets[i].y > boss.y:
                    if hero.del_index.count(i) == 0:
                        hero.del_index.append(i)
                    boss.health -= 1
                    boss.get_damage = True
            for i in range(len(boss.bullets)):
                if hero.x <= boss.bullets[i].x + 8 < hero.x + 42 and hero.y + 20 > boss.bullets[i].y > hero.y:
                    if boss.del_index.count(i) == 0:
                        boss.del_index.append(i)
                    hero.get_damage = True
                    hero.health -= 1
            if hero.x <= boss.mega_x + 35 < hero.x + 42 and hero.y + 20 > boss.mega_y > hero.y:
                boss.mega_y = -40
                boss.mega_x = -40
                boss.megabul_fire = False
                hero.get_damage = True
                hero.health -= 2
            if boss.health <= 0:
                score.score += 50
                score.boss_destroy += 1
                untill_boss_score += untill_boss_score + 400
                boss.bullets.clear()
                boss.megabul_fire = False
                boss.mega_y = -40
                boss.mega_x = -40
        for i in enemys_arr:
            if i.get_damage:
                i.destroy()
            elif i.health <= 0 or i.y > HEIGHT:
                enemys_arr[enemys_arr.index(i)] = Enemy()
                if score.score < untill_boss_score:
                    score.score += 10
        if hero.get_damage:
            hero.destroy()
        if boss.get_damage:
            boss.destroy()
        if createenemy_time <= timeing_create and score.score < untill_boss_score:
            timeing_create = 0
            enemys_arr.append(Enemy())
        else:
            timeing_create += 1

        score.update(hero.health)
        pygame.display.update()
        pygame.time.wait(5)

def main():
    bg = pygame.image.load(os.path.join('source', 'background.jpg'))
    buttontimer = pygame.time.get_ticks()
    pygame.mouse.set_visible(1)

    play = Button("Start Game", (255, 255, 255), 30, start_game)
    exit = Button("exit", (255, 255, 255), 120, sys.exit)

    InvasionSurf = (pygame.font.Font('freesansbold.ttf', 32)).render('The Invasion', True, (255, 0, 0))
    InvasionRect = InvasionSurf.get_rect()
    InvasionRect.center = (WIDTH / 2, HEIGHT / 2 - 10)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.blit(bg, (0, 0))
        SCREEN.blit(InvasionSurf, InvasionRect)

        play.update()
        exit.update()

        if pygame.time.get_ticks() - buttontimer >= 1000:
            buttontimer = pygame.time.get_ticks()
            play.enabled = True
            exit.enabled = True
        pygame.display.update()
        pygame.time.wait(5)


if __name__ == "__main__":
    main()
