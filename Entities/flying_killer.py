import pygame
import math
from entities.character import Character
from entities.bullet import Bullet

class FlyingKiller(Character): 
    def __init__(self, x = 0 , y= 0):
        super().__init__(x,y)
        self.is_alive = True
        self.tick = 0
        self.initial_y = y
        self.amplitude = 55  # Amplitud del movimiento vertical
        self.frecuency = 0.1  # Frecuencia del movimiento vertical
        self.flying_frames = []
        self.frame_timer = 0
        self.current_frame = 0
        self.frame_rate = 5
        self.last_shot_time = 0
        self.shot_interval = 1000
        self.shots_remaining = 3
        self.load_walk_sprites_from_sheet("Sprites/flying_killer/killer.png", frame_width=41, frame_height=37, frame_count=12)

    def load_walk_sprites_from_sheet(self, sheet_path, frame_width, frame_height, frame_count):
        sheet = pygame.image.load(sheet_path).convert_alpha()
        
        for i in range(frame_count):
            # calculamos la posicion de cada frame dentro del srpite
            x = i * frame_width
            
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), pygame.Rect(x, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (50, 70))
            self.flying_frames.append(frame)

    def draw(self, surface, scroll_x=0):
        if self.is_alive:
            # Actualiza la animacion si se esta moviendo
            self.frame_timer += 1 
            if self.frame_timer >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.flying_frames)
                self.frame_timer = 0
            # dibujamos el frame de caminata
            surface.blit(self.flying_frames[self.current_frame], (self.x - scroll_x, self.y - self.height))
    
    def move(self):
        if self.is_alive:
            self.x -= self.speed
            self.tick += 1
            self.y = self.initial_y + self.amplitude * math.sin(self.frecuency * self.tick)

    def can_shoot(self, current_time):
        return self.is_alive and self.shots_remaining > 0 and current_time - self.last_shot_time >= self.shot_interval

    def shoot(self, current_time):
        self.last_shot_time = current_time
        self.shots_remaining -= 1
        return Bullet(self.x, self.y, -1, "Sprites/bullet/enemy_bullet.png")

    def remove(self):
        self.is_alive = False
        self.x = -1000