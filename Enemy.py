"""
Class make enemies

"""
import pygame


class Enemy:
    # each object is single instance of enemy moving down the path
    def __init__(self, img: pygame.Surface, speed: int, hp: int, height: int, width: int,
                 last_move_time: int = 0):
        self.img = img
        self.speed = speed
        self.path_index = 0
        self.hp = hp
        self.last_move_time = last_move_time
        self.height = height
        self.width = width

    def move(self, speed: int = 1):
        self.path_index += speed
