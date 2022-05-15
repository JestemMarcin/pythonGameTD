"""
Class make defenders shooting projectiles on enemies

"""
import pygame
from Projectile import *


class Defender:
    # turrets, towers shooting projectiles on enemies
    def __init__(self, img: pygame.Surface, img_projectile: pygame.Surface, attack_speed: int,
                 projectile_speed: int, damage: int, height: int, width: int, xy: (int, int), last_move_time: int = 0):
        self.img = img
        self.img_projectile = img_projectile
        self.attack_speed = attack_speed
        self.projectile_speed = projectile_speed
        self.xy = xy
        self.damage = damage
        self.last_move_time = last_move_time
        self.height = height
        self.width = width
        self.projectiles = []

    def shot(self, xy_target: (int, int)):
        self.projectiles.append(
            Projectile(self.xy, xy_target, self.img_projectile, pygame.time.get_ticks()))
