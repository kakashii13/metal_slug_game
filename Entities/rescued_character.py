from entities.character import Character
import pygame

class RescuedCharacter(Character):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_rate = 5
        self.load_sprites("Sprites/rescued_character", frame_count=4)
        self._is_saved = False

    def load_sprites(self, folder_path, frame_count):
        for i in range(frame_count):
            path = f"{folder_path}/{i}.png"
            frame = pygame.image.load(path).convert_alpha()
            frame =  pygame.transform.scale(frame, (50, 70))
            self.frames.append(frame)

    def draw(self, surface, scroll_x=0):
        self.frame_timer += 1
        if self.frame_timer >= self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_timer = 0
        surface.blit(self.frames[self.current_frame], (self.x - scroll_x, self.y - self.height + 10))  # Ajuste de altura
    
    def remove(self):
        self.x = -100

    @property
    def is_saved(self):
        return self._is_saved
    @is_saved.setter
    def is_saved(self, value):
        self._is_saved = value
        if value:
            self.x = -100  # Mueve el personaje fuera de la pantalla al ser rescatado