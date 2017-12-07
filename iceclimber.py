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
        images['hammer'] = pygame.image.load('assets/sprites/Hammer.png').convert_alpha()
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

    def make_clips(self):
        sprites = {}
        sprites['player'] = self.clip(rectangle=(4, 22, 14, 23), scale=(27, 47))
        return sprites


loader = LoadAssets()
images = loader.images()
sounds = loader.sounds()

sheet = SpriteSheet('assets/sprites/SpriteSheetTweaked.png')
sprites = sheet.make_clips()


def main_menu():
    print('main_menu()')
    # load background image
    screen.blit(images['main_menu'], (0,0))
    screen.blit(images['hammer'], (105, 255))
    # loop main theme forever
    sounds['main_menu'].play(-1)
    return sounds['main_menu']


def render_start():
    print('render_start()')
    showing_level = sounds['show_level'].play()
    for scroll_Y_axis in [n/2.0 for n in range(-2380, 0, 1)]:
        screen.fill((0, 0, 0))
        screen.blit(images['level'], (0, scroll_Y_axis))
        pygame.display.update()
    # wait until sound stops
    while showing_level.get_busy():
        pygame.time.wait(100)


def main_game():
    print('main_game()')
    screen.fill((0, 0, 0))
    screen.blit(images['level'], (0, -1190))
    screen.blit(sprites['player'], (256, 415))
    sounds['background'].play(-1)
    pygame.display.update()


def jump():
    sounds['jump'].play()


is_in_game = False
done = False

main_menu_event = main_menu()

single_player = True

while True:
    event = pygame.event.get()

    try:
        event, *_ = event
    except ValueError:
        continue

    if event.type == 2 and event.key in (303, 304):
        if single_player:
            pygame.draw.rect(screen, (0,0,0), (105,255,24,24))
            screen.blit(images['hammer'], (105, 288))
        else:
            pygame.draw.rect(screen, (0,0,0), (105,288,24,24))
            screen.blit(images['hammer'], (105, 255))

        single_player = not single_player

    elif event.type == 2 and event.key in (13, 271):
        break

    pygame.time.Clock().tick(60)
    pygame.display.update()


main_menu_event.stop()
render_start()
main_game()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == KEYDOWN and event.key == K_RETURN and not is_in_game:
            main_menu()
            is_in_game = True
        if event.type == KEYDOWN and event.key == K_x and is_in_game:
            jump()
    # run the window with max 60 fps
    pygame.time.Clock().tick(60)
    pygame.display.update()
