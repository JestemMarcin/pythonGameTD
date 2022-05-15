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
    def __init__(self, img: pygame.Surface, speed: int, hp: int, height: int, width: int,
                 last_move_time: int = 0):
        self.img = img
        self.speed = speed  # speed how many moves in millisecond
        self.path_index = 0
        self.hp = hp
        self.last_move_time = last_move_time
        self.height = height
        self.width = width


    def move(self, speed: int = 1):
        self.path_index += speed


class Defender:
    # turrets, towers shooting projectiles on enemies
    def __init__(self, img: pygame.Surface, img_projectile, attack_speed: int, projectile_speed: int, damage: int, height: int, width: int, xy: (int, int),
                 last_move_time: int = 0):
        self.img = img
        self.img_projectile = img_projectile
        self.attack_speed = attack_speed  # speed how many attacks in millisecond
        self.projectile_speed = projectile_speed # speed how many moves projectile got in millisecond
        self.xy = xy
        self.damage = damage
        self.last_move_time = last_move_time
        self.height = height
        self.width = width
        self.projectiles = []

    def shot(self, xy_target: (int, int)):
        self.projectiles.append(Projectile(self.xy, xy_target, self.img_projectile, self.projectile_speed, pygame.time.get_ticks()))


class Projectile:
    def __init__(self, xy: (int, int), xy_target: (int, int), img, projectile_speed, last_move_time: int = 0):
        self.xy = [xy[0]*1.0, xy[1]*1.0]
        self.xy_target = xy_target
        self.img = img
        self.last_move_time = last_move_time
        difference_x = max(xy[0], xy_target[0]) - min(xy[0], xy_target[0])
        difference_y = max(xy[1], xy_target[1]) - min(xy[1], xy_target[1])

        self.x_movement = difference_x/(difference_y+difference_x)
        self.y_movement = 1 - self.x_movement
        if self.xy[0]-self.xy_target[0]>=0:
            self.x_movement *= -1
        if self.xy[1] - self.xy_target[1] >= 0:
            self.y_movement *= -1
    def move(self):
        self.xy[0]+=self.x_movement
        self.xy[1]+=self.y_movement





def start():
    # Pygame resolution automatic resizing, fix found in the internet for windows only I guess

    ####################

    pygame.init()

    # set up the drawing window

    screen = pygame.display.set_mode([850, 850], pygame.FULLSCREEN)  # [850, 850]
    clock = pygame.time.Clock()

    # load asset
    arena1 = pygame.image.load('assets/arenas/arena1.png').convert_alpha()
    enemy1 = pygame.image.load('assets/enemies/alien.png').convert_alpha() # stolen from <a href="https://www.flaticon.com/free-icons/alien" title="alien icons">Alien icons created by Freepik - Flaticon</a>
    defender1 = pygame.image.load('assets/defenders/defender1/defender1.png').convert_alpha()
    projectile1 = pygame.image.load('assets/defenders/defender1/defender1_projectile.png')
    path = read_path()
    enemies = []
    defenders = []
    sprites = []

    enemies.append(Enemy(enemy1, 6, 30, 32, 32, pygame.time.get_ticks()))


    # fps
    fps = 100
    # run until the user asks to quit
    exit_game = False
    while not exit_game:
        # main loop
        last_move_time= pygame.time.get_ticks() if 'last_move_time' not in locals() else last_move_time
        # enemies creator
        time_difference = pygame.time.get_ticks() - last_move_time
        move_countt = time_difference // 500  # operator count how many times thing contains, always forget it
        last_move_time = pygame.time.get_ticks() - time_difference % 500  # replace last time and
        alien_hp=30
        for i in range(move_countt):
            enemies.append(Enemy(enemy1, 6, alien_hp, 32, 32, pygame.time.get_ticks()))
            alien_hp+=1


        # event managment
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                defenders.append(
                    Defender(defender1, projectile1, 200, 2, 10, 51, 51, pos, pygame.time.get_ticks()))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    path = read_path()

        ####################

        # draw stuff
        screen.blit(arena1, (0, 0))

        # draw path
        for point in path:
            pygame.draw.circle(screen, (200, 90, 90), (point[0], point[1]), 3)

        for defender in defenders:
            # draw defenders
            screen.blit(defender.img, (defender.xy[0]-defender.width/2,defender.xy[1]-defender.height/2))

            # draw projectiles
            for projectile in defender.projectiles:
                screen.blit(projectile.img, projectile.xy)
                # move projectiles
                time_diff = pygame.time.get_ticks() - projectile.last_move_time
                move_count = time_diff // defender.projectile_speed  # operator count how many times thing contains, always forget it
                projectile.last_move_time = pygame.time.get_ticks() - time_diff % enemy.speed  # replace last time and
                # added leftover time difference not used for move
                projectile_exist =  True
                for i in range(move_count):
                    if not projectile_exist:
                        break
                    projectile.move()
                    if projectile.xy[0] > 850 or projectile.xy[0] < 0:
                        defender.projectiles.remove(projectile)
                        projectile_exist = False
                    elif projectile.xy[1] > 850 or projectile.xy[1] < 0:
                        defender.projectiles.remove(projectile)
                        projectile_exist = False
            # defenders shot
            time_diff = pygame.time.get_ticks() - defender.last_move_time
            move_count = time_diff // defender.attack_speed  # operator count how many times thing contains, always forget it
            defender.last_move_time = pygame.time.get_ticks() - time_diff % defender.attack_speed  # replace last time and
            for i in range(move_count):
                if len(enemies)>0:
                    defender.shot(path[enemies[0].path_index])

        for enemy in enemies:
            # draw enemies
            screen.blit(enemy.img, (path[enemy.path_index][0] - enemy.width / 2,
                                    path[enemy.path_index][1] - enemy.height / 2))

            # move enemies
            time_diff = pygame.time.get_ticks() - enemy.last_move_time
            move_count = time_diff // enemy.speed  # operator count how many times thing contains, always forget it
            enemy.last_move_time = pygame.time.get_ticks() - time_diff % enemy.speed  # replace last time and
            # added leftover time difference not used for move
            for i in range(move_count):
                enemy.move()
                if enemy.path_index == len(path):
                    enemies.remove(enemy)


            enemy_exist=True
            for defender in defenders:
                if not enemy_exist:
                    break
                for projectile in defender.projectiles:
                    # check projectile colizions with enemies
                    if pygame.Rect((path[enemy.path_index][0]-enemy.width/2,path[enemy.path_index][1]-enemy.height/2),(enemy.width,enemy.height)).collidepoint(projectile.xy):
                        defender.projectiles.remove(projectile)
                        enemy.hp -= defender.damage
                        if enemy.hp <= 0:
                            enemies.remove(enemy)
                            enemy_exist=False

        # update display with flip rather than update because it's faster for whole screen ?
        pygame.display.flip()
        # game period - refresh rate
        clock.tick(fps)
    pygame.quit()
