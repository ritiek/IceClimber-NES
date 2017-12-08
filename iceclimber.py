#!/usr/bin/env python

import pygame
from pygame.locals import *
import time
import os


pygame.init()
# set window dimensions
screen = pygame.display.set_mode((512,480))
# set window title
pygame.display.set_caption('NES - Ice Climber')


class LoadAssets:
    def __init__(self, assets):
        self.sprites = os.path.join(assets, 'sprites')
        self.audio = os.path.join(assets, 'audio')

    def images(self):
        images = {}
        images['main_menu'] = pygame.image.load(os.path.join(self.sprites, 'MainMenu.png')).convert_alpha()
        images['level'] = pygame.image.load(os.path.join(self.sprites, 'Level.png')).convert_alpha()
        images['hammer'] = pygame.image.load(os.path.join(self.sprites, 'Hammer.png')).convert_alpha()
        return images

    def sounds(self):
        sounds = {}
        sounds['main_menu'] = pygame.mixer.Sound(os.path.join(self.audio, 'MainMenu.wav'))
        sounds['show_level'] = pygame.mixer.Sound(os.path.join(self.audio, 'ShowLevel.wav'))
        sounds['background'] = pygame.mixer.Sound(os.path.join(self.audio, 'Background.wav'))
        sounds['jump'] = pygame.mixer.Sound(os.path.join(self.audio, 'Jump.wav'))
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


class MainMenu:
    def __init__(self):
        menu_music = self.draw()
        self.interact()
        menu_music.stop()
        self.show_mountain()

    def draw(self):
        # load background image
        screen.blit(images['main_menu'], (0,0))
        screen.blit(images['hammer'], (105, 255))
        pygame.display.update()
        # loop main theme forever
        music = sounds['main_menu'].play(-1)
        return music

    def interact(self):
        single_player_selected = True
        start_game = False

        while not start_game:
            event = pygame.event.get()
            try:
                event, *_ = event
            except ValueError:
                continue

            key = self.match_keys(event)

            if key == "enter":
                start_game = single_player_selected

            elif key == "shift":
                if single_player_selected:
                    pygame.draw.rect(screen, (0,0,0), (105,255,24,24))
                    screen.blit(images['hammer'], (105, 288))
                else:
                    pygame.draw.rect(screen, (0,0,0), (105,288,24,24))
                    screen.blit(images['hammer'], (105, 255))

                single_player_selected = not single_player_selected
                pygame.display.update()


    def match_keys(self, event):
        if event.type == 2:
            if event.key in (303, 304):
                return "shift"

            elif event.key in (13, 271):
                return "enter"

        else:
            return None

    def show_mountain(self):
        showing_level = sounds['show_level'].play()
        for scroll_Y_axis in [n/2.0 for n in range(-2380, 0, 1)]:
            screen.fill((0, 0, 0))
            screen.blit(images['level'], (0, scroll_Y_axis))
            pygame.display.update()
        # wait until sound stops
        while showing_level.get_busy():
            pygame.time.wait(100)


class MainGame:
    def __init__(self):
        self.draw()

    def draw(self):
        print('main_game()')
        screen.fill((0, 0, 0))
        screen.blit(images['level'], (0, -1190))
        screen.blit(sprites['player'], (256, 415))
        sounds['background'].play(-1)
        pygame.display.update()

    def jump(self):
        sounds['jump'].play()


loader = LoadAssets(assets='assets')
images = loader.images()
sounds = loader.sounds()

sheet = SpriteSheet('assets/sprites/SpriteSheetTweaked.png')
sprites = sheet.make_clips()

MainMenu()
MainGame()

is_in_game = False
done = False

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
