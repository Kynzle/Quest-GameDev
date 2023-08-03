import pygame
import math
import random

RED = (255, 0, 0)
WHITE = (255, 255, 255)

#описываем класс курсора
class Mouse(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('cursor.png')
        self.rect = pygame.Rect(0, 0, 0, 0)

#описываем класс оружия
class Weapon(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('weapon.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def draw(self):
        screen.blit(self.image, self.rect)
    
    #создание объекта пуля
    def shoot(self,angle,a,b):
        bullet = Bullet(500, self.rect.top,angle,a, b)
        all_sprites.add(bullet)
        bullets.add(bullet)

#описываем класс мишеней
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(-150, 0)
        self.rect.y = random.randrange(50, 300)
        self.speedy = random.randrange(-2,2)
        self.speedx = random.randrange(3,9)
    
    #описываем,что мишени движутся хаотично
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > 800 + 10  < -25 or self.rect.right > 1200 + 20:
            self.rect.x = random.randrange(-100, 0)
            self.rect.y = random.randrange(50, 300)
            self.speedy = random.randrange(-1,1)
            self.speedx = random.randrange(3,5)

#описываем класс пуль 
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, a,b):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image = pygame.image.load('bullet.png')
        self.rect = self.image.get_rect()
        self.rect.y= y
        self.rect.x = x
        self.speed = 50
        self.speedx = 0
        self.speedy = 0

        #расчитываем скорость в зависимости от угла, в которой направлена пуля
        self.speedx = (self.speed * math.cos(angle/57.2))
        self.speedy = (self.speed * math.sin(angle/57.2))
      
    def update(self):
        self.rect.x += self.speedx
        self.rect.y -= self.speedy
        # удаляем пулю, если она заходит за верхнюю или правую часть экрана
        if self.rect.y < 0 or self.rect.x > 1000:
            self.kill()       

pygame.init()
 
screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()
mouse = Mouse((0, 0))
weapon = Weapon((500, 500))
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites.add(bullets)

for i in range(5):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
   
otstup = pygame.math.Vector2(10, 10)
 
running = [True]
while running:
        screen.fill(WHITE)
 
        # получаем позицию курсора
        mouse_pos = pygame.mouse.get_pos()
        mouse.rect.x = mouse_pos[0]
        mouse.rect.y = mouse_pos[1]

        #скрываем системный курсор
        pygame.mouse.set_visible(0)
 
        #сохраняем координаты точки нахождения курсора
        b = mouse.rect.x + 68
        a = mouse.rect.y + 68
        
        #вычисляем растояние между точкой курсора и точкой в которой находится оружие
        delx = b - 500
        dely = 500 - a
        
        #расчитываем sin и cos для этих точек
        cos = delx / ((math.sqrt(math.pow(dely , 2) + math.pow(delx , 2))) + 0.01)
        sin = dely / ((math.sqrt(math.pow(dely , 2) + math.pow(delx , 2))) + 0.01)
        
        #расчитываем градус угла к точке в который находится курсор мыши 
        angle = (((math.acos(cos))*57.2)) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    weapon.shoot(angle, a, b)
        
        all_sprites.update()

        #задаем шкалу вращение и переворачиваем оружие на заданный угол
        weapon_image = pygame.transform.rotozoom(weapon.image, angle-90, 1)
        weapon_otstup = otstup.rotate(-angle)
        weapon_rect = weapon_image.get_rect(center=(500, 450) + weapon_otstup)
      
        #проверка на попадание в мишени
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        screen.blit(mouse.image, mouse.rect)
 
        all_sprites.draw(screen)
        screen.blit(weapon_image, weapon_rect)  
        pygame.display.flip()              
        clock.tick(24)


pygame.quit ()
