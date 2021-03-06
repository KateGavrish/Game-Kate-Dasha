import pygame
import os
import sys
from random import randint, choice
import sqlite3

pygame.init()
clock = pygame.time.Clock()
size = width, height = 900, 700
screen = pygame.display.set_mode(size)
screen_rect = (0, 0, width, height)

SPEED = 5
WIDTH = 22
HEIGHT = 32
JUMP = 5
GRAVITY = 0.45
FPS = 50
HAMMER_UNACTIDE = 30
STAR_TIMER = 10

pygame.time.set_timer(STAR_TIMER, 1000)


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


def load_sound(name):
    fullname = os.path.join('data', name)
    sound = pygame.mixer.Sound(fullname)
    return sound


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
    [platforms.append(Platforms(80 + 50 * i, 830, -1)) for i in range(3)]
    [platforms.append(Platforms(80 + 50 * i, 900, -1)) for i in range(15)]

    stairs.append(Stairs(680, 245))
    stairs.append(Stairs(155, 334))
    stairs.append(Stairs(580, 425))
    stairs.append(Stairs(155, 515))
    stairs.append(Stairs(580, 625))
    stairs.append(Stairs(155, 745))
    stairs.append(Stairs(220, 825))
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


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png", pygame.Color('black'))]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(stars_sprites)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


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
    still_hammer = load_image('still_with_hammer.png', pygame.Color('white'))
    still_hammer = pygame.transform.scale(still_hammer, (40, 32))

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
        self.hammer_activated = False
        self.r = 0

    def update(self, left, right, up, down, platforms, stairs, hammer_activated):
        print(hammer_activated, self.hammer)
        self.hammer_activated = hammer_activated
        a = {Player.left1: Player.left2, Player.left2: Player.left1,
             Player.right1: Player.right2, Player.right2: Player.right1}
        if left:
            self.xv = -SPEED
            if not hammer_activated:
                if self.image == (Player.still or Player.still_hammer or Player.right2 or Player.right1):
                    self.image = Player.left1
                else:
                    self.image = a.get(self.image, Player.left1)
        if right:
            self.xv = SPEED
            if not hammer_activated:
                if self.image == (Player.still or Player.still_hammer or Player.left2 or Player.left1):
                    self.image = Player.right1
                else:
                    self.image = a.get(self.image, Player.right1)
        if not (left or right):
            self.xv = 0
            if not hammer_activated:
                self.image = Player.still
        if up:
            if self.onPlat:
                self.yv = -JUMP

        if hammer_activated:
            self.image = Player.still_hammer

        if not self.onPlat:
            self.yv += GRAVITY

        self.onPlat = False
        self.rect.y += self.yv
        self.collide(0, self.yv, platforms, stairs, down, door)

        self.rect.x += self.xv  # переносим свои положение на xv
        self.collide(self.xv, 0, platforms, stairs, down, door)

    def collide(self, xv, yv, platforms, stairs, down, door):
        global score, bucks_v, count_life
        if pygame.sprite.collide_rect(self, hammer):
            self.hammer = True
        if pygame.sprite.collide_rect(self, spell):
            self.spell = True
            m = 29
            pygame.time.set_timer(m, 10000)
            pygame.time.set_timer(28, 1000)
            self.r = 10

        if self.rect.y > 930:
            count_life -= 1
            lives[count_life].image = life_images[0]
            hero.death()

        if pygame.sprite.collide_rect(self, door):
            door.level += 1
            score += 250
            bucks_v += 1
            self.rect.x = self.startX
            self.rect.y = self.startY
            if door.level == 4:
                aplod.play()
                win_screen()
            else:
                next_level.play()
                new_level()

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

    def death(self):
        global score
        score = max(0, score - 500)
        pygame.time.wait(500)
        self.rect.x = self.startX
        self.rect.y = self.startY


class Buck(pygame.sprite.Sprite):
    boom = load_image('boom.png', (0, 0, 0))
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
        self.death = False
        self.c = 0

    def update(self):
        self.player_collide()
        self.is_on_stair()
        self.is_on_plat()
        self.rect.x += self.xv

    def player_collide(self):
        global count_life, score
        if pygame.sprite.collide_rect(self, hero) and (not hero.hammer_activated and not hero.spell and not self.death):
            count_life -= 1
            lives[count_life].image = life_images[0]
            hero.death()
        elif pygame.sprite.collide_rect(self, hero) and hero.hammer_activated:
            if not self.death:
                score += 100
            self.death = True
            self.image = Buck.boom

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


class Door(pygame.sprite.Sprite):
    door_image = load_image('door.png', pygame.Color('white'))
    princess_image = pygame.transform.scale(load_image('prin.png', pygame.Color('white')), (40, 60))

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Door.door_image
        self.rect = self.image.get_rect().move(x, y)
        self.level = 1

    def become_princess(self):
        self.image = Door.princess_image
        self.rect.y = 90


def terminate():
    pygame.quit()
    sys.exit()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, choice(numbers), choice(numbers))


def start_screen():
    play = pygame.sprite.Sprite()
    info = pygame.sprite.Sprite()
    record = pygame.sprite.Sprite()
    buttons_start.add(play)
    buttons_start.add(info)
    buttons_start.add(record)

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

    record_images = [load_image('menu_record1.png'), load_image('menu_record2.png')]
    record.image = record_images[0]
    record.rect = record.image.get_rect()
    record.rect.x = 290
    record.rect.y = 500

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
                if record.rect.collidepoint(x, y):
                    record.image = record_images[1]
                else:
                    record.image = record_images[0]
            elif event.type == pygame.MOUSEBUTTONUP:  # проверяем, если было нажатие на стартовом экране
                x, y = event.pos
                if info.rect.collidepoint(x, y):
                    show_info()
                elif play.rect.collidepoint(x, y):
                    start.play()
                    game()
                    running = False
                elif record.rect.collidepoint(x, y):
                    show_records()
                    running = False
        font = pygame.font.Font(None, 100)
        text = font.render('Cats and grannies', 1, pygame.Color('red'))
        screen.blit(text, ((900 - text.get_width()) // 2, 100))
        buttons_start.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def death_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                enter_your_name()
                running = False
        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, pygame.Color('red'), (160, 245, 580, 150), 5)
        font = pygame.font.Font(None, 150)
        text = font.render('Game over', 1, pygame.Color('red'))
        font2 = pygame.font.Font(None, 50)
        text2 = font2.render('Press space to continue', 1, pygame.Color('red'))
        screen.blit(text, (170, 270))
        screen.blit(text2, (250, 420))

        pygame.display.flip()


def enter_your_name():
    global score
    running = True
    name = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if 1 in pygame.key.get_pressed():
                if (97 <= pygame.key.get_pressed().index(1) <= 122 or 48 <= pygame.key.get_pressed().index(
                        1) <= 57 and len(name) < 10):
                    name.append(chr(pygame.key.get_pressed().index(1)).upper())
                    pygame.time.delay(350)

                elif pygame.key.get_pressed().index(1) == 8 and name:
                    del name[-1]
                    pygame.time.delay(350)

                elif pygame.key.get_pressed().index(1) == 13 and name:
                    con = sqlite3.connect('data/records.db')
                    cur = con.cursor()
                    result = cur.execute('''SELECT * FROM record''').fetchall()
                    i = 0
                    while result[i][2] > score:
                        i += 1
                    if i != 10:
                        result.insert(i, (i + 1, ''.join(name), score))
                        for j in range(i, 10):
                            cur.execute(f'''UPDATE record
                                           SET name="{result[j][1]}", score={result[j][2]}
                                           WHERE id={j + 1}''')
                    con.commit()
                    con.close()
                    start_screen()
                    running = False
        screen.fill((30, 30, 30))
        font2 = pygame.font.Font(None, 50)
        text2 = font2.render('Enter your name', 1, pygame.Color('red'))
        font = pygame.font.Font(None, 150)
        text = font.render(''.join(name), 1, pygame.Color('red'))
        screen.blit(text, ((900 - text.get_width()) // 2, 270))
        screen.blit(text2, ((900 - text2.get_width()) // 2, 400))
        pygame.display.flip()


def show_records():
    running = True
    con = sqlite3.connect('data/records.db')
    cur = con.cursor()
    records = cur.execute("""SELECT * FROM record""").fetchall()
    records.sort(key=lambda x: -x[2])
    text_records = []
    font = pygame.font.Font(None, 50)

    for i in range(min(len(records), 10)):
        text_records.append([])
        text_records[i].append(font.render(str(records[i][0]), 1, (255, 0, 0)))
        text_records[i].append(font.render(str(records[i][1]), 1, (255, 0, 0)))
        text_records[i].append(font.render(str(records[i][2]), 1, (255, 0, 0)))
    con.close()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                start_screen()
                running = False

        screen.fill((30, 30, 30))
        font = pygame.font.Font(None, 70)
        text = font.render('RECORDS', 1, (255, 0, 0))
        screen.blit(text, (340, 25))
        pygame.draw.line(screen, (255, 0, 0), (100, 70), (100, 650), 3)
        pygame.draw.line(screen, (255, 0, 0), (700, 70), (700, 650), 3)

        for i in range(128, 593, 58):
            pygame.draw.line(screen, (255, 0, 0), (50, i), (850, i), 3)

        for i in range(min(len(records), 10)):
            screen.blit(text_records[i][0], (50 + (50 - text_records[i][0].get_width()) // 2, (i - 1) * 58 + 140))
            screen.blit(text_records[i][1], (120, (i - 1) * 58 + 140))
            screen.blit(text_records[i][2], (710, (i - 1) * 58 + 140))
        pygame.display.flip()


def show_info():
    text = ['Игра Cats and Grannies приветствует вас',
            'Бегай, взбирайся на лестницы, разбивай бочки ',
            'и помоги Коту спасти бабульку',
            'Для управления котом используй стрелки клавиатуры.', 'Чтобы активировать молот на 1 секунду нажми S',
            'Нажатие Esc поставит игру на паузу',
            'Молоток поможет не умереть от бочек,', 'а зелье сделает тебя невидимым для них на 10 секунд',
            'Будь акуратен. Число жизней ограничено',
            'Разбей как можно больше бочек', 'и взберись на вершину доски почета', 'Удачи)']
    cords = [50, 110, 140, 200, 230, 260, 320, 350, 410, 460, 490, 550]
    font = pygame.font.Font(None, 40)
    for i in range(len(text)):
        text[i] = font.render(text[i], 1, pygame.Color('red'))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False
        for i in range(len(text)):
            screen.blit(text[i], ((900 - text[i].get_width()) // 2, cords[i]))
        pygame.display.flip()
    start_screen()


def new_level():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False
        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, pygame.Color('red'), (160, 245, 580, 150), 5)
        font = pygame.font.Font(None, 150)
        text = font.render(f'    Level {str(door.level)}', 1, pygame.Color('red'))
        font2 = pygame.font.Font(None, 50)
        text2 = font2.render('Press space to continue', 1, pygame.Color('red'))
        screen.blit(text, (170, 270))
        screen.blit(text2, (250, 420))
        pygame.display.flip()


def win_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                enter_your_name()
                running = False
            if event.type == STAR_TIMER:
                create_particles((450, 0))

        stars_sprites.update()
        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, pygame.Color('red'), (160, 245, 580, 150), 5)
        font = pygame.font.Font(None, 150)
        text = font.render('  You win!', 1, pygame.Color('red'))
        font2 = pygame.font.Font(None, 50)
        text2 = font2.render('Press space to continue', 1, pygame.Color('red'))
        stars_sprites.draw(screen)
        screen.blit(text, (170, 270))
        screen.blit(text2, (250, 420))
        pygame.display.flip()
        clock.tick(50)


def pause_screen():
    global score, count_life, bucks_v
    buttons = pygame.sprite.Group()
    continue_ = pygame.sprite.Sprite()
    start_over = pygame.sprite.Sprite()
    buttons.add(continue_)
    buttons.add(start_over)

    continue_images = [load_image('menu_play1.png'), load_image('menu_play2.png')]  # заменить картинку
    continue_.image = continue_images[0]
    continue_.rect = continue_.image.get_rect()
    continue_.rect.x = 290
    continue_.rect.y = 300

    start_images = [load_image('menu_start1.png'), load_image('menu_start2.png')]
    start_over.image = start_images[0]
    start_over.rect = start_over.image.get_rect().move(290, 400)

    running = True
    while running:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if continue_.rect.collidepoint(x, y):
                    continue_.image = continue_images[1]
                else:
                    continue_.image = continue_images[0]
                if start_over.rect.collidepoint(x, y):
                    start_over.image = start_images[1]
                else:
                    start_over.image = start_images[0]

            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if continue_.rect.collidepoint(x, y):
                    return
                if start_over.rect.collidepoint(x, y):
                    preparing_for_new_game()
                    next_level.play()
                    new_level()
                    return

        buttons.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def preparing_for_new_game():
    global score, count_life, bucks_v
    door.level = 1
    door.image = Door.door_image
    door.rect.y = 100
    hero.rect.x = hero.startX
    hero.rect.y = hero.startY
    score = 0
    count_life = 3
    for i in range(3):
        lives[i].image = life_images[1]


def game():
    global count_life, score, bucks_v
    for i in range(3):
        lives[i].image = life_images[1]
    bucks_v = randint(2, 5)
    count_life = 3
    a = 31

    left = right = up = down = False
    hammer_activated = False
    font = pygame.font.Font(None, 50)
    running = True
    while running:
        if door.level == 1:
            x = [1, 1, 0, 0, 0, 0]
        elif door.level == 2:
            x = [1, 1, 1, 0, 0, 0]
        else:
            door.become_princess()
            x = [1, 1, 1, 1, 0, 0]
        if pygame.time.get_ticks() % 80 == 0 and choice(x):
            Buck(bucks_v)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_screen()
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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s and hero.hammer:
                hammer_activated = True
                pygame.time.set_timer(HAMMER_UNACTIDE, 1000)
            if event.type == pygame.KEYUP and event.key == pygame.K_s or event.type == HAMMER_UNACTIDE:
                hammer_activated = False

            for spr in bucks_group:

                if spr.death and spr.c == 3:
                    bucks_group.remove(spr)
                    all_sprites.remove(spr)
                if spr.death:
                    spr.c += 1

            if event.type == 29:
                hero.spell = False
            if event.type == 28:
                hero.r -= 1
                if hero.r < 0:
                    hero.r = 0

        screen.fill((30, 30, 30))
        text = font.render(str(hero.r), 1, pygame.Color('red'))
        screen.blit(text, (850, 80))
        camera.update(hero)
        for spr in all_sprites:
            screen.blit(spr.image, camera.apply(spr))

        if count_life <= 0:
            game_over.play()
            death_screen()
            break

        pygame.draw.rect(screen, pygame.Color('red'), (790, 10, 100, 30), 1)
        font = pygame.font.Font(None, 35)
        text = font.render(str(score).rjust(6, '0'), 1, (255, 0, 0))  # счет
        screen.blit(text, (799, 14))

        hero.update(left, right, up, down, platforms, stairs, hammer_activated)
        spell.update()
        hammer.update()
        bucks_group.update()
        monster.update()
        life_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()


game_over = load_sound('12 - Game Over.wav')
next_level = load_sound('11 - All Rounds Cleared.wav')
start = load_sound('03 - How High Can You Get.wav')
aplod = load_sound('00162.wav')

buttons_start = pygame.sprite.Group()
player = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
stairs_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
life_group = pygame.sprite.Group()
bucks_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
stars_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

platforms, stairs = generate_level()
hero = Player(400, 850)
hammer = Hammer(90, 770)
spell = Spell(650, 400)
monster = Monster(120, 160)
door = Door(300, 100)
all_sprites.add(hero)
all_sprites.add(hammer)
all_sprites.add(spell)
all_sprites.add(monster)
all_sprites.add(door)

life_images = [pygame.transform.scale(load_image('life.png', (255, 255, 255)), (33, 30)),
               pygame.transform.scale(load_image('life2.png', (255, 255, 255)), (33, 30))]
lives = []
for i in range(10, 160, 50):  # жизни
    life = pygame.sprite.Sprite()
    life_group.add(life)
    life.image = life_images[1]
    life.rect = life.image.get_rect().move(10, i)
    lives.append(life)
count_life = 3
score = 0

level_width = 900
level_height = 1000

camera = Camera(camera_state, level_width, level_height)

start_screen()
# завершение работы:
pygame.quit()
