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
        self._layer = 2
        self.good = getRandBool(70)
        if self.good:
            color = green
        else:
            color = red
        self.radius = 30
        self.image = pygame.Surface((self.radius*2,self.radius*2),flags=pygame.SRCALPHA)
        self.image.convert_alpha()
        pygame.draw.circle(self.image,color,(self.radius,self.radius),30,0)
        self.rect = self.image.get_rect()
        
        startY = random.randrange(sizeY-60)
        self.moveSpeed = random.randrange(2)
        self.moveDir = random.randrange(2)
        self.rect.x = sizeX + 30
        self.rect.y = startY
        self.floatX = float(self.rect.x)
        self.floatY = float(self.rect.y)

        
    def update(self,x_speed,block_group):

        if self.rect.y + self.radius*2 >= sizeY:
            self.moveDir = 2
        elif self.rect.y <= 0:
            self.moveDir = 0
            
        coll_block = 0
        coll_bool = False
        for b in block_group:
            if pygame.sprite.collide_rect(b,self):
                coll_block = get_collideDir(b,self)
                coll_bool = True
                obj_block = b
                break
        
        if coll_block == 1 and coll_bool:
            self.floatX -= x_speed + self.moveSpeed*0.5
            if self.moveDir == 2:
                self.floatY += (1 - self.moveDir)
            else:
                self.floatY = float(obj_block.rect.top-self.rect.height)
        #--#
        elif coll_block == 2 and coll_bool:
            self.floatX -= x_speed + self.moveSpeed*0.5
            if self.moveDir == 0:
                self.floatY += (1 - self.moveDir)
            else:
                self.floatY = float(obj_block.rect.bottom)
        #--#
        elif coll_block == 4 and coll_bool:
            self.floatY += (1 - self.moveDir)
        #--#
        elif coll_block == 5 and coll_bool:
            self.kill()
        
        else:
            self.floatX -= x_speed + self.moveSpeed*0.5
            self.floatY += (1 - self.moveDir)
        
        self.rect.x = int(self.floatX)
       
        #self.floatX -= x_speed
        self.rect.y = int(self.floatY)
        if (self.rect.x < -50) or (
            (self.rect.top + 1 >= sizeY) or (self.rect.bottom - 1 <= 0)):
            self.kill()
        
       
class PlayerBall(pygame.sprite.DirtySprite):
    def __init__ (self,number,posX,posY):
        #self._layer = 2
        pygame.sprite.DirtySprite.__init__(self)
        self._layer = 2
        self.image = pygame.image.load('spaceship.png')
        self.rect = self.image.get_rect()
        
        self.fallBeginT = 400
        self.fallBeginY = posY
        self.rect.x = posX
        self.rect.y = posY
        self.freeFall = True
        self.losted = False
        self.moveSpeed = 0
    def update(self,block_group):
        global sizeY
        if self.freeFall:
            if (sizeY - self.rect.height)>self.rect.y : 
                self.rect.y = freeFall(pygame.time.get_ticks()-self.fallBeginT,self.fallBeginY)
            else:
                self.rect.y = sizeY - self.rect.height
                
        if self.rect.y < (sizeY - self.rect.height):
            self.moveSpeed = 0.8
        else:
            self.moveSpeed = 0
                
    def startFall(self):
        self.fallBeginT = pygame.time.get_ticks()
        self.fallBeginY = self.rect.y
        self.freeFall = True
