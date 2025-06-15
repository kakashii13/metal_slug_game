import pygame 
import sys
import resources.colors as colors
from entities.main_character import MainCharacter
from entities.bullet import Bullet
from entities.soldier import Soldier
from start_screen import StartScreen
from game_over import GameOverScreen

# tamaño de la ventana 
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def start_game(screen, clock):
     # posicion del personaje al inicio
    width = 100
    floor = 500
    character = MainCharacter(width, floor)

    # soldado 
    last_spawn_time = 0 # tiempo de spawn
    spawn_interval = 2000 # tiempo entre cada spawn

    # bala del personaje
    character_bullets = []
    last_bullet_time = 0 # tiempo de disparo
    shoot_delay = 200 # tiempo de espera para disparar

    # soldados
    soldiers = []

    # bucle del juego
    is_collision = False
    while not is_collision: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(colors.WHITE) # color de fondo

        keys = pygame.key.get_pressed() # teclas presionadas

        # tiempo actual en milisegundos
        current_time = pygame.time.get_ticks() 
        
        # mover personaje
        character.move(keys)
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
        if current_time - last_spawn_time > spawn_interval: 
            last_spawn_time = current_time
            soldier = Soldier(WINDOW_WIDTH - 100, floor)
            soldiers.append(soldier)

        # dibujar soldados
        for soldier in soldiers:
            soldier.move()
            soldier.draw(screen)

        # detectar colisiones entre balas y soldados
        for bullet in character_bullets[:]: # recorro una copia de la lista de balas para evitar errores
            bullet_rect = pygame.Rect(bullet.position[0], bullet.position[1], 10, 10) # rectangulo de la bala
            for soldier in soldiers: # recorro la lista de soldados
                if soldier.is_alive: # si el soldado esta vivo
                    soldier_rect = pygame.Rect(soldier.position[0], soldier.position[1] - soldier.size[1], soldier.size[0], soldier.size[1]) # rectangulo del soldado
                    if bullet_rect.colliderect(soldier_rect): # si la bala colisiona con el soldado
                        soldier.remove() # elimino el soldado
                        character_bullets.remove(bullet) # elimino la bala
                        #TODO: como reemplazar el break? 
                        break # salgo del for interno para evitar errores con balas ya eliminadas

        # detectar colisiones entre personaje y soldados
        character_rect = pygame.Rect(character.position[0], character.position[1], character.size[0], character.size[1])
        for soldier in soldiers[:]: # recorro una copia de la lista de soldados para evitar errores
            if soldier.is_alive: # si el soldado esta vivo
                soldier_rect = pygame.Rect(soldier.position[0], soldier.position[1], soldier.size[0], soldier.size[1]) # rectangulo del soldado
                if character_rect.colliderect(soldier_rect): # si el personaje colisiona con el soldado
                    soldier.remove() # elimino el soldado
                    is_collision = True

        pygame.display.update()
        clock.tick(20)



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


if __name__ == "__main__":
    main()