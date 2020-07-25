import pygame
import random
import math
from pygame import mixer

#initializing the game
pygame.init()

#Screen Height, Width 
screen = pygame.display.set_mode((800,600))

#Title 
pygame.display.set_caption('Space Invaders')
#Icon 
icon=pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#Background
background=pygame.image.load('background.jpg')

#Background sound
mixer.music.load('background.wav') #music is not sound. sound is played over sound
mixer.music.play(-1) #play in a loop

#Spaceship
playerImg = pygame.image.load('space-invaders.png')
playerX= 350
playerY= 500 #location of the spaceship (X, Y)
playerX_change =0 #in the beginning the spaceship can't not move  

def player(x,y): #since we want the ship move, DO NOT SAY AN UNIQUE VALUE
	screen.blit(playerImg,(x,y)) #drawing something on the screen

#Bullet
##Ready = you can't see the bullet
##Fire = Shot a bullet
bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=600
bulletY_change=20
bullet_state='ready'

#SCORE

score_value=0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#GAME OVER TEXT
font_over = pygame.font.Font('freesansbold.ttf',115)

def show_score(x,y):
	score = font.render('Score: '+ str(score_value),True, (255,255,255))
	screen.blit(score, (x,y))

def game_over_text():
	over = font.render('GAME OVER',True, (255,255,255))
	screen.blit(over, (200,250))


def fire_bullet(x,y): #How the bullet follow the space and start from the top on the spaceship
	global bullet_state
	bullet_state='fire'
	screen.blit(bulletImg, (x+16, y+10)) #center the bullet 

def collision_bullet(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
	if distance < 27:
		return True #collision occurs
	else:
		return False

def collision_space(enemyX, enemyY, playerX, playerY):
	distance = math.sqrt(math.pow(enemyX - playerX, 2) + (math.pow(enemyY - playerY, 2)))
	if distance < 27:
		return True #collision occurs
	else:
		return False

#Enemy
##Multiple elements
enemyImg=[]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load('alien.png'))
	enemyX.append(random.randint(0,735))
	enemyY.append(random.randint(50,200)) #location of the enemimes between 50 and 200 px on Y axis
	enemyX_change.append(2) # start moving 2 px on the X axis 
	enemyY_change.append(30) #move down 30 px every time the enemy hits the wall

def enemy(x,y, i): #since we want the ship move, DO NOT SAY AN UNIQUE VALUE
	screen.blit(enemyImg[i],(x,y)) #drawing something on the screen

#Game Loop 
running=True
while running:
		#First draw the screen 
	screen.fill(pygame.Color('black')) #or RGB color screen.fill((R, G, B)) number
#Now you add anything on top of the screen
	#Background Image
	screen.blit(background,(0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT: #close the file
			running = False #break the loop

		#Movements inside the game 
		if event.type == pygame.KEYDOWN:
			
			if event.key == pygame.K_LEFT: #if the left key is pressed (left arrow), move to left
				playerX_change = -5 # adding - 0.1 each "time" you click on the left arrow
			
			if event.key == pygame.K_RIGHT: #if the right key is pressed (right arrow), move to right
				playerX_change = 5 # adding 0.1 each "time" you click on the right arrow
			
			if event.key ==pygame.K_SPACE:
				if bullet_state =='ready':
					mixer.Sound('laser.wav').play()
					bulletX=playerX
					fire_bullet(bulletX, bulletY)
			
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0 #when we stop to move the ship, the ship will stop

#anything that you want to continue on the screen in has to be inside the while loop
	playerX += playerX_change #the final position is the sum of the movements made by playerX_change
	
	
	if playerX<=0:
		playerX = 0
	if playerX >=(800-64):
		playerX = (800-64)

		#MOVING ENEMY 
	for i in range(num_of_enemies):

		#GAME OVER T.T
		if enemyY[i]>500:
			for j in range(num_of_enemies):
				enemyY[j] = 2000

			game_over_text()
			break


		collision_s=collision_space(enemyX[i], enemyY[i], playerX, playerY)
		if collision_s:
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			#mixer.Sound('explosion.wav').play()
			game_over_text()
			break


		enemyX[i] += enemyX_change[i] #the final position is the sum of the movements made by playerX_change
		
		if enemyX[i]<=0:
			enemyX_change[i] = 2
			enemyY[i] +=enemyY_change[i]
		elif enemyX[i] >=(800-64):
			enemyX_change[i] = -2
			enemyY[i] +=enemyY_change[i]
		
		if 20>=score_value<= 40:
			if enemyX[i]<=0:
				enemyX_change[i] =3
				enemyY[i] +=enemyY_change[i]

			elif enemyX[i] >=(800-64):
				enemyX_change[i] = -3
				enemyY[i] +=enemyY_change[i]

		if score_value>= 41:
			if enemyX[i]<=0:
				enemyX_change[i] =4
				enemyY[i] +=enemyY_change[i]

			elif enemyX[i] >=(800-64):
				enemyX_change[i] = -4
				enemyY[i] +=enemyY_change[i]

		#collision
		collision_b = collision_bullet(enemyX[i],enemyY[i],bulletX, bulletY)
		if collision_b:

			mixer.Sound('explosion.wav').play()

			bulletY = 480 #reset bullet
			bullet_state = 'ready'
			score_value +=1
			
			#when we hit a enemy, reset then
			enemyX[i]= random.randint(0,735)
			enemyY[i]= random.randint(50,200)
		enemy(enemyX[i],enemyY[i], i)

	#MOVING BULLET
	if bulletY<=0:
		bulletY = 480
		bullet_state = 'ready'
	if bullet_state =='fire':
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change

	player(playerX, playerY) #execute player fuction
	show_score(textX,textY)
	pygame.display.update()

