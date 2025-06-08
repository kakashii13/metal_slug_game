import pygame
from Entities.character import Character

class MainCharacter(Character):
    def __init__(self, x = 0, y = 0, width = 100, height = 100):
        super().__init__(x, y, width, height)
        self.color = (0, 0, 255)
        self.initial_y = y
        self.initial_x = x
        self.is_jumping = False
        self.is_crouching = False
        self.jump_height = -30
        self.gravity = 2.8
        self.velocity_y = 0

    def move(self, keys):
        self.stand()
        if keys[pygame.K_LEFT]:
            if self.x > 0:
                self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            if self.x < 800 - self.width:
                self.x += self.speed
        if keys[pygame.K_DOWN]:
            self.crouch()
        if keys[pygame.K_UP] and not self.is_jumping:
            self.jump()
        self.apply_gravity()

    def jump(self): # para que el personaje salte
        self.velocity_y += self.jump_height
        self.is_jumping = True

    def crouch(self): # para que el personaje se agache
        if not self.is_crouching:
            self.y += 50
            self.height = 50
            self.is_crouching = True
    
    def stand(self): # para que el personaje se quede de pie
        if self.is_crouching:
            self.y -= 50
            self.height = 100
            self.is_crouching = False

    def apply_gravity(self): # aplico la gravedad al salto
        if self.is_jumping:
            self.velocity_y += self.gravity # gravedad para que el personaje caiga lento    
            self.y += self.velocity_y

        # si el personaje esta en el suelo, no se aplica la gravedad
        if self.y >= self.initial_y - self.height:
            self.y = self.initial_y - self.height
            self.velocity_y = 0
            self.is_jumping = False