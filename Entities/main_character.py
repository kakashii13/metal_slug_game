import pygame
from entities.character import Character

class MainCharacter(Character):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)
        self.color = (0, 0, 255)
        self.initial_y = y # representa el suelo
        self.initial_x = x 
        self.is_jumping = False
        self.is_crouching = False # para que el personaje se agache
        self.jump_height = -25 # altura del salto
        self.gravity = 2.8 # gravedad para que el personaje caiga lento
        self.velocity_y = 0 # velocidad del salto
        self.is_shooting = False
        self._hit_box_height = self.height
        # Sprite de caminata
        self.walk_frames = []
        self.current_frame = 0 # frame actual de la animacion
        self.frame_timer = 0 # contador de frames para la animacion
        self.frame_rate = 3  # cuanto mas bajo, mas rapido se cambia el frame
        self.load_walk_sprites("Sprites/main_character", frame_count=5)  # 5 frames de caminata
        self.shoot_stand_frames = self.load_shoot_sprites(
            "Sprites/main_character", frame_count=5
        )  # 5 frames de disparo parado
        self.shoot_crouch_frames = self.load_shoot_crouch_sprites(
            "Sprites/main_character", frame_count=3
        )  # 3 frames de disparo agachado
        self.crounch_frame = pygame.image.load(
            "Sprites/main_character/crouch_0.png"
        ).convert_alpha()  # frame de agachado
        self.shoot_granade_frames = []  # Sprite de disparo con granada
        self.load_shoot_granade_sprites(
            "Sprites/main_character/granade", frame_count=7
        )
        self.is_granade = False # para que el personaje dispare granadas
        self._is_stuck = False

    def load_walk_sprites(self, folder_path, frame_count):
        # recorro el numero de frames de la animacion de caminata
        for i in range(frame_count):
            path = f"{folder_path}/walk_{i}.png"
            frame = pygame.image.load(path).convert_alpha()
            frame = pygame.transform.scale(frame, (60, 80))
            self.walk_frames.append(frame)

    def load_shoot_sprites(self, folder_path, frame_count):
        """Carga y devuelve los sprites de disparo de pie."""
        frames = []
        for i in range(frame_count):
            path = f"{folder_path}/shoot_{i}.png"
            frame = pygame.image.load(path).convert_alpha()
            frame = pygame.transform.scale(frame, (60, 80))
            frames.append(frame)
        return frames

    def load_shoot_crouch_sprites(self, folder_path, frame_count):
        """Carga y devuelve los sprites de disparo agachado."""
        frames = []
        for i in range(frame_count):
            path = f"{folder_path}/shoot_crouch_{i}.png"
            frame = pygame.image.load(path).convert_alpha()
            frame = pygame.transform.scale(frame, (60, 80))
            frames.append(frame)
        return frames

    def load_shoot_granade_sprites(self, folder_path, frame_count):
        # recorro el numero de frames de la animacion de disparo con granada
        for i in range(frame_count):
            path = f"{folder_path}/{i}.png"
            frame = pygame.image.load(path).convert_alpha()
            frame = pygame.transform.scale(frame, (60, 80))
            self.shoot_granade_frames.append(frame)

    def draw(self, surface, scroll_x=0):
        # Actualiza la animación si se está moviendo
        keys = pygame.key.get_pressed()

        if self.is_shooting:
            frames = self.shoot_crouch_frames if self.is_crouching else self.shoot_stand_frames
            self.frame_timer += 1
            if self.frame_timer >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(frames)  # cambiamos el frame cuando se cumple el frame_rate
                self.frame_timer = 0
            # Validamos el índice por si venimos de otra animación
            if self.current_frame >= len(frames):
                self.current_frame = 0
            # dibujamos el frame de disparo
            frame = frames[self.current_frame]
            surface.blit(frame, (self.x - scroll_x, self.y - self.height)) # restamos para igualar la altura del personaje con el sprite
        elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames) # cambiamos el frame cuando se cumple el frame_rate
                self.frame_timer = 0
            # dibujamos el frame de caminata
            if self.current_frame >= len(self.walk_frames):
                self.current_frame = 0
            frame = self.walk_frames[self.current_frame]
            surface.blit(frame, (self.x - scroll_x, self.y - self.height))
        elif self.is_crouching:
            # dibujamos el frame de agachado
            frame = pygame.transform.scale(self.crounch_frame, (70, 80)) # escalamos el frame de agachado
            surface.blit(frame, (self.x - scroll_x, self.y - self.height)) # restamos para igualar la altura del personaje con el sprite
            # personaje disparando una granada
        elif self.is_granade:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.shoot_granade_frames)
            frame = self.shoot_granade_frames[self.current_frame]
            surface.blit(frame, (self.x - scroll_x, self.y - self.height))
        else:
            # personaje quieto: mostramos el primer frame sin animar
            self.current_frame = 0
            self.frame_timer = 0
            frame = self.walk_frames[0]
            surface.blit(frame, (self.x - scroll_x, self.y - self.height))  # dibujamos el personaje en la pantalla
        #  # Fuente para dibujar texto
        # font = pygame.font.SysFont(None, 24)
        
        # # Crear texto con la posición
        # coord_text = font.render(f"({self.x}, {self.y}, {self.height})", True, (0, 0, 0))  # negro
        
        # # Dibujar texto sobre el personaje
        # surface.blit(coord_text, (self.x + 50, self.y - 20))  # un poco más arriba

    # TODO: por que "camina" el personaje cuando no lo estoy moviendo?
    def move(self, keys):
        scroll_amount = 0

        if not keys[pygame.K_DOWN]:
            self.stand()
        if not keys[pygame.K_g]:
        # TODO: terminar de configurar la granada
            self.is_granade = False
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
        if keys[pygame.K_g] and not self.is_granade:
            self.is_granade = True
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