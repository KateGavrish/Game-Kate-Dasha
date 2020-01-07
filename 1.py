import pygame
import os
import sys
from random import randint

pygame.init()
clock = pygame.time.Clock()
size = width, height = 900, 700
screen = pygame.display.set_mode(size)

SPEED = 5
WIDTH = 22
HEIGHT = 32
JUMP = 5
GRAVITY = 0.45
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
    [platforms.append(Platforms(280 + 50 * i, 150, 1)) for i in range(3)]
    [platforms.append(Platforms(80 + 50 * i, 240, 1)) for i in range(8)]
    [platforms.append(Platforms(480 + 50 * i, 240 + 2 * i, 1)) for i in range(4)]
    [platforms.append(Platforms(180 + 50 * i, 268 + 70 - 2 * i, -1)) for i in range(12)]
    [platforms.append(Platforms(80 + 50 * i, 240 + 170 + 3 * i, 1)) for i in range(7)]
    [platforms.append(Platforms(430 + 50 * i, 240 + 190, 1)) for i in range(3)]
    [platforms.append(Platforms(180 + 50 * i, 420 + 100 - 2 * i, -1)) for i in range(12)]
    [platforms.append(Platforms(80 + 50 * i, 610 + 3 * i, 1)) for i in range(7)]
    [platforms.append(Platforms(430 + 50 * i, 630, 1)) for i in range(3)]
    [platforms.append(Platforms(180 + 50 * i, 750 - 2 * i, -1)) for i in range(12)]
    [platforms.append(Platforms(80 + 50 * i, 830, 1)) for i in range(3)]
    [platforms.append(Platforms(80 + 50 * i, 900, 1)) for i in range(15)]

    stairs.append(Stairs(680, 248))
    stairs.append(Stairs(155, 338))
    stairs.append(Stairs(580, 425))
    stairs.append(Stairs(155, 515))
    stairs.append(Stairs(580, 625))
    stairs.append(Stairs(155, 745))
    stairs.append(Stairs(220, 825))
    stairs.append(Stairs(430, 150))

    buck_v = randint(1, 7)
    count_life = 3

    return platforms, stairs, buck_v, count_life


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
    still = load_image('still.png', pygame.Color('black'))
    still = pygame.transform.scale(still, (22, 32))
    left1 = load_image('left.png', pygame.Color('black'))
    left1 = pygame.transform.scale(left1, (22, 32))
    left2 = load_image('left2.png', pygame.Color('black'))
    left2 = pygame.transform.scale(left2, (22, 32))
    right1 = load_image('right.png', pygame.Color('black'))
    right1 = pygame.transform.scale(right1, (22, 32))
    right2 = load_image('right2.png', pygame.Color('black'))
    right2 = pygame.transform.scale(right2, (22, 32))

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xv = 0
        self.startX = x
        self.startY = y
        self.yv = 0
        self.onPlat = False
        self.image = Player.still
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)
        self.spell = None
        self.hammer = None

    def update(self, left, right, up, platforms):
        a = {Player.left1: Player.left2, Player.left2: Player.left1,
             Player.right1: Player.right2, Player.right2: Player.right1}
        if left:
            self.xv = -SPEED
            if self.image == Player.still:
                self.image = Player.left1
            else:
                self.image = a[self.image]
        if right:
            self.xv = SPEED
            if self.image == Player.still:
                self.image = Player.right1
            else:
                self.image = a[self.image]
        if not (left or right):
            self.xv = 0
            self.image = Player.still
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
        if pygame.sprite.collide_rect(self, spell):
            print(2)  # доделать зелье
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


class Buck(pygame.sprite.Sprite):
    buck_images = [load_image('buck3.png', (255, 255, 255)),
                   pygame.transform.scale(load_image('buck2.png', (255, 255, 255)), (50, 47)),
                   pygame.transform.scale(load_image('buck.png', (255, 255, 255)), (50, 47))]

    def __init__(self, v):
        super().__init__(all_sprites, bucks_group)
        self.buck_change = {Buck.buck_images[1]: Buck.buck_images[2],
                            Buck.buck_images[2]: Buck.buck_images[1]}
        self.image = Buck.buck_images[0]
        self.v = v
        self.yv = 1
        self.xv = v
        self.rect = self.image.get_rect().move(129, 208)

    def update(self):
        self.is_on_stair()
        self.is_on_plat()
        self.rect.x += self.xv

    def is_on_stair(self):
        for stair in stairs_group:
            if pygame.sprite.collide_rect(self, stair) and self.rect.top < stair.rect.top:
                self.image = self.buck_change.get(self.image, Buck.buck_images[1])
                self.xv = 0
                self.yv = 2

    def is_on_plat(self):
        for platform in platform_group:
            if pygame.sprite.collide_rect(self, platform):
                self.rect.bottom = platform.rect.top + 1
                self.xv = self.v * platform.v
                if self.yv == 2:
                    self.image = Buck.buck_images[0]
                    self.xv = self.v * platform.v
                else:
                    self.image = pygame.transform.rotate(self.image, 90)
                self.yv = 1
                return
        self.rect.y += self.yv


class Stairs(pygame.sprite.Sprite):
    stairs_image = load_image('stairs.png', pygame.Color('white'))

    def __init__(self, x, y):
        super().__init__(stairs_group, all_sprites)
        self.image = Stairs.stairs_image
        self.image = pygame.transform.scale(self.image, (30, 100))  # размер лестницы
        self.rect = self.image.get_rect().move(x, y)


class Platforms(pygame.sprite.Sprite):
    platform_image = load_image('platform.png', pygame.Color('white'))

    def __init__(self, x, y, v):
        super().__init__(platform_group, all_sprites)
        self.image = Platforms.platform_image
        self.image = pygame.transform.scale(self.image, (50, 20))  # размер платформы
        self.rect = self.image.get_rect().move(x, y)
        self.v = v


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, hero):
        return hero.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


class Monster(pygame.sprite.Sprite):

    still1 = load_image('kongstill0.png', pygame.Color('black'))
    still1 = pygame.transform.scale(still1, (72, 80))
    still2 = load_image('kongstill1.png', pygame.Color('black'))
    still2 = pygame.transform.scale(still2, (72, 80))
    still3 = load_image('kongstill11.png', pygame.Color('black'))
    still3 = pygame.transform.scale(still3, (72, 80))

    left1 = load_image('kong21.png', pygame.Color('black'))
    left1 = pygame.transform.scale(left1, (72, 80))
    left2 = load_image('kong11.png', pygame.Color('black'))
    left2 = pygame.transform.scale(left2, (72, 80))

    right1 = load_image('kong2.png', pygame.Color('black'))
    right1 = pygame.transform.scale(right1, (72, 80))
    right2 = load_image('kong3.png', pygame.Color('black'))
    right2 = pygame.transform.scale(right2, (72, 80))

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xv = 0
        self.startX = x
        self.startY = y
        self.onPlat = True
        self.image = Monster.right1
        self.rect = pygame.Rect(x, y, 25, 35)
        self.animation = True

    def update(self):
        a = {Monster.left1: Monster.left2, Monster.left2: Monster.left1,
             Monster.right1: Monster.right2, Monster.right2: Monster.right1}
        if not self.animation:
            self.xv = -SPEED
            if self.image == (Monster.right1 or Monster.still1 or Monster.right2):
                self.image = Monster.left1
            else:
                self.image = a[self.image]
        if self.animation:
            self.xv = SPEED
            if self.image != (Monster.right1 or Monster.right2):
                self.image = Monster.right1
            else:
                self.image = a[self.image]
        if self.animation == 3:
            self.xv = 0
            self.image = Monster.still1
            pass

        if self.rect.x == 270:
            self.animation = False
        elif self.rect.x == 120:
            self.animation = True
        self.rect.x += self.xv


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

    running = True
    while running:
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
                    running = False
        buttons_start.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


buttons_start = pygame.sprite.Group()
player = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
stairs_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
life_group = pygame.sprite.Group()
bucks_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

hero = Player(400, 850)
hammer = Hammer(90, 770)
spell = Spell(650, 400)
monster = Monster(120, 160)
all_sprites.add(hero)
all_sprites.add(hammer)
all_sprites.add(spell)
all_sprites.add(monster)

life_images = [pygame.transform.scale(load_image('life.png', (255, 255, 255)), (33, 30)),
               pygame.transform.scale(load_image('life2.png', (255, 255, 255)), (33, 30))]
for i in range(10, 160, 50):  # жизни
    life = pygame.sprite.Sprite()
    life_group.add(life)
    life.image = life_images[1]
    life.rect = life.image.get_rect().move(10, i)
score = 0

left = right = up = down = False
running = True

platforms, stairs, bucks_v, count_life = generate_level()

level_width = 900
level_height = 1000

camera = Camera(camera_state, level_width, level_height)

start_screen()
running = True
while running:
    if pygame.time.get_ticks() % 40 == 0 and randint(0, 1):
        Buck(bucks_v)
    if count_life == 0:
        running = False
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
    text = font.render(str(score).rjust(6, '0'), 1, (255, 0, 0))  # счет
    screen.blit(text, (799, 14))

    hero.update(left, right, up, platforms)
    spell.update()
    hammer.update()
    bucks_group.update()
    monster.update()
    life_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
# завершение работы:
pygame.quit()
