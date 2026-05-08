import pygame
import sys
import src.opciones as opciones
from src.personaje import Personaje



pygame.init()

# 🖥️ Configuración visual
pantalla = pygame.display.set_mode((opciones.ANCHO_PANTALLA, opciones.ALTO_PANTALLA))
# Titulo de la ventana
pygame.display.set_caption("Mi Juego1")


# Definir variables de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False


# 🧍 Crear personaje
# Creamos el personaje en la posicion 400, 300 (casi el centro de la pantalla)
jugador = Personaje(400, 300)
# Mostramos el personaje en la pantalla
jugador.dibujar_personaje(pantalla)

# 1️⃣ DEFINIR LAS BANDERAS ANTES DEL BUCLE (si no, da error de variable no definida)
mover_derecha = False
mover_izquierda = False
mover_arriba = False
mover_abajo = False




run = True
while run:
    
    for event in pygame.event.get():
        # Evento para cerrar aplicacion en la x o con ALT+F4
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            elif event.key == pygame.K_d:
                mover_derecha = True
            elif event.key == pygame.K_s:
                mover_abajo = True
            elif event.key == pygame.K_w:
                mover_arriba = True
            elif event.key == pygame.K_LEFT:
                mover_izquierda = True
            elif event.key == pygame.K_RIGHT:
                mover_derecha = True
            elif event.key == pygame.K_DOWN:
                mover_abajo = True
            elif event.key == pygame.K_UP:
                mover_arriba =  True
        
        
        # ✅ SOLTAR TECLA → Desactivar bandera (¡ESTO ES LO QUE FALTABA!)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                mover_izquierda = False
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                mover_derecha = False
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                mover_arriba = False
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                mover_abajo = False
            elif event.key == pygame.K_LEFT:
                mover_izquierda = False
            elif event.key == pygame.K_RIGHT:
                mover_derecha = False
            elif event.key == pygame.K_DOWN:
                mover_abajo = False
            elif event.key == pygame.K_UP:
                mover_arriba =  False
        
    # Calcular el movimiento del jugador
    delta_x = 0
    delta_y = 0
    
    if mover_derecha:
        delta_x = 50
    elif mover_izquierda:
        delta_x = -50
    elif mover_arriba:
        delta_y = -50
    elif mover_abajo:
        delta_y = 50

    # 👇 APLICAR EL MOVIMIENTO AL PERSONAJE (esto faltaba para que se viera el cambio)
    jugador.rect.x += delta_x
    jugador.rect.y += delta_y
    
    # 🔒 Evitar que salga de la pantalla (buena práctica)
    jugador.rect.clamp_ip(pygame.Rect(0, 0, opciones.ANCHO_PANTALLA, opciones.ALTO_PANTALLA))
    print(f"{delta_x}, {delta_y}")
    
    # Esto es lo que actualiza los componentes en la pantalla
    pygame.display.flip()

pygame.quit()
sys.exit()





