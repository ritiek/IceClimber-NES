#!/usr/bin/env python

# we need pygame ofcourse
import pygame
from pygame.locals import *

pygame.init()	# initialize pygame
screen = pygame.display.set_mode((770,620))	# set display dimensions
pygame.display.set_caption('NES - Ice Climber')	# set window title

def loadImages():	# a function to load all the images
	images = {}
	images['main_menu'] = pygame.image.load('assets/sprites/MainMenu.png').convert_alpha()
	return images
def loadSounds():	# a function to load all the sounds
	sounds = {}
	sounds['main_menu'] = pygame.mixer.Sound('assets/audio/MainMenu.wav')
	return sounds

images = loadImages()	# let images be the return value of loadImages()
sounds = loadSounds()	# let sounds be the return value of loadSounds()


# I added an argument state to the below functions
# state=True means to start the function
# state=False means to exit the function gracefully

def mainMenu(state):	# works for the main menu of the game
	if state:	# if state==True
		screen.blit(images['main_menu'], (0,0))	# load background image
		sounds['main_menu'].play(-1)	# play iceclimber's menu theme. -1 means in endless loop
	else:	# if state==False
		sounds['main_menu'].stop()	# stop playing the iceclimber's menu theme

def renderStart(state):	# show the level when enter is pressed on main menu
	pass

def mainGame(state):	# the main game
	pass

done = False	# helps to determine the game must end when crossed is clicked on window

mainMenu(state=True)	# show main menu
while not done:
	for event in pygame.event.get():	# get all the user inputs
		if event.type == pygame.QUIT:	# if cross clicked on window
			done = True	# done==True means the while loop must end
		if event.type == KEYDOWN and event.key == K_RETURN:	#	if return key is pressed
			mainMenu(state=False)	# run mainMenu(state) with state=False
			print('RenderStart()')	# helps in debug
			renderStart(state=True)
			print('mainGame()')
			mainGame(state=True)

	pygame.time.Clock().tick(60)	# run the window with max 60 fps
	pygame.display.flip()	# show display
