import pygame
import sys

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.title_color = (255,255,255)
        raw_image = pygame.image.load("Sprites/background/game_over.jpg").convert()
        self.frame = pygame.transform.scale(raw_image, (800, 600))

    def draw(self):
        waiting = True
        while waiting:
            self.screen.blit(self.frame, (0, 0))

            instruction = self.font.render("R para reiniciar", True, self.title_color)

            self.screen.blit(instruction, (220, 50))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    waiting = False  # termina y permite reiniciar
