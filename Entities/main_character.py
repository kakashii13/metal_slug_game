import pygame
from Entities.character import Character

class MainCharacter(Character):
    def __init__(self, x = 0, y = 0, width = 50, height = 50):
        super().__init__(x, y, width, height)
        self.color = (0, 0, 255)
        self.initial_y = y
        self.initial_x = x
        self.is_jumping = False
        self.is_crouching = False
        self.jump_height = -30
        self.gravity = 2.8
        self.velocity_y = 0
        # Sprite de caminata
        self.walk_frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_rate = 10  # cuanto mas bajo, mas rapido camina
        self.load_walk_sprites("Sprites/MainCharacter", frame_count=5)  # 3 frames de caminata
        self.is_shooting = False
        self.shoot_frames = []
        self.load_shoot_sprites("Sprites/MainCharacter", frame_count=3)

    def load_walk_sprites(self, folder_path, frame_count):
        for i in range(frame_count):
            path = f"{folder_path}/walk_{i}.png"
            frame = pygame.image.load(path).convert_alpha()
            self.walk_frames.append(frame)

    def load_shoot_sprites(self, folder_path, frame_count):
        for i in range(frame_count):
            path = f"{folder_path}/shoot_{i}.png"
            frame = pygame.image.load(path).convert_alpha()
            self.shoot_frames.append(frame)

    def draw(self, surface):
        # Actualiza la animación si se está moviendo
        keys = pygame.key.get_pressed()
        if self.is_shooting:
            frame = self.shoot_frames[self.current_frame]
            surface.blit(frame, (self.x, self.y + self.height - frame.get_height()))
        else:
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                self.frame_timer += 1
                if self.frame_timer >= self.frame_rate:
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
                    self.frame_timer = 0
            else:
                self.current_frame = 0  # frame quieto

        frame = self.walk_frames[self.current_frame]
        surface.blit(frame, (self.x, self.y + self.height - frame.get_height()))



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
            self.y += 30
            self.height = 30
            self.is_crouching = True
    
    def stand(self): # para que el personaje se quede de pie
        if self.is_crouching:
            self.y -= 30
            self.height = 30
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
    
    def get_shoot_position(self):
        return (self.x + 25, self.y + 25)
    
    def shoot(self):
        self.is_shooting = True

    def stop_shooting(self):
        self.is_shooting = False