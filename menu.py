#menu.py
import pygame
from color import*

clock = pygame.time.Clock()
sizeX = 800
sizeY = 500
background = pygame.image.load('background.jpg')

def draw(screen):
    mouse_up = False
    rect1 =  pygame.Rect(0,0,230,70)
    rect1.center = (sizeX/2,sizeY/2-100)
    
    rect2 =  pygame.Rect(0,0,230,70)
    rect2.center = (sizeX/2,sizeY/2)
    
    rect3 =  pygame.Rect(0,0,230,70)
    rect3.center = (sizeX/2,sizeY/2+100)
    
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
            return 1
        else:
            pygame.draw.rect(screen,darkgreen,rect1)
    else:
        pygame.draw.rect(screen,green,rect1)

    if rect2.collidepoint(mX,mY):
        if mouse_up:
            return 2
        else:
            pygame.draw.rect(screen,darkgreen,rect2)
    else:
        pygame.draw.rect(screen,green,rect2)

    if rect3.collidepoint(mX,mY):
        if mouse_up:
            return 3
        else:
            pygame.draw.rect(screen,darkgreen,rect3)
    else:
        pygame.draw.rect(screen,green,rect3)
        
    font = pygame.font.SysFont("comicsansms",30)
    Label = font.render('Single Player',True,white)
    screen.blit(Label,
                ((sizeX - Label.get_width())/2,(sizeY - Label.get_height())/2-100))
    Label = font.render('Two Players',True,white)
    screen.blit(Label,
                ((sizeX - Label.get_width())/2,(sizeY - Label.get_height())/2))
    Label = font.render('Credits',True,white)
    screen.blit(Label,
                ((sizeX - Label.get_width())/2,(sizeY - Label.get_height())/2+100))
    pygame.display.flip()
    clock.tick(60)
    
        
