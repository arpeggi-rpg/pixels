# add a grid too!
# rewrite highlights as an object, also pixels grid - consistency
# crashes when closing colour window without selecting colour, also save windows
import pygame
from tkinter.colorchooser import askcolor
import tkinter.filedialog as fd
import numpy as np
import pickle
from PIL import Image
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
BACKGROUND_COLOUR = (85, 85, 85)
DEFAULT_PALETTE = ((0, 0, 0),)
screen = pygame.display.set_mode((532, 600))
pygame.display.set_caption('Pixel Art')
screen.fill(BACKGROUND_COLOUR)
pygame.display.flip()

TRANSPARENT = (85, 85, 85)
BLUE = (0, 0, 255)
TINT = (100, 100, 100)
sprite_list = pygame.sprite.Group()
active_px = None


class Brush:
    def __init__(self):
        self.current_colour = (0, 0, 0)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, colour=(0, 0, 0), height=0, width=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, colour, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()
        self._colour = colour
        self.height = height
        self.width = width
        sprite_list.add(self)

        if type(self) is Palette:
            self._current_palette = DEFAULT_PALETTE

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


def increment_rgb():
    r = g = b = 0
    while (r, g, b) != (255, 255, 255):
        yield r, g, b
        if r == g == b:
            r += 1
        elif r > g == b:
            g += 1
        else:
            b += 1


class PixelArt:
    def __init__(self):
        self.pixels = [[x for x in range(64)] for y in range(64)]
        for x in range(64):
            for y in range(64):
                self.pixels[y][x] = Pixel(TRANSPARENT, 8, 8)
                self.pixels[y][x].rect.x = 10 + (x * 8)
                self.pixels[y][x].rect.y = 10 + (y * 8)

    def key_transparent(self):
        opaque_l = list()
        for y in self.pixels:
            for x in y:
                if x.transparent:
                    continue
                else:
                    opaque_l.append(x.colour)

        key_found = False
        while not key_found:
            for c in increment_rgb():
                if c not in opaque_l:
                    key = c
                    key_found = True
                    break

        save_pixels = [[x for x in range(64)] for y in range(64)]
        for i, y in enumerate(self.pixels):
            for j, x in enumerate(y):
                if x.transparent:
                    save_pixels[i][j] = key
                else:
                    save_pixels[i][j] = x.colour
        return save_pixels, key

    def pixel_art_array(self, is_array=False):
        if not is_array:
            return self.key_transparent()
        else:
            px_key = self.key_transparent()
            px_a = np.array(px_key[0])
            return_a = (px_a, px_key[1])
            return return_a

    def pixel_art_surf(self):
        px_alpha = self.pixel_art_array(is_array=True)
        px_array = px_alpha[0]
        px_surf = pygame.pixelcopy.make_surface(px_array)
        px_surf = pygame.transform.rotate(px_surf, 270)
        px_surf = pygame.transform.flip(px_surf, flip_x=True, flip_y=False)
        return px_surf, px_alpha[1]

    def convert_to_img(self):
        px_alpha = self.pixel_art_surf()
        surf_bytes = pygame.image.tobytes(px_alpha[0], 'RGBA')
        image = Image.frombytes('RGBA', (64, 64), surf_bytes)
        array = np.array(image, dtype=np.ubyte)
        mask = (array[:, :, :3] == px_alpha[1]).all(axis=2)
        alpha = np.where(mask, 0, 255)
        array[:, :, -1] = alpha
        return_img = Image.fromarray(np.ubyte(array))
        return return_img

    def export(self):
        export_surf = self.convert_to_img()
        file_ext = (('Bitmap Image', '*.bmp'), ('PNG Image', '*.png'), ('JPEG Image', '*.jpg'))
        try:
            export_surf.save(fd.asksaveasfilename(confirmoverwrite=True, filetypes=file_ext, initialfile='image', defaultextension=file_ext))
        except FileNotFoundError:
            pass
        del export_surf

    def save(self):
        save_list = self.pixel_art_array()
        try:
            with open(fd.asksaveasfilename(confirmoverwrite=True, filetypes=(("SAV File", "*.sav"),), initialfile='image.sav', defaultextension='*.sav'), 'wb') as f:
                pickle.dump(save_list, f)
        except FileNotFoundError:
            pass

    def load(self):
        try:
            with open(fd.askopenfilename(filetypes=(("SAV File", "*.sav"),), initialfile='image.sav', defaultextension='*.sav'), 'rb') as f:
                colour_list = pickle.load(f)
                print(type(colour_list))
                print(type(colour_list[0]), type(colour_list[1]))
                new_pixels = [[x for x in range(64)] for y in range(64)]
                for y, row in enumerate(colour_list[0]):
                    for x, colour in enumerate(row):
                        new_pixels[y][x] = Pixel(colour, 8, 8)
                        new_pixels[y][x].rect.x = 10 + (x * 8)
                        new_pixels[y][x].rect.y = 10 + (y * 8)
                        if colour == colour_list[1]:
                            new_pixels[y][x].colour = (85, 85, 85)
                        else:
                            new_pixels[y][x].transparent = False
                self.pixels = new_pixels
        except FileNotFoundError:
            pass


class Pixel(Sprite):
    def __init__(self, colour=(0, 0, 0), height=0, width=0):
        super().__init__(colour, height, width)
        self.is_active = False
        self.highlight = None
        self.transparent = True

    def update(self):
        self.is_active = True if self.rect.collidepoint(pygame.mouse.get_pos()) else False
        if self.is_active:
            if self.highlight is None:
                self.highlight = Highlight(self.colour, 8, 8)
                self.highlight.rect.x = self.rect.x
                self.highlight.rect.y = self.rect.y
        else:
            self.highlight = None
        pygame.draw.rect(self.image, self.colour, pygame.Rect(0, 0, self.width, self.height))
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                if eraser.is_active:
                    self.transparent = True
                else:
                    self.transparent = False
                self.colour = cur.current_colour
                self.highlight = None


class Highlight(Sprite):
    def __init__(self, colour=(0, 0, 0), height=8, width=8):
        super().__init__(colour, height, width)
        self.hi_colour = list(self.colour)
        self.ttl = None
        for i, v in enumerate(self.hi_colour):
            v += 100
            if v > 255:
                v = 255
            self.hi_colour[i] = v
        self.colour = self.hi_colour

    def update(self):
        pygame.draw.rect(self.image, self.colour, pygame.Rect(0, 0, self.width, self.height))
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.kill()


class PaletteColour(Sprite):
    def update(self):
        pygame.draw.rect(self.image, self.colour, pygame.Rect(0, 0, self.width, self.height))
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            for ev in events:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    cur.current_colour = self.colour
                    new_pal = list(pal.current_palette)
                    new_pal.remove(self.colour)
                    new_pal.insert(0, self.colour)
                    pal.current_palette = tuple(new_pal)
                    pal.draw_palette()


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

    current_drawn = pygame.sprite.Group()

    def draw_palette(self):
        for sp in self.current_drawn.sprites():
            sp.kill()
        self.current_drawn.add([PaletteColour(self.current_palette[i], 30, 30) for i in range(len(self._current_palette))])
        for i, c in enumerate(self.current_palette):
            self.current_drawn.sprites()[i].colour = c
            self.current_drawn.sprites()[i].rect.x = 10 + (i * 30)
            self.current_drawn.sprites()[i].rect.y = 532


class PalTool(Sprite):
    def __init__(self, colour=(0, 0, 0), height=30, width=30):
        super().__init__(colour, height, width)
        palicon = pygame.image.load('palicon.png')
        palicon.convert_alpha()
        self.image = palicon
        self.rect.x = 10
        self.rect.y = 562

    def update(self):
        screen.blit(self.image, self.rect)
        if self.rect.collidepoint(pygame.mouse.get_pos()) or pygame.key.get_pressed()[K_p]:
            if pygame.mouse.get_pressed()[0] or pygame.key.get_pressed()[K_p]:
                picked_colour = askcolor(initialcolor=pal.current_palette[0], title="Colour Chooser")[0]
                new_pal = list(pal.current_palette)
                if picked_colour in new_pal:
                    new_pal.remove(picked_colour)
                    new_pal.insert(0, picked_colour)
                else:
                    new_pal.insert(0, picked_colour)
                if len(new_pal) > 16:
                    new_pal.pop(-1)
                pal.current_palette = tuple(new_pal)
                pal.draw_palette()
                if eraser.is_active:
                    eraser.current_colour = picked_colour
                else:
                    cur.current_colour = picked_colour
        if pygame.key.get_pressed()[K_d]:
            print(pal.current_palette)


class EraserTool(Sprite):
    def __init__(self, colour=(0, 0, 0), height=30, width=30):
        super().__init__(colour, height, width)
        erasericon = pygame.image.load('erasericon.png')
        erasericon.convert_alpha()
        self.image = erasericon
        self.rect.x = 40
        self.rect.y = 562
        self.is_active = False
        self.current_colour = cur.current_colour

    def update(self):
        screen.blit(self.image, self.rect)

    def button_pressed(self):
        print(True)
        if self.is_active:
            self.is_active = False
            cur.current_colour = self.current_colour
        else:
            self.is_active = True
            self.current_colour = cur.current_colour
            cur.current_colour = TRANSPARENT


class SaveTool(Sprite):
    def __init__(self, colour=(0, 0, 0), height=30, width=30):
        super().__init__(colour, height, width)
        saveicon = pygame.image.load('saveicon.png')
        saveicon.convert_alpha()
        self.image = saveicon
        self.rect.x = 402
        self.rect.y = 562

    def update(self):
        screen.blit(self.image, self.rect)
        if self.rect.collidepoint(pygame.mouse.get_pos()) or pygame.key.get_pressed()[K_s]:
            if pygame.mouse.get_pressed()[0] or pygame.key.get_pressed()[K_s]:
                px_art.save()


class LoadTool(Sprite):
    def __init__(self, colour=(0, 0, 0), height=30, width=30):
        super().__init__(colour, height, width)
        loadicon = pygame.image.load('loadicon.png')
        loadicon.convert_alpha()
        self.image = loadicon
        self.rect.x = 432
        self.rect.y = 562

    def update(self):
        screen.blit(self.image, self.rect)
        if self.rect.collidepoint(pygame.mouse.get_pos()) or pygame.key.get_pressed()[K_l]:
            if pygame.mouse.get_pressed()[0] or pygame.key.get_pressed()[K_l]:
                px_art.load()


class ExportTool(Sprite):
    def __init__(self, colour=(0, 0, 0), height=30, width=30):
        super().__init__(colour, height, width)
        exporticon = pygame.image.load('exporticon.png')
        exporticon.convert_alpha()
        self.image = exporticon
        self.rect.x = 462
        self.rect.y = 562

    def update(self):
        screen.blit(self.image, self.rect)
        if self.rect.collidepoint(pygame.mouse.get_pos()) or pygame.key.get_pressed()[K_x]:
            if pygame.mouse.get_pressed()[0] or pygame.key.get_pressed()[K_x]:
                px_art.export()


px_art = PixelArt()
cur = Brush()
pal = Palette()
pal.draw_palette()
PalTool()
SaveTool()
LoadTool()
ExportTool()
eraser = EraserTool()
running = True
while running:
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif eraser.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                eraser.button_pressed()
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[K_e]:
                eraser.button_pressed()

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
