# add a grid too!
# rewrite highlights as an object, also pixels grid - consistency

import pygame
import numpy
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
BACKGROUND_COLOUR = (85, 85, 85)
DEFAULT_PALETTE = numpy.array(([220, 20, 60], [255, 85, 10], [255, 190, 10], [35, 140, 35], [60, 135, 255],
                              [50, 50, 205], [100, 0, 205]))
screen = pygame.display.set_mode((532, 600))
pygame.display.set_caption('Pixel Art')
screen.fill(BACKGROUND_COLOUR)
pygame.display.flip()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
TINT = (100, 100, 100)
sprite_list = pygame.sprite.Group()
highlight_group = pygame.sprite.GroupSingle()
active_px = None


class Brush:
    def __init__(self):
        self.current_colour = pygame.Color((0, 0, 255))


class Sprite(pygame.sprite.Sprite):
    def __init__(self, colour=(0, 0, 0, 0), height=0, width=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, colour, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()
        self._colour = colour
        self.height = height
        self.width = width
        self.is_active = False
        sprite_list.add(self)

        if type(self) is Palette:
            self._current_palette = DEFAULT_PALETTE
            self._drawn_palette = [PaletteColour(DEFAULT_PALETTE[i], 30, 30) for i in range(7)]

    def _get_colour(self):
        return self._colour

    def _set_colour(self, new_colour):
        self._colour = new_colour

    colour = property(
        fget=_get_colour,
        fset=_set_colour,
        doc='Sprite Colour'
    )

    def update(self):
        pygame.draw.rect(self.image, self.colour, pygame.Rect(0, 0, self.width, self.height))


class Pixel(Sprite):
    def update(self):
        self.is_active = True if self.rect.collidepoint(pygame.mouse.get_pos()) else False
        pygame.draw.rect(self.image, self.colour, pygame.Rect(0, 0, self.width, self.height))
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.colour = cur.current_colour


class PaletteColour(Sprite):
    def update(self):
        pygame.draw.rect(self.image, self.colour, pygame.Rect(0, 0, self.width, self.height))
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                cur.current_colour = self.colour


class Palette(Sprite):

    def _get_palette(self):
        return self._current_palette

    def _set_palette(self, new_palette):
        self._current_palette = new_palette

    current_palette = property(
        fget=_get_palette,
        fset=_set_palette,
        doc="Current Palette"
    )

    def _get_drawn(self):
        return self._drawn_palette

    def _set_drawn(self, new_drawn):
        self._drawn_palette = new_drawn

    current_drawn = property(
        fget=_get_drawn,
        fset=_set_drawn,
        doc="Palette drawn to screen."
    )

    def draw_palette(self):
        for i, c in enumerate(self.current_palette):
            self.current_drawn[i].colour = c
            self.current_drawn[i].rect.x = 10 + (i * 30)
            self.current_drawn[i].rect.y = 532

''' 
    def update(self):
        pygame.draw.rect(self.image, self.colour, pygame.Rect(0, 0, self.width, self.height))
        self.is_active = True if self.rect.collidepoint(pygame.mouse.get_pos()) else False
        if self.is_active:
            print('active')
            if pygame.mouse.get_pressed()[0]:
                print('pressed')
                cur.current_colour = self.colour
'''


pixels = [[x for x in range(64)] for y in range(64)]
for x in range(64):
    for y in range(64):
        pixels[x][y] = Pixel(RED, 8, 8)
        pixels[x][y].rect.x = 10 + (x * 8)
        pixels[x][y].rect.y = 10 + (y * 8)

    cur = Brush()
    pal = Palette()
    pal.draw_palette()
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    '''
    for sp in sprite_list:
        if type(sp) is Pixel:
            if sp.is_active:
                active_px = sp

    if active_px:
        highlight_colour = [0, 0, 0]
        for i, v in enumerate(highlight_colour):
            highlight_colour[i] = active_px.colour[i] + TINT[i]
            v = highlight_colour[i]
            if v > 255:
                highlight_colour[i] = 255
        highlight = Sprite(highlight_colour, 8, 8)
        highlight.rect.x = active_px.rect.x
        highlight.rect.y = active_px.rect.y
        highlight_group.add(highlight)
    '''

    sprite_list.update()
    highlight_group.update()
    sprite_list.draw(screen)
    highlight_group.draw(screen)

    pygame.draw.rect(screen, (255, 255, 255), ((10, 10), (513, 513)), 1)
    for x in range(18, 522, 8):
        pygame.draw.line(screen, (255, 255, 255), (x, 10), (x, 521))
        for y in range(18, 522, 8):
            pygame.draw.line(screen, (255, 255, 255), (10, y), (521, y))
    pygame.draw.rect(screen, (255, 255, 255), ((10, 532), (512, 60)), 1)
    for x in range(40, 510, 30):
        pygame.draw.line(screen, (255, 255, 255), (x, 532), (x, 591))
    pygame.draw.line(screen, (255, 255, 255), (10, 562), (521, 562))

    pygame.event.pump()
    pygame.display.update()
