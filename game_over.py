import pygame
import sys

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.title_color = (255,255,255)
        raw_image = pygame.image.load("Sprites/background/game_over.jpg").convert()
        self.frame = pygame.transform.scale(raw_image, (800, 600))
        self.letter_r = pygame.image.load("Sprites/hud/letter_r.png").convert_alpha()

        # Inicializa el sonido de Game Over
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound("resources/sounds/game_over.wav") 
        self.sound.set_volume(0.3)

    def draw(self):
        self.sound.play()

        waiting = True
        while waiting:
            self.screen.blit(self.frame, (0, 0))

            text_before = self.font.render("Presiona", True, self.title_color)
            text_after = self.font.render("para reiniciar", True, self.title_color)    

            self.screen.blit(text_before, (250, 500))
            self.screen.blit(self.letter_r, (350, 495))
            self.screen.blit(text_after, (390, 500))


            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    waiting = False  # termina y permite reiniciar
                    self.sound.stop()
