#!/usr/bin/env python

import pygame

pygame.init()
screen = pygame.display.set_mode((770,620))
pygame.display.set_caption('NES - Ice Climber')

images, sounds = {}, {}

images['menu'] = pygame.image.load('assets/sprites/menu.png').convert_alpha()
sounds['menu'] = pygame.mixer.Sound('assets/audio/IceClimber.wav')

screen.blit(images['menu'], (0,0))
sounds['menu'].play(-1)

done = False

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	#pressed = pygame.get.key_pressed()
	#if pressed[pygame.K_UP]: pass
	#if pressed[pygame.K_LEFT]: pass
	#if pressed[pygame.K_RIGHT]: pass
	pygame.time.Clock().tick(60)
	pygame.display.flip()
