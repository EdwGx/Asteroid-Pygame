#credit.py
import pygame
from color import*

clock = pygame.time.Clock()
sizeX = 800
sizeY = 500
background = pygame.image.load('background.jpg')

def draw(screen):
    mouse_up = False
    rect1 =  pygame.Rect(0,0,100,60)
    rect1.center = (sizeX/2,sizeY/2 +120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_up = True
    mX = (pygame.mouse.get_pos())[0]
    mY = (pygame.mouse.get_pos())[1]
    screen.blit(background,background.get_rect())
    if rect1.collidepoint(mX,mY):
        if mouse_up:
            return True
        else:
            pygame.draw.rect(screen,darkgreen,rect1)
    else:
        pygame.draw.rect(screen,green,rect1)
    font = pygame.font.SysFont("comicsansms",30)
    Label = font.render('back',True,white)
    screen.blit(Label,
                ((sizeX - Label.get_width())/2,
                 (sizeY - Label.get_height())/2 + 120))

    sfont = pygame.font.SysFont("comicsansms",50)
    creditLabel = sfont.render('Credits',True,white)
    screen.blit(creditLabel,
                ((sizeX - creditLabel.get_width())/2,
                 (sizeY - creditLabel.get_height())/2-170))

    creditLabel1 = sfont.render('xxx',True,white)
    screen.blit(creditLabel1,
                ((sizeX - creditLabel1.get_width())/2,
                 (sizeY - creditLabel1.get_height())/2-120))

    creditLabel2 = sfont.render('xxxxx',True,white)
    screen.blit(creditLabel2,
                ((sizeX - creditLabel2.get_width())/2,
                 (sizeY - creditLabel2.get_height())/2-70))

    creditLabel3 = sfont.render('xxxx',True,white)
    screen.blit(creditLabel3,
                ((sizeX - creditLabel3.get_width())/2,
                 (sizeY - creditLabel3.get_height())/2-20))
    
    pygame.display.flip()
    clock.tick(60)
    
        
