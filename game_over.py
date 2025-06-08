import pygame
import sys

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.title_color = (0, 0, 0)

    def draw(self):
        waiting = True
        while waiting:
            self.screen.fill((255, 255, 255))

            title = self.font.render("¡Perdiste!", True, self.title_color)
            instruction = self.font.render("Presiona R para reiniciar", True, self.title_color)

            self.screen.blit(title, (320, 200))
            self.screen.blit(instruction, (220, 300))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    waiting = False  # termina y permite reiniciar
