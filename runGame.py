import pygame as pyg
from sys import exit
from random import randint

def displayScore(): # Display score
    currTime = int((pyg.time.get_ticks() - startTime)/1000)
    scoreSurf = font.render(f"Score: {currTime}", False, (64,64,64))
    scoreRect = scoreSurf.get_rect(center = (400,50))
    src.blit(scoreSurf, scoreRect)
    return currTime

def obstacleMovement(obstacleList):
    if obstacleList:
        for obstRect in obstacleList:
            obstRect.x -= 5
            if obstRect.bottom == 300:
                src.blit(snailSurf, obstRect)
            else:
                src.blit(flySurf, obstRect)
        obstacleList = [ob for ob in obstacleList if ob.x > -100]
        return obstacleList
    else:
        return []

def collisions(plr, obstacles):
    if obstacles:
        for obst in obstacles:
            if plr.colliderect(obst): return False
    return True

def playerAnim():
    global plrSurf, plrIndex

    if plrRect.bottom < 300:
        plrSurf = plrJump
    else:
        plrIndex += 0.1
        if plrIndex >= len(plr_walk): plrIndex = 0
        plrSurf = plr_walk[int(plrIndex)]

# Set up the window
pyg.init()
src = pyg.display.set_mode((800, 400))
pyg.display.set_caption('Runner Game')
clock = pyg.time.Clock()
font = pyg.font.Font('font/Pixeltype.ttf', 50)
gameState = 0
startTime = 0
score = 0

# set up the stage
skySurf = pyg.image.load('graphics/Sky.png').convert()
groundSurf = pyg.image.load('graphics/ground.png').convert()
##textSurf = font.render('Running game', True, (64,64,64))
##textRect = textSurf.get_rect(topleft = (300, 100))

# Obstacles
snailSurf = pyg.image.load('graphics/snail/snail1.png').convert_alpha()
flySurf = pyg.image.load('graphics/Fly/Fly1.png').convert_alpha()
obstacleList = []

# player stuff
plr_walk1 = pyg.image.load('graphics/player/player_walk_1.png').convert_alpha()
plr_walk2 = pyg.image.load('graphics/player/player_walk_2.png').convert_alpha()
plr_walk = [plr_walk1, plr_walk2]
plrIndex = 0
plrJump = pyg.image.load('graphics/player/jump.png').convert_alpha()
plrSurf = plr_walk[plrIndex]
plrRect = plrSurf.get_rect(midbottom = (80, 300))
plrGrav = 0

# Intro screen
plrStand = pyg.image.load('graphics/player/player_stand.png').convert_alpha()
plrStand = pyg.transform.rotozoom(plrStand, 0,2)
plrStandRect = plrStand.get_rect(center = (400, 200))

gameName = font.render('Snail Jump', False, (111,196,169))
nameRect = gameName.get_rect(center = (400, 80))

gameMessage = font.render('Press space to run!', False, (111, 196, 169))
messageRect = gameMessage.get_rect(center = (400, 320))

# Timer
obstacleTimer = pyg.USEREVENT + 1
pyg.time.set_timer(obstacleTimer, 900)


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
                startTime = pyg.time.get_ticks()

        if e.type == obstacleTimer and gameState: # Add an obstacle; a snail, or a fly
            if randint(0, 2):
                obstacleList.append(snailSurf.get_rect(bottomright = (randint(900, 1100), 300)))
            else:
                obstacleList.append(flySurf.get_rect(bottomright = (randint(900, 1100), 210)))
    if gameState:
      src.blit(skySurf, (0,0))
      src.blit(groundSurf, (0, 300))
##      pyg.draw.rect(src, '#c0e8ec', textRect)
##      pyg.draw.rect(src, '#c0e8ec', textRect, 6)
##      src.blit(textSurf, textRect)
      score = displayScore()
##      snailRect.x -= 4

      plrGrav += 1
      plrRect.y += plrGrav
      playerAnim()
      if plrRect.bottom >= 300:
          plrRect.bottom = 300
      src.blit(plrSurf, plrRect)

      # Obstacle movement
      obstacleList = obstacleMovement(obstacleList)

##      snailRect.left -= 1
##      if snailRect.right <= 0:
##         snailRect.left = 800

      gameState = collisions(plrRect, obstacleList)

    else:
        src.fill((94,129,162))
        src.blit(plrStand, plrStandRect)
        obstacleList.clear()
        plrRect.midbottom = (80, 300)
        plrGrav = 0
        
        scoreMsg = font.render(f"Your score is {score}",False,(111,196,169))
        msgRect = scoreMsg.get_rect(center = (400,330))
        src.blit(gameName, nameRect)
        
        if score == 0:
            src.blit(gameMessage, messageRect)
        else:
            src.blit(scoreMsg, msgRect)
        

    pyg.display.update()
    clock.tick(60)
