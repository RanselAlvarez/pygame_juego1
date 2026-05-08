import pygame
import sys
import src.opciones as opciones
from src.personaje import Personaje


pygame.init()

# Tamanio de pantalla
pantalla = pygame.display.set_mode((opciones.ANCHO_PANTALLA, opciones.ALTO_PANTALLA))

# Titulo de la ventana
pygame.display.set_caption("Mi Juego1")





# Creamos el personaje en la posicion 400, 300 (casi el centro de la pantalla)
jugador = Personaje(400, 300)
# Mostramos el personaje en la pantalla
jugador.dibujar_personaje(pantalla)





run = True
while run:
    
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
            elif event.key == pygame.K_LEFT:
                print("Izquierda")
            elif event.key == pygame.K_RIGHT:
                print("Derecha")
            elif event.key == pygame.K_DOWN:
                print("Abajo")
            elif event.key == pygame.K_UP:
                print("Arriba")
        
    # Esto es lo que actualiza los componentes en la pantalla
    pygame.display.flip()

pygame.quit()
sys.exit()





