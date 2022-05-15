"""
Class make projectiles shooting projectiles on enemies

"""
import pygame


class Projectile:
    def __init__(self, xy: (int, int), xy_target: (int, int), img: pygame.Surface, last_move_time: int = 0):
        self.xy = [xy[0] * 1.0, xy[1] * 1.0]
        self.xy_target = xy_target
        self.img = img
        self.last_move_time = last_move_time
        difference_x = max(xy[0], xy_target[0]) - min(xy[0], xy_target[0])
        difference_y = max(xy[1], xy_target[1]) - min(xy[1], xy_target[1])

        self.x_movement = difference_x / (difference_y + difference_x)
        self.y_movement = 1 - self.x_movement
        if self.xy[0] - self.xy_target[0] >= 0:
            self.x_movement *= -1
        if self.xy[1] - self.xy_target[1] >= 0:
            self.y_movement *= -1

    def move(self):
        self.xy[0] += self.x_movement
        self.xy[1] += self.y_movement
