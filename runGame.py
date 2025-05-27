import pygame as pyg
from sys import exit
from random import *

class Player(pyg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        plr_walk1 = pyg.image.load('graphics/player/player_walk_1.png').convert_alpha()
        plr_walk2 = pyg.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.plr_walk = [plr_walk1, plr_walk2]
        self.plrIndex = 0
        self.plrJump = pyg.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.plr_walk[self.plrIndex]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        self.jumpSound = pyg.mixer.Sound('audio/jump.mp3')
        self.jumpSound.set_volume(0.5)

    def plrInput(self):
        keys = pyg.key.get_pressed()
        if keys[pyg.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jumpSound.play()

    def applyGravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.plrInput()
        self.applyGravity()
        self.animate()

    def animate(self):
        if self.rect.bottom < 300:
            self.image = self.plrJump
        else:
            self.plrIndex += 0.1
            if self.plrIndex >= len(self.plr_walk): self.plrIndex = 0
            self.image = self.plr_walk[int(self.plrIndex)]

class Obstacle(pyg.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            flyFrame1 = pyg.image.load('graphics/Fly/Fly1.png').convert_alpha()
            flyFrame2 = pyg.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [flyFrame1, flyFrame2]
            yPos = 210
        else:
            snailFrame1 = pyg.image.load('graphics/snail/snail1.png').convert_alpha()
            snailFrame2 = pyg.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snailFrame1, snailFrame2]
            yPos = 300
        self.animationIndex = 0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), yPos))

    def animation(self):
        self.animationIndex += 0.1
        if self.animationIndex >= len(self.frames): self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]

    def update(self):
        self.animation()
        self.rect.left -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

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

def collisionSprite():
    if pyg.sprite.spritecollide(plr.sprite, obstacleGroup, True):
        obstacleGroup.empty()
        return False
    else:
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
bgMusic = pyg.mixer.Sound('audio/music.wav')

plr = pyg.sprite.GroupSingle()
plr.add(Player())

obstacleGroup = pyg.sprite.Group()

# set up the stage
skySurf = pyg.image.load('graphics/Sky.png').convert()
groundSurf = pyg.image.load('graphics/ground.png').convert()
##textSurf = font.render('Running game', True, (64,64,64))
##textRect = textSurf.get_rect(topleft = (300, 100))

# Obstacles
snailFrame1 = pyg.image.load('graphics/snail/snail1.png').convert_alpha()
snailFrame2 = pyg.image.load('graphics/snail/snail2.png').convert_alpha()
snailFrames = [snailFrame1, snailFrame2]
snailIndex = 0
snailSurf = snailFrames[snailIndex]
flyFrame1 = pyg.image.load('graphics/Fly/Fly1.png').convert_alpha()
flyFrame2 = pyg.image.load('graphics/Fly/Fly2.png').convert_alpha()
flyFrames = [flyFrame1, flyFrame2]
flyIndex = 0
flySurf = flyFrames[flyIndex]
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

snailAnimTimer = pyg.USEREVENT + 2
pyg.time.set_timer(snailAnimTimer, 500)

flyAnimTimer = pyg.USEREVENT + 3
pyg.time.set_timer(flyAnimTimer, 200)

bgMusic.play(loops = -1)
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
        if gameState:
            if e.type == obstacleTimer: # Add an obstacle; a snail, or a fly
                if randint(0, 2):
                    obstacleGroup.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                #     # obstacleList.append(snailSurf.get_rect(bottomright = (randint(900, 1100), 300)))
                # else:
                #     obstacleGroup.add(Obstacle('fly'))
                #     # obstacleList.append(flySurf.get_rect(bottomright = (randint(900, 1100), 210)))
            if e.type == snailAnimTimer: # Animate a snail
                snailIndex = 1 if snailIndex == 0 else 0
                snailSurf = snailFrames[snailIndex]
            if e.type == flyAnimTimer: # Animate a fly
                flyIndex = 1 if flyIndex == 0 else 0
                flySurf = flyFrames[flyIndex]
    if gameState:
      src.blit(skySurf, (0,0))
      src.blit(groundSurf, (0, 300))
##      pyg.draw.rect(src, '#c0e8ec', textRect)
##      pyg.draw.rect(src, '#c0e8ec', textRect, 6)
##      src.blit(textSurf, textRect)
      score = displayScore()
##      snailRect.x -= 4

      # plrGrav += 1
      # plrRect.y += plrGrav
      # playerAnim()
      # if plrRect.bottom >= 300:
      #     plrRect.bottom = 300
      # src.blit(plrSurf, plrRect)
      plr.draw(src)
      plr.update()

      obstacleGroup.draw(src)
      obstacleGroup.update()

      # Obstacle movement
      # obstacleList = obstacleMovement(obstacleList)

##      snailRect.left -= 1
##      if snailRect.right <= 0:
##         snailRect.left = 800

      gameState = collisionSprite()
      # gameState = collisions(plrRect, obstacleList)

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
