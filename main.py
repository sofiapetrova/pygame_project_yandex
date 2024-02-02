import random
import pygame as pg


class Hero(pg.sprite.Sprite):
    def __init__(self, number, file='img/fishes/fish8.png'):
        pg.sprite.Sprite.__init__(self)
        # порядковый номер игрока
        self.number = number
        self.file = file
        self.size = 0.1
        self.image = pg.image.load(self.file)
        self.image = pg.transform.scale(self.image,
                                        (self.image.get_width() * self.size, self.image.get_height() * self.size))
        self.rect = self.image.get_rect(center=(SIZE[0] // 2 + 100 * self.number, SIZE[1] // 2))
        self.speedx = 5
        self.speedy = 3
        self.move_to_left = False
        self.move_to_right = False
        # съеденные рыбки
        self.count = 0
        # state_of_game:
        # 1 - начало игры, начальная заставка
        # 2 - игра в процессе
        # 3 - игрок проиграл
        # 4 - игрок выиграл
        self.state_of_game = 1
        self.eat_sound = pg.mixer.Sound('sounds/eat.ogg')
        # первый игрок управляет стрелочками, второй - wasd
        if self.number == 1:
            self.control = {'left': pg.K_LEFT, 'right': pg.K_RIGHT, 'up': pg.K_UP, 'down': pg.K_DOWN}
        elif self.number == 2:
            self.control = {'left': pg.K_a, 'right': pg.K_d, 'up': pg.K_w, 'down': pg.K_s}

    def update(self) -> None:
        self.move_hero()
        self.contact()
        if self.state_of_game == 3 or self.state_of_game == 4:
            self.restart_hero()

    def move_hero(self):
        key = pg.key.get_pressed()
        # движение влево
        if key[self.control['left']] and self.rect.left >= 0 and not self.move_to_left:
            self.rect.x -= self.speedx
            self.move_to_left = True
            self.move_to_right = False
            self.image = pg.transform.flip(self.image, 1, 0)
        elif key[self.control['left']] and self.rect.left >= 0:
            self.rect.x -= self.speedx
        # движение вправо
        if key[self.control['right']] and self.rect.right <= SIZE[0] and not self.move_to_right:
            self.rect.x += self.speedx
            self.move_to_left = False
            self.move_to_right = True
            self.image = pg.transform.flip(self.image, 1, 0)
        elif key[self.control['right']] and self.rect.right <= SIZE[0]:
            self.rect.x += self.speedx
        # движение вверх и вниз
        if key[self.control['up']] and self.rect.top >= 0:
            self.rect.y -= self.speedy

        if key[self.control['down']] and self.rect.bottom <= SIZE[1]:
            self.rect.y += self.speedx

    def contact(self):
        """
         перебираем список рыбок. если столкнулись с маленькой рыбкой, то съедаем ее и увеличиваем счетчик
         если столкнулись с большой рыбкой - меняем свое состояние self.state_of_game =3 -  состояние проигрыша

        """

        for fish in fishes:
            if pg.sprite.collide_mask(self, fish):
                if self.image.get_width() > fish.image.get_width() or self.image.get_height() > fish.image.get_height():
                    self.size += 0.05
                    self.count += 1
                    self.eat_sound.play()
                    self.move_to_left = False
                    self.move_to_right = False
                    x, y = self.rect.x, self.rect.y
                    self.image = pg.image.load(self.file)
                    self.image = pg.transform.scale(self.image,
                                                    (self.image.get_width() * self.size,
                                                     self.image.get_height() * self.size))
                    self.rect = self.image.get_rect(x=x, y=y)
                else:
                    self.state_of_game = 3

                fishes.remove(fish)
                fish.kill()
                fishes.add(Fish())

        # если съели достаточно - меняем свое состояние self.state_of_game =4 -  состояние выигрыша
        if self.count >= COUNT:
            self.state_of_game = 4

    def restart_hero(self):
        """
        сброс состояния игрока к первоначальному
        """
        self.file = 'img/fishes/fish8.png'
        self.size = 0.1
        self.image = pg.image.load(self.file)
        self.image = pg.transform.scale(self.image,
                                        (self.image.get_width() * self.size, self.image.get_height() * self.size))
        self.rect = self.image.get_rect(center=(SIZE[0] // 2 + 100 * self.number, SIZE[1] // 2))
        self.speedx = 5
        self.speedy = 3
        self.move_to_left = False
        self.move_to_right = False
        self.count = 0


class Bubble(pg.sprite.Sprite):
    bubble_skin = ['img/bubble/bubble01.png', 'img/bubble/bubble02.png', 'img/bubble/bubble03.png']

    def __init__(self, file='img/bubble/bubble01.png'):
        pg.sprite.Sprite.__init__(self)
        self.file = file
        self.image = pg.image.load(self.file)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.speed = random.randint(1, 4)
        self.rect = self.image.get_rect(y=SIZE[1], x=random.randint(0, SIZE[0]))
        self.koef_scale = 1

    def update(self) -> None:
        if self.rect.bottom >= 0:
            self.rect.y -= self.speed
        else:
            self.rect.y = SIZE[1]
            self.rect.x = random.randint(-50, SIZE[0])
            self.speed = random.randint(1, 4)
            self.koef_scale = random.choice([1, 0.5, 2.3, 0.7, 2])
            self.image = pg.image.load(self.file)
            self.image = pg.transform.scale(self.image, (50 * self.koef_scale, 50 * self.koef_scale))


class Fish(pg.sprite.Sprite):
    fish_skin = ['img/fishes/fish1.png', 'img/fishes/fish2.png',
                 'img/fishes/fish3.png', 'img/fishes/fish4.png',
                 'img/fishes/fish5.png', 'img/fishes/fish6.png',
                 'img/fishes/fish7.png', 'img/fishes/fish8.png']

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.file = random.choice(Fish.fish_skin)
        self.image = pg.image.load(self.file)
        self.koef_scale = random.choice([1, 0.5, 2.3, 0.7, 2, 0.05, 0.1, 0.2, 0.07])
        self.image = pg.transform.scale(self.image, (
            self.image.get_size()[0] * self.koef_scale, self.image.get_size()[1] * self.koef_scale))
        self.direction = random.choice((1, -1))  # 1 = слева направо, -1 = справа налево
        if self.direction == 1:
            self.rect = self.image.get_rect(right=random.randint(-100, 0),
                                            y=random.randint(0, SIZE[1] - self.image.get_height()))
        else:
            self.image = pg.transform.flip(self.image, 1, 0)
            self.rect = self.image.get_rect(left=random.randint(SIZE[0], SIZE[0] + 150),
                                            y=random.randint(0, SIZE[1] - self.image.get_height()))
        self.koef_speed = 1
        self.speed = random.randrange(1 * self.koef_speed, 7 * self.koef_speed, self.koef_speed)

    def update(self) -> None:
        # рыбка плывет
        if self.rect.x <= SIZE[0] and self.direction == 1:
            self.rect.x += self.speed
        elif self.rect.right >= 0 and self.direction == -1:
            self.rect.x += self.speed * self.direction
        # если уплыла за край - обновляем ее состояние и под видом другой рыбы снова отправляем плавать с новыми настройками
        else:
            self.speed = random.randrange(1 * self.koef_speed, 7 * self.koef_speed, self.koef_speed)
            self.file = random.choice(Fish.fish_skin)
            self.image = pg.image.load(self.file)
            self.koef_scale = random.choice([1, 0.5, 2.3, 0.7, 2, 0.05, 0.1, 0.2, 0.07])
            self.image = pg.transform.scale(self.image, (
                self.image.get_size()[0] * self.koef_scale, self.image.get_size()[1] * self.koef_scale))
            self.direction = random.choice((1, -1))  # 1 = слева направо, -1 = справа налево
            if self.direction == 1:

                self.rect = self.image.get_rect(right=random.randint(-100, 0),
                                                y=random.randint(0, SIZE[1] - self.image.get_height()))
            else:
                self.image = pg.transform.flip(self.image, 1, 0)
                self.rect = self.image.get_rect(left=random.randint(SIZE[0], SIZE[0] + 150),
                                                y=random.randint(0, SIZE[1] - self.image.get_height()))


def render_text(screen: pg.Surface, win: pg.Surface, msg):
    """
    выводит на экран текст из списка
    :param поверхность, на которой будет выводится текст:
    :param основное окно игры:
    :param список с фразами, которые надо выводить на экран:
    :return: текст на экране
    """
    x, y = 10, 10
    for line in msg:
        text = font_of_game.render(line, True, (0, 0, 255))
        screen.blit(text, (x, y))
        y += 50
    win.blit(screen, (0, 0))


def start():
    """
    первоначальный экран - выводится если все игроки в состоянии
    self.state_of_game =1
    выводятся парвили игры и возможност выбрать режим - 1 или 2 игрока. по умолчанию - 1 игрок
    после нажатия на пробел - игроки переводятся в состояние self.state_of_game =2
    """
    global players
    if list(filter(lambda hero: hero.state_of_game == 1, heros[:players])):
        render_text(screen_start, window, msg_s)
        key = pg.key.get_pressed()
        if key[pg.K_1]:
            players = 1
        if key[pg.K_2]:
            players = 2
        if key[pg.K_SPACE]:
            for hero in heros[:players]:
                hero.state_of_game = 2


def game():
    if list(filter(lambda hero: hero.state_of_game == 2, heros[:players])):
        screen_game.blit(fon2, (0, 0))
        # герои игры
        for hero in heros[:players]:
            hero.update()
            screen_game.blit(hero.image, hero.rect)
        # рыбы
        fishes.update()
        fishes.draw(screen_game)
        # пузырьки
        bubbles.update()
        bubbles.draw(screen_game)
        # табло игры
        tablo()
        window.blit(screen_game, (0, 0))


def fiasco():
    """
    если хотябы один игрок проиграл - оба переходят в состояние проигрыша
    сброс игры
    """
    if list(filter(lambda hero: hero.state_of_game == 3, heros[:players])):
        render_text(screen_looser, window, msg_f)
        for hero in heros[:players]:
            hero.state_of_game = 3
    restart()


def winner():
    """
        если хотябы один игрок съел достаточно - оба переходят в состояние выигрыша
        сброс игры
        """
    if list(filter(lambda hero: hero.state_of_game == 4, heros[:players])):
        render_text(screen_winner, window, msg_w)
        for hero in heros[:players]:
            hero.state_of_game = 4
    restart()


def tablo():
    for hero in heros[:players]:
        text = font_of_game.render(str(hero.count), True, (0, 0, 250))
        screen_game.blit(text, (10 + hero.number * 100, 10))


def restart():
    global gameover
    global players
    key = pg.key.get_pressed()
    if key[pg.K_1]:
        players = 1
    if key[pg.K_2]:
        players = 2
    if key[pg.K_SPACE] and len(list(filter(lambda hero: hero.state_of_game != 2, heros[:players]))) == players:
        for hero in heros[:players]:
            hero.state_of_game = 2
            hero.restart_hero()
    if key[pg.K_ESCAPE]:
        gameover = True


def read_text(filename):
    """

    :param filename: имя файла с текстом, который  надо будет выводить на экран
    :return: функция возвращает списк из строк
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            msg = []
            line = file.readline().rstrip()
            x, y = 10, 10
            while line:
                msg.append(line)
                line = file.readline().rstrip()
        return msg
    except Exception:
        return ['oops']


pg.init()
pg.mixer.pre_init(44100, -16, 1, 512)
pg.mixer.init()
SIZE = (1200, 780)
window = pg.display.set_mode(SIZE)
font_of_game = pg.font.SysFont('Lucida Console', 30, bold=False, italic=True)

# создаем экран для старта игры
screen_start = pg.Surface(SIZE)
fon = pg.image.load('img/bg/fon_start.jpg')
fon = pg.transform.scale(fon, SIZE)
screen_start.blit(fon, (0, 0))
# считываем из файла текст экрана
msg_s = read_text('msg/msg_start.txt')

# экран (поверхность) для основной игры
screen_game = pg.Surface(SIZE)
fon2 = pg.image.load('img/bg/fon1.jpg')
fon2 = pg.transform.scale(fon2, SIZE)
screen_game.blit(fon2, (0, 0))

# # экран (поверхность) для проигрыша
screen_looser = pg.Surface(SIZE)
fon3 = pg.image.load('img/bg/fon_looser.jpg')
fon3 = pg.transform.scale(fon3, SIZE)
screen_looser.blit(fon3, (0, 0))
# считываем из файла текст экрана
msg_f = read_text('msg/msg_fail.txt')

# # экран (поверхность) для Выигрыша
screen_winner = pg.Surface(SIZE)
fon4 = pg.image.load('img/bg/fon_winner.jpg')
fon4 = pg.transform.scale(fon4, SIZE)
screen_winner.blit(fon4, (0, 0))
# считываем из файла текст экрана
msg_w = read_text('msg/msg_win.txt')

heros = [Hero(1), Hero(2)]
players = 1  # количество игроков в игре. по умолчанию - один
bubbles = pg.sprite.Group()
for i in range(6):
    bubbles.add(Bubble(file=random.choice(Bubble.bubble_skin)))

fishes = pg.sprite.Group()
for i in range(10):
    fishes.add(Fish())

gameover = False
game_sound = pg.mixer.Sound('sounds/sea.ogg')
game_sound.play(-1)
FPS = 40
COUNT = 2  # количество рыбок, которых нужно съесть для победы
timer = pg.time.Clock()
while not gameover:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            gameover = True
    start()
    game()
    winner()
    fiasco()
    pg.display.flip()
    timer.tick(FPS)
if gameover:
    pg.quit()
