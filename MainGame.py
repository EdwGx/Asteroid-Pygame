import pygame
import random

from physic import*
from color import*
from sprite import*

class MagBall(pygame.sprite.DirtySprite):
    def __init__ (self,number,color,mu,di):
        #Lower than block and mouse
        self._layer = 2
        pygame.sprite.DirtySprite.__init__(self,full_list,ball_list)
        #basic init
        self.radius = 30
        self.mu = mu
        self.di = di
        self.color = color
        self.number = number 
        #shape
        self.redraw()
        self.rect = self.image.get_rect()
        
    def redraw(self):
        self.image = pygame.Surface((self.radius*2,self.radius*2),flags=pygame.SRCALPHA)
        self.image.convert_alpha()
        pygame.draw.circle(self.image,self.color,(self.radius,self.radius),30,0)
        if self.number > 0:
            if self.mu:
                strings = '*'+ str(self.number)
            elif self.di:
                strings = '/'+ str(self.number)
            else:
                strings = '+' + str(self.number)
        elif self.number < 0:
            if self.mu:
                strings = '*('+ str(self.number) +')'
            elif self.di:
                strings = '/('+ str(self.number) + ')'
            else:
                strings = str(self.number)
        else:
            strings = '0'
        numberFont = pygame.font.SysFont("Arial",20,True)
        numberLabel = numberFont.render(strings,True,white)
        self.image.blit(numberLabel,
                        (self.radius-int(numberLabel.get_width()/2),
                         self.radius-int(numberLabel.get_height()/2)))

class BadBall(MagBall):
    def __init__ (self):
        global bad_list
        rand = random.randrange(9)
        randNum = random.randint(-5,5)
        if rand < 2:
            mu = False
            di = False
        elif rand < 6:
            mu = False
            di = False
        elif rand < 8:
            mu = True
            di = False
        else:
            mu = False
            di = True
        if (randNum < 0) or (di):
            color = red
        else:
            color = green
        MagBall.__init__(self,randNum,color,mu,di)
        startY = random.randrange(sizeY-60)
        self.moveSpeed = random.randrange(2)
        self.moveDir = random.randrange(2)
        self.rect.x = sizeX + 30
        self.rect.y = startY
        self.floatX = float(self.rect.x)
        self.floatY = float(self.rect.y)
        bad_list.add(self)
        
    def update(self):
        if self.rect.x < -50:
            self.kill()
        self.floatX -= 0.8 + self.moveSpeed*0.5
        self.rect.x = int(self.floatX)
        
       
class PlayerBall(MagBall):
    def __init__ (self,number,posX,posY):
        MagBall.__init__(self,number,blue,False,False)
        self.fallBeginT = 400
        self.fallBeginY = posY
        self.rect.x = posX
        self.rect.y = posY
        self.freeFall = True
    def update(self):
        global sizeY,playerLosted
        if self.number == 0:
            playerLosted = True
            print 'you lost'
        if self.freeFall:
            if (sizeY - self.radius*2)>self.rect.y : 
                self.rect.y = freeFall(pygame.time.get_ticks()-self.fallBeginT,self.fallBeginY)
            else:
                self.rect.y = sizeY - self.radius*2
    def startFall(self):
        self.fallBeginT = pygame.time.get_ticks()
        self.fallBeginY = self.rect.y
        self.freeFall = True

def draw_mouse():
    global mX,mY
    line_len = 10
    from_center = 5
    # - part
    pygame.draw.line(screen,red,
                     (mX-line_len-from_center,mY),
                     (mX-from_center,mY),3)
    pygame.draw.line(screen,red,
                     (mX+line_len+from_center,mY),
                     (mX+from_center,mY),3)
    # | part
    pygame.draw.line(screen,red,
                     (mX,mY-line_len-from_center),
                     (mX,mY-from_center),3)
    pygame.draw.line(screen,red,
                     (mX,mY+line_len+from_center),
                     (mX,mY+from_center),3)
    # center part
    pygame.draw.circle(screen,red,(mX,mY),3,0)

'''def number_collide(spriteA,spriteB):
    if ((spriteA.mu == False) and (spriteA.di == False)) and(
        (spriteB.mu == False) and (spriteB.di == False)):
            spriteA.number += spriteB.number
    elif badBall.mu:
        player.number = player.number*badBall.number
    elif badBall.di:
        if player.number%badBall.number == 0:
            player.number = int(player.number/badBall.number)
        else:
            print ('not integer')
    player.redraw()'''

def jump_bar():
    global jumPower, moveY
    if jumPower > 0:
        if jumPower > 0.3:
            draw_color = green
        else:
            draw_color = red
        pygame.draw.rect(screen,
                         draw_color,
                         pygame.Rect(10,sizeY-30,100*jumPower,20))
    else:
        jumPower = 0
        if moveY:
            moveY = False
            player.startFall()

    
                                     
pygame.init()
#Things must be do first
full_list = pygame.sprite.LayeredUpdates()
ball_list = pygame.sprite.LayeredUpdates()
bad_list = pygame.sprite.Group()

pygame.mouse.set_visible(False)

#Def varibles
sizeX = 800
sizeY = 500
jumPower = 1
screen = pygame.display.set_mode([sizeX,sizeY])
font = pygame.font.SysFont("comicsansms",30)
pygame.display.set_caption("My Game")
playerLosted = False

#init player
player = PlayerBall(1,200,400)
player.add(full_list,ball_list)
BadBall()
player.add(full_list,ball_list)
BadBall()
BadBall()
BadBall()
moveY = False


done = False

 
clock = pygame.time.Clock()
 
while done == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                moveY = True
                player.freeFall = False
            if event.key == pygame.K_a:
                player.ion += 2
                player.redraw()
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                moveY = False
                player.startFall()
        
    if moveY and jumPower > 0:
        if player.rect.y >= 2:
            player.rect.y -= 2
        else:
            player.rect.y = 0
            
        jumPower -= 0.02
    else:
        if jumPower <= 0.98:
            jumPower += 0.02
            

    mX = (pygame.mouse.get_pos())[0]
    mY = (pygame.mouse.get_pos())[1]
    frames = 60
    #logic
    #coll_mouse_list = atom_list.get_sprites_at((mX,mY))
    for badBall in bad_list:
        for ballB in pygame.sprite.spritecollide(badBall,bad_list,False,pygame.sprite.collide_circle):
            if not(badBall == ballB):
                print 'killed'
                number_collide(badBall,ballB,True,True)
            
        
        coll_bad_player = pygame.sprite.spritecollide(player,bad_list,True,pygame.sprite.collide_circle)
    for badBall in coll_bad_player:
        kill_player = number_collide(player,badBall,False,True)
        if kill_player:
            playerLosted = True
            print 'you lost'

                    
                    
                
        
    
    
    #draw
    screen.fill(grey)
    #test
    t = pygame.time.get_ticks()
    timeLabel = font.render(str(t),True,green)
    screen.blit(timeLabel,(300,300))

    #real draw
    full_list.update()
    full_list.draw(screen)

    jump_bar()
    draw_mouse()
    #draw end
     
    pygame.display.flip()
    clock.tick(frames)
     

pygame.quit()

