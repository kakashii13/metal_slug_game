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
        self.jump_height = -30 # altura del salto
        self.gravity = 2.8 # gravedad para que el personaje caiga lento
        self.velocity_y = 0 # velocidad del salto
        self.is_shooting = False
        # Sprite de caminata
        self.walk_frames = []
        self.current_frame = 0 # frame actual de la animacion
        self.frame_timer = 0 # contador de frames para la animacion
        self.frame_rate = 3  # cuanto mas bajo, mas rapido se cambia el frame
        self.load_walk_sprites("Sprites/main_character", frame_count=5)  # 5 frames de caminata
        self.shoot_frames = [] # Sprite de disparo
        self.crounch_frame = pygame.image.load("Sprites/main_character/crouch_0.png").convert_alpha() # frame de agachado

    def load_walk_sprites(self, folder_path, frame_count):
        # recorro el numero de frames de la animacion de caminata
        for i in range(frame_count):
            path = f"{folder_path}/walk_{i}.png"
            frame = pygame.image.load(path).convert_alpha()
            self.walk_frames.append(frame)

    def load_shoot_sprites(self, folder_path, frame_count):
        # recorro el numero de frames de la animacion de disparo
        for i in range(frame_count):
            path = f"{folder_path}/shoot_{i}.png"
            frame = pygame.image.load(path).convert_alpha()
            self.shoot_frames.append(frame)

    def load_shoot_crouch_sprites(self, folder_path, frame_count):
        # recorro el numero de frames de la animacion de disparo agachado
        for i in range(frame_count):
            path = f"{folder_path}/shoot_crouch_{i}.png"
            frame = pygame.image.load(path).convert_alpha()
            self.shoot_frames.append(frame)

    def draw(self, surface):
        # Actualiza la animación si se está moviendo
        keys = pygame.key.get_pressed()

        # TODO: Hay un bug cuando el personaje dispara agachado, vuelve la animacion hacia arriba
        if self.is_shooting:
            if self.is_crouching: # si el personaje esta agachado
                self.load_shoot_crouch_sprites("Sprites/main_character", frame_count=3) # 3 frames de disparo agachado
            else: 
                self.load_shoot_sprites("Sprites/main_character", frame_count=5) # 5 frames de disparo parado
            self.frame_timer += 1 
            if self.frame_timer >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.shoot_frames) # cambiamos el frame cuando se cumple el frame_rate
                self.frame_timer = 0
            # dibujamos el frame de disparo
            frame = self.shoot_frames[self.current_frame]
            surface.blit(frame, (self.x, self.y - self.height)) # restamos para igualar la altura del personaje con el sprite
        elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames) # cambiamos el frame cuando se cumple el frame_rate
                self.frame_timer = 0
            # dibujamos el frame de caminata
            if self.current_frame >= len(self.walk_frames):
                self.current_frame = 0
            frame = self.walk_frames[self.current_frame]
            surface.blit(frame, (self.x, self.y - self.height))
        elif self.is_crouching:
            # dibujamos el frame de agachado
            surface.blit(self.crounch_frame, (self.x, self.y - self.height)) # restamos para igualar la altura del personaje con el sprite
        else:
            #personaje quieto
            surface.blit(self.walk_frames[0], (self.x, self.y - self.height)) # dibujamos el personaje en la pantalla
         # Fuente para dibujar texto
        font = pygame.font.SysFont(None, 24)
        
        # Crear texto con la posición
        coord_text = font.render(f"({self.x}, {self.y}, {self.height})", True, (0, 0, 0))  # negro
        
        # Dibujar texto sobre el personaje
        surface.blit(coord_text, (self.x + 50, self.y - 20))  # un poco más arriba

    # TODO: hay un bug del personaje cuando aprieto la tecla de abajo y moverme, el personaje se despega del suelo al caminar
    def move(self, keys):
        if not keys[pygame.K_DOWN]:
            self.stand()
        if keys[pygame.K_LEFT]:
            if self.x > 0:
                self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            if self.x < 800 - self.width:
                self.x += self.speed
        if keys[pygame.K_DOWN]:
            self.crouch()
        if keys[pygame.K_UP]:
            self.jump()
        self.apply_gravity()

    def jump(self): # para que el personaje salte
        if not self.is_jumping:
            self.velocity_y += self.jump_height
            self.is_jumping = True

    def crouch(self): # para que el personaje se agache
        if not self.is_crouching and not self.is_jumping:
            self.is_crouching = True
    
    def stand(self): # para que el personaje se quede de pie
        if self.is_crouching:
            # self.height = self.height * 2
            self.is_crouching = False

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