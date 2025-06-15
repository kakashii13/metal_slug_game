import pygame
from entities.character import Character

class Soldier(Character):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)
        self.color = (0, 255, 0)
        self.is_alive = True
        self.walk_frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_rate = 5
        self.load_walk_sprites("Sprites/chinese_soldier", frame_count=6)  # 6 frames de caminata

    def load_walk_sprites(self, folder_path, frame_count):
        # recorro el numero de frames de la animacion de caminata
        for i in range(frame_count):
            path = f"{folder_path}/chinese_soldier_{i}.png"
            frame = pygame.image.load(path).convert_alpha()
            self.walk_frames.append(frame)

    def draw(self, surface):
        if self.is_alive:
            # Actualiza la animacion si se esta moviendo
            self.frame_timer += 1 
            if self.frame_timer >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
                self.frame_timer = 0
            # dibujamos el frame de caminata
            surface.blit(self.walk_frames[self.current_frame], (self.x, self.y - self.height))
        # Fuente para dibujar texto
        font = pygame.font.SysFont(None, 24)
        
        # Crear texto con la posición
        coord_text = font.render(f"({self.x}, {self.y}, {self.height})", True, (0, 0, 0))  # negro
        
        # Dibujar texto sobre el personaje
        surface.blit(coord_text, (self.x + 50, self.y - 20))  # un poco más arriba
            

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