import pygame

class Bullet:
    def __init__(self, x, y, direction, sprite_path="Sprites/Bullet/bullet.png", speed = 15):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.sprite_path = sprite_path

    def draw(self, screen):
        bullet_sprite = pygame.image.load(self.sprite_path).convert_alpha()
        screen.blit(bullet_sprite, (self.x, self.y))
       
    def move(self):
        self.x += self.speed * self.direction

    @property
    def position(self):
        return (self.x, self.y)