import pygame
class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        self.bg_color = (255, 255, 255)
        self.title_color = (255, 255, 255)
        self.text_color = (255, 255, 255)
        self.title = self.font.render("Shooter Game", True, (0, 0, 0))
        raw_image = pygame.image.load("Sprites/background/start_screen.png").convert()
        self.frame = pygame.transform.scale(raw_image, (800, 600))
        self.title_rect = self.title.get_rect(center=(400, 200))
        self.letter_e = pygame.image.load("Sprites/hud/letter_e.png").convert_alpha()

        # Inicializa musica de fondo
        pygame.mixer.init()
        pygame.mixer.music.load("resources/sounds/start_screen.wav")
        pygame.mixer.music.set_volume(0.3)


    def draw(self):
        # Reproduce la musica de fondo
        pygame.mixer.music.play(-1)
        while True:
            self.screen.blit(self.frame, (0, 0))
            title = self.font.render("¡Bienvenido a metal slug casero!", True, self.title_color)
            text_before = self.small_font.render("Presiona", True, self.text_color)
            text_after = self.small_font.render("para comenzar", True, self.text_color)

            self.screen.blit(text_before, (250, 500))
            self.screen.blit(self.letter_e, (320, 495)) 
            self.screen.blit(text_after, (360, 500))

            self.screen.blit(title, (200, 450))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # el usuario cerro 
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    pygame.mixer.music.stop()
                    return True  # el usuario quiere jugar