import pygame

# Clase padre de los personajes
class Character: 
    def __init__(self, x = 0, y = 0, width = 100, height = 100, speed = 10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = (255, 0, 0)    

    @property
    def position(self):
        return self.x, self.y

    def draw(self, screen):
        pygame.draw.rect(screen,self.color, (self.x, self.y, self.width, self.height))
