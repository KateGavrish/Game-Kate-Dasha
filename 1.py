import pygame
import os

pygame.init()
size = width, height = 900, 700
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Player(pygame.sprite.Group):
    pass


class Buck(pygame.sprite.Group):
    pass


class Stairs(pygame.sprite.Group):
    pass


class Platforms(pygame.sprite.Group):
    pass


class Monster(pygame.sprite.Group):
    pass



player = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((30, 30, 30))
    pygame.display.flip()
# завершение работы:
pygame.quit()
