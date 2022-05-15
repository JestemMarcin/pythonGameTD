import csv
from Defender import *
from Enemy import *
# idk right now how to make packages namespaces or whatever so imports go like that


def read_path() -> [(int, int)]:
    # read path from file return as list
    path = []
    with open('arena1_path.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            path.append((int(row[0]), int(row[1])))
    return path


# pygame init function
pygame.init()

# set up the drawing window
screen = pygame.display.set_mode([850, 850], pygame.FULLSCREEN)  # [850, 850]
clock = pygame.time.Clock()

# load asset
arena1 = pygame.image.load('assets/arenas/arena1.png').convert_alpha()
enemy1 = pygame.image.load(
    'assets/enemies/alien.png').convert_alpha()
# stolen from https://www.flaticon.com/free-icons/alien Alien icons created by Freepik - Flaticon

defender1 = pygame.image.load('assets/defenders/defender1/defender1.png').convert_alpha()
projectile1 = pygame.image.load('assets/defenders/defender1/defender1_projectile.png')

path = read_path()
enemies = []
defenders = []
sprites = []

# fps limit
fps = 100

# main loop
exit_game = False
while not exit_game:

    # enemies creator
    last_move_time = pygame.time.get_ticks() if 'last_move_time' not in locals() else last_move_time
    time_difference = pygame.time.get_ticks() - last_move_time
    move_countt = time_difference // 500  # operator count how many times thing contains, always forget it
    last_move_time = pygame.time.get_ticks() - time_difference % 500  # replace last time and
    alien_hp = 30
    for i in range(move_countt):
        enemies.append(Enemy(enemy1, 6, alien_hp, 32, 32, pygame.time.get_ticks()))
        alien_hp += 1

    # event management
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            defenders.append(
                Defender(defender1, projectile1, 200, 1, 10, 51, 51, pos, pygame.time.get_ticks()))

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                path = read_path()

    # draw stuff
    screen.blit(arena1, (0, 0))

    for defender in defenders:
        # draw defenders
        screen.blit(defender.img, (defender.xy[0] - defender.width / 2, defender.xy[1] - defender.height / 2))

        # draw projectiles
        for projectile in defender.projectiles:
            screen.blit(projectile.img, projectile.xy)
            # move projectiles
            time_diff = pygame.time.get_ticks() - projectile.last_move_time
            move_count = time_diff // defender.projectile_speed
            projectile.last_move_time = pygame.time.get_ticks() - time_diff % defender.projectile_speed
            # added leftover time difference not used for move
            projectile_exist = True
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
        move_count = time_diff // defender.attack_speed
        defender.last_move_time = pygame.time.get_ticks() - time_diff % defender.attack_speed
        for i in range(move_count):
            if len(enemies) > 0:
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

        enemy_exist = True
        for defender in defenders:
            if not enemy_exist:
                break
            for projectile in defender.projectiles:
                # check projectile collisions with enemies
                if pygame.Rect(
                        (path[enemy.path_index][0] - enemy.width / 2, path[enemy.path_index][1] - enemy.height / 2),
                        (enemy.width, enemy.height)).collidepoint(projectile.xy):
                    defender.projectiles.remove(projectile)
                    enemy.hp -= defender.damage
                    if enemy.hp <= 0:
                        enemies.remove(enemy)
                        enemy_exist = False

    # update display with flip rather than update because it's faster for whole screen ?
    pygame.display.flip()
    # game period - refresh rate
    clock.tick(fps)
pygame.quit()
