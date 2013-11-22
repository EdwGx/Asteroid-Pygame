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
    font = pygame.font.SysFont("Candara",30)
    Label = font.render('back',True,white)
    screen.blit(Label,
                ((sizeX - Label.get_width())/2,
                 (sizeY - Label.get_height())/2 + 120))

    tfont = pygame.font.SysFont("Candara",40)
    creditLabel = tfont.render('Created by',True,white)
    screen.blit(creditLabel,
                ((sizeX - creditLabel.get_width())/2,
                 (sizeY - creditLabel.get_height())/2-170))

    sfont = pygame.font.SysFont("Candara",50)
    creditLabel1 = sfont.render('Steven DesBrisay',True,white)
    screen.blit(creditLabel1,
                ((sizeX - creditLabel1.get_width())/2,
                 (sizeY - creditLabel1.get_height())/2-90))

    creditLabel2 = sfont.render('Edward Guo',True,white)
    screen.blit(creditLabel2,
                ((sizeX - creditLabel2.get_width())/2,
                 (sizeY - creditLabel2.get_height())/2-40))

    creditLabel3 = sfont.render('Vincent Tran',True,white)
    screen.blit(creditLabel3,
                ((sizeX - creditLabel3.get_width())/2,
                 (sizeY - creditLabel3.get_height())/2+10))
    
    pygame.display.flip()
    clock.tick(60)
    
        
