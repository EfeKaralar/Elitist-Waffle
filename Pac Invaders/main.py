import pygame
import time
import random
import math
from pygame import mixer



"""The Statement of the Main Loop"""
running = True

#initialize pygame
pygame.init()  #ALWAYS PUT THIS COMMAND
screen = pygame.display.set_mode((800,600)) # sets the resolution of the screen. !!! DOUBLE PARANTHESIS !!!

"""Background"""
background = pygame.image.load('background.jpg')

background_sound = mixer.music.load('pacman-dubstep-remix.mp3')
mixer.music.play(-1)    #to play in a loop, write -1 in the function play

"""Title and Icon"""
pygame.display.set_caption('Pac\'s Personal Space Invaders by Efe')
icon = pygame.image.load('satellite.png')
pygame.display.set_icon(icon)


"""Player"""
playerImg = pygame.image.load('pacman.png')
playerX = 370   #x coordinates of player
playerY = 480   #y coordinates of player
playerX_change = 0


"""Enemy"""

enemyImg = []   #we need to create lists to create multiple enemies
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
deadGhosts = 0

numOfEnemies = 6

addEnemy = True

while addEnemy:     #I will add a function that increases the number of enemies by one every 15 seconds.
    for i in range(numOfEnemies):
        enemyImg.append(pygame.image.load('ghost2.png'))
        enemyX.append(random.randint(0,736))   #initial x coordinates of enemy
        enemyY.append(32)  #initial y coordinates of enemy
        enemyX_change.append(1.5)
        enemyY_change.append(16)
    addEnemy = False



"""Bullet"""

bulletImg = pygame.image.load('bullet_tra.png')
bulletY = 480
bulletY_change = 3
bulletX = playerX
bulletState = "ready"   #ready = bullet is unseen   fire = bullet is moving

"""Score"""

score_value = 0
font = pygame.font.Font('Alien-Encounters-Bold.ttf', 32)
scoreX = 16
scoreY = 16

"""Game Over"""
over_font = pygame.font.Font('Alien-Encounters-Bold.ttf', 64)




def showScore(x,y):
    score = font.render("Score:    " + str(score_value), True , ( 255 , 186 , 0 ) )
    screen.blit(score , ( x , y ))

def game_over_text():
    over = over_font.render("Game Over!", True, (255, 255, 255))
    screen.blit(over , (230 , 250))

def player(x,y):
    screen.blit(playerImg , ( x , y ))   #to draw things on pygame screen, use command .blit

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16 , y + 16))

def isCollision(X1, Y1, X2, Y2):
    distance = math.sqrt(math.pow(X1 - X2, 2) + math.pow(Y1 - Y2, 2))
    global deadGhosts
    if distance <= 27:
        return True
        deadGhosts +=1
    else:
        return False





"""Game Loop"""

while running:

    """Keys and Buttons"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #  if a key is pressed, check if it is right or left or space
        if event.type == pygame.KEYDOWN:    #KEYDOWN = pressing he key
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bulletState is "ready":
                bulletSound = mixer.Sound('waka-waka2.wav')
                bulletSound.play()
                bulletX = playerX  # same initial position as player
                fire_bullet(bulletX, playerY)


        if event.type == pygame.KEYUP:      #KEYUP = releasing the key
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    """To add enemies"""
    if deadGhosts >= 3:
        numOfEnemies += 1
        addEnemy = True
        deadGhosts = 0



    """Screen"""
    #Red, Green, Blue goes to 255
    #screen.fill((72,61,139))    #for background color
    screen.blit(background, (0,0)) #for background image (Since background image makes the program run slower, increase player_change and enemy_change)


    playerX += playerX_change

    """Border for player"""
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    """Bullet Movement"""

    if bulletState is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"



    """Border for enemy"""
    for i in range(numOfEnemies):

        enemyX[i] += enemyX_change[i]

        if enemyX[i] == 32:
            enemyX[i] = 31
            enemyY[i] += enemyY_change[i]
            if enemyX[i] == 16:
                enemyX[i] = 15
                enemyY[i] += enemyY_change[i]
                if enemyX[i] <= 0:
                    enemyX[i] = 0
                    enemyX_change[i] = 1.5
                    enemyY[i] += 2*enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -1.5
            enemyY[i] += enemyY_change[i]


        """Collision"""
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            ded = mixer.Sound('Ghost-dead.wav')
            ded.play()
            bulletY = 480
            bulletState = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = 50

        """Game Over"""
        if enemyY[i] > 424:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            game_over_text()
            break



        enemy(enemyX[i], enemyY[i], i)


    player(playerX, playerY)    #call method player() after method screen.fill()
    showScore(scoreX, scoreY)
    pygame.display.update() #ALWAYS PUT THIS COMMAND or it will not update the display
