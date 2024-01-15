import pygame
import numpy
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
BACKGROUND_COLOUR = (85, 85, 85)
screen = pygame.display.set_mode((532, 600))
pygame.display.set_caption('Pixel Art')
screen.fill(BACKGROUND_COLOUR)
pygame.display.flip()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
TINT = numpy.array([100, 100, 100])
sprite_list = pygame.sprite.Group()
highlight_group = pygame.sprite.GroupSingle()
active_px = None
pixel_active = False


class Sprite(pygame.sprite.Sprite):
    def __init__(self, colour, height, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, colour, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()
        self.colour = colour
        self.is_active = False

    def update(self, event_list=pygame.event.get()):
        self.is_active = True if self.rect.collidepoint(pygame.mouse.get_pos()) else False
        if self.is_active:
            print(self.is_active)
            for ev in event_list:
                if ev == pygame.MOUSEBUTTONUP:
                    self.colour = BLUE
                    print('click!')


pixel = [[x for x in range(64)] for y in range(64)]
for x in range(64):
    for y in range(64):
        pixel[x][y] = Sprite(RED, 8, 8)
        pixel[x][y].rect.x = 10 + (x * 8)
        pixel[x][y].rect.y = 10 + (y * 8)
        sprite_list.add(pixel[x][y])

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for x in pixel:
        for sp in x:
            if sp.is_active:
                active_px = sp
                pixel_active = True
    if not pixel_active:
        active_px = None

    if active_px:
        highlight_colour = active_px.colour + TINT
        for i, v in enumerate(highlight_colour):
            if v > 255:
                highlight_colour[i] = 255
        highlight = Sprite(highlight_colour, 8, 8)
        highlight.rect.x = active_px.rect.x
        highlight.rect.y = active_px.rect.y
        highlight_group.add(highlight)

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

    pygame.display.update()
