import pygame
import chemistry

black    = (   0,   0,   0)
white    = ( 255, 255, 255)
asphalt = (52, 73, 94)
green    = (  46, 204, 113)
red      = ( 231, 76, 60)
blue     = ( 52, 152, 219)
turquoise =  (26, 188, 156)
grey = (149, 165, 166)

class Atom(pygame.sprite.DirtySprite):
    def __init__ (self,at_num):
        #Lower than block and mouse
        self._layer = 2
        pygame.sprite.DirtySprite.__init__(self,full_list,atom_list)
        #basic init
        self.radius = 30
        self.ion = 0
        self.atomic = at_num
        self.shell = chemistry.get_shells(at_num) 
        
        #shape
        self.redraw()
        self.rect = self.image.get_rect()
        
    def redraw(self):
        self.image = pygame.Surface((self.radius*2,self.radius*2),flags=pygame.SRCALPHA)
        self.image.convert_alpha()
        pygame.draw.circle(self.image,blue,(self.radius,self.radius),30,0)
        #symbol
        symbolFont = pygame.font.SysFont("Georgia",20)
        symbolLabel = symbolFont.render(chemistry.getSymbol(self.atomic),True,white)
        #Get Letters Size and Center
        #ion
        if self.ion == 0:
            finLabel = symbolLabel
        else:
            symbolFont = pygame.font.SysFont("Georgia",10)
            if self.ion > 0:
                ionText = str(abs(self.ion)) + "+"
            elif self.ion < 0:
                ionText = str(abs(self.ion)) + "-"
            ionLabel = symbolFont.render(ionText,True,white)

            finLabel = pygame.Surface(
                (symbolLabel.get_width()+ionLabel.get_width(),symbolLabel.get_height()),
                flags=pygame.SRCALPHA)
            finLabel.blit(symbolLabel,(0,0))
            finLabel.blit(ionLabel,(symbolLabel.get_width(),0))
        #draw label
        self.image.blit(finLabel,
                        (self.radius-int(symbolLabel.get_width()/2),
                         self.radius-int(symbolLabel.get_height()/2)))
        
        
class PlayerAtom(Atom):
    def __init__ (self,at_num,posX,posY):
        Atom.__init__(self,at_num)
        self.fallBeginT = 400
        self.fallBeginY = posY
        self.rect.x = posX
        self.rect.y = posY
        self.freeFall = True
    def update(self):
        global sizeY
        if self.freeFall and ((sizeY - self.radius*2)>self.rect.y): 
            self.rect.y = freeFall(pygame.time.get_ticks()-self.fallBeginT,self.fallBeginY)
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
    
                                    
def freeFall(time_after,start_y):   
    return int((start_y + (9.81* time_after * time_after / 1000000)))


    
 
pygame.init()
#Things must be do first
full_list = pygame.sprite.LayeredUpdates()
atom_list = pygame.sprite.LayeredUpdates()
pygame.mouse.set_visible(False)

#Def varibles
sizeX = 800
sizeY = 500
screen = pygame.display.set_mode([sizeX,sizeY])
font = pygame.font.SysFont("comicsansms",30)
pygame.display.set_caption("My Game")

#init player
player = PlayerAtom(1,200,400)
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
        
    if moveY:
        player.rect.y -= 2

    mX = (pygame.mouse.get_pos())[0]
    mY = (pygame.mouse.get_pos())[1]
    frames = 60
    #logic
    coll_mouse_list = atom_list.get_sprites_at((mX,mY))
    
    #draw
    screen.fill(grey)
    t = pygame.time.get_ticks()
    timeLabel = font.render(str(t),True,green)
    screen.blit(timeLabel,(300,300))

    full_list.update()
    full_list.draw(screen)

    draw_mouse()
    #draw end
     
    pygame.display.flip()
    clock.tick(frames)
     

pygame.quit()

