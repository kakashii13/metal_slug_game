import pygame

class Obstacle: 
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        # match obstacle sprite dimensions for accurate collisions
        self.width = 120
        self.height = 80
        self.obstacle_frame = pygame.image.load(
            "Sprites/extras/truck.png"
        ).convert_alpha()
    
    def draw(self, surface, scroll_x=0):
        frame = pygame.transform.scale(self.obstacle_frame, (self.width, self.height))
        surface.blit(
            frame,
            (self.x - scroll_x, self.y - self.height),
        )  # restamos para igualar la altura del obstaculo con el sprite

    def move(self):
        self.x -= 5

    @property
    def position(self):
        return (self.x, self.y)
    @property
    def size(self):
        return (self.width, self.height)