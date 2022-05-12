import os
import csv
import pygame


def read_path() -> [(int, int)]:
    # read path from file return as list
    path = []
    with open('arena1_path.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            path.append((int(row[0]), int(row[1])))
    return path


class Enemy:
    # each object is single instance of enemy moving down the path
    def __init__(self, img, speed: int, hp: int, height: int, width: int,
                 last_move_time: int = 0):  # img should have type Surface but it didn't see it?
        # c.d. pygame image.load should return that type
        self.img = img
        self.speed = speed  # speed how many moves in millisecond
        self.path_index = 0
        self.hp = hp
        self.last_move_time = last_move_time
        self.height = height
        self.width = width

    def move(self, speed: int = 1):
        self.path_index += speed


def start():
    # Pygame resolution automatic resizing, fix found in the internet for windows only I guess
    if os.name == 'nt':
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
    ####################

    pygame.init()

    # set up the drawing window

    screen = pygame.display.set_mode([1920, 1080], pygame.FULLSCREEN)  # [850, 850]
    clock = pygame.time.Clock()

    # load asset
    arena1 = pygame.image.load('assets/arenas/arena1.png').convert_alpha()
    enemy1 = pygame.image.load('assets/enemies/enemy1.png').convert_alpha()
    path = read_path()
    enemies = []
    sprites = []
    enemies.append(Enemy(enemy1, 6, 100, 51, 51, pygame.time.get_ticks()))
    # fps
    fps = 100
    # run until the user asks to quit
    exit_game = False
    while not exit_game:
        # main loop

        # event managment
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                # get a list of all sprites that are under the mouse cursor
                clicked_sprites = [s for s in sprites if s.rect.collidepoint(pos)]
                # do something with the clicked sprites...
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    path = read_path()

        ####################

        # draw stuff
        screen.fill((255, 3, 255))
        pygame.draw.rect(screen, (1, 2, 3), pygame.Rect(0, 0, 850, 850))
        pygame.draw.rect(screen, (1, 112, 23), pygame.Rect(1070, 0, 850, 850))
        pygame.draw.line(screen, (0, 0, 255), (0, 0), (900, 500), 5)
        screen.blit(arena1, (0, 0))

        # draw path
        for point in path:
            pygame.draw.circle(screen, (200, 90, 90), (point[0], point[1]), 3)

        # move enemies
        for enemy in enemies:
            time_diff = pygame.time.get_ticks() - enemy.last_move_time
            move_count = time_diff // enemy.speed  # operator count how many times thing contains, always forget it
            enemy.last_move_time = pygame.time.get_ticks() - time_diff % enemy.speed  # replace last time and
            # added leftover time difference not used for move
            for i in range(move_count):
                print(str(i) + " " + str(time_diff))
                enemy.move()
                if enemy.path_index == len(path):
                    enemies.remove(enemy)
        # draw enemies
        for enemy in enemies:
            print()
            screen.blit(enemy.img, (path[enemy.path_index][0] - enemy.width / 2,
                                    path[enemy.path_index][1] - enemy.height / 2))

        # update display with flip rather than update because it's faster for whole screen ?
        pygame.display.flip()
        # game period - refresh rate
        clock.tick(fps)
    pygame.quit()
