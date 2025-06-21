import pygame 
import sys
from entities.main_character import MainCharacter
from entities.bullet import Bullet
from entities.soldier import Soldier
from start_screen import StartScreen
from game_over import GameOverScreen
from entities.flying_killer import FlyingKiller
from entities.obstacle import Obstacle
from entities.rescued_character import RescuedCharacter
from hud import Hud

#TODO agregar sonido

# tamaño de la ventana 
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# game constants
DIFFICULTY_INTERVAL = 10000
INITIAL_SOLDIER_SPEED = 10
CHINESE_SOLDIER_SPAWN_INTERVAL = 1200
FLYING_KILLER_SPAWN_INTERVAL = 6000
FLYING_KILLER_INITIAL_DELAY = 1000
OBSTACLE_SPAWN_INTERVAL = 10000
RESCUED_CHARACTER_SPAWN_INTERVAL = 5000
SHOOT_DELAY = 600
SCORE_INCREMENT = 50


def main(): 
    pygame.init()

    # pantalla del juego
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Metal Slug casero") # titulo de la ventana

    # reloj
    clock = pygame.time.Clock()

    # bucle del juego
    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

        # pantalla de inicio
        start_screen = StartScreen(screen)
        start_screen.draw()
        
        # bucle del juego
        start_game(screen, clock)

        # Mostrar pantalla de Game Over
        game_over_screen = GameOverScreen(screen)
        game_over_screen.draw()  # espera hasta que presione "R" o cierre ventana

        pygame.display.update()
        clock.tick(20)

    pygame.quit()
    sys.exit()


# funcion que compara si existe una superposicion entre un objeto y una posicion x
def exist_superposition(x, objects, margin = 200):
    for obj in objects:
        if abs(obj.x - x) < margin:
            return True
    return False


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def spawn_enemies(current_time, floor, scroll_x, soldier_speed, soldiers,
                  flying_killers, obstacles, rescued_characters, spawn_timers):
    if current_time - spawn_timers['soldier'] > CHINESE_SOLDIER_SPAWN_INTERVAL:
        spawn_timers['soldier'] = current_time
        soldier = Soldier(WINDOW_WIDTH - 100, floor)
        soldier.speed = soldier_speed
        soldiers.append(soldier)

    if current_time - spawn_timers['flying_killer'] > FLYING_KILLER_SPAWN_INTERVAL:
        spawn_timers['flying_killer'] = current_time
        flying_killer = FlyingKiller(WINDOW_WIDTH - 100, floor - 60)
        flying_killers.append(flying_killer)

    if current_time - spawn_timers['obstacle'] > OBSTACLE_SPAWN_INTERVAL:
        spawn_timers['obstacle'] = current_time
        obstacle = Obstacle(scroll_x + 600, floor)
        obstacles.append(obstacle)

    if current_time - spawn_timers['rescued'] > RESCUED_CHARACTER_SPAWN_INTERVAL:
        if not exist_superposition(scroll_x + 600, obstacles):
            spawn_timers['rescued'] = current_time
            rescued_character = RescuedCharacter(scroll_x + 600, floor)
            rescued_characters.append(rescued_character)


def update_bullets(character, keys, current_time, character_bullets,
                   flying_killers, flying_killer_bullets, last_bullet_time, screen):
    if keys[pygame.K_SPACE] and current_time - last_bullet_time > SHOOT_DELAY:
        last_bullet_time = current_time
        bullet = Bullet(character.get_shoot_position[0],
                        character.get_shoot_position[1], 1)
        character_bullets.append(bullet)
        character.is_shooting = True
    else:
        character.is_shooting = False

    for bullet in character_bullets:
        bullet.move()
        bullet.draw(screen)

    for flying_killer in flying_killers:
        if flying_killer.can_shoot(current_time):
            enemy_bullet = flying_killer.shoot(current_time)
            flying_killer_bullets.append(enemy_bullet)

    for enemy_bullet in flying_killer_bullets:
        enemy_bullet.move()
        enemy_bullet.draw(screen)

    return last_bullet_time


def draw_entities(screen, soldiers, flying_killers, obstacles,
                  rescued_characters, scroll_x):
    for soldier in soldiers:
        soldier.move()
        soldier.draw(screen)

    for flying_killer in flying_killers:
        flying_killer.move()
        flying_killer.draw(screen)

    for obstacle in obstacles:
        obstacle.draw(screen, scroll_x)

    for rescued_character in rescued_characters:
        rescued_character.draw(screen, scroll_x)


def check_collisions(character, character_bullets, soldiers, flying_killers,
                     flying_killer_bullets, obstacles, rescued_characters,
                     hud, scroll_x, max_lives):
    character_rect = pygame.Rect(
        character.position[0],
        character.position[1] - character.hit_box_height,
        character.size[0],
        character.size[1],
    )

    # Adjuta la posicion del personaje rescatado para que coincida con el personaje principal
    adjusted_position = 15

    for rescued_character in rescued_characters[:]:
        rescued_chacter_rect = pygame.Rect(
            rescued_character.position[0] - scroll_x,
            rescued_character.position[1] - rescued_character.size[1] + adjusted_position,
            rescued_character.size[0],
            rescued_character.size[1],
        )
        if character_rect.colliderect(rescued_chacter_rect):
            rescued_character.is_saved = True
            hud.rescue_character()
            rescued_character.remove()

    for obstacle in obstacles[:]:
        obstacle_rect = pygame.Rect(
            obstacle.position[0] - scroll_x,
            obstacle.position[1] - obstacle.size[1],
            obstacle.size[0],
            obstacle.size[1],
        )
        if character_rect.colliderect(obstacle_rect):
            character.is_stuck = True

    for bullet in character_bullets[:]:
        bullet_rect = pygame.Rect(
            bullet.position[0] - scroll_x, bullet.position[1], 10, 10
        )
        bullet_removed = False
        for soldier in soldiers:
            if bullet_removed:
                continue
            if soldier.is_alive:
                soldier_rect = pygame.Rect(
                    soldier.position[0] - scroll_x,
                    soldier.position[1] - soldier.size[1],
                    soldier.size[0],
                    soldier.size[1],
                )
                if bullet_rect.colliderect(soldier_rect):
                    hud.add_score(SCORE_INCREMENT)
                    soldier.remove()
                    character_bullets.remove(bullet)
                    bullet_removed = True

    for soldier in soldiers[:]:
        if soldier.is_alive:
            soldier_rect = pygame.Rect(
                soldier.position[0],
                soldier.position[1],
                soldier.size[0],
                soldier.size[1],
            )
            if character_rect.colliderect(soldier_rect):
                hud.lose_life()
                max_lives -= 1
                soldier.remove()

    for enemy_bullet in flying_killer_bullets[:]:
        enemy_bullet_rect = pygame.Rect(
            enemy_bullet.position[0], enemy_bullet.position[1], 10, 10
        )
        if enemy_bullet_rect.colliderect(character_rect):
            hud.lose_life()
            max_lives -= 1
            flying_killer_bullets.remove(enemy_bullet)

    for flying_killer in flying_killers[:]:
        if flying_killer.is_alive:
            flying_killer_rect = pygame.Rect(
                flying_killer.position[0],
                flying_killer.position[1] - flying_killer.height,
                flying_killer.width,
                flying_killer.height,
            )
            if character_rect.colliderect(flying_killer_rect):
                hud.lose_life()
                max_lives -= 1
                flying_killer.remove()

    for bullet in character_bullets[:]:
        bullet_rect = pygame.Rect(
            bullet.position[0] - scroll_x, bullet.position[1], 10, 10
        )
        bullet_removed = False
        for flying_killer in flying_killers:
            if bullet_removed:
                continue
            if flying_killer.is_alive:
                flying_killer_rect = pygame.Rect(
                    flying_killer.position[0] - scroll_x,
                    flying_killer.position[1] - flying_killer.height,
                    flying_killer.width,
                    flying_killer.height,
                )
                if bullet_rect.colliderect(flying_killer_rect):
                    hud.add_score(SCORE_INCREMENT)
                    flying_killer.remove()
                    character_bullets.remove(bullet)
                    bullet_removed = True

    return max_lives

def start_game(screen, clock):
    # posiciones iniciales del personaje y el suelo
    width = 100
    floor = 500

    scroll_x = 0  # variable para el scroll-x

     # imagen de fondo
    background = pygame.image.load("Sprites/background/map.png").convert()
    

    # personaje principal
    character = MainCharacter(width, floor)
    max_lives = 3 # vidas del personaje

    # dificultad del juego
    start_time = pygame.time.get_ticks()
    difficulty_interval = DIFFICULTY_INTERVAL
    last_dificulty_increase = 0
    soldier_speed = INITIAL_SOLDIER_SPEED

    # soldado
    spawn_timers = {
        'soldier': 0,
        'flying_killer': FLYING_KILLER_INITIAL_DELAY,
        'obstacle': 0,
        'rescued': 0,
    }

    # bala del personaje
    character_bullets = []
    last_bullet_time = 0  # tiempo de disparo

    # soldados
    soldiers = []

    # flying killer
    flying_killers = []
    flying_killer_bullets = []


    # obstaculos
    obstacles = []

    # personaje rescatado
    rescued_characters = []  # lista de personajes rescatados

    # hud 
    hud = Hud()

    # bucle del juego
    while max_lives > 0:
        handle_events()

        # dibujamos el fondo 
        screen.blit(
            background,
            (0, 0),
            area=pygame.Rect(scroll_x, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
        )

        # dibujamos el hud
        hud.draw(screen)

        keys = pygame.key.get_pressed()  # teclas presionadas

        # tiempo actual en milisegundos
        current_time = pygame.time.get_ticks() 
        
        elapsed_time = current_time - start_time
        if elapsed_time - last_dificulty_increase > difficulty_interval:
            last_dificulty_increase = current_time
            soldier_speed += 5 # aumento la velocidad de los soldados

        # mover personaje
        scroll_delta = character.move(keys)
        scroll_x += scroll_delta # actualizo el scroll-x
        character.draw(screen) # dibujar personaje

        last_bullet_time = update_bullets(
            character,
            keys,
            current_time,
            character_bullets,
            flying_killers,
            flying_killer_bullets,
            last_bullet_time,
            screen,
        )

        spawn_enemies(
            current_time,
            floor,
            scroll_x,
            soldier_speed,
            soldiers,
            flying_killers,
            obstacles,
            rescued_characters,
            spawn_timers,
        )

        draw_entities(
            screen,
            soldiers,
            flying_killers,
            obstacles,
            rescued_characters,
            scroll_x,
        )

        max_lives = check_collisions(
            character,
            character_bullets,
            soldiers,
            flying_killers,
            flying_killer_bullets,
            obstacles,
            rescued_characters,
            hud,
            scroll_x,
            max_lives,
        )

        pygame.display.update()
        clock.tick(20)




if __name__ == "__main__":
    main()
