#!/usr/bin/env python

import pygame
from pygame.locals import *
import time


pygame.init()
# set window dimensions
screen = pygame.display.set_mode((512,480))
# set window title
pygame.display.set_caption('NES - Ice Climber')


class LoadAssets:
    def images(self):
        images = {}
        images['main_menu'] = pygame.image.load('assets/sprites/MainMenu.png').convert_alpha()
        images['level'] = pygame.image.load('assets/sprites/Level.png').convert_alpha()
        return images

    def sounds(self):
        sounds = {}
        sounds['main_menu'] = pygame.mixer.Sound('assets/audio/MainMenu.wav')
        sounds['show_level'] = pygame.mixer.Sound('assets/audio/ShowLevel.wav')
        sounds['background'] = pygame.mixer.Sound('assets/audio/Background.wav')
        sounds['jump'] = pygame.mixer.Sound('assets/audio/Jump.wav')
        return sounds


class SpriteSheet:
    def __init__(self, path):
        self.sheet = pygame.image.load(path).convert_alpha()

    def clip(self, rectangle, scale):
        self.sheet.set_clip(pygame.Rect(rectangle))
        sprite = self.sheet.subsurface(self.sheet.get_clip())
        scaled_sprite = pygame.transform.scale(sprite, scale)
        return scaled_sprite


"""
class Sprites(SpriteSheet):
    def __init__(self):
        pass
"""


loader = LoadAssets()
images = loader.images()
sounds = loader.sounds()

sheet = SpriteSheet('assets/sprites/SpriteSheetTweaked.png')
player = sheet.clip(rectangle=(4, 22, 14, 23), scale=(27, 47))


def main_menu(state):
	print('main_menu(' + str(state) + ')')
	if state:	# if state==True
        # load background image
		screen.blit(images['main_menu'], (0,0))
        # loop main theme forever
		sounds['main_menu'].play(-1)
	else:
		sounds['main_menu'].stop()


def render_start():
	print('render_start()')
	showing_level = sounds['show_level'].play()
	for scroll_Y_axis in [n/2.0 for n in range(-2380, 0, 1)]:
		screen.fill((0, 0, 0))
		screen.blit(images['level'], (0, scroll_Y_axis))
		pygame.display.update()
	# sound is playing
	while showing_level.get_busy():
		pygame.time.wait(100)


def main_game():
	print('main_game()')
	screen.fill((0, 0, 0))
	screen.blit(images['level'], (0, -1190))
	screen.blit(player, (256, 415))
	sounds['background'].play(-1)
	pygame.display.update()


def jump():
	sounds['jump'].play()


is_in_game = False
done = False

main_menu(state=True)
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == KEYDOWN and event.key == K_RETURN and not is_in_game:
			main_menu(state=False)
			render_start()
			main_game()
			is_in_game = True
		if event.type == KEYDOWN and event.key == K_x and is_in_game:
			jump()
	# run the window with max 60 fps
	pygame.time.Clock().tick(60)
	pygame.display.update()
