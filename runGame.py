import pygame as pyg
from sys import exit

def displayScore():
    currTime = int((pyg.time.get_ticks() - startTime)/1000)
    scoreSurf = font.render(f"Score: {currTime}", False, (64,64,64))
    scoreRect = scoreSurf.get_rect(center = (400,50))
    src.blit(scoreSurf, scoreRect)

pyg.init()
src = pyg.display.set_mode((800, 400))
pyg.display.set_caption('Runner Game')
clock = pyg.time.Clock()
font = pyg.font.Font('font/Pixeltype.ttf', 50)
gameState = 1
startTime = 0

skySurf = pyg.image.load('graphics/Sky.png').convert()
groundSurf = pyg.image.load('graphics/ground.png').convert()
##textSurf = font.render('Running game', True, (64,64,64))
##textRect = textSurf.get_rect(topleft = (300, 100))
snailSurf = pyg.image.load('graphics/snail/snail1.png').convert_alpha()
snailXPos = 600

plrSurf = pyg.image.load('graphics/player/player_walk_1.png').convert_alpha()
plrRect = plrSurf.get_rect(midbottom = (80, 300))
plrGrav = 0

snailRect = snailSurf.get_rect(midbottom = (600, 300))

while 1:
    for e in pyg.event.get():
        if e.type == pyg.QUIT:
            pyg.quit()
            exit()
        if gameState:
            if e.type == pyg.MOUSEBUTTONDOWN:
                print('click')
                if plrRect.collidepoint(e.pos) and plrRect.bottom >= 300:
                    plrGrav -= 20
                    
            if e.type == pyg.KEYDOWN:
                if e.key == pyg.K_SPACE and plrRect.bottom >= 300:
                    plrGrav = -20
        else: #Restart game
            if e.type == pyg.KEYDOWN and e.key == pyg.K_SPACE:
                gameState = 1
                snailRect.left = 800
                startTime = pyg.time.get_ticks()

    if gameState:
      src.blit(skySurf, (0,0))
      src.blit(groundSurf, (0, 300))
##      pyg.draw.rect(src, '#c0e8ec', textRect)
##      pyg.draw.rect(src, '#c0e8ec', textRect, 6)
##      src.blit(textSurf, textRect)
      displayScore()
      src.blit(snailSurf, snailRect)
      snailRect.x -= 4

      plrGrav += 1
      plrRect.y += plrGrav
      if plrRect.bottom >= 300:
          plrRect.bottom = 300
      src.blit(plrSurf, plrRect)

      snailRect.left -= 1
      if snailRect.right <= 0:
         snailRect.left = 800
         
      if plrRect.colliderect(snailRect):
         gameState = 0
         
    else:
        src.fill('Yellow')

    pyg.display.update()
    clock.tick(60)
