import random, sys, copy, os, pygame
import pygame


# def create_path():


def start():
    # Pygame resolution automatic resizing, idk if its pygame problem or what, fix is for windows I guess
    if os.name == 'nt':
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()

    pygame.init()

    # Set up the drawing window

    screen = pygame.display.set_mode([1920, 1080], pygame.FULLSCREEN)  # [850, 850]
    arena1 = pygame.image.load('assets/arenas/arena1.png').convert_alpha()
    path = []
    game_loop_period = 20
    sprites = []
    # Run until the user asks to quit
    exit_game = False
    while not exit_game:

        # Did the user click the window close button?
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
                if event.key == pygame.K_RIGHT:
                    print("You have pressed right arrow key")
                elif event.key == pygame.K_LEFT:
                    print("You have pressed left arrow key")

        # Fill the background with white
        screen.fill((255, 3, 255))

        pygame.draw.rect(screen, (1, 2, 3), pygame.Rect(0, 0, 850, 850))
        pygame.draw.rect(screen, (1, 112, 23), pygame.Rect(1070, 0, 850, 850))
        # Draw a green line
        pygame.draw.line(screen, (0, 0, 255), (0, 0), (900, 500), 5)
        screen.blit(arena1, (0, 0))
        #draw path
        last_point = []
        for point in path:
            pygame.draw.circle(screen, (100,100,100),(point[0],point[1]),10)
            if len(last_point) != 0:
                pygame.draw.line(screen, (0, 0, 255), point, last_point, 5)
            last_point = point;
        # Update display with flip rather than update cause it's faster for whole screen ?
        pygame.display.flip()

        # Game period - refresh rate
        pygame.time.delay(game_loop_period)

    pygame.quit()