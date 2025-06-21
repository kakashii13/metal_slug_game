import pygame

class Hud: 
    def __init__(self, max_lives=3):
        self.max_lives = max_lives
        self.lives = max_lives
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.rescued = 0
        self.font = pygame.font.SysFont(None, 36)
        self.heart_icon = pygame.image.load("Sprites/hud/heart.png").convert_alpha()
        self.rescue_icon = pygame.image.load("Sprites/rescued_character/0.png").convert_alpha()

    def draw(self, screen):
        score_text = self.font.render(f"Puntaje: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # vidas
        for i in range(self.lives):
            screen.blit(self.heart_icon, (10 + i * 40, 50))

        # personajes rescatados
        screen.blit(self.rescue_icon, (10, 100))
        rescue_text = self.font.render(f"Rescatados: {self.rescued}", True, (255, 255, 255))
        screen.blit(rescue_text, (50, 100))

    def add_score(self, points):
        self.score += points

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1

    def rescue_character(self):
        self.rescued += 1
        self.score += 50
    