import os
import pygame
import random

pygame.init()

HEIGHT = 400
WIDTH = 300

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('The Invasion')

DAMAGE_IMG = pygame.image.load(os.path.join('source/explosion', 'damage.png'))
DESTROY_IMG = pygame.image.load(os.path.join('source/explosion', 'destroy.png'))


class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, 30)

    def update(self, life):
        textsurface = self.font.render('Score: {}'.format(self.score), True, (255, 255, 255))
        SCREEN.blit(textsurface, (0, 0))
        textsurface = self.font.render('Health: {}'.format(life), True, (255, 255, 255))
        SCREEN.blit(textsurface, (0, 30))


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


class Boss(pygame.sprite.Sprite):
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
        self.img = pygame.image.load(os.path.join('source/boss', 'boss.png'))

    def update(self):
        pass

    def fire(self):
        pass

    def destroy(self):
        pass

def main():
    endgame = False
    createenemy_time = 2000
    timeing_create = 0
    bg = pygame.image.load(os.path.join('source', 'background.jpg'))
    enemys_arr = [Enemy() for i in range(2)]
    hero = Hero()
    score = Score()
    while not endgame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        SCREEN.blit(bg, (0, 0))
        hero.interface()
        hero.update()
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

        for i in enemys_arr:
            if i.get_damage:
                i.destroy()
            elif i.health <= 0 or i.y > HEIGHT:
                enemys_arr[enemys_arr.index(i)] = Enemy()
                score.score += 10
        if hero.get_damage:
            hero.destroy()
        if createenemy_time <= timeing_create:
            timeing_create = 0
            enemys_arr.append(Enemy())
        else:
            timeing_create += 1
        score.update(hero.health)
        pygame.display.update()
        pygame.time.wait(5)


if __name__ == "__main__":
    main()
