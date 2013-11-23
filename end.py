#end.py
import pygame
from color import*

clock = pygame.time.Clock()
sizeX = 800
sizeY = 500
background = pygame.image.load('background.jpg')

def draw(screen,score,dual_player=False,score2=0):
    mouse_up = False
    rect1 =  pygame.Rect(0,0,100,60)
    rect1.center = (sizeX/2,sizeY/2 +100)

    rect2 =  pygame.Rect(0,0,100,60)
    rect2.center = (sizeX/2,sizeY/2 +180)
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
                                              
    font = pygame.font.SysFont("comicsansms",30)
    Label = font.render('Retry',True,white)
    screen.blit(Label,
                ((sizeX - Label.get_width())/2,(sizeY - Label.get_height())/2 +100))

    Label = font.render('Menu',True,white)
    screen.blit(Label,
                ((sizeX - Label.get_width())/2,(sizeY - Label.get_height())/2 +180))
    
    if not(dual_player): 
        sfont = pygame.font.SysFont("comicsansms",50)
        scoreLabel = sfont.render(('Your Score is ') + str(score),True,white)
        screen.blit(scoreLabel,
                    ((sizeX - scoreLabel.get_width())/2,
                     (sizeY - scoreLabel.get_height())/2-100))
    else:
        sfont = pygame.font.SysFont("comicsansms",50)
        scoreLabel = sfont.render(('Your Score is'),True,white)
        screen.blit(scoreLabel,
                    ((sizeX - scoreLabel.get_width())/2,
                     (sizeY - scoreLabel.get_height())/2-100))

        ssfont = pygame.font.SysFont("comicsansms",40)
        scoreLabel2 = ssfont.render(str(score),True,white)
        screen.blit(scoreLabel2,
                    ((sizeX - scoreLabel2.get_width())/2-100,
                     (sizeY - scoreLabel2.get_height())/2))

        scoreLabel3 = ssfont.render(str(score2),True,white)
        screen.blit(scoreLabel3,
                    ((sizeX - scoreLabel3.get_width())/2+100,
                     (sizeY - scoreLabel3.get_height())/2))
        
        image1 = pygame.image.load('spaceship.png')
        screen.blit(image1,
                    ((sizeX - image1.get_width())/2-200,
                     (sizeY - image1.get_height())/2))
        
        image2 = pygame.image.load('spaceship2.png')
        screen.blit(image2,
                    ((sizeX - image2.get_width())/2+200,
                     (sizeY - image2.get_height())/2))
    
    pygame.display.flip()
    clock.tick(60)
    
        
