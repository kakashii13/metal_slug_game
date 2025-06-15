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
         # Fuente para dibujar texto
        font = pygame.font.SysFont(None, 24)
        
        # Crear texto con la posición
        coord_text = font.render(f"({self.x}, {self.y})", True, (0, 0, 0))  # negro
        
        # Dibujar texto sobre el personaje
        screen.blit(coord_text, (self.x + 50, self.y - 20))  # un poco más arriba
       
    def move(self):
        self.x += self.speed * self.direction

    @property
    def position(self):
        return (self.x, self.y)