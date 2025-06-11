import pygame

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 15

    def draw(self, screen):
        bullet_sprite = pygame.image.load("Sprites/Bullet/bullet.png").convert_alpha()
        screen.blit(bullet_sprite, (self.x, self.y))
       
    def move(self):
        self.x += self.speed * self.direction