import pygame 
import sys
import Resources.colors as colors
from Entities.main_character import MainCharacter
from Entities.bullet import Bullet
from Entities.soldier import Soldier
from start_screen import StartScreen
from game_over import GameOverScreen

# window's size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def start_game(screen, clock):
     # character
    character_x = 100
    character_y = 500
    character = MainCharacter(character_x, character_y)

    # soldier
    last_spawn_time = 0 # tiempo de spawn
    spawn_interval = 2000 # tiempo entre cada spawn

    # character's bullet
    character_bullets = []
    last_bullet_time = 0 # tiempo de disparo
    shoot_delay = 200 # tiempo de espera para disparar

    # soldiers
    soldiers = []

    # game loop
    is_collision = False
    while not is_collision: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(colors.WHITE)

        keys = pygame.key.get_pressed()
        character.move(keys)

        current_time = pygame.time.get_ticks() # tiempo actual en milisegundos
        
         # draw character
        character.draw(screen)

        # draw bullet
        if keys[pygame.K_SPACE] and current_time - last_bullet_time > shoot_delay: 
            last_bullet_time = current_time # actualizo el tiempo de disparo
            bullet = Bullet(character.get_shoot_position()[0], character.get_shoot_position()[1], 1)
            character_bullets.append(bullet)
            character.is_shooting = True
        
        for bullet in character_bullets:
            bullet.move()
            bullet.draw(screen)

        # spawn soldier
        if current_time - last_spawn_time > spawn_interval: 
            last_spawn_time = current_time
            soldier = Soldier(WINDOW_WIDTH - 100, 400)
            soldiers.append(soldier)

        # draw soldiers
        for soldier in soldiers:
            soldier.move()
            soldier.draw(screen)

        # detect collisions between bullets and soldiers
        for bullet in character_bullets[:]: # recorro una copia de la lista de balas para evitar errores
            bullet_rect = pygame.Rect(bullet.x, bullet.y, 10, 10) # rectangulo de la bala
            for soldier in soldiers: # recorro la lista de soldados
                if soldier.is_alive: # si el soldado esta vivo
                    soldier_rect = pygame.Rect(soldier.x, soldier.y, soldier.width, soldier.height) # rectangulo del soldado
                    if bullet_rect.colliderect(soldier_rect): # si la bala colisiona con el soldado
                        soldier.remove() # elimino el soldado
                        character_bullets.remove(bullet) # elimino la bala
                        break # salgo del for interno para evitar errores con balas ya eliminadas

        # detect collisions between character and soldiers
        character_rect = pygame.Rect(character.x, character.y, character.width, character.height)
        for soldier in soldiers[:]: # recorro una copia de la lista de soldados para evitar errores
            if soldier.is_alive: # si el soldado esta vivo
                soldier_rect = pygame.Rect(soldier.x, soldier.y, soldier.width, soldier.height) # rectangulo del soldado
                if character_rect.colliderect(soldier_rect): # si el personaje colisiona con el soldado
                    soldier.remove() # elimino el soldado
                    is_collision = True

        pygame.display.update()
        clock.tick(20)



def main(): 
    pygame.init()

    # screen's game
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame Window")

    # clock
    clock = pygame.time.Clock()

    # game loop
    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

        # start screen
        start_screen = StartScreen(screen)
        start_screen.draw()
        
        # game loop
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