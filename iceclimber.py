#!/usr/bin/env python

# we need pygame ofcourse
import pygame
from pygame.locals import *
import time

pygame.init()	# initialize pygame
screen = pygame.display.set_mode((512,480))	# set display dimensions
pygame.display.set_caption('NES - Ice Climber')	# set window title

def loadImages():	# a function to load all the images
	images = {}
	images['main_menu'] = pygame.image.load('assets/sprites/MainMenu.png').convert_alpha()
	images['level'] = pygame.image.load('assets/sprites/level.png').convert_alpha()
	images['sprites1'] = pygame.image.load('assets/sprites/sprites1.png').convert_alpha()
	images['sprites2'] = pygame.image.load('assets/sprites/sprites2.png').convert_alpha()
	return images
def loadSounds():	# a function to load all the sounds
	sounds = {}
	sounds['main_menu'] = pygame.mixer.Sound('assets/audio/MainMenu.wav')
	sounds['show_level'] = pygame.mixer.Sound('assets/audio/ShowLevel.wav')
	sounds['background'] = pygame.mixer.Sound('assets/audio/Background.wav')
	sounds['jump'] = pygame.mixer.Sound('assets/audio/Jump.wav')
	return sounds

images = loadImages()	# let images be the return value of loadImages()
sounds = loadSounds()	# let sounds be the return value of loadSounds()

#sheet.set_clip(pygame.Rect(SPRT_RECT_X, SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)) #Locate the sprite you want
#draw_me = sheet.subsurface(sheet.get_clip()) #Extract the sprite you want

images['sprites1'].set_clip(pygame.Rect(7, 24, 12, 19))
player = pygame.transform.scale(images['sprites1'].subsurface(images['sprites1'].get_clip()), (30, 50))


# I added an argument state to the below function
# state=True means to start the function
# state=False means to exit the function gracefully

def mainMenu(state):	# works for the main menu of the game
	print('mainMenu(' + str(state) + ')')	# helps in debug xD
	if state:	# if state==True
		screen.blit(images['main_menu'], (0,0))	# load background image
		sounds['main_menu'].play(-1)	# play iceclimber's menu theme. -1 means in endless loop
	else:	# if state==False
		sounds['main_menu'].stop()	# stop playing the iceclimber's menu theme

def renderStart():	# show the level when enter is pressed on main menu
	print('RenderStart()')
	showing_level = sounds['show_level'].play()
	for scroll_Y_axis in [n/2.0 for n in range(-2380, 0, 1)]:	# got these values experimentally and another for loop to use float to scroll level slowly
		screen.fill((0, 0, 0))
		screen.blit(images['level'], (0, scroll_Y_axis))
		pygame.display.update()	# update screen
	while showing_level.get_busy():	# pause as long as show_level sound is playing
		pygame.time.wait(100)

def mainGame():	# the main game
	print('mainGame()')
	screen.fill((0, 0, 0))
	#screen.blit(images['level'], (0, -1190))
	screen.blit(player, (0, 0))
	sounds['background'].play(-1)
	pygame.display.update()

def Jump():
	sounds['jump'].play()

is_in_game = False	# to know if user is in actual game
done = False	# helps to determine the game must end when crossed is clicked on window

mainMenu(state=True)	# show main menu
while not done:
	for event in pygame.event.get():	# get all the user inputs
		if event.type == pygame.QUIT:	# if cross clicked on window
			done = True	# done==True means the while loop must end
		if event.type == KEYDOWN and event.key == K_RETURN and not is_in_game:	#	if return key is pressed
			mainMenu(state=False)	# run mainMenu(state) with state=False
			renderStart()
			mainGame()
			is_in_game = True	# actual game begins
		if event.type == KEYDOWN and event.key == K_x and is_in_game:
			Jump()

	pygame.time.Clock().tick(60)	# run the window with max 60 fps
	pygame.display.update()	# update screen
