import pygame
from Entities.character import Character

class Soldier(Character):
    def __init__(self, x = 0, y = 0, width = 100, height = 100):
        super().__init__(x, y, width, height)
        self.color = (0, 255, 0)
        self.is_alive = True

    def move(self):
        if self.is_alive:
            self.x -= self.speed
    
    def remove(self):
        self.x = -100
        self.is_alive = False
    
    @property
    def is_alive(self):
        return self._is_alive
    
    @is_alive.setter
    def is_alive(self, value):
        self._is_alive = value