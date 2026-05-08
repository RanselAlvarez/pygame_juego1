import pygame
import sys
import src.opciones as opciones
from src.personaje import Personaje


pygame.init()

# Tamanio de pantalla
pantalla = pygame.display.set_mode((opciones.ANCHO_PANTALLA, opciones.ALTO_PANTALLA))

# Titulo de la ventana
pygame.display.set_caption("Mi Juego1")

# Creacion el reloj para fps
reloj = pygame.time.Clock()  # ← AQUÍ se crea, UNA SOLA VEZ




# Creamos el personaje en la posicion 400, 300 (casi el centro de la pantalla)
jugador = Personaje(400, 300)
# Mostramos el personaje en la pantalla
jugador.dibujar_personaje(pantalla)





run = True
while run:
    # ⏱️ SIEMPRE al inicio del bucle. Limita FPS + devuelve tiempo real en ms
    dt = reloj.tick(opciones.FPS_OBJETIVO) / 1000.0  
    
    for event in pygame.event.get():
        # Evento para cerrar aplicacion en la x o con ALT+F4
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("Izquierda")
            elif event.key == pygame.K_d:
                print("Derecha")
            elif event.key == pygame.K_s:
                print("Abajo")
            elif event.key == pygame.K_w:
                print("Arriba")

        
    # Esto es lo que actualiza los componentes en la pantalla
    pygame.display.flip()

pygame.quit()
sys.exit()





