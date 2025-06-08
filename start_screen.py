import pygame
import sys

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        self.bg_color = (255, 255, 255)
        self.title_color = (0, 0, 0)
        self.text_color = (0, 0, 0)
        self.title = self.font.render("Shooter Game", True, (0, 0, 0))
        self.title_rect = self.title.get_rect(center=(400, 200))

    def draw(self):
         while True:
            self.screen.fill(self.bg_color)

            title = self.font.render("¡Bienvenido al juego!", True, self.title_color)
            instruction = self.small_font.render("Presioná E para comenzar", True, self.text_color)

            self.screen.blit(title, (200, 200))
            self.screen.blit(instruction, (220, 300))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # el usuario cerro 
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    return True  # el usuario quiere jugar