#!/usr/bin/env python

import pygame

pygame.init()
screen = pygame.display.set_mode((x,y))
clock = pygame.time.Clock()

done = False

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		pygame.get.key_pressed()
		if pressed[pygame.K_UP]:
		if pressed[pygame.K_LEFT]:
		if pressed[pygame.K_RIGHT]:
	pygame.time.Clock(60)
	pygame.display.flip()
