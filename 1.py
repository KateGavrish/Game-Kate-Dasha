import pygame
import os
import sys

pygame.init()
clock = pygame.time.Clock()
size = width, height = 900, 700
screen = pygame.display.set_mode(size)

SPEED = 7
WIDTH = 22
HEIGHT = 32
JUMP = 5
GRAVITY = 0.5
FPS = 50

# основной персонаж
player = None


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


def generate_level():
    platforms = []
    stairs = []
    [platforms.append(Platforms(280 + 50 * i, 150)) for i in range(3)]
    [platforms.append(Platforms(80 + 50 * i, 240)) for i in range(8)]
    [platforms.append(Platforms(480 + 50 * i, 240 + 2 * i)) for i in range(4)]
    [platforms.append(Platforms(180 + 50 * i, 268 + 70 - 2 * i)) for i in range(12)]
    [platforms.append(Platforms(80 + 50 * i, 240 + 170 + 3 * i)) for i in range(7)]
    [platforms.append(Platforms(430 + 50 * i, 240 + 190)) for i in range(3)]
    [platforms.append(Platforms(180 + 50 * i, 420 + 100 - 2 * i)) for i in range(12)]
    [platforms.append(Platforms(80 + 50 * i, 610 + 3 * i)) for i in range(7)]
    [platforms.append(Platforms(430 + 50 * i, 630)) for i in range(3)]
    [platforms.append(Platforms(180 + 50 * i, 750 - 2 * i)) for i in range(12)]
    [platforms.append(Platforms(80 + 50 * i, 830)) for i in range(3)]
    [platforms.append(Platforms(80 + 50 * i, 900)) for i in range(15)]

    stairs.append(Stairs(680, 248))
    stairs.append(Stairs(155, 338))
    stairs.append(Stairs(580, 430))
    stairs.append(Stairs(155, 520))
    stairs.append(Stairs(580, 630))
    stairs.append(Stairs(155, 750))
    stairs.append(Stairs(220, 830))
    stairs.append(Stairs(430, 150))

    return platforms, stairs


def camera_state(camera, target_rect):
    left, top = target_rect[0], target_rect[1]
    width_, height_ = camera[2], camera[3]
    left, top = -left + width / 2, -top + height / 2

    left = min(0, left)
    left = max(-(camera.width - width), left)
    top = max(-(camera.height - height), top)
    top = min(0, top)

    return pygame.Rect(left, top, width_, height_)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xv = 0
        self.startX = x
        self.startY = y
        self.yv = 0
        self.onPlat = False
        self.image = pygame.Surface((WIDTH, HEIGHT))  # сделать изображение героя
        self.image.fill(pygame.Color('grey'))
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)
        self.spell = None
        self.hammer = None

    def update(self, left, right, up, platforms):
        if left:
            self.xv = -SPEED
        if right:
            self.xv = SPEED
        if not (left or right):
            self.xv = 0
        if up:
            if self.onPlat:
                self.yv = -JUMP

        if not self.onPlat:
            self.yv += GRAVITY

        self.onPlat = False
        self.rect.y += self.yv
        self.collide(0, self.yv, platforms)

        self.rect.x += self.xv  # переносим свои положение на xv
        self.collide(self.xv, 0, platforms)

    def collide(self, xv, yv, platforms):
        if pygame.sprite.collide_rect(self, hammer):
            print(1)  # доделать молот
        for s in stairs:
            if pygame.sprite.collide_rect(self, s):
                if yv > 0 and down:
                    self.rect.bottom = s.rect.bottom
                if yv < 0:
                    self.rect.top = s.rect.top - 50

        for plat in platforms:
            if pygame.sprite.collide_rect(self, plat):
                if xv > 0:
                    self.rect.right = plat.rect.left
                if xv < 0:
                    self.rect.left = plat.rect.right
                if yv > 0:
                    self.rect.bottom = plat.rect.top
                    self.onPlat = True
                    self.yv = 0
                if yv < 0:
                    self.rect.top = plat.rect.bottom
                    self.yv = 0


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


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, hero):
        return hero.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


class Monster(pygame.sprite.Sprite):
    pass


class Hammer(pygame.sprite.Sprite):
    hammer_image = load_image('hammer.png', pygame.Color('white'))
    hammer_image1 = pygame.transform.scale(hammer_image, (40, 40))
    hammer_image2 = pygame.transform.scale(hammer_image, (42, 42))
    hammer_image3 = pygame.transform.scale(hammer_image, (44, 44))
    hammer_image4 = pygame.transform.scale(hammer_image, (46, 46))
    hammer_image5 = pygame.transform.scale(hammer_image, (48, 48))
    hammer_image6 = pygame.transform.scale(hammer_image, (50, 50))

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Hammer.hammer_image1
        self.rect = self.image.get_rect().move(x, y)
        self.hammer_animation = True
        self.c = 0
        self.images = [Hammer.hammer_image1, Hammer.hammer_image2, Hammer.hammer_image3,
                       Hammer.hammer_image4, Hammer.hammer_image5, Hammer.hammer_image6]

    def update(self):
        self.check()
        if self.hammer_animation:
            self.image = self.images[self.c]
            self.c += 1
        else:
            self.image = self.images[self.c]
            self.c -= 1

    def check(self):
        if hammer.image.get_rect()[3] == 48:
            self.hammer_animation = False
        if hammer.image.get_rect()[3] == 42:
            self.hammer_animation = True


class Spell(pygame.sprite.Sprite):
    spell_image1 = load_image('spell1.png', pygame.Color('white'))
    spell_image2 = load_image('spell2.png', pygame.Color('white'))
    spell_image1 = pygame.transform.scale(spell_image1, (30, 30))
    spell_image2 = pygame.transform.scale(spell_image2, (32, 32))

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spell.spell_image1
        self.rect = self.image.get_rect().move(x, y)
        self.c = 0
        self.images = {
            Spell.spell_image1: Spell.spell_image2,
            Spell.spell_image2: Spell.spell_image1
        }

    def update(self):
        self.image = self.images[self.image]


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


buttons_start = pygame.sprite.Group()
player = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
stairs_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
life_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

hero = Player(400, 850)
hammer = Hammer(90, 770)
spell = Spell(650, 400)
all_sprites.add(hero)
all_sprites.add(hammer)
all_sprites.add(spell)

life_images = [pygame.transform.scale(load_image('life.png', (255, 255, 255)), (33, 30)),
               pygame.transform.scale(load_image('life2.png', (255, 255, 255)), (33, 30))]
for i in range(10, 160, 50):
    life = pygame.sprite.Sprite()
    life_group.add(life)
    life.image = life_images[1]
    life.rect = life.image.get_rect().move(10, i)
score = 0

left = right = up = down = False
running = True

platforms, stairs = generate_level()

level_width = 900
level_height = 1000

camera = Camera(camera_state, level_width, level_height)

# start_screen()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            left = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            right = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            up = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            down = True

        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            down = False
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            right = False
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            left = False
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            up = False
    screen.fill((30, 30, 30))
    camera.update(hero)
    for spr in all_sprites:
        screen.blit(spr.image, camera.apply(spr))

    pygame.draw.rect(screen, pygame.Color('red'), (790, 10, 100, 30), 1)
    font = pygame.font.Font(None, 35)
    text = font.render(str(score).rjust(6, '0'), 1, (255, 0, 0))
    screen.blit(text, (799, 14))

    hero.update(left, right, up, platforms)
    spell.update()
    hammer.update()
    life_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
# завершение работы:
pygame.quit()
