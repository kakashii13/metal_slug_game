import pygame
from entities.character import Character

class MainCharacter(Character):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)

        # estado inicial
        self.color = (0, 0, 255)
        self.initial_x = x
        self.initial_y = y
        self.is_jumping = False
        self.is_crouching = False
        self.is_shooting = False
        self._is_stuck = False

        # fisicas
        self.jump_height = -25
        self.gravity = 2.8
        self.velocity_y = 0
        self._hit_box_height = self.height

        # animacion
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_rate = 3

        # cargar los sprites
        self._load_sprites()

    def _load_sprites(self):
        folder = "Sprites/main_character"
        self.walk_frames = self._load_sprite_sequence(folder, "walk", 5)
        self.shoot_stand_frames = self._load_sprite_sequence(folder, "shoot", 5)
        self.shoot_crouch_frames = self._load_sprite_sequence(folder, "shoot_crouch", 3)
        self.crouch_frame = pygame.image.load(f"{folder}/crouch_0.png").convert_alpha()

    # cargamos la secuencia de sprites desde la carpeta de sprites
    def _load_sprite_sequence(self, folder_path, prefix, frame_count, size=(60, 80)):
        frames = []
        for i in range(frame_count):
            path = f"{folder_path}/{prefix}_{i}.png"
            frame = pygame.image.load(path).convert_alpha()
            frame = pygame.transform.scale(frame, size)
            frames.append(frame)
        return frames

    def draw(self, surface, scroll_x=0):
        keys = pygame.key.get_pressed()
        frame = None  # frame final a dibujar

        if self.is_shooting:
            frames = self.shoot_crouch_frames if self.is_crouching else self.shoot_stand_frames
        elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            frames = self.walk_frames
        else:
            frames = None

        if frames:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(frames)
                self.frame_timer = 0
            if self.current_frame >= len(frames):
                self.current_frame = 0
            frame = frames[self.current_frame]

        elif self.is_crouching:
            frame = pygame.transform.scale(self.crouch_frame, (70, 80))
        else:
            self.current_frame = 0
            self.frame_timer = 0
            frame = self.walk_frames[0]

        # Dibujar el frame final
        if frame:
            surface.blit(frame, (self.x - scroll_x, self.y - self.height))

    def move(self, keys):
        scroll_amount = 0
        if not keys[pygame.K_DOWN]:
            self.stand()
        if keys[pygame.K_LEFT]:
            if self.x > 0:
                self.x -= self.speed
        if keys[pygame.K_RIGHT]:
             if self.is_stuck:
                pass  # atascado, no se mueve
             elif self.x < 300:
                self.x += self.speed
             else:
                scroll_amount = self.speed
        if keys[pygame.K_DOWN]:
            self.crouch()
        if keys[pygame.K_UP]:
            self.jump()
        self.apply_gravity()
        if self.is_jumping or self.y < self.initial_y:
            self.is_stuck = False
        return scroll_amount

    def jump(self): # para que el personaje salte
        if not self.is_jumping:
            self.velocity_y += self.jump_height
            self.is_jumping = True

    def crouch(self): # para que el personaje se agache
        if not self.is_crouching and not self.is_jumping:
            self.is_crouching = True
            self._hit_box_height = self.height // 2# altura del personaje agachado
    
    def stand(self): # para que el personaje se quede de pie
        if self.is_crouching:
            self.is_crouching = False
            self._hit_box_height = self.height

    def apply_gravity(self): # aplico la gravedad al salto
        if self.is_jumping:
            self.velocity_y += self.gravity # gravedad para que el personaje caiga lento    
            self.y += self.velocity_y

        if self.y >= self.initial_y:
            self.y = self.initial_y 
            self.velocity_y = 0
            self.is_jumping = False
    
    @property
    def get_shoot_position(self):
        return (self.x + 25, self.y - 25)
    
    def shoot(self):
        self.is_shooting = True

    def stop_shooting(self):
        self.is_shooting = False
    
    @property
    def is_stuck(self):
        return self._is_stuck

    @is_stuck.setter
    def is_stuck(self, value):
        self._is_stuck = value

    @property
    def hit_box_height(self):
        return self._hit_box_height
    
    @hit_box_height.setter
    def hit_box_height(self, value):
        self._hit_box_height = value