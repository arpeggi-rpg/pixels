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
TINT = numpy.array([50, 255, 50])
sprite_list = pygame.sprite.Group()


class Sprite(pygame.sprite.Sprite):
    def __init__(self, colour, height, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, colour, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()

        self.colour = colour


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

    try:
        if not highlight.rect.collidepoint(pygame.mouse.get_pos()):
            sprite_list.remove(highlight)
    except NameError:
        pass

    for x in pixel:
        for sp in x:
            if sp.rect.collidepoint(pygame.mouse.get_pos()):
                highlight_colour = sp.colour + TINT
                for i, v in enumerate(highlight_colour):
                    if v > 255:
                        highlight_colour[i] = 255
                highlight = Sprite(highlight_colour, 8, 8)
                highlight.rect.x = sp.rect.x
                highlight.rect.y = sp.rect.y
                sprite_list.add(highlight)

    sprite_list.update()
    sprite_list.draw(screen)

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
