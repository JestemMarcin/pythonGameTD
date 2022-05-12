import os
import csv
import pygame


def save_path(path: [(int, int)]):
    # save given path to file
    with open('arena1_path.csv', 'w', newline='', encoding='UTF8') as f:
        # create the csv writer
        writer = csv.writer(f, delimiter=';')
        # write a row to the csv file
        writer.writerows(path)


def read_path() -> [(int, int)]:
    # read path from file return as list
    path = []
    with open('arena1_path.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            path.append((int(row[0]), int(row[1])))
    return path


def point_to_point_path_random_algorythm_by_myself(point1: [int, int], point2: [int, int]) -> [(int, int)]:
    # calculate path points in straight line from point to point without first starting point
    path = []
    # path.append(point1[0],point1[1])
    difference_x = max(point1[0], point2[0]) - min(point1[0], point2[0])
    difference_y = max(point1[1], point2[1]) - min(point1[1], point2[1])
    points_count = max(difference_x, difference_y)
    direction = [-1, 0] if point1[0] - point2[0] > 0 else [1, 0]
    direction[1] = -1 if point1[1] - point2[1] > 0 else 1
    while not (round(point1[0]) == point2[0] and round(point1[1]) == point2[1]):
        point1[0] += direction[0] * difference_x / points_count
        point1[1] += direction[1] * difference_y / points_count
        path.append((round(point1[0]), round(point1[1])))

    return path


def process_path(path: [(int, int)]):
    # process path, adding path xy cords between all points if possible
    complex_path = []
    old_point = []
    for point in path:
        if len(old_point) != 0:
            complex_path += point_to_point_path_random_algorythm_by_myself(list(old_point), list(point))
        else:
            complex_path.append(point)
        old_point = point

    return complex_path


def start():
    # Pygame resolution automatic resizing, fix found in the internet for windows only I guess
    if os.name == 'nt':
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
    ####################

    pygame.init()

    # set up the drawing window

    screen = pygame.display.set_mode([1920, 1080], pygame.FULLSCREEN)  # [850, 850]

    # load asset
    arena1 = pygame.image.load('assets/arenas/arena1.png').convert_alpha()

    path = []
    game_loop_period = 20
    sprites = []

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
                path.append(pos)
                # get a list of all sprites that are under the mouse cursor
                clicked_sprites = [s for s in sprites if s.rect.collidepoint(pos)]
                # do something with the clicked sprites...
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    save_path(path)
                elif event.key == pygame.K_o:
                    path = read_path()
                elif event.key == pygame.K_p:
                    path = process_path(path)
        ####################

        # draw stuff
        screen.fill((255, 3, 255))
        pygame.draw.rect(screen, (1, 2, 3), pygame.Rect(0, 0, 850, 850))
        pygame.draw.rect(screen, (1, 112, 23), pygame.Rect(1070, 0, 850, 850))
        pygame.draw.line(screen, (0, 0, 255), (0, 0), (900, 500), 5)
        screen.blit(arena1, (0, 0))

        # draw path
        last_point = []
        for point in path:
            pygame.draw.circle(screen, (100, 100, 100), (point[0], point[1]), 10)
            if len(last_point) != 0:
                pygame.draw.line(screen, (0, 0, 255), point, last_point, 5)
            last_point = point;

        # update display with flip rather than update because it's faster for whole screen ?
        pygame.display.flip()

        # Game period - refresh rate
        pygame.time.delay(game_loop_period)

    pygame.quit()
