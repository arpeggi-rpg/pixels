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

colour = (255, 0, 0)


class PixelArt(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pixels = numpy.array([[colour for x in range(64)] for y in range(64)])
        self.canvas = pygame.Rect(10, 10, 513, 513)

    def drawpixels(self):
        pixel_array = pygame.PixelArray(screen)
        for x in range(64):
            for y in range(64):
                pixel_array[self.canvas.left:self.canvas.right, self.canvas.top: self.canvas.bottom] = colour
        pixel_array.close()
        pygame.display.flip()



PixelArt().drawpixels()

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
