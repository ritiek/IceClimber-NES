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
PLAYER_POS = (256, 415)
PLAYER_SPEED = 4


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

    def clip(self, rectangle, scale=None):
        self.sheet.set_clip(pygame.Rect(rectangle))
        sprite = self.sheet.subsurface(self.sheet.get_clip())
        if scale:
            sprite = pygame.transform.scale(sprite, scale)
        return sprite

    def make_clips(self):
        sprites = {}
        sprites['player_right'] = []
        sprites['player_right'].append(self.clip(rectangle=(4, 22, 14, 23), scale=(27, 47)))
        sprites['player_right'].append(self.clip(rectangle=(19, 22, 14, 23), scale=(27, 43)))
        sprites['player_right'].append(self.clip(rectangle=(35, 21, 13, 19), scale=(27, 43)))
        sprites['player_right'].append(self.clip(rectangle=(53, 21, 16, 19), scale=(27, 43)))
        sprites['player_left'] = [pygame.transform.flip(x, True, False)
                                  for x in sprites['player_right']]
        sprites['green_full_brick'] = self.clip(rectangle=(6, 160, 9, 8), scale=(16, 13))
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
        screen.blit(sprites['player_right'][0], (256, 415))
        screen.blit(sprites['green_full_brick'], (128, 360))
        sounds['background'].play(-1)
        pygame.display.update()

    def jump(self):
        sounds['jump'].play()


class Movement:
    def __init__(self, pos, speed):
        self.x, self.y = pos
        self.speed = speed

    def left(self, sprite):
        self.x -= self.speed
        self.draw(sprite)

    def right(self, sprite):
        self.x += self.speed
        self.draw(sprite)

    def draw(self, sprite):
        self.erase()
        screen.blit(sprite, (self.x, self.y))
        pygame.display.update()

    def erase(self):
        #pygame.draw.rect(screen, (0,0,0), (self.x, self.y, 27, 39))
        pygame.draw.rect(screen, (0,0,0), (self.x-4, self.y, 35, 39))


loader = LoadAssets(assets='assets')
images = loader.images()
sounds = loader.sounds()

sheet = SpriteSheet('assets/sprites/SpriteSheetTweaked.png')
sprites = sheet.make_clips()

move = Movement(pos=PLAYER_POS, speed=PLAYER_SPEED)

MainMenu()
MainGame()

done = False
r_sprite = 0
l_sprite = 0
while not done:
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT]:
        r_sprite += 1
        if r_sprite > 3:
            r_sprite = 0
        print('move.right()')
        move.right(sprites['player_right'][r_sprite])
        pygame.time.wait(60)
        move.draw(sprites['player_right'][0])
    elif keys[K_LEFT]:
        l_sprite += 1
        if l_sprite > 3:
            l_sprite = 0
        print('move.left()')
        move.left(sprites['player_left'][l_sprite])
        pygame.time.wait(60)
        move.draw(sprites['player_left'][0])


    for event in pygame.event.get():
        print(event)
        if event.type == 2 and event.key == 120:
            pass
    # run the window with max 60 fps
    #pygame.display.update()
    #pygame.time.Clock().tick(60)
