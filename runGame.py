import pygame as pyg
from sys import exit

pyg.init()
src = pyg.display.set_mode((800, 400))
pyg.display.set_caption('Runner Game')
clock = pyg.time.Clock()
font = pyg.font.Font('font/Pixeltype.ttf', 50)

skySurf = pyg.image.load('graphics/Sky.png').convert()
groundSurf = pyg.image.load('graphics/ground.png').convert()
textSurf = font.render('Running game', True, 'black')
textRect = textSurf.get_rect(topleft = (300, 100))
snailSurf = pyg.image.load('graphics/snail/snail1.png').convert_alpha()
snailXPos = 600

plrSurf = pyg.image.load('graphics/player/player_walk_1.png').convert_alpha()
plrRect = plrSurf.get_rect(midbottom = (80, 300))
snailRect = snailSurf.get_rect(midbottom = (600, 300))

while 1:
    for e in pyg.event.get():
        if e.type == pyg.QUIT:
            pyg.quit()
            exit()
##        if e.type == pyg.MOUSEMOTION:
##            if plrRect.collidepoint(e.pos):
##                print('collision')
    src.blit(skySurf, (0,0))
    src.blit(groundSurf, (0, 300))
    pyg.draw.rect(src, 'Pink', textRect)
    pyg.draw.rect(src, 'Pink', textRect, 6)
    src.blit(textSurf, textRect)
    src.blit(snailSurf, snailRect)
    snailRect.x -= 4
    src.blit(plrSurf, plrRect)

    mousePos = pyg.mouse.get_pos()
##    if plrRect.collidepoint(mousePos):
##        print(pyg.mouse.get_pressed())
    
    pyg.display.update()
    clock.tick(60)
    snailRect.left -= 1
    if snailRect.right <= 0:
        snailRect.left = 800
