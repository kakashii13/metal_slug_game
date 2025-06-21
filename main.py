import pygame 
import sys
import resources.colors as colors
from entities.main_character import MainCharacter
from entities.bullet import Bullet
from entities.soldier import Soldier
from start_screen import StartScreen
from game_over import GameOverScreen
from entities.flying_killer import FlyingKiller
from entities.obstacle import Obstacle
from entities.rescued_character import RescuedCharacter
from hud import Hud

# tamaño de la ventana 
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


def main(): 
    pygame.init()

    # pantalla del juego
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame Window") # titulo de la ventana

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

def start_game(screen, clock):
     # posiciones iniciales del personaje y el suelo
    width = 100
    floor = 500

    scroll_x = 0 # variable para el scroll-x

     # imagen de fondo
    background = pygame.image.load("Sprites/background/map.png").convert()
    

    # personaje principal
    character = MainCharacter(width, floor)
    max_lives = 3 # vidas del personaje

    # dificultad del juego
    start_time = pygame.time.get_ticks()
    difilcuty_interval = 10000
    last_dificulty_increase= 0
    soldier_speed = 10

    # soldado 
    last_spawn_chinese_soldier = 0 # tiempo de spawn
    spawn_interval_chinese_soldier = 1200 # tiempo entre cada spawn
    # flying killer
    last_spawn_flying_killer = 1000 # tiempo de spawn
    spawn_interval_flying_killer = 6000

    # bala del personaje
    character_bullets = []
    last_bullet_time = 0 # tiempo de disparo
    shoot_delay = 200 # tiempo de espera para disparar

    # soldados
    soldiers = []

    # flying killer
    flying_killers = []
    flying_killer_bullets = []


    # obstaculos
    obstacles = []
    last_spawn_obstacle = 0 # tiempo de spawn
    spawn_interval_obstacle = 10000 # tiempo entre cada spawn de obstaculo

    # personaje rescatado
    rescued_characters = [] # lista de personajes rescatados
    last_spawn_rescued_character = 0 # tiempo de spawn
    spawn_interval_rescued_character = 5000 # tiempo entre cada spawn de personaje rescatado

    # hud 
    hud = Hud()

    # bucle del juego
    while max_lives > 0: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # dibujamos el fondo 
        screen.blit(background, (0, 0), area=pygame.Rect(scroll_x, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        # dibujamos el hud
        hud.draw(screen)

        keys = pygame.key.get_pressed() # teclas presionadas

        # tiempo actual en milisegundos
        current_time = pygame.time.get_ticks() 
        
        elapsed_time = current_time - start_time
        if elapsed_time - last_dificulty_increase > difilcuty_interval:
            last_dificulty_increase = current_time
            soldier_speed += 5 # aumento la velocidad de los soldados

        # mover personaje
        scroll_delta = character.move(keys)
        scroll_x += scroll_delta # actualizo el scroll-x
        character.draw(screen) # dibujar personaje

        # se agrega un delay para que no se dispare una bala por cada tecla presionada
        if keys[pygame.K_SPACE] and current_time - last_bullet_time > shoot_delay: 
            last_bullet_time = current_time # actualizo el tiempo de disparo
            bullet = Bullet(character.get_shoot_position[0], character.get_shoot_position[1], 1)
            character_bullets.append(bullet)
            character.is_shooting = True
        else:
            character.is_shooting = False
        
        for bullet in character_bullets:
            bullet.move()
            bullet.draw(screen)

        # se agrega un delay para no spawnear un soldado constantemente
        if current_time - last_spawn_chinese_soldier > spawn_interval_chinese_soldier: 
            last_spawn_chinese_soldier = current_time
            soldier = Soldier(WINDOW_WIDTH - 100, floor)
            soldier.speed = soldier_speed
            soldiers.append(soldier)

        # dibujar soldados
        for soldier in soldiers:
            soldier.move()
            soldier.draw(screen)

        # TODO: a medida que pasa el tiempo el tick deberia aumentar
        if current_time - last_spawn_flying_killer > spawn_interval_flying_killer:
            last_spawn_flying_killer = current_time
            flying_killer = FlyingKiller(WINDOW_WIDTH - 100, floor - 60)
            flying_killers.append(flying_killer)

        # dibujar flying killers
        for flying_killer in flying_killers:
            flying_killer.move()
            flying_killer.draw(screen)
            
            if flying_killer.can_shoot(current_time):
                enemy_bullet = flying_killer.shoot(current_time)
                flying_killer_bullets.append(enemy_bullet)
        
        for enemy_bullet in flying_killer_bullets:
            enemy_bullet.move()
            enemy_bullet.draw(screen)

        # personaje para rescatar
        if current_time - last_spawn_rescued_character > spawn_interval_rescued_character:
            if not exist_superposition(scroll_x + 600, obstacles):
                last_spawn_rescued_character = current_time
                rescued_character = RescuedCharacter(scroll_x + 600, floor)
                rescued_characters.append(rescued_character)

        for rescued_character in rescued_characters:
            rescued_character.draw(screen, scroll_x)

        # obstaculos
        if current_time - last_spawn_obstacle > spawn_interval_obstacle:
            last_spawn_obstacle = current_time
            obstacle = Obstacle(scroll_x + 600, floor)
            obstacles.append(obstacle)
        
        for obstacle in obstacles:
            obstacle.draw(screen, scroll_x)

        character_rect = pygame.Rect(character.position[0], character.position[1] - character.hit_box_height, character.size[0], character.size[1])

        # detectar colision entre personaje y personaje rescatado
        for rescued_character in rescued_characters[:]: # recorro una copia de la lista de personajes rescatados para evitar errores
            rescued_character_rect = pygame.Rect(rescued_character.position[0] - scroll_x, rescued_character.position[1] - rescued_character.size[1] + 15, rescued_character.size[0] , rescued_character.size[1])
            if character_rect.colliderect(rescued_character_rect):
                rescued_character.is_saved = True
                hud.rescue_character()
                rescued_character.remove()
            
        # detectar colisiones entre obstaculos y personaje
        for obstacle in obstacles[:]: # recorro una copia de la lista de obstaculos para evitar errores
            obstacle_rect = pygame.Rect(obstacle.position[0] - scroll_x, obstacle.position[1], obstacle.size[0], obstacle.size[1]) # rectangulo del obstaculo
            if character_rect.colliderect(obstacle_rect): # si el personaje colisiona con el obstaculo  
                character.is_stuck = True # el personaje se queda pegado al obstaculo

        # detectar colisiones entre balas y soldados
        for bullet in character_bullets[:]: # recorro una copia de la lista de balas para evitar errores
            bullet_rect = pygame.Rect(bullet.position[0] - scroll_x, bullet.position[1], 10, 10) # rectangulo de la bala
            for soldier in soldiers: # recorro la lista de soldados
                if soldier.is_alive: # si el soldado esta vivo
                    soldier_rect = pygame.Rect(soldier.position[0] - scroll_x, soldier.position[1] - soldier.size[1], soldier.size[0], soldier.size[1]) # rectangulo del soldado
                    if bullet_rect.colliderect(soldier_rect): # si la bala colisiona con el soldado
                        hud.add_score(50) # aumento el puntaje
                        soldier.remove() # elimino el soldado
                        character_bullets.remove(bullet) # elimino la bala
                        #TODO: como reemplazar el break? 
                        break # salgo del for interno para evitar errores con balas ya eliminadas

        # detectar colisiones entre personaje y soldados
        for soldier in soldiers[:]: # recorro una copia de la lista de soldados para evitar errores
            if soldier.is_alive: # si el soldado esta vivo
                soldier_rect = pygame.Rect(soldier.position[0], soldier.position[1], soldier.size[0], soldier.size[1]) # rectangulo del soldado
                if character_rect.colliderect(soldier_rect): # si el personaje colisiona con el soldado
                    hud.lose_life()
                    max_lives -= 1
                    soldier.remove() # elimino el soldado

        # detectar colisiones entre balas de flying killer y personaje
        for enemy_bullet in flying_killer_bullets[:]:
            enemy_bullet_rect = pygame.Rect(enemy_bullet.position[0], enemy_bullet.position[1], 10, 10)
            if enemy_bullet_rect.colliderect(character_rect):
                hud.lose_life()
                max_lives -= 1
                flying_killer_bullets.remove(enemy_bullet)

        # detectar colisiones entre personaje y flying killers
        for flying_killer in flying_killers[:]:
            if flying_killer.is_alive:
                flying_killer_rect = pygame.Rect(flying_killer.position[0], flying_killer.position[1] - flying_killer.height, flying_killer.width, flying_killer.height)
                if character_rect.colliderect(flying_killer_rect):
                    hud.lose_life()
                    max_lives -= 1
                    flying_killer.remove()

        # detectar colisiones entre balas del personaje y el flying killer
        for bullet in character_bullets[:]:
            bullet_rect = pygame.Rect(bullet.position[0] - scroll_x, bullet.position[1], 10, 10)
            for flying_killer in flying_killers:
                if flying_killer.is_alive:
                    flying_killer_rect = pygame.Rect(flying_killer.position[0] - scroll_x, flying_killer.position[1] - flying_killer.height, flying_killer.width, flying_killer.height)
                    if bullet_rect.colliderect(flying_killer_rect):
                        hud.add_score(100)
                        flying_killer.remove()
                        character_bullets.remove(bullet)
                        break

        pygame.display.update()
        clock.tick(20)




if __name__ == "__main__":
    main()