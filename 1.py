import pygame
import os
import sys


pygame.init()
clock = pygame.time.Clock()
size = width, height = 900, 700
screen = pygame.display.set_mode(size)

FPS = 50

# основной персонаж
player = None

buttons_start = pygame.sprite.Group()
player = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
stairs_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


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


def generate_level(level):
    # реализация генерации уровня
    pass


class Player(pygame.sprite.Group):
    def __init__(self, pos_x, pos_y):
        super().__init__(player, all_sprites)
        self.image = None                      # сделать изображение героя
        self.rect = 0, 0                       # выбрать поожение героя
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move()
        # реализовать перемещение героя


class Buck(pygame.sprite.Group):
    pass


class Stairs(pygame.sprite.Sprite):
    stairs_image = load_image('stairs.png', pygame.Color('white'))

    def __init__(self, x, y):
        super().__init__(stairs_group, all_sprites)
        self.image = Stairs.stairs_image
        self.image = pygame.transform.scale(self.image, (30, 100))  # размер лестницы
        self.rect = self.image.get_rect().move(x, y)
        # self.rect.x = x
        # self.rect.y = y


class Platforms(pygame.sprite.Sprite):
    platform_image = load_image('platform.png', pygame.Color('white'))

    def __init__(self, x, y):
        super().__init__(platform_group, all_sprites)
        self.image = Platforms.platform_image
        self.image = pygame.transform.scale(self.image, (50, 30))  # размер платформы
        self.rect = self.image.get_rect().move(x, y)
        # self.rect.x = x
        # self.rect.y = y


class Monster(pygame.sprite.Group):
    pass


class Hammer(pygame.sprite.Group):
    pass


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    play = pygame.sprite.Sprite()
    info = pygame.sprite.Sprite()
    buttons_start.add(play)
    buttons_start.add(info)

    play_images = [load_image('menu_play1.png'), load_image('menu_play2.png')]
    play.image = play_images[0]
    play.rect = play.image.get_rect()
    play.rect.x = 290
    play.rect.y = 300

    info_images = [load_image('menu_info1.png'), load_image('menu_info2.png')]
    info.image = info_images[0]
    info.rect = info.image.get_rect()
    info.rect.x = 290
    info.rect.y = 400

    while True:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:  # находится ли курсор на одной из кнопок
                x, y = event.pos
                if play.rect.collidepoint(x, y):
                    play.image = play_images[1]
                else:
                    play.image = play_images[0]
                if info.rect.collidepoint(x, y):
                    info.image = info_images[1]
                else:
                    info.image = info_images[0]
            elif event.type == pygame.MOUSEBUTTONUP:  # проверяем, если было нажатие на стартовом экране
                x, y = event.pos
                if info.rect.collidepoint(x, y):
                    pass
                elif play.rect.collidepoint(x, y):
                    pass
        buttons_start.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # сделать реализацию движения героя с помощью стрелок
            if event.key == pygame.K_UP:
                pass
            elif event.key == pygame.K_DOWN:
                pass
            elif event.key == pygame.K_LEFT:
                pass
            elif event.key == pygame.K_RIGHT:
                pass
    screen.fill((30, 30, 30))
    all_sprites.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
# завершение работы:
pygame.quit()
