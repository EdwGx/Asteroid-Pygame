#Block
import pygame
import random
from color import*
import physic

sizeX = 800
sizeY = 500

def draw_plus(surface,pos):
    pygame.draw.rect(surface,white,(pos[0]-5,pos[1]-15,10,30))
    pygame.draw.rect(surface,white,(pos[0]-15,pos[1]-5,30,10))

def draw_minus(surface,pos):
    pygame.draw.rect(surface,white,(pos[0]-10,pos[1]-5,30,10))
    

class Block(pygame.sprite.DirtySprite):
    def __init__(self):
        self._layer = 3
        pygame.sprite.DirtySprite.__init__(self)
        self.good = physic.getRandBool(30)
        self.moveSpeed = random.randrange(1)
        self.moveUp = True
        self.image = pygame.Surface((56,156))
        if self.good:
            self.image.fill(green)
            draw_plus(self.image,(28,48))
            draw_plus(self.image,(28,108))
        else:
            self.image.fill(red)
            draw_minus(self.image,(28,48))
            draw_minus(self.image,(28,108))
        self.rect = self.image.get_rect()
        self.rect.x = sizeX + 60
        self.rect.y = 0
        self.floatX = float(self.rect.x)
        self.floatY = float(self.rect.y)
        
    def update(self,y_speed):
        self.floatX -= y_speed
        self.rect.x = int(self.floatX)

        if self.rect.y <= 0:
            self.floatY = float(0)
            self.moveUp = False
        elif self.rect.y >= sizeY - 156:
            self.floatY = float(sizeY - 156)
            self.moveUp = True
            
        if self.moveUp:
            self.floatY -= 1 + self.moveSpeed*0.8
            self.rect.y = int(self.floatY)
        else:
            self.floatY += 1 + self.moveSpeed*0.8
            self.rect.y = int(self.floatY)

        if self.rect.x < -80:
            self.kill()
        
