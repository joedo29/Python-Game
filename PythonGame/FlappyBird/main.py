# CS320 Programming Language
# Author: Joe Do
# Date: March 01, 2018
# The purpose of this program is to create a clone of the Flappy Bird game

import pygame
import random
import time

# initiate pygame module
pygame.init()

# set text color
black = (0, 0, 0)
white = (255, 255, 255)
red   = (255, 0, 0)

# set width and height for the game
display_width  = 288
display_height = 512
bird_height    = 24
base_height    = 112
pipe_height    = 320

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Flappy Bird Clone')
clock = pygame.time.Clock()

# load all the graphics and sound here
startScreen  = pygame.image.load('assets/images/message1.png')
birdImage    = pygame.image.load('assets/images/redbird-upflap.png')
pipeImage    = pygame.image.load('assets/images/pipe-red.png')
bg           = pygame.image.load('assets/images/background-night.png')
base         = pygame.image.load('assets/images/base.png')
gameover     = pygame.image.load('assets/images/gameover.png')
soundWing    = pygame.mixer.Sound('assets/audio/wing.wav')
soundHit     = pygame.mixer.Sound('assets/audio/hit.wav')
soundDie     = pygame.mixer.Sound('assets/audio/die.ogg')
soundPoint   = pygame.mixer.Sound('assets/audio/point.ogg')
soundWin     = pygame.mixer.Sound('assets/audio/point.wav')

# Flip the pipe over
pipeInvert   = pygame.transform.rotate(pipeImage,180)

# bird function to display the bird
def bird(x, y):
    gameDisplay.blit(birdImage, (x, y)) # blit bird image in x and y coordinates

# move base accorss the screen
def base_move(baseStartX):
   baseEndX = baseStartX % base.get_rect().width
   gameDisplay.blit(base,(baseEndX - base.get_rect().width, display_height - 112))
   if baseEndX < display_width:
       gameDisplay.blit(base, (baseEndX, display_height - 112))

# this function will print out score
def passedPipe(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(count), True, white)
    gameDisplay.blit(text, (0, 0))

# Display the bottom pipe
def bottomPipe(xCoordinate, yCoordinate):
    gameDisplay.blit(pipeImage, (xCoordinate, yCoordinate))

# Display the top pipe
def topPipe(xCoordinate, yCoordinate):
    gameDisplay.blit(pipeInvert, (xCoordinate, yCoordinate))

# Keep the game going after bird crashed
def crash():
    game_loop()

# display start screen at start of game, and when player loses
def game_intro():
   startInitialized = False
   while not startInitialized:
       gameDisplay.blit(bg, (0, 0))
       gameDisplay.blit(startScreen,(55,80))
       gameDisplay.blit(base,(0, display_height - 112))
       pygame.display.update()
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               quit()
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_b:
                   startInitialized = True

# this is the main game loop
def game_loop():
    birdX       = display_width / 3
    birdY       = (display_height - base_height) / 2
    birdMove    = 0
    pipeStartX  = display_width + 100
    pipeBottomY = 250
    pipeTopY    = -170
    pipe_speed  = 4
    passed      = 0
    baseStartX  = 0

    game_intro()

    # when crashed is true, quit the game
    gameExit = False
    while not gameExit:
        for event in pygame.event.get(): # event-handling's loop
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN: # this event happens when a key is pressed
                if event.key == pygame.K_SPACE: # press spacebar to jump
                    soundWing.play()
                    birdMove = -4

            if event.type == pygame.KEYUP: # this event happens when a key is released
                if event.key == pygame.K_SPACE:
                    birdMove = 2

        birdY += birdMove
        gameDisplay.blit(bg, (0, 0)) # draw background

        # draw top pipe
        bottomPipe(pipeStartX, pipeBottomY)

        #calls baseMove to display the base image
        base_move(baseStartX)
        #updates base image x to make it look like it's moving
        baseStartX -= 2

        bird(birdX, birdY) # draw bird

        # draw the bottom pipe
        topPipe(pipeStartX, pipeTopY)

        pipeStartX -= pipe_speed # make the pipe move left four pixel at a time

        # update score when bird passed a pipe
        if birdX == pipeStartX + 52:
            soundWin.play()
            passed += 1

        passedPipe(passed)

        # When bird hit base, pipe or top of screen, it will crash
        if birdY > display_height - bird_height - base_height:
            soundDie.play()
            time.sleep(2)
            crash()

        # bird crashes when it hits any pipe
        if birdX + 25 > pipeStartX and birdX - 50 < pipeStartX:
            if birdX + 25 > pipeStartX and (birdY < pipeTopY + pipe_height or birdY + 24 > pipeBottomY):
                soundHit.play()
                time.sleep(2)
                crash()

        # moving pipes accross the screen
        if pipeStartX < -50:
            pipeStartX = display_width

            # make pipes change y coordinate randomly
            pipeTopY = random.randint(-200, -40)
            pipeBottomY = pipe_height + 100 + pipeTopY
            0 + pipeTopY

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
