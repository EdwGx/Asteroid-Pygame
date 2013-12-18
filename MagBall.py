import pygame
import random
from color import*
from physic import*
sizeX = 800
sizeY = 500

class bullet(pygame.sprite.DirtySprite):
    def __init__ (self,x,y,right = True):
        pygame.sprite.DirtySprite.__init__(self)
        self._layer = 1
        self.go_right = right
        self.shooter = 0
        self.image = pygame.Surface((10,8),flags=pygame.SRCALPHA)
        self.image.convert_alpha()
        if self.go_right:
            pygame.draw.polygon(self.image,yellow,((0,0),(0,8),(10,4)),0)
        else:
            pygame.draw.polygon(self.image,yellow,((10,0),(10,8),(0,4)),0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        if self.go_right:
            self.rect.x += 3
            if self.rect.x >= 830:
                self.kill()
        else:
            self.rect.x -= 3
            if self.rect.x <= -30:
                self.kill()

class BadBall(pygame.sprite.DirtySprite):
    def __init__ (self):
        pygame.sprite.DirtySprite.__init__(self)
        self.moveSpeed = random.randrange(2)
        self.moveDir = random.randrange(2)

    def update(self,x_speed):

        if self.rect.y + self.rect.height >= sizeY:
            self.moveDir = 2
        elif self.rect.y <= 0:
            self.moveDir = 0
            
        self.floatX -= x_speed + self.moveSpeed*0.5
        self.floatY += (1 - self.moveDir)
        
        self.rect.x = int(self.floatX)
       
        #self.floatX -= x_speed
        self.rect.y = int(self.floatY)
        if (self.rect.x < -50) or (
            (self.rect.top + 1 >= sizeY) or (self.rect.bottom - 1 <= 0)):
            self.kill()

class Asteroid(BadBall):
    def __init__ (self):
        BadBall.__init__(self)
        self._layer = 4
        self.good = True
        self.image = pygame.image.load('asteroid.png')
        self.rect = self.image.get_rect()
        startY = random.randrange(sizeY-60)
        self.rect.x = sizeX + 30
        self.rect.y = startY
        self.floatX = float(self.rect.x)
        self.floatY = float(self.rect.y)

class Bomb(BadBall):
    def __init__ (self):
        BadBall.__init__(self)
        self._layer = 5
        self.good = False
        self.image = pygame.image.load('bomb.png')
        self.rect = self.image.get_rect()
        startY = random.randrange(sizeY-60)
        self.rect.x = sizeX + 30
        self.rect.y = startY
        self.floatX = float(self.rect.x)
        self.floatY = float(self.rect.y)
        
class Missile(pygame.sprite.DirtySprite):
    def __init__ (self):
        pygame.sprite.DirtySprite.__init__(self)
        self._layer = 2
        self.image = pygame.image.load('missile.png')
        self.rect = self.image.get_rect()
        self.rect.x = -135
        self.rect.y = 200
    def update(self):
        if self.rect.x > 0:
            mY = (pygame.mouse.get_pos())[1]
            if self.rect.y -1 > mY:
                self.rect.y -= 2
            elif self.rect.y +1 < mY:
                self.rect.y += 2
            else:
                self.rect.y = mY
        self.rect.x += 3
        if self.rect.x > 810:
            self.kill()
                
        

class PlayerBall(pygame.sprite.DirtySprite):
    def __init__ (self,posX,posY,green_pic=False):
        #self._layer = 2
        pygame.sprite.DirtySprite.__init__(self)
        self._layer = 2
        if green_pic:
            self.image = pygame.image.load('spaceship2.png')
        else:
            self.image = pygame.image.load('spaceship.png')
        self.rect = self.image.get_rect()

        self.score = 0
        self.fallBeginT = 400
        self.fallBeginY = posY
        self.rect.x = posX
        self.rect.y = posY
        self.freeFall = True
        self.losted = False
        self.moveSpeed = 1.2
    def update(self):
        global sizeY
        if self.freeFall:
            if (sizeY - self.rect.height)>self.rect.y : 
                self.rect.y = freeFall(pygame.time.get_ticks()-self.fallBeginT,self.fallBeginY)
            else:
                self.rect.y = sizeY - self.rect.height

    def startFall(self):
        self.fallBeginT = pygame.time.get_ticks()
        self.fallBeginY = self.rect.y
        self.freeFall = True
